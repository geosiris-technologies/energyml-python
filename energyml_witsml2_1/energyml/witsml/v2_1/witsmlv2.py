from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class AbstractBottomHoleTemperature:
    """
    One of either circulating or static temperature.

    :ivar bottom_hole_temperature: Bottomhole temperature for the job or
        reporting period.
    """

    bottom_hole_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "BottomHoleTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class AbstractCementJob:
    """
    Defines common elements for both cement job designs and reports.

    :ivar cement_engr: Cementing engineer.
    :ivar etim_waiting_on_cement: Duration for waiting on cement to set.
    :ivar plug_interval: If plug used,  measured depth interval between
        the top and base of the plug.
    :ivar md_hole: Measured depth at the bottom of  the hole.
    :ivar contractor: Pointer to a BusinessAssociate representing the
        cementing contractor.
    :ivar rpm_pipe: Pipe rotation rate (commonly in rotations per minute
        (RPM)).
    :ivar tq_init_pipe_rot: Pipe rotation: initial torque.
    :ivar tq_pipe_av: Pipe rotation: average torque.
    :ivar tq_pipe_mx: Pipe rotation: maximum torque.
    :ivar over_pull: String-up weight during reciprocation.
    :ivar slack_off: String-down weight during reciprocation.
    :ivar rpm_pipe_recip: Pipe reciprocation (RPM).
    :ivar len_pipe_recip_stroke: Pipe reciprocation: stroke length.
    :ivar reciprocating: Is the pipe being reciprocated (raised and
        lowered)? Values are "true" (or "1") and "false" (or "0").
    """

    cement_engr: Optional[str] = field(
        default=None,
        metadata={
            "name": "CementEngr",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_waiting_on_cement: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimWaitingOnCement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    plug_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "PlugInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    contractor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contractor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rpm_pipe: Optional[str] = field(
        default=None,
        metadata={
            "name": "RpmPipe",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tq_init_pipe_rot: Optional[str] = field(
        default=None,
        metadata={
            "name": "TqInitPipeRot",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tq_pipe_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "TqPipeAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tq_pipe_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "TqPipeMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    over_pull: Optional[str] = field(
        default=None,
        metadata={
            "name": "OverPull",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    slack_off: Optional[str] = field(
        default=None,
        metadata={
            "name": "SlackOff",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rpm_pipe_recip: Optional[str] = field(
        default=None,
        metadata={
            "name": "RpmPipeRecip",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_pipe_recip_stroke: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenPipeRecipStroke",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    reciprocating: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Reciprocating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class AbstractConnectionType:
    """
    The choice of connection type.
    """


@dataclass
class AbstractEventExtension:
    """
    Event extension schema.
    """


@dataclass
class AbstractItemWtOrVolPerUnit:
    """
    Item weight or volume per unit.
    """


@dataclass
class AbstractOperatingRange:
    """
    :ivar comment:
    :ivar end_inclusive: Is the end inclusive or exclusive in the range.
    :ivar start_inclusive: Is the start inclusive or exclusive in the
        range.
    :ivar start:
    :ivar end:
    """

    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_inclusive: Optional[bool] = field(
        default=None,
        metadata={
            "name": "EndInclusive",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    start_inclusive: Optional[bool] = field(
        default=None,
        metadata={
            "name": "StartInclusive",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    start: Optional[float] = field(
        default=None,
        metadata={
            "name": "Start",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    end: Optional[float] = field(
        default=None,
        metadata={
            "name": "End",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class AbstractRotarySteerableTool:
    """
    Choice placeholder in a rotary steerable tool.
    """


class AccelerometerAxisCombination(Enum):
    XY = "xy"
    XYZ = "xyz"


@dataclass
class AnchorState:
    """
    :ivar anchor_name: The anchor number within a mooring system, or
        name if a name is used instead.
    :ivar anchor_angle: Angle of the anchor or mooring line.
    :ivar anchor_tension: Tension on the mooring line represented by the
        named anchor.
    :ivar description: Free-test description of the state of this anchor
        or mooring line.
    """

    anchor_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "AnchorName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    anchor_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "AnchorAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    anchor_tension: Optional[str] = field(
        default=None,
        metadata={
            "name": "AnchorTension",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class AuthorizationStatus(Enum):
    AGREED = "agreed"
    PROVISIONAL = "provisional"
    OBSOLETE = "obsolete"


class BackupScaleType(Enum):
    """
    Backup scale types.
    """

    X10 = "x10"
    OFFSCALE_LEFT_RIGHT = "offscale left/right"
    OTHER = "other"


class BearingType(Enum):
    """
    Specifies the bearing type of a motor.
    """

    OIL_SEAL = "oil seal"
    MUD_LUBE = "mud lube"
    OTHER = "other"


@dataclass
class Bend:
    """
    Tubular Bend Component Schema.

    :ivar angle: Angle of the bend.
    :ivar dist_bend_bot: Distance of the bend from the bottom of the
        component.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Bend.
    """

    angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "Angle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_bend_bot: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistBendBot",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class BhaRun:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class BitDullCode(Enum):
    """
    Specifies the reason a drill bit was declared inoperable; these codes were
    originally defined by the IADC.

    :cvar BC: Broken Cone
    :cvar BF: Bond Failure
    :cvar BT: Broken Teeth/Cutters
    :cvar BU: Balled Up
    :cvar CC: Cracked Cone
    :cvar CD: Cone Dragged
    :cvar CI: Cone Interference
    :cvar CR: Cored
    :cvar CT: Chipped Teeth
    :cvar ER: Erosion
    :cvar FC: Flat Crested Wear
    :cvar HC: Heat Checking
    :cvar JD: Junk Damage
    :cvar LC: Lost Cone
    :cvar LN: Lost Nozzle
    :cvar LT: Lost Teeth/Cutters
    :cvar NO: No Dull/No Other Wear
    :cvar NR: Not Reusable
    :cvar OC: Off-Center Wear
    :cvar PB: Pinched Bit
    :cvar PN: Plugged Nozzle
    :cvar RG: Rounded Gauge
    :cvar RO: Ring Out
    :cvar RR: Re-usable
    :cvar SD: Shirttail Damage
    :cvar SS: Self-Sharpening Wear
    :cvar TR: Tracking
    :cvar WO: WashOut on Bit
    :cvar WT: Worn Teeth/Cutters
    """

    BC = "BC"
    BF = "BF"
    BT = "BT"
    BU = "BU"
    CC = "CC"
    CD = "CD"
    CI = "CI"
    CR = "CR"
    CT = "CT"
    ER = "ER"
    FC = "FC"
    HC = "HC"
    JD = "JD"
    LC = "LC"
    LN = "LN"
    LT = "LT"
    NO = "NO"
    NR = "NR"
    OC = "OC"
    PB = "PB"
    PN = "PN"
    RG = "RG"
    RO = "RO"
    RR = "RR"
    SD = "SD"
    SS = "SS"
    TR = "TR"
    WO = "WO"
    WT = "WT"


class BitReasonPulled(Enum):
    """
    Specifies the reason for pulling a drill bit from the wellbore, these codes
    were originally defined by the IADC.

    :cvar BHA: Change Bottom Hole Assembly
    :cvar CM: Condition Mud
    :cvar CP: Core Point
    :cvar DMF: Downhole Motor Failure
    :cvar DP: Drill Plug
    :cvar DST: Drill Stem Test
    :cvar DTF: Downhole Tool Failure
    :cvar FM: Formation Change
    :cvar HP: Hole Problems
    :cvar HR: Hours on Bit
    :cvar LOG: Run Logs
    :cvar PP: Pump Pressure
    :cvar PR: Penetration Rate
    :cvar RIG: Rig Repairs
    :cvar TD: Total Depth/Casing Depth
    :cvar TQ: Torque
    :cvar TW: Twist Off
    :cvar WC: Weather Conditions
    """

    BHA = "BHA"
    CM = "CM"
    CP = "CP"
    DMF = "DMF"
    DP = "DP"
    DST = "DST"
    DTF = "DTF"
    FM = "FM"
    HP = "HP"
    HR = "HR"
    LOG = "LOG"
    PP = "PP"
    PR = "PR"
    RIG = "RIG"
    TD = "TD"
    TQ = "TQ"
    TW = "TW"
    WC = "WC"


class BitType(Enum):
    """
    Specifies the  values that represent the type of drill or core bit.

    :cvar DIAMOND: Diamond bit.
    :cvar DIAMOND_CORE: Diamond core bit.
    :cvar INSERT_ROLLER_CONE: Insert roller cone bit.
    :cvar PDC: Polycrystalline diamond compact fixed-cutter bit.
    :cvar PDC_CORE: Polycrystalline diamond compact core bit.
    :cvar ROLLER_CONE: Milled-tooth roller-cone bit.
    """

    DIAMOND = "diamond"
    DIAMOND_CORE = "diamond core"
    INSERT_ROLLER_CONE = "insert roller cone"
    PDC = "PDC"
    PDC_CORE = "PDC core"
    ROLLER_CONE = "roller cone"


class BladeShapeType(Enum):
    """Blade shape of the stabilizer: melon, spiral, straight, etc."""

    DYNAMIC = "dynamic"
    MELON = "melon"
    SPIRAL = "spiral"
    STRAIGHT = "straight"
    VARIABLE = "variable"


class BladeType(Enum):
    """
    Specifies the blade type of the stabilizer.
    """

    CLAMP_ON = "clamp-on"
    INTEGRAL = "integral"
    SLEEVE = "sleeve"
    WELDED = "welded"


class BopType(Enum):
    """
    Specifies the type of blowout preventer.
    """

    ANNULAR_PREVENTER = "annular preventer"
    SHEAR_RAM = "shear ram"
    BLIND_RAM = "blind ram"
    PIPE_RAM = "pipe ram"
    DRILLING_SPOOL = "drilling spool"
    FLEXIBLE_JOINT = "flexible joint"
    CONNECTOR = "connector"


@dataclass
class BoreholeStringReference:
    """
    Reference to a borehole string.

    :ivar borehole_string: Reference to a borehole string.
    :ivar string_equipment: Optional references to string equipment
        within the BoreholeString.
    """

    borehole_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "BoreholeString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    string_equipment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StringEquipment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class BoreholeType(Enum):
    """
    Specifies the values for the type of borehole.
    """

    CAVERN = "cavern"
    CAVITY = "cavity"
    NORMALBOREHOLE = "normalborehole"
    UNDERREAM = "underream"


@dataclass
class BottomHoleLocation:
    """
    This class is used to represent the bottomhole location of a wellbore.

    :ivar location: The bottomhole's position.
    :ivar osdulocation_metadata: Additional OSDU-specific metadata about
        the location.
    """

    location: Optional[str] = field(
        default=None,
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    osdulocation_metadata: Optional[str] = field(
        default=None,
        metadata={
            "name": "OSDULocationMetadata",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class BoxPinConfig(Enum):
    """
    Specifies values that represent the type of box and pin configuration.
    """

    BOTTOM_BOX_TOP_BOX = "bottom box top box"
    BOTTOM_BOX_TOP_PIN = "bottom box top pin"
    BOTTOM_PIN_TOP_PIN = "bottom pin top pin"
    BOTTOM_PIN_TOP_BOX = "bottom pin top box"


class BrineType(Enum):
    """
    Specifies the class of brine.
    """

    CALCIUM_BROMIDE = "calcium bromide"
    POTASSIUM_BROMIDE = "potassium bromide"
    SODIUM_BROMIDE = "sodium bromide"
    ZINC_DIBROMIDE = "zinc dibromide"
    AMMONIUM_CHLORIDE = "ammonium chloride"
    CALCIUM_CHLORIDE = "calcium chloride"
    POTASSIUM_CHLORIDE = "potassium chloride"
    SODIUM_CHLORIDE = "sodium chloride"
    CESIUM_FORMATE = "cesium formate"
    POTASSIUM_FORMATE = "potassium formate"
    SODIUM_FORMATE = "sodium formate"
    BLEND = "blend"


class CalibrationPointRole(Enum):
    """
    The role of a calibration point in a log depth registration.

    :cvar LEFT_EDGE: Denotes the calibration being made on the left edge
        of the image.
    :cvar RIGHT_EDGE: Denotes the calibration being made on the right
        edge of the image.
    :cvar FRACTION: Denotes an intermediate point from the left edge to
        the right edge.
    :cvar OTHER: The value is not known. Avoid using this value. All
        reasonable attempts should be made to determine the appropriate
        value. Use of this value may result in rejection in some
        situations.
    """

    LEFT_EDGE = "left edge"
    RIGHT_EDGE = "right edge"
    FRACTION = "fraction"
    OTHER = "other"


class CasingConnectionTypes(Enum):
    """
    Specifies the values for connection type of casing.
    """

    LANDED = "landed"
    SELF_SEALING_THREADED = "self-sealing-threaded"
    WELDED = "welded"


@dataclass
class CementAdditive:
    """
    Cement Additive Component Schema.

    :ivar name_add: Additive name.
    :ivar type_add: Additive type or function (e.g., retarder,
        visosifier, weighting agent).
    :ivar form_add: Wet or dry.
    :ivar dens_add: Additive density.
    :ivar additive: Additive amount.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for the additive.
    """

    name_add: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameAdd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    type_add: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeAdd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    form_add: Optional[str] = field(
        default=None,
        metadata={
            "name": "FormAdd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dens_add: Optional[str] = field(
        default=None,
        metadata={
            "name": "DensAdd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    additive: Optional[str] = field(
        default=None,
        metadata={
            "name": "Additive",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class CementJob:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class CementJobEvaluation:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class CementPumpScheduleStep:
    """
    Cement Pump Schedule Component Schema, which defines the cement pumping
    schedule for a given step in a cement job.

    :ivar fluid: Reference to a fluid used in CementJob.
    :ivar ratio_fluid_excess: The ratio of excess fluid to total fluid
        pumped during the step.
    :ivar etim_pump: The duration of the fluid pumping.
    :ivar rate_pump: Rate at which the fluid is pumped. 0 means it is a
        pause.
    :ivar vol_pump: Volume pumped = eTimPump * ratePump.
    :ivar stroke_pump: Number of pump strokes for the fluid to be pumped
        (assumes the pump output is known).
    :ivar pres_back: Back pressure applied during the pumping stage.
    :ivar etim_shutdown: The duration of the shutdown event.
    :ivar comments: Comments and remarks.
    :ivar uid: Unique identifier for this pump schedule step.
    """

    fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    ratio_fluid_excess: Optional[str] = field(
        default=None,
        metadata={
            "name": "RatioFluidExcess",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_pump: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimPump",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rate_pump: Optional[str] = field(
        default=None,
        metadata={
            "name": "RatePump",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_pump: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolPump",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    stroke_pump: Optional[int] = field(
        default=None,
        metadata={
            "name": "StrokePump",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_back: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresBack",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_shutdown: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimShutdown",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Channel:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class ChannelData:
    """
    Contains the bulk data for the log, either as a base64-encoded string or as a
    reference to an external file.

    :ivar data: The data blob in JSON form. This attribute lets you
        embed the bulk data in a single file with the xml, to avoid the
        issues that arise when splitting data across multiple files.
        BUSINESS RULE: Either this element or the FileUri element must
        be present. STORE MANAGED. This is populated by a store on read.
        Customer provided values are ignored on write
    :ivar file_uri: The URI of a file containing the bulk data. If this
        field is non-null, then the data field is ignored. For files
        written to disk, this should normally contain a simple file name
        in relative URI form. For example, if an application writes a
        log file to disk, it might write the xml as abc.xml, and the
        bulk data as abc.avro. In this case, the value of this element
        would be './abc.avro'. BUSINESS RULE: Either this element or the
        Data element must be present.
    """

    data: Optional[str] = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    file_uri: Optional[str] = field(
        default=None,
        metadata={
            "name": "FileUri",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class ChannelDataKind(Enum):
    """
    Specifies the kind of data contained in a channel.

    :cvar BOOLEAN: True or false values.
    :cvar BYTES: Integer data value (nominally a one-byte value). The
        value must conform to the format of the xsd:dateTime data type
        (minInclusive=-128 and maxInclusive=127).
    :cvar DOUBLE: Double-precision floating-point value (nominally an
        8-byte value). The value must conform to the format of the
        xsd:double data type.
    :cvar FLOAT: Single-precision floating-point value (nominally a
        4-byte value). The value must conform to the format of the
        xsd:float data type
    :cvar INT: Integer data value (nominally a 4-byte value). The value
        must conform to the format of the xsd:int data type.
    :cvar LONG: Long integer data value (nominally an 8-byte value). The
        value must conform to the format of the xsd:long data type.
    :cvar STRING: Character string data. The value must conform to the
        format of the xsd:string data type. The maximum length of a
        value is determined by individual servers.
    :cvar MEASURED_DEPTH: Measured depth.
    :cvar TRUE_VERTICAL_DEPTH: True vertical depth.
    :cvar PASS_INDEXED_DEPTH: An index value that includes pass,
        direction, and depth values This can only refer to measured
        depths.
    :cvar DATE_TIME: Date with time.
    :cvar ELAPSED_TIME: Time that has elapsed.
    """

    BOOLEAN = "boolean"
    BYTES = "bytes"
    DOUBLE = "double"
    FLOAT = "float"
    INT = "int"
    LONG = "long"
    STRING = "string"
    MEASURED_DEPTH = "measured depth"
    TRUE_VERTICAL_DEPTH = "true vertical depth"
    PASS_INDEXED_DEPTH = "pass indexed depth"
    DATE_TIME = "date time"
    ELAPSED_TIME = "elapsed time"


@dataclass
class ChannelIndex:
    """
    Common information about a primary or secondary index for a channel or channel
    set.

    :ivar index_kind: The kind of index (date time, measured depth,
        etc.). IMMUTABLE. Set on object creation and MUST NOT change
        thereafter. Customer provided changes after creation are an
        error.
    :ivar index_property_kind: An optional value pointing to a
        PropertyKind. Energistics provides a list of standard property
        kinds that represent the basis for the commonly used properties
        in the E&amp;P subsurface workflow. This PropertyKind
        enumeration is in the external PropertyKindDictionary XML file
        in the Common ancillary folder. IMMUTABLE. Set on object
        creation and MUST NOT change thereafter. Customer provided
        changes after creation are an error.
    :ivar uom: The unit of measure of the index. Must be one of the
        units allowed for the specified IndexKind (e.g., time or depth).
        IMMUTABLE. Set on object creation and MUST NOT change
        thereafter. Customer provided changes after creation are an
        error.
    :ivar direction: The direction of the index, either increasing or
        decreasing. Index direction may not change within the life of a
        channel or channel set. This only affects the order in which
        data is streamed or serialized. IMMUTABLE. Set on object
        creation and MUST NOT change thereafter. Customer provided
        changes after creation are an error.
    :ivar mnemonic: The mnemonic for the index. IMMUTABLE. Set on object
        creation and MUST NOT change thereafter. Customer provided
        changes after creation are an error.
    :ivar datum: For depth indexes, this is a pointer to the reference
        point defining the vertical datum, in a channel's Well object,
        to which all of the index values are referenced. IMMUTABLE. Set
        on object creation and MUST NOT change thereafter. Customer
        provided changes after creation are an error.
    :ivar index_interval: The index value range for this index for the
        channel or channel set. This MUST reflect the minimum and
        maximum index values for this index for data points in the
        channel or channel set. This is independent of the direction for
        the primary index. This MUST be specified when there are data
        points in the channel or channel set, and it MUST NOT be
        specified when there are no data points in the channel or
        channel set. STORE MANAGED. This is populated by a store on
        read. Customer provided values are ignored on write
    """

    index_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "IndexKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    index_property_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "IndexPropertyKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "Uom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    direction: Optional[str] = field(
        default=None,
        metadata={
            "name": "Direction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    mnemonic: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mnemonic",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    datum: Optional[str] = field(
        default=None,
        metadata={
            "name": "Datum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    index_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "IndexInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class ChannelKind:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class ChannelKindDictionary:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class ChannelOsduintegration:
    """
    Information about a Channel that is relevant for OSDU integration but does not
    have a natural place in a Channel object.

    :ivar channel_quality: The quality of the channel.
    :ivar intermediary_service_company: Pointer to a BusinessAssociate
        that represents the company who engaged the service company
        (ServiceCompany) to perform the logging.
    :ivar is_regular: Boolean property indicating the sampling mode of
        the primary index. True means all channel data values are
        regularly spaced (see NominalSamplingInterval); false means
        irregular or discrete sample spacing.
    :ivar zero_time: Optional time reference for time-based primary
        indexes. The ISO date time string representing zero time. Not to
        be confused with seismic travel time zero.
    :ivar channel_business_value: The business value of the channel.
    :ivar channel_main_family: The Geological Physical Quantity measured
        by the channel such as porosity.
    :ivar channel_family: The detailed Geological Physical Quantity
        measured by the channel such as neutron porosity.
    """

    class Meta:
        name = "ChannelOSDUIntegration"

    channel_quality: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChannelQuality",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    intermediary_service_company: Optional[str] = field(
        default=None,
        metadata={
            "name": "IntermediaryServiceCompany",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_regular: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsRegular",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    zero_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "ZeroTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    channel_business_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChannelBusinessValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    channel_main_family: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChannelMainFamily",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    channel_family: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChannelFamily",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class ChannelSet:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class ChannelSetOsduintegration:
    """
    Information about a ChannelSet that is relevant for OSDU integration but does
    not have a natural place in a ChannelSet object.

    :ivar channel_set_version: The channel set version. Distinct from
        objectVersion.
    :ivar frame_identifier: For multi-frame or multi-section files, this
        identifier defines the source frame in the file. If the
        identifier is an index number the index starts with zero and is
        converted to a string for this property.
    :ivar intermediary_service_company: Pointer to a BusinessAssociate
        that represents the company who engaged the service company
        (ServiceCompany) to perform the logging.
    :ivar is_regular: Boolean property indicating the sampling mode of
        the primary index. True means all channel data values are
        regularly spaced (see NominalSamplingInterval); false means
        irregular or discrete sample spacing.
    :ivar zero_time: Optional time reference for time-based primary
        indexes. The ISO date time string representing zero time. Not to
        be confused with seismic travel time zero.
    """

    class Meta:
        name = "ChannelSetOSDUIntegration"

    channel_set_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChannelSetVersion",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    frame_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "FrameIdentifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    intermediary_service_company: Optional[str] = field(
        default=None,
        metadata={
            "name": "IntermediaryServiceCompany",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_regular: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsRegular",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    zero_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "ZeroTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class Chromatograph:
    """
    Analysis done to determine the components in a show.

    :ivar chromatograph_md_interval: Measured interval related to the
        chromatograph results.
    :ivar date_time_gas_sample_processed: The date and time at which the
        gas sample was processed.
    :ivar chromatograph_type: Chromatograph type.
    :ivar etim_chrom_cycle: Chromatograph cycle time. Commonly in
        seconds.
    :ivar chrom_report_time: Chromatograph integrator report time;
        format may be variable due to recording equipment.
    :ivar mud_weight_in: Mud density in (active pits).
    :ivar mud_weight_out: Mud density out (flowline).
    :ivar meth_av: Methane (C1) ppm (average).
    :ivar meth_mn: Methane (C1) ppm (minimum).
    :ivar meth_mx: Methane (C1) ppm (maximum).
    :ivar eth_av: Ethane (C2) ppm (average).
    :ivar eth_mn: Ethane (C2) ppm (minimum).
    :ivar eth_mx: Ethane (C2) ppm (maximum).
    :ivar prop_av: Propane (C3) ppm (average).
    :ivar prop_mn: Propane (C3) ppm (minimum).
    :ivar prop_mx: Propane (C3) ppm (maximum).
    :ivar ibut_av: iso-Butane (iC4) ppm (average).
    :ivar ibut_mn: iso-Butane (iC4) ppm (minimum).
    :ivar ibut_mx: iso-Butane (iC4) ppm (maximum).
    :ivar nbut_av: nor-Butane (nC4) ppm (average).
    :ivar nbut_mn: nor-Butane (nC4) ppm (minimum).
    :ivar nbut_mx: nor-Butane (nC4) ppm (maximum).
    :ivar ipent_av: iso-Pentane (iC5) ppm (average).
    :ivar ipent_mn: iso-Pentane (iC5) ppm (minimum).
    :ivar ipent_mx: iso-Pentane (iC5) ppm (maximum).
    :ivar npent_av: nor-Pentane (nC5) ppm (average).
    :ivar npent_mn: nor-Pentane (nC5) ppm (minimum).
    :ivar npent_mx: nor-Pentane (nC5) ppm (maximum).
    :ivar epent_av: neo-Pentane (eC5) ppm (average).
    :ivar epent_mn: neo-Pentane (eC5) ppm (minimum).
    :ivar epent_mx: neo-Pentane (eC5) ppm (maximum).
    :ivar ihex_av: iso-Hexane (iC6) ppm (average).
    :ivar ihex_mn: iso-Hexane (iC6) ppm (minimum).
    :ivar ihex_mx: iso-Hexane (iC6) ppm (maximum).
    :ivar nhex_av: nor-Hexane (nC6) ppm (average).
    :ivar nhex_mn: nor-Hexane (nC6) ppm (minimum).
    :ivar nhex_mx: nor-Hexane (nC6) ppm (maximum).
    :ivar co2_av: Carbon Dioxide ppm (average).
    :ivar co2_mn: Carbon Dioxide ppm (minimum).
    :ivar co2_mx: Carbon Dioxide ppm (maximum).
    :ivar h2s_av: Hydrogen Sulfide (average) ppm.
    :ivar h2s_mn: Hydrogen Sulfide (minimum) ppm.
    :ivar h2s_mx: Hydrogen Sulfide (maximum) ppm.
    :ivar acetylene: Acetylene.
    :ivar channel:
    """

    chromatograph_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChromatographMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    date_time_gas_sample_processed: Optional[str] = field(
        default=None,
        metadata={
            "name": "DateTimeGasSampleProcessed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    chromatograph_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChromatographType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_chrom_cycle: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimChromCycle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    chrom_report_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChromReportTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mud_weight_in: Optional[str] = field(
        default=None,
        metadata={
            "name": "MudWeightIn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mud_weight_out: Optional[str] = field(
        default=None,
        metadata={
            "name": "MudWeightOut",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    meth_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "MethAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    meth_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "MethMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    meth_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "MethMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    eth_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "EthAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    eth_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "EthMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    eth_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "EthMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    prop_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "PropAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    prop_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "PropMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    prop_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "PropMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ibut_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "IbutAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ibut_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "IbutMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ibut_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "IbutMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nbut_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "NbutAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nbut_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "NbutMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nbut_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "NbutMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ipent_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "IpentAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ipent_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "IpentMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ipent_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "IpentMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    npent_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "NpentAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    npent_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "NpentMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    npent_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "NpentMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    epent_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "EpentAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    epent_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "EpentMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    epent_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "EpentMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ihex_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "IhexAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ihex_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "IhexMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ihex_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "IhexMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nhex_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "NhexAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nhex_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "NhexMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nhex_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "NhexMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    co2_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "Co2Av",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    co2_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "Co2Mn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    co2_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "Co2Mx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    h2s_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "H2sAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    h2s_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "H2sMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    h2s_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "H2sMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    acetylene: Optional[str] = field(
        default=None,
        metadata={
            "name": "Acetylene",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class Coating(Enum):
    """
    Specifies the values for the type of inside or outside coating of this piece of
    equipment.
    """

    BARE = "bare"
    CARBONNITRIDED = "carbonnitrided"
    CARBURIZED = "carburized"
    CARBURIZED_HARDENED = "carburized-hardened"
    CEMENTLINED = "cementlined"
    CHROME = "chrome"
    CHROME_PLATED = "chrome-plated"
    CHROMEPLATED_GROOVED = "chromeplated-grooved"
    CHROMEPLATED_HEAVY = "chromeplated-heavy"
    CORROSION_COATING = "corrosion coating"
    DBLGALV = "dblgalv"
    DUOLIN20WR = "duolin20wr"
    DUOLINE = "duoline"
    DUOLINE10 = "duoline10"
    DUOLINE20 = "duoline20"
    EPDM = "epdm"
    FIBERGLASS_LINED = "fiberglass-lined"
    GALVANIZED = "galvanized"
    HARDENED = "hardened"
    HARD_LINED = "hard-lined"
    INS = "ins"
    IPC = "ipc"
    IPC_EPOXY = "ipc-epoxy"
    IPC_EPXTHK = "ipc-epxthk"
    IPC_EPXTHN = "ipc-epxthn"
    IPC_NYLON = "ipc-nylon"
    IPC_RWRAP = "ipc-rwrap"
    IPC_S505 = "ipc-s505"
    IPC_S650 = "ipc-s650"
    IPC_TK70 = "ipc-tk70"
    IPC_TK75 = "ipc-tk75"
    LP = "lp"
    MOLY = "moly"
    MTR = "mtr"
    N_A = "n/a"
    NICKEL_CARBIDE = "nickel-carbide"
    NICKEL_PLATED = "nickel-plated"
    NITRIDED = "nitrided"
    NITRILE = "nitrile"
    PAP = "pap"
    PELINED = "pelined"
    PHOSPHATE = "phosphate"
    PHOSPHORUS = "phosphorus"
    PLASTIC = "plastic"
    PLUNGER_LUBRICANT = "plunger-lubricant"
    POLISHED_RODLINER = "polished-rodliner"
    POLYPROPYLENE = "polypropylene"
    PPW_NITRL = "ppw/nitrl"
    PVCLINED = "pvclined"
    RODGUIDE_1 = "rodguide-1"
    RODGUIDE_2 = "rodguide-2"
    RODGUIDE_2_1 = "rodguide-2."
    RODGUIDE_3 = "rodguide-3"
    RODGUIDE_4 = "rodguide-4"
    RODGUIDE_5 = "rodguide-5"
    RODGUIDE_6 = "rodguide-6"
    RODGUIDE_7 = "rodguide-7"
    RODGUIDE_FX = "rodguide-fx"
    RODGUIDE_SO = "rodguide-so"
    RODGUIDE_SO1 = "rodguide-so1"
    RODGUIDE_SO2 = "rodguide-so2"
    RODGUIDE_SO3 = "rodguide-so3"
    RODGUIDE_SO4 = "rodguide-so4"
    RODGUIDE_SO5 = "rodguide-so5"
    RODGUIDE_SO6 = "rodguide-so6"
    RODGUIDE_SO8 = "rodguide-so8"
    RODGUIDE_SP = "rodguide-sp"
    SPRAY_METAL = "spray-metal"
    SPRAY_METAL_MONEL = "spray-metal-monel"
    SPRAYMETAL_MONEL_1 = "spraymetal-monel"
    SPRAYMETAL_NICKEL = "spraymetal-nickel"
    SPRAYMETAL_OD_NICKELPLATED_ID = "spraymetal-od/nickelplated-id"
    SPRAYMETAL_STEEL = "spraymetal-steel"
    SPRAYMETAL_THICK = "spraymetal-thick"
    SSLINED = "sslined"
    TEFLON = "teflon"
    TEFLON_RED = "teflon-red"
    TEFLON_TAN = "teflon-tan"
    TEFLON_YELLOW = "teflon-yellow"
    THERMO = "thermo"
    TK_4 = "tk-4"
    TK_99 = "tk-99"
    TUFFR = "tuffr"
    TUNGSTEN_PLATED = "tungsten plated"
    ZINCPLATED = "zincplated"


class CompletionStatus(Enum):
    """
    Specifies the values of the status of a wellbore completion.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    PERMANENTLY_ABANDONED = "permanently abandoned"
    PLANNED = "planned"
    SUSPENDED = "suspended"
    TEMPORARILY_ABANDONED = "temporarily abandoned"
    TESTING = "testing"


class ConcentrationParameterKind(Enum):
    """
    Specifies the values for mud log parameters that are measured in units of
    concentration.

    :cvar CUTTINGS_GAS: The cuttings gas concentration averaged over the
        interval.
    """

    CUTTINGS_GAS = "cuttings gas"


class ConnectionFormType(Enum):
    """
    Specifies the values for the type of equipment-to-equipment connection.
    """

    BOX = "box"
    FLANGE = "flange"
    MANDREL = "mandrel"
    PIN = "pin"
    WELDED = "welded"


class ConnectionPosition(Enum):
    """
    Specifies the position of a connection.

    :cvar BOTH: The connection is the same at both ends of the
        component.
    :cvar BOTTOM: This connection is only at the bottom of the
        component.
    :cvar TOP: This connection is only at the top of the component.
    """

    BOTH = "both"
    BOTTOM = "bottom"
    TOP = "top"


@dataclass
class CuttingsGeology:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class CuttingsGeologyInterval:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class DeflectionMethod(Enum):
    """
    Specifies the method used to direct the deviation of the trajectory in
    directional drilling.

    :cvar HYBRID: Rotary steerable system that changes the trajectory of
        a wellbore using both point-the-bit and push-the-bit methods.
    :cvar POINT_BIT: Rotary steerable system that changes the trajectory
        of a wellbore by tilting the bit to point it in the desired
        direction.
    :cvar PUSH_BIT: Rotary steerable system that changes the trajectory
        of a wellbore by inducing a side force to push the bit in the
        desired direction.
    """

    HYBRID = "hybrid"
    POINT_BIT = "point bit"
    PUSH_BIT = "push bit"


@dataclass
class DepthRegImage:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class DepthRegParameter:
    """
    Specifies parameters associated with the log section and includes top and
    bottom indexes, a description string, and mnemonic.

    :ivar mnemonic: A dictionary-controlled mnemonic.
    :ivar dictionary: The name or identifier of the controlling
        dictionary.
    :ivar index_interval: The index value range for the vertical region
        for which the parameter value is applicable.
    :ivar value: The value assigned to the parameter. The unit of
        measure should be consistent with the property implied by
        'mnemonic' in 'dictionary'. If the value is unitless, then use a
        unit of 'Euc'.
    :ivar description: A description or definition for the mnemonic;
        required when ../dictionary is absent.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for the parameter.
    """

    mnemonic: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mnemonic",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    dictionary: Optional[str] = field(
        default=None,
        metadata={
            "name": "Dictionary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    index_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "IndexInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DepthRegPoint:
    """
    The position of a pixel of an image, in x-y coordinates.

    :ivar x: The x pixel position of a point.
    :ivar y: The y pixel position of a point.
    """

    x: Optional[str] = field(
        default=None,
        metadata={
            "name": "X",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    y: Optional[str] = field(
        default=None,
        metadata={
            "name": "Y",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class DownholeComponent:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class DownholeStringReference:
    """
    Reference to a downhole string.

    :ivar downhole_string: Reference to a downhole string.
    :ivar string_equipment: Optional references to string equipment
        within the downhole string.
    """

    downhole_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "DownholeString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    string_equipment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StringEquipment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class DownholeStringType(Enum):
    """
    Specifies the values for the type of downhole strings.
    """

    CASING = "casing"
    OTHERS = "others"
    ROD = "rod"
    TUBING = "tubing"
    WELLHEAD = "wellhead"


class DrillActivityTypeType(Enum):
    """
    Activity classifier, e.g., planned, unplanned, downtime.
    """

    PLANNED = "planned"
    UNPLANNED = "unplanned"
    DOWNTIME = "downtime"


class DrillActivityCode(Enum):
    """
    A code to specify the drilling activity.
    """

    ABANDONMENT = "abandonment"
    ABANDONMENT_LOG_PLUGS = "abandonment -- log plugs"
    ABANDONMENT_RUN_PLUGS = "abandonment -- run plugs"
    ABANDONMENT_WAIT_ON_CEMENT = "abandonment -- wait on cement"
    CASING = "casing"
    CEMENT = "cement"
    CEMENT_CIRCULATE = "cement -- circulate"
    CEMENT_OTHER = "cement -- other"
    CEMENT_RIG_UP = "cement -- rig up"
    CEMENT_WAIT_ON_CEMENT = "cement -- wait on cement"
    CIRCULATE = "circulate"
    CIRCULATE_BOULDER_OR_GRAVEL = "circulate -- boulder or gravel"
    CIRCULATE_CASING = "circulate -- casing"
    CIRCULATE_CEMENTING = "circulate -- cementing"
    CIRCULATE_CIRCULATE_SAMPLES = "circulate -- circulate samples"
    CIRCULATE_CORING = "circulate -- coring"
    CIRCULATE_DRILLING = "circulate -- drilling"
    CIRCULATE_FISHING = "circulate -- fishing"
    CIRCULATE_GUMBO_ATTACK = "circulate -- gumbo attack"
    CIRCULATE_LOGGING = "circulate -- logging"
    CIRCULATE_LOST_CIRCULATION = "circulate -- lost circulation"
    CIRCULATE_WELL_CONTROL = "circulate -- well control"
    COMPLETION_OPERATIONS = "completion operations"
    COMPLETION_OPERATIONS_GRAVEL_PACKING = (
        "completion operations -- gravel packing"
    )
    COMPLETION_OPERATIONS_LOGGING = "completion operations -- logging"
    COMPLETION_OPERATIONS_RIG_UP = "completion operations -- rig up"
    COMPLETION_OPERATIONS_RUNNING_LINER = (
        "completion operations -- running liner"
    )
    COMPLETION_OPERATIONS_TEAR_DOWN = "completion operations -- tear down"
    COMPLETION_OPERATIONS_TESTING = "completion operations -- testing"
    COND_MUD = "cond mud"
    CORING = "coring"
    CORING_CONVENTIONAL = "coring -- conventional"
    CORING_FLOW_CHECK = "coring -- flow check"
    CORING_LAYDOWN_BARREL = "coring -- laydown barrel"
    CORING_ORIENTED = "coring -- oriented"
    CORING_PLASTIC_SLEEVE = "coring -- plastic sleeve"
    CORING_RIG_UP_CORE_BARREL = "coring -- rig up core barrel"
    CORING_SPONGE = "coring -- sponge"
    CUT = "cut"
    DEVIATION_SURVEY = "deviation survey"
    DEVIATION_SURVEY_DIR_MULTI_SHOT = "deviation survey -- dir multi-shot"
    DEVIATION_SURVEY_DIR_SINGLE_SHOT = "deviation survey -- dir single shot"
    DEVIATION_SURVEY_DRIFT = "deviation survey -- drift"
    DEVIATION_SURVEY_GYRO = "deviation survey -- gyro"
    DEVIATION_SURVEY_MWD = "deviation survey -- MWD"
    DIR_WORK = "dir work"
    DIR_WORK_HORIZONTAL_DRILLING = "dir work -- horizontal drilling"
    DIR_WORK_MOTOR_DRILLING = "dir work -- motor drilling"
    DIR_WORK_ORIENT = "dir work -- orient"
    DIR_WORK_ROTARY_DRILLING = "dir work -- rotary drilling"
    DIR_WORK_SLANT_DRILLING = "dir work -- slant drilling"
    DRILLING = "drilling"
    DRILLING_CASING = "drilling -- casing"
    DRILLING_CONNECTION = "drilling -- connection"
    DRILLING_DRILL_CEMENT = "drilling -- drill cement"
    DRILLING_FLOW_CHECK = "drilling -- flow check"
    DRILLING_HOLE_OPENING = "drilling -- hole opening"
    DRILLING_NEW_HOLE = "drilling -- new hole"
    DRILLING_SIDETRACKING = "drilling -- sidetracking"
    DRILLING_UNDER_REAMING = "drilling -- under-reaming"
    DST = "DST"
    DST_CASED_HOLE = "DST -- cased hole"
    DST_LAY_DOWN_TOOLS = "DST -- lay down tools"
    DST_OPEN_HOLE = "DST -- open hole"
    DST_OPEN_HOLE_CLOSED_CHAMBER = "DST -- open hole closed chamber"
    DST_RIG_UP_TOOLS = "DST -- rig up tools"
    FISHING = "fishing"
    FISHING_BHA = "fishing -- BHA"
    FISHING_CASING = "fishing -- casing"
    FISHING_CONES = "fishing -- cones"
    FISHING_OTHER = "fishing -- other"
    FISHING_STUCK_PIPE = "fishing -- stuck pipe"
    FISHING_WIRELINE_TOOLS = "fishing -- wireline tools"
    FLOAT_EQUIP = "float equip"
    HSE = "HSE"
    HSE_HOLD_DRILL = "HSE -- hold drill"
    HSE_INCIDENT = "HSE -- incident"
    HSE_SAFETY_MEETING = "HSE -- safety meeting"
    MILL = "mill"
    MILL_CUT_CASING_OR_TUBING = "mill -- cut casing or tubing"
    MILL_MILLING = "mill -- milling"
    MISCELLANEOUS = "miscellaneous"
    NIPPLE_UP_BOP = "nipple up BOP"
    NIPPLE_UP_BOP_DIVERTER = "nipple up BOP -- diverter"
    NIPPLE_UP_BOP_MANIFOLD = "nipple up BOP -- manifold"
    NIPPLE_UP_BOP_OTHER = "nipple up BOP -- other"
    NIPPLE_UP_BOP_PVT_SYSTEM = "nipple up BOP -- PVT system"
    NIPPLE_UP_BOP_STACK = "nipple up BOP -- stack"
    PLUG_BACK = "plug back"
    PLUG_BACK_ABANDONMENT = "plug back -- abandonment"
    PLUG_BACK_KICK_OFF_PLUG = "plug back -- kick off plug"
    PLUG_BACK_LOST_CIRCULATION = "plug back -- lost circulation"
    PLUG_BACK_WAIT_ON_CEMENT = "plug back -- wait on cement"
    PLUG_BACK_WELL_CONTROL = "plug back -- well control"
    PRESSURE_TEST = "pressure test"
    PRESSURE_TEST_BOP_MANIFOLD = "pressure test -- BOP manifold"
    PRESSURE_TEST_BOP_STACK = "pressure test -- BOP stack"
    PRESSURE_TEST_FORM_INTEGRITY_TEST = "pressure test -- form integrity test"
    PRESSURE_TEST_FORM_LEAK_OFF_TEST = "pressure test -- form leak off test"
    PRESSURE_TEST_PACKER = "pressure test -- packer"
    PRESSURE_TEST_PIT = "pressure test -- PIT"
    REAMING = "reaming"
    REAMING_BACK_REAMING = "reaming -- back reaming"
    REAMING_CORING = "reaming -- coring"
    REAMING_DRILL = "reaming -- drill"
    REAMING_LOGGING = "reaming -- logging"
    REAMING_UNDER_REAMING = "reaming -- under-reaming"
    RIG_MOVE = "rig move"
    RIG_MOVE_ANCHOR_HANDLING = "rig move -- anchor handling"
    RIG_MOVE_INTER_PAD_MOVE = "rig move -- inter-pad move"
    RIG_MOVE_INTER_WELL_MOVE = "rig move -- inter-well move"
    RIG_MOVE_JACK_UP_OR_DOWN = "rig move -- jack up or down"
    RIG_MOVE_OTHER = "rig move -- other"
    RIG_MOVE_POSITION_RIG = "rig move -- position rig"
    RIG_MOVE_SKID_RIG = "rig move -- skid rig"
    RIG_RELEASE = "rig release"
    RIG_RELEASE_CUT_CASING = "rig release -- cut casing"
    RIG_RELEASE_INSTALL_CAPPING_ASSEMBLY = (
        "rig release -- install capping assembly"
    )
    RIG_RELEASE_MOB_OR_DE_MOB = "rig release -- MOB or DE-MOB"
    RIG_REPAIRS = "rig repairs"
    RIG_REPAIRS_DRAWWORKS = "rig repairs -- drawworks"
    RIG_REPAIRS_ELECTRICAL = "rig repairs -- electrical"
    RIG_REPAIRS_MUD_SYSTEM = "rig repairs -- mud system"
    RIG_REPAIRS_OTHER = "rig repairs -- other"
    RIG_REPAIRS_ROTARY = "rig repairs -- rotary"
    RIG_REPAIRS_SUBSEA_EQUIPMENT = "rig repairs -- subsea equipment"
    RIG_REPAIRS_WELL_CONTROL_EQUIPMENT = (
        "rig repairs -- well control equipment"
    )
    RIG_SERVICE = "rig service"
    RIG_SERVICE_LUBRICATE_RIG = "rig service -- lubricate rig"
    RIG_SERVICE_TEST_EQUIPMENT = "rig service -- test equipment"
    RIG_UP_OR_TEAR_DOWN = "rig up or tear down"
    RIG_UP_OR_TEAR_DOWN_RIG_UP = "rig up or tear down -- rig up"
    RIG_UP_OR_TEAR_DOWN_SITE_WORK = "rig up or tear down -- site work"
    RIG_UP_OR_TEAR_DOWN_TEAR_DOWN = "rig up or tear down -- tear down"
    RUN_CASING = "run casing"
    RUN_LINER = "run liner"
    RUN_OR_PULL_RISER = "run or pull riser"
    RUN_OR_PULL_RISER_OTHER = "run or pull riser -- other"
    RUN_OR_PULL_RISER_RUN_OR_PULL_RISER = (
        "run or pull riser -- run or pull riser"
    )
    SET = "set"
    SLIP_DRILLING_LINE = "slip drilling line"
    SQUEEZE_CEMENT = "squeeze cement"
    SQUEEZE_CEMENT_CASING_REPAIR = "squeeze cement -- casing repair"
    SQUEEZE_CEMENT_CASING_SHOE = "squeeze cement -- casing shoe"
    SQUEEZE_CEMENT_PARTED_CASING = "squeeze cement -- parted casing"
    SQUEEZE_CEMENT_PERFORATIONS_DST = "squeeze cement -- perforations DST"
    STUCK_PIPE = "stuck pipe"
    SURFACE_STRING_HANDLING = "surface string handling"
    TEST_COMPLETION = "test completion"
    TESTING_GENERAL = "testing general"
    TESTING_GENERAL_EQUIPMENT = "testing general -- equipment"
    TESTING_GENERAL_FLOW = "testing general -- flow"
    TRIPPING = "tripping"
    TRIPPING_BACK_REAMING = "tripping -- back-reaming"
    TRIPPING_FLOW_CHECK = "tripping -- flow check"
    TRIPPING_SHORT_TRIP_IN = "tripping -- short trip in"
    TRIPPING_SHORT_TRIP_OUT = "tripping -- short trip out"
    TRIPPING_TRIP_IN_FROM_SURFACE = "tripping -- trip in (from surface)"
    TRIPPING_TRIP_OUT_TO_SURFACE = "tripping -- trip out (to surface)"
    WAIT = "wait"
    WAIT_DAYLIGHT = "wait -- daylight"
    WAIT_ENVIRONMENTAL_OR_REGULATORY = "wait -- environmental or regulatory"
    WAIT_EQUIPMENT = "wait -- equipment"
    WAIT_HOLIDAY = "wait -- holiday"
    WAIT_ICE = "wait -- ice"
    WAIT_ON_ORDERS = "wait -- on orders"
    WAIT_OPERATOR = "wait -- operator"
    WAIT_OTHER = "wait -- other"
    WAIT_PARTNERS = "wait -- partners"
    WAIT_SERVICE_COMPANY = "wait -- service company"
    WAIT_WEATHER = "wait -- weather"
    WELL_CONTROL = "well control"
    WELL_CONTROL_MIX = "well control -- mix"
    WELL_CONTROL_SHUT_IN = "well control -- shut in"
    WELL_CONTROL_STRIP = "well control -- strip"
    WELL_CONTROL_WELL_KILL = "well control -- well kill"
    WELL_SRVC = "well srvc"
    WELL_SRVC_CASING_REPAIR = "well srvc -- casing repair"
    WELL_SRVC_CLEAN_WELL_TO_COMPL_FLUID = (
        "well srvc -- clean well to compl fluid"
    )
    WELL_SRVC_COILED_TUBING_WORK = "well srvc -- coiled tubing work"
    WELL_SRVC_GRAVEL_PACK = "well srvc -- gravel pack"
    WELL_SRVC_INSTALL_OR_TEST_XMAS_TREE = (
        "well srvc -- install or test xmas tree"
    )
    WELL_SRVC_KILL_WELL = "well srvc -- kill well"
    WELL_SRVC_LAND = "well srvc -- land"
    WELL_SRVC_PERFORATE = "well srvc -- perforate"
    WELL_SRVC_PULL_COMPLETION = "well srvc -- pull completion"
    WELL_SRVC_PULL_SUSPENSION_PLUGS = "well srvc -- pull suspension plugs"
    WELL_SRVC_RUN_COMPLETION = "well srvc -- run completion"
    WELL_SRVC_RUN_SCREENS = "well srvc -- run screens"
    WELL_SRVC_SAND_CONTROL = "well srvc -- sand control"
    WELL_SRVC_STIMULATION = "well srvc -- stimulation"
    WELL_SRVC_SUBSEA_WORK = "well srvc -- subsea work"
    WELL_SRVC_SURFACE_LINE_WORK = "well srvc -- surface line work"
    WELL_SRVC_SUSPEND_WELL_OR_PULL_BOPS = (
        "well srvc -- suspend well or pull BOPs"
    )
    WELL_SRVC_TEST_WELL = "well srvc -- test well"
    WELL_SRVC_WASH = "well srvc -- wash"
    WELL_SRVC_WIRELINE_WORK = "well srvc -- wireline work"
    WELL_SRVC_WORK_TUBULARS = "well srvc -- work tubulars"
    WELL_SRVC_WORKSTRING_RUN = "well srvc -- workstring run"
    WIRELINE_LOGS = "wireline logs"
    WIRELINE_LOGS_ABANDONMENT = "wireline logs -- abandonment"
    WIRELINE_LOGS_EVALUATION = "wireline logs -- evaluation"
    WIRELINE_LOGS_FORM_TESTER = "wireline logs -- form tester"
    WIRELINE_LOGS_OTHER = "wireline logs -- other"
    WIRELINE_LOGS_SIDE_WALL_CORES = "wireline logs -- side wall cores"
    WIRELINE_LOGS_VELOCITY = "wireline logs -- velocity"


@dataclass
class DrillReport:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class DrillReportEquipFailureInfo:
    """
    General information about equipment failure that occurred during the drill
    report period.

    :ivar dtim: Date and time that the equipment failed.
    :ivar md: The measured depth of the operation end point where the
        failure happened.
    :ivar tvd: The true vertical depth of the  operation end point where
        failure the failure happened.
    :ivar equip_class: The classification of the equipment that failed.
    :ivar etim_miss_production: The missed production time because of
        the equipment failure.
    :ivar dtim_repair: The date and time at which the production
        equipment was repaired and ready for production.
    :ivar description: A description of the equipment failure.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        DrillReportEquipFailureInfo.
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md: Optional[str] = field(
        default=None,
        metadata={
            "name": "Md",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    equip_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "EquipClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_miss_production: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimMissProduction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_repair: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimRepair",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportFormTestInfo:
    """
    General information about a wireline formation test that occurred during the
    drill report period.

    :ivar dtim: Date and time that the wireline formation test was
        completed.
    :ivar md: Measured depth at which the wireline formation test was
        conducted.
    :ivar tvd: True vertical depth at which the wireline formation test
        was conducted.
    :ivar pres_pore: The formation pore pressure. The pressure of fluids
        within the pores of a reservoir, usually hydrostatic pressure,
        or the pressure exerted by a column of water from the
        formation's depth to sea level.
    :ivar good_seal: Was there a good seal for the wireline formation
        test? Values are "true" or "1" or "false" or "0".
    :ivar md_sample: Measured depth where the fluid sample was taken.
    :ivar dominate_component: The dominate component in the fluid
        sample.
    :ivar density_hc: The density of the hydrocarbon component of the
        fluid sample.
    :ivar volume_sample: The volume of the fluid sample.
    :ivar description: A detailed description of the wireline formation
        test.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        DrillReportFormTestInfo.
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md: Optional[str] = field(
        default=None,
        metadata={
            "name": "Md",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_pore: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresPore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    good_seal: Optional[bool] = field(
        default=None,
        metadata={
            "name": "GoodSeal",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_sample: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdSample",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dominate_component: Optional[str] = field(
        default=None,
        metadata={
            "name": "DominateComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    density_hc: Optional[str] = field(
        default=None,
        metadata={
            "name": "DensityHC",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    volume_sample: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolumeSample",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportLithShowInfo:
    """
    General information about the lithology and shows in an interval encountered
    during the drill report period.

    :ivar dtim: Date and time that the well test was completed.
    :ivar show_md_interval: Measured depth interval over which the show
        appears.
    :ivar show_tvd_interval: True vertical depth interval over which the
        show appears.
    :ivar show: A textual description of any shows in the interval.
    :ivar lithology: A geological/lithological description/evaluation of
        the interval.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        DrillReportLithShowInfo
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    show_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "ShowMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    show_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "ShowTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    show: Optional[str] = field(
        default=None,
        metadata={
            "name": "Show",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lithology: Optional[str] = field(
        default=None,
        metadata={
            "name": "Lithology",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportPerfInfo:
    """
    General information about a perforation interval related to the drill report
    period.

    :ivar dtim_open: The date and time at which the well perforation
        interval is opened.
    :ivar dtim_close: The date and time at which the well perforation
        interval is closed.
    :ivar perforation_md_interval: Measured depth interval between the
        top and the base of the perforations.
    :ivar perforation_tvd_interval: True vertical depth interval between
        the top and the base of the perforations.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        DrillReportPerfInfo.
    """

    dtim_open: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimOpen",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_close: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimClose",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportStratInfo:
    """
    General information about stratigraphy for the drill report period.

    :ivar dtim: Date and time at which a preliminary zonation was
        established.
    :ivar md_top: Measured depth at the top of the formation.
    :ivar tvd_top: True vertical depth at the top of the formation.
    :ivar description: A lithological description of the geological
        formation at the given depth.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        DrillReportStratInfo.
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_top: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_top: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportSurveyStation:
    """
    Trajectory station information for the drill report period.

    :ivar dtim: The date at which the directional survey took place.
    :ivar md: Measured depth of measurement from the drill datum.
    :ivar tvd: True vertical depth of the measurements.
    :ivar incl: Hole inclination, measured from vertical.
    :ivar azi: Hole azimuth, corrected to a well's azimuth reference.
    :ivar vert_sect: Distance along the vertical section of an azimuth
        plane.
    :ivar dls: Dogleg severity.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar location:
    :ivar uid: Unique identifier for this instance of
        DrillReportSurveyStation.
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    md: Optional[str] = field(
        default=None,
        metadata={
            "name": "Md",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    incl: Optional[str] = field(
        default=None,
        metadata={
            "name": "Incl",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    azi: Optional[str] = field(
        default=None,
        metadata={
            "name": "Azi",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vert_sect: Optional[str] = field(
        default=None,
        metadata={
            "name": "VertSect",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dls: Optional[str] = field(
        default=None,
        metadata={
            "name": "Dls",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    location: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportWellboreInfo:
    """
    General information about a wellbore for a drill report period.

    :ivar dtim_spud: Date and time at which the well was spudded. This
        is when the well drilling equipment began to bore into the
        earth's surface for the purpose of drilling a well.
    :ivar dtim_pre_spud: Date and time at which the well was predrilled.
        This is when the well drilling equipment begin to bore into the
        earth's surface for the purpose of drilling a well.
    :ivar date_drill_complete: The date when the drilling activity was
        completed.
    :ivar operator: Pointer to a BusinessAssociate representing the
        drilling Operator company responsible for the well being drilled
        (the company for whom the well is being drilled).
    :ivar drill_contractor: Pointer to a BusinessAssociate representing
        the lling contractor company.
    :ivar rig: Optional pointers to RigUtilization objects representing
        the rigs(s) used to drill the wellbore.
    """

    dtim_spud: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimSpud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_pre_spud: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimPreSpud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    date_drill_complete: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "DateDrillComplete",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    operator: Optional[str] = field(
        default=None,
        metadata={
            "name": "Operator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    drill_contractor: Optional[str] = field(
        default=None,
        metadata={
            "name": "DrillContractor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rig: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Rig",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class DxcStatistics:
    """
    Information on corrected drilling exponents.

    :ivar average: Corrected drilling exponent calculated for the
        interval.
    :ivar channel: Log channel from which the drilling coefficient
        statistics were calculated.
    """

    average: Optional[str] = field(
        default=None,
        metadata={
            "name": "Average",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class EcdStatistics:
    """
    Information on equivalent circulating density statistics.

    :ivar average: Average equivalent circulating density at TD through
        the interval.
    :ivar channel: Log channel from which the equivalent circulating
        density at TD statistics were calculated.
    """

    average: Optional[str] = field(
        default=None,
        metadata={
            "name": "Average",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class EquipmentType(Enum):
    """
    Specifies the values for type of equipment.
    """

    BRIDGE_PLUG = "bridge plug"
    BULL_PLUG = "bull plug"
    CAPILLARY_TUBING = "capillary tubing"
    CASING_CROSSOVER = "casing crossover"
    CASING_HANGER = "casing hanger"
    CASING_HEAD = "casing head"
    CASING_LINER_EXPANDABLE = "casing liner-expandable"
    CASING_SHOE = "casing shoe"
    CASING_SPOOL = "casing spool"
    CASING_CASING_LINER = "casing/casing liner"
    CEMENT_BEHIND_CASING = "cement (behind casing)"
    CEMENT_BASKET = "cement basket"
    CEMENT_RETAINER = "cement retainer"
    CEMENT_SQUEEZE = "cement squeeze"
    CEMENT_STAGE_TOOL = "cement stage tool"
    CHEMICAL_INJECTION_MANDREL = "chemical injection mandrel"
    CHEMICAL_INJECTION_VALVE = "chemical injection valve"
    CORROSION_COUPON_CARRIER = "corrosion coupon carrier"
    DIP_TUBE = "dip tube"
    DOWNHOLE_CHOKE = "downhole choke"
    DOWNHOLE_SENSOR = "downhole sensor"
    ESP_ASSEMBLY = "ESP assembly"
    ESP_BOLT_ON_DISCHARGE = "ESP bolt on discharge"
    ESP_BOLT_ON_INTAKE = "ESP bolt on intake"
    ESP_BOLT_ON_MOTOR_BASE = "ESP bolt on motor base"
    ESP_BOLT_ON_MOTOR_HEAD = "ESP bolt on motor head"
    ESP_CABLE = "ESP cable"
    ESP_GAS_HANDLER = "ESP gas handler"
    ESP_GAS_SEPARATOR = "ESP gas separator"
    ESP_LOWER_PIGTAIL = "ESP lower pigtail"
    ESP_MOTOR = "ESP motor"
    ESP_MOTOR_BASE_CENTRALIZER = "ESP motor base centralizer"
    ESP_MOTOR_FLAT_CABLE = "ESP motor flat cable"
    ESP_MOTOR_SHROUD = "ESP motor shroud"
    ESP_PROMOTOR = "ESP promotor"
    ESP_PUMP = "ESP pump"
    ESP_PUMP_DISCHARGE_SENSOR_SUB = "ESP pump discharge sensor sub"
    ESP_SEAL = "ESP seal"
    EXPANSION_JOINT = "expansion joint"
    EXTERNAL_CEMENTING_PORT = "external cementing port"
    FILL = "fill"
    FISH = "fish"
    FLOAT_COLLAR = "float collar"
    FLOAT_SHOE_GUIDE_SHOE = "float shoe/guide shoe"
    GAS_ANCHOR = "gas anchor"
    GAS_LIFT_MANDREL = "gas lift mandrel"
    GAS_LIFT_VALVE = "gas lift valve"
    GRAVEL_PACK_SCREEN = "gravel pack screen"
    HYDRAULIC_PUMP = "hydraulic pump"
    INJECTION_MANDREL = "injection mandrel"
    INJECTION_VALVE = "injection valve"
    JUNK_IN_WELLBORE = "junk in wellbore"
    LANDING_COLLAR = "landing collar"
    LINER_ENTRY_GUIDE = "liner entry guide"
    LINER_HANGER = "liner hanger"
    MULE_SHOE = "mule shoe"
    NOTCHED_COLLAR = "notched collar"
    ON_OFF_TOOL = "on-off tool"
    OVERSHOT = "overshot"
    PACKER = "packer"
    PACKER_PLUG = "packer plug"
    PACKER_MULTIPLE_STRINGS = "packer-multiple strings"
    PACKOFF_TUBING = "packoff (tubing)"
    PCP_FLEX_SHAFT_INTAKE = "pcp-flex shaft intake"
    PCP_GEAR_REDUCER_SUBSURFACE = "pcp-gear reducer (subsurface)"
    PCP_NO_TURN_TOOL_TORQUE_ANCHOR = "pcp-no turn tool/torque anchor"
    PCP_ROTOR = "pcp-rotor"
    PCP_STATOR = "pcp-stator"
    PCP_TAG_BAR = "pcp-tag bar"
    PLUG_CEMENT = "plug - cement"
    PLUG_MUD = "plug - mud"
    PLUNGER_LIFT_BALL = "plunger lift ball"
    PLUNGER_LIFT_BOTTOM_HOLE_BUMPER_ASSEMBLY = (
        "plunger lift bottom hole bumper assembly"
    )
    PLUNGER_LIFT_BUMPER_SPRING = "plunger lift bumper spring"
    PLUNGER_LIFT_COLLAR_STOP = "plunger lift collar stop"
    PLUNGER_LIFT_PLUNGER = "plunger lift plunger"
    POLISHED_ROD = "polished rod"
    POLISHED_ROD_LINER = "polished rod liner"
    PORTED_COLLAR = "ported collar"
    PROFILE_NIPPLE = "profile nipple"
    PROFILE_NIPPLE_PLUG = "profile nipple plug"
    PUMP_OUT_PLUG = "pump-out plug"
    SAND_SCREEN_TUBING = "sand screen-tubing"
    SAND_SEPARATOR = "sand separator"
    SCREEN_LINER_INSERT = "screen liner/insert"
    SEAL_ASSEMBLY = "seal assembly"
    SEAL_BORE_EXTENSION = "seal bore extension"
    SEAT_NIPPLE_SHOE = "seat nipple/shoe"
    SHEAR_TOOL = "shear tool"
    SLIDING_SLEEVE = "sliding sleeve"
    STEAM_CUP_MANDREL = "steam cup mandrel"
    STEAM_DEFLECTORS = "steam deflectors"
    STRAINER_NIPPLE = "strainer nipple"
    SUBSURFACE_SAFETY_VALVE = "subsurface safety valve"
    SUCKER_ROD = "sucker rod"
    SUCKER_ROD_BACKOFF_COUPLING = "sucker rod backoff coupling"
    SUCKER_ROD_PUMP_INSERT = "sucker rod pump-insert"
    SUCKER_ROD_PUMP_JACKET = "sucker rod pump-jacket"
    SUCKER_ROD_PUMP_TUBING_PUMP_BARREL = "sucker rod pump-tubing pump barrel"
    SUCKER_ROD_PUMP_TUBING_PUMP_PLUNGER = "sucker rod pump-tubing pump plunger"
    SUCKER_ROD_SUB = "sucker rod sub"
    SUCKER_ROD_CONTINUOUS = "sucker rod-continuous"
    SUCKER_ROD_RIBBON = "sucker rod-ribbon"
    SUCKER_ROD_SINKER_BAR = "sucker rod-sinker bar"
    TCP_GUN = "tcp gun"
    TUBING = "tubing"
    TUBING_COILED = "tubing (coiled)"
    TUBING_ANCHOR_CATCHER = "tubing anchor/catcher"
    TUBING_CROSSOVER = "tubing crossover"
    TUBING_DRAIN = "tubing drain"
    TUBING_HANGER = "tubing hanger"
    TUBING_HEAD_SPOOL = "tubing head (spool)"
    TUBING_PURGE_CHECK_VALVE = "tubing purge check valve"
    TUBING_SUB = "tubing sub"
    WELLBORE_NOTES = "wellbore notes"
    WHIPSTOCK = "whipstock"
    WIRELINE_RE_ENTRY_GUIDE_BELL_COLLAR = (
        "wireline re-entry guide (bell collar)"
    )
    Y_TOOL = "y-tool"


@dataclass
class ErrorTerm:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class ErrorTermDictionary:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class ErrorTermValue:
    """
    :ivar magnitude: Business Rule : The unconstrained uom of the
        magnitude is actually constrained by the MeasureClass set to the
        associated ErrorTerm.
    :ivar mean_value: Business Rules : - The unconstrained uom of the
        mean value is actually constrained by the MeasureClass set to
        the associated ErrorTerm. - If propagation mode is set to 'B'
        then MeanValue must exist
    :ivar error_term:
    """

    magnitude: Optional[str] = field(
        default=None,
        metadata={
            "name": "Magnitude",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    mean_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeanValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    error_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "ErrorTerm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


class EventTypeType(Enum):
    """Qualifies the type of event: daily report, job, npt, etc."""

    DAILY_COST = "daily cost"
    DAILY_REPORT = "daily report"
    FAILURE_DOWNHOLE_EQUIPMENT_ONLY = "failure (downhole equipment only)"
    JOB = "job"
    JOB_PLAN_PHASES = "job plan (phases)"
    MUD_ATTRIBUTES = "mud attributes"
    NPT_LOST_TIME_EVENT = "npt (lost time event)"
    TIME_LOG_TIME_MEASURE = "time log (time measure)"


@dataclass
class EventRefInfo:
    """
    Event reference information.

    :ivar event: The referencing eventledger event.
    :ivar event_date: Install/pull date.
    """

    event: Optional[str] = field(
        default=None,
        metadata={
            "name": "Event",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    event_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "EventDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class ExtPropNameValue:
    """
    Name-value extensions for the equipment property.

    :ivar name: A string representing the name of property.
    :ivar value: A value string representing the units of measure of the
        value.
    :ivar uid: Unique identifier for this instance of ExtPropNameValue.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class FluidsReport:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class ForceParameterKind(Enum):
    """
    Specifies the values for mud log parameters that are measured in units of
    force.

    :cvar OVERPULL_ON_CONNECTION: Additional hookload recorded in excess
        of static drill string weight when making a connection.
    :cvar OVERPULL_ON_TRIP: Additional hookload recorded in excess of
        static drill string weight when making a trip.
    """

    OVERPULL_ON_CONNECTION = "overpull on connection"
    OVERPULL_ON_TRIP = "overpull on trip"


@dataclass
class GasInMud:
    """
    Information on amount of gas in the mud.

    :ivar average: Average percentage of gas in the mud.
    :ivar maximum: Maximum percentage of gas in the mud.
    :ivar channel:
    """

    average: Optional[str] = field(
        default=None,
        metadata={
            "name": "Average",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    maximum: Optional[str] = field(
        default=None,
        metadata={
            "name": "Maximum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


class GasPeakType(Enum):
    """
    Type of gas reading.
    """

    CIRCULATING_BACKGROUND_GAS = "circulating background gas"
    CONNECTION_GAS = "connection gas"
    DRILLING_BACKGROUND_GAS = "drilling background gas"
    DRILLING_GAS_PEAK = "drilling gas peak"
    FLOW_CHECK_GAS = "flow check gas"
    NO_READINGS = "no readings"
    OTHER = "other"
    SHUT_DOWN_GAS = "shut down gas"
    TRIP_GAS = "trip gas"


@dataclass
class GeochronologicalUnit:
    """A unit of geological time that can be used as part of an interpretation of a
    geology sequence.

    Use it for major units of geological time such as "Paleozoic",
    "Mesozoic" or for more detailed time intervals such as "Permian",
    "Triassic", "Jurassic", etc.

    :ivar authority: Person or collective body responsible for
        authorizing the information.
    :ivar kind: Defines the time spans in geochronology.
    """

    authority: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    kind: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class GeologyType(Enum):
    """
    Specifies the values for type of geology.
    """

    AQUIFER = "aquifer"
    RESERVOIR = "reservoir"


class GradeType(Enum):
    """
    Specifies the values for the grade level of this piece of equipment.
    """

    VALUE_13_CR = "13CR"
    VALUE_13_CR_80 = "13CR- 80"
    VALUE_13_CR_85 = "13CR- 85"
    VALUE_13_CR_95 = "13CR- 95"
    VALUE_13_CR_110 = "13CR-110"
    VALUE_35 = "35"
    VALUE_45 = "45"
    VALUE_46 = "46"
    VALUE_50 = "50"
    VALUE_620_C = "620C"
    VALUE_75 = "75"
    VALUE_750_N = "750N"
    VALUE_75_A = "75A"
    VALUE_780_M = "780M"
    VALUE_95 = "95"
    VALUE_960_M = "960M"
    VALUE_970_N = "970N"
    A53 = "A53"
    A53_A = "A53A"
    A53_B = "A53B"
    ARMCO_95 = "Armco-95"
    B = "B"
    C = "C"
    C_110 = "C-110"
    C_75 = "C-75"
    C_90 = "C-90"
    C_95 = "C-95"
    D = "D"
    DE = "DE"
    DER = "DER"
    DR = "DR"
    DWR = "DWR"
    E = "E"
    E_75 = "E-75"
    EL = "EL"
    F_25 = "F-25"
    FG = "FG"
    FS_80 = "FS-80"
    FSS_95 = "FSS-95"
    G = "G"
    G_105 = "G-105"
    GT_80_S = "GT-80S"
    H2_S_90 = "H2S-90"
    H2_S_95 = "H2S-95"
    H_40 = "H-40"
    HC_95 = "HC-95"
    HCK_55 = "HCK-55"
    HCL_80 = "HCL-80"
    HCN_80 = "HCN-80"
    HCP_110 = "HCP-110"
    HCQ_125 = "HCQ-125"
    HO_70 = "HO-70"
    HS = "HS"
    J_20 = "J-20"
    J_55 = "J-55"
    K = "K"
    K_40 = "K-40"
    K_55 = "K-55"
    KD = "KD"
    KD_63 = "KD-63"
    L_80 = "L-80"
    LS_140 = "LS-140"
    LS_50 = "LS-50"
    LS_65 = "LS-65"
    M_65 = "M-65"
    M_90 = "M-90"
    M_95 = "M-95"
    MAV_50 = "MAV-50"
    MD_56 = "MD-56"
    MMS = "MMS"
    N_105 = "N-105"
    N_23 = "N-23"
    N_30 = "N-30"
    N_40 = "N-40"
    N_54 = "N-54"
    N_75 = "N-75"
    N_78 = "N-78"
    N_80 = "N-80"
    N_90 = "N-90"
    N_96 = "N-96"
    N_97 = "N-97"
    P_105 = "P-105"
    P_110 = "P-110"
    PCP_900 = "PCP  900"
    PCP_1000 = "PCP 1000"
    PCP_1500 = "PCP 1500"
    PCP_2500 = "PCP 2500"
    PH_6 = "PH-6"
    PLUS = "Plus"
    Q_125 = "Q-125"
    QT_1000 = "QT-1000"
    QT_1200 = "QT-1200"
    QT_700 = "QT-700"
    QT_800 = "QT-800"
    QT_900 = "QT-900"
    S = "S"
    S_135 = "S-135"
    S_59 = "S-59"
    S_60 = "S-60"
    S_67 = "S-67"
    S_80 = "S-80"
    S_87 = "S-87"
    S_88 = "S-88"
    S_95 = "S-95"
    SC_90 = "SC-90"
    SE = "SE"
    SER = "SER"
    SM = "SM"
    SOO_95 = "SOO-95"
    STAINLESS = "Stainless"
    SWR = "SWR"
    T = "T"
    T_66 = "T-66"
    T_95 = "T-95"
    T_D61 = "T-D61"
    T_D63 = "T-D63"
    T_K65 = "T-K65"
    UHS = "UHS"
    USS_125 = "USS-125"
    USS_140 = "USS-140"
    USS_50 = "USS-50"
    USS_95 = "USS-95"
    V_150 = "V-150"
    WC_50 = "WC-50"
    X = "X"
    X_140 = "X-140"
    X_42 = "X-42"
    X_46 = "X-46"
    X_52 = "X-52"
    X_56 = "X-56"
    X_60 = "X-60"
    X_70 = "X-70"
    X_95 = "X-95"
    XD = "XD"


class GyroAxisCombination(Enum):
    Z = "z"
    XY = "xy"
    XYZ = "xyz"


class HoleOpenerType(Enum):
    """
    Specifies the types of hole openers.
    """

    UNDER_REAMER = "under-reamer"
    FIXED_BLADE = "fixed blade"


@dataclass
class Iso135032CrushTestData:
    """
    Crush test data point.

    :ivar fines: Mass percentage of fines after being exposed to stress.
    :ivar stress: Stress measured at a point during a crush test.
    :ivar uid: Unique identifier for this instance of
        ISO13503_2CrushTestData.
    """

    class Meta:
        name = "ISO13503_2CrushTestData"

    fines: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fines",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    stress: Optional[str] = field(
        default=None,
        metadata={
            "name": "Stress",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Iso135032SieveAnalysisData:
    """Proppant properties on percent retained and sieve number.

    Data from this ISO anaylsis.

    :ivar percent_retained: The percentage of mass retained in the
        sieve.
    :ivar sieve_number: ASTM US Standard mesh opening size used in the
        sieve analysis test.  To indicate "Pan",  use "0".
    :ivar uid: Unique identifier for this instance of
        ISO13503_2SieveAnalysisData.
    """

    class Meta:
        name = "ISO13503_2SieveAnalysisData"

    percent_retained: Optional[str] = field(
        default=None,
        metadata={
            "name": "PercentRetained",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    sieve_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SieveNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class IadcBearingWearCode(Enum):
    """
    Specifies the condition codes for the bearing wear.
    """

    VALUE_0 = "0"
    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"
    VALUE_4 = "4"
    VALUE_5 = "5"
    VALUE_6 = "6"
    VALUE_7 = "7"
    VALUE_8 = "8"
    E = "E"
    F = "F"
    N = "N"
    X = "X"


class IadcIntegerCode(Enum):
    """
    Specifies the IADC integer codes for the inner or outer tooth rows.
    """

    VALUE_0 = "0"
    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"
    VALUE_4 = "4"
    VALUE_5 = "5"
    VALUE_6 = "6"
    VALUE_7 = "7"
    VALUE_8 = "8"


@dataclass
class Incident:
    """Operations HSE Schema.

    Captures data for a specific incident.

    :ivar dtim: Date and time the information is related to.
    :ivar reporter: Name of the person who prepared the incident report.
    :ivar num_minor_injury: Number of personnel with minor injuries.
    :ivar num_major_injury: Number of personnel with major injuries.
    :ivar num_fatality: Number of personnel killed due to the incident.
    :ivar is_near_miss: Near miss incident occurrence? Values are "true"
        (or "1") and "false" (or "0").
    :ivar desc_location: Location description.
    :ivar desc_accident: Accident description.
    :ivar remedial_action_desc: Remedial action description.
    :ivar cause_desc: Cause description.
    :ivar etim_lost_gross: Number of hours lost due to the incident.
    :ivar cost_loss_gross: Gross estimate of the cost incurred due to
        the incident.
    :ivar responsible_company: Pointer to a BusinessAssociate
        representing the company that caused the incident.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Incident
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    reporter: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reporter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_minor_injury: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumMinorInjury",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_major_injury: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumMajorInjury",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_fatality: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumFatality",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_near_miss: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsNearMiss",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    desc_location: Optional[str] = field(
        default=None,
        metadata={
            "name": "DescLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    desc_accident: Optional[str] = field(
        default=None,
        metadata={
            "name": "DescAccident",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    remedial_action_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "RemedialActionDesc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cause_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "CauseDesc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_lost_gross: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimLostGross",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cost_loss_gross: Optional[str] = field(
        default=None,
        metadata={
            "name": "CostLossGross",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    responsible_company: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResponsibleCompany",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class InnerBarrelType(Enum):
    """
    Core inner barrel type.

    :cvar UNDIFFERENTIATED: A pipe that is located inside a core barrel
        to hold the core sample.
    :cvar ALUMINUM: An inner core barrel made of aluminium.
    :cvar GEL: An inner core barrel that that seals off the core sample
        using gel as the sealing material.
    :cvar FIBERGLASS: An inner core barrel made of glass fiber
        reinforced plastic.
    """

    UNDIFFERENTIATED = "undifferentiated"
    ALUMINUM = "aluminum"
    GEL = "gel"
    FIBERGLASS = "fiberglass"


@dataclass
class InterpretedGeology:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class InterpretedGeologyInterval:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class ItemState(Enum):
    """
    These values represent the state of a WITSML object.

    :cvar ACTUAL: Actual data measured or entered at the well site.
    :cvar MODEL: Model data used for "what if" calculations.
    :cvar PLAN: A planned object. That is, one which is expected to be
        executed in the future.
    """

    ACTUAL = "actual"
    MODEL = "model"
    PLAN = "plan"


class JarAction(Enum):
    """
    Specifies the type of jar action.
    """

    UP = "up"
    DOWN = "down"
    BOTH = "both"
    VIBRATING = "vibrating"


class JarType(Enum):
    """
    Specifies the type of jar.
    """

    MECHANICAL = "mechanical"
    HYDRAULIC = "hydraulic"
    HYDRO_MECHANICAL = "hydro mechanical"


@dataclass
class LicensePeriod:
    """
    This class is used to represent a period of time when a particular license was
    valid.

    :ivar num_license: License number.
    :ivar termination_date_time: The date and time when the license
        ceased to be effective.
    :ivar effective_date_time: The date and time when the license became
        effective.
    """

    num_license: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumLicense",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    termination_date_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "TerminationDateTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    effective_date_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "EffectiveDateTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class LineStyle(Enum):
    """
    Specifies the style of line used to define the DepthRegTrackCurve.
    """

    DASHED = "dashed"
    SOLID = "solid"
    DOTTED = "dotted"
    SHORT_DASHED = "short dashed"
    LONG_DASHED = "long dashed"


@dataclass
class LithologyQualifier:
    """
    A description of minerals or accessories that constitute a fractional part of a
    CuttingsIntervalLithology.

    :ivar kind: The type of qualifier.
    :ivar md_interval: The measured depth interval represented by the
        qualifier. This must be within the range of the parent geologic
        interval. If MdInterval is not given then the qualifier is
        deemed to exist over the entire depth range of the parent
        geologyInterval.
    :ivar abundance: The relative abundance of the qualifier estimated
        based on a "visual area" by inspecting the cuttings spread out
        on the shaker table before washing, or in the sample tray after
        washing. This represents the upper bound of the observed range,
        and is in the following increments at the upper bound: 1 = less
        than or equal to 1% 2 = greater than 1% and less than 2% 5 =
        greater than or equal to 2% and less than 5% and then in 5%
        increments, 10 (=5-10%), 15 (=10-15%) up to 100 (=95-100%). The
        end user can then elect to either display the %, or map them to
        an operator-specific term or coding, e.g., 1 less than or equal
        to 1% = rare trace, or occasional, or very sparse, etc.,
        depending on the end users' terminology. i.e. 1 less then or
        equal to 1%=Rare Trace, or occasional, or very sparse etc.,
        depending on the the end users' terminology.)
    :ivar description: A textual description of the qualifier.
    :ivar uid: Unique identifier for this instance of LithologyQualifier
    """

    kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    abundance: Optional[str] = field(
        default=None,
        metadata={
            "name": "Abundance",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LithostratigraphicUnit:
    """The name of a lithostratigraphy, with the "kind" attribute specifying the
    lithostratigraphic unit-hierarchy (group, formation, member or bed).

    The entry at each level is free text for the local lithostratigraphy
    at that level in the hierarchy. If a single hierarchy is defined, it
    is assumed this is at the formation level in the hierarchy and
    kind=formation should be used for the entry. Used to hold
    information about the stratigraphic units that an interpreted
    lithology may belong to. These are based primarily on the
    differences between rock types rather than their specific age. For
    example, in the Grand Canyon, some of the major lithostratigraphic
    units are the "Navajo", "Kayenta", "Wingate", "Chinle" and
    "Moenkopi" formations, each of which is represented by a particular
    set of rock properties or characteristics.

    :ivar authority: Person or collective body responsible for
        authorizing the information.
    :ivar kind: Specifies the lithostratigraphic unit-hierarchy (group,
        formation, member or bed).
    """

    authority: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    kind: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Log:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class LogChannelAxis:
    """Metadata by which the array structure of a compound value is defined.

    It defines one axis of an array type used in a log channel.

    :ivar axis_start: Value of the initial entry in the list of axis
        index values.
    :ivar axis_spacing: The increment to be used to fill out the list of
        the log channel axis index values.
    :ivar axis_count: The count of elements along this axis of the
        array.
    :ivar axis_name: The name of the array axis.
    :ivar axis_property_kind: The property type by which the array axis
        is classified. Like "measured depth" or "elapsed time".
    :ivar axis_uom: A string representing the units of measure of the
        axis values.
    :ivar uid: A unique identifier for an instance of a log channel axis
    """

    axis_start: Optional[float] = field(
        default=None,
        metadata={
            "name": "AxisStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    axis_spacing: Optional[float] = field(
        default=None,
        metadata={
            "name": "AxisSpacing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    axis_count: Optional[str] = field(
        default=None,
        metadata={
            "name": "AxisCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    axis_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "AxisName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    axis_property_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "AxisPropertyKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    axis_uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "AxisUom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LogOsduintegration:
    """
    Information about a Log that is relevant for OSDU integration but does not have
    a natural place in a Log object.

    :ivar log_version: The log version. Distinct from objectVersion.
    :ivar zero_time: Optional time reference for time-based primary
        indexes. The ISO date time string representing zero time. Not to
        be confused with seismic travel time zero.
    :ivar frame_identifier: For multi-frame or multi-section files, this
        identifier defines the source frame in the file. If the
        identifier is an index number the index starts with zero and is
        converted to a string for this property.
    :ivar is_regular: Boolean property indicating the sampling mode of
        the primary index. True means all channel data values are
        regularly spaced (see NominalSamplingInterval); false means
        irregular or discrete sample spacing.
    :ivar intermediary_service_company: Pointer to a BusinessAssociate
        that represents the company who engaged the service company
        (ServiceCompany) to perform the logging.
    """

    class Meta:
        name = "LogOSDUIntegration"

    log_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "LogVersion",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    zero_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "ZeroTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    frame_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "FrameIdentifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_regular: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsRegular",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    intermediary_service_company: Optional[str] = field(
        default=None,
        metadata={
            "name": "IntermediaryServiceCompany",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class LogRectangleType(Enum):
    """
    Specifies the type of content from the original log defined by the rectangle.

    :cvar HEADER: Denotes rectangle bounds a header section
    :cvar ALTERNATE:
    """

    HEADER = "header"
    ALTERNATE = "alternate"


class LogSectionType(Enum):
    """
    Specifies the type of log section.

    :cvar MAIN:
    :cvar REPEAT: An interval of log that has been recorded for a second
        time.
    :cvar CALIBRATION:
    :cvar TIE_IN:
    :cvar GOING_IN_HOLE:
    :cvar OTHER: The value is not known. Avoid using this value. All
        reasonable attempts should be made to determine the appropriate
        value. Use of this value may result in rejection in some
        situations.
    """

    MAIN = "main"
    REPEAT = "repeat"
    CALIBRATION = "calibration"
    TIE_IN = "tie in"
    GOING_IN_HOLE = "going in hole"
    OTHER = "other"


class LogTrackType(Enum):
    """
    Specifies the kinds of track.

    :cvar CURVES:
    :cvar DATA:
    :cvar DEPTH: The index used by the track is depth
    :cvar TRACES:
    :cvar OTHER: The index used by the track is something other than
        depth.
    """

    CURVES = "curves"
    DATA = "data"
    DEPTH = "depth"
    TRACES = "traces"
    OTHER = "other"


@dataclass
class LoggingToolKind:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class LoggingToolKindDictionary:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class MaterialType(Enum):
    """
    Specifies the primary type of material that a component is made of.
    """

    ALUMINUM = "aluminum"
    BERYLLIUM_COPPER = "beryllium copper"
    CHROME_ALLOY = "chrome alloy"
    COMPOSITE = "composite"
    OTHER = "other"
    NON_MAGNETIC_STEEL = "non-magnetic steel"
    PLASTIC = "plastic"
    STEEL = "steel"
    STEEL_ALLOY = "steel alloy"
    TITANIUM = "titanium"


class MeasurementType(Enum):
    """Specifies the type of sensor in a tubular string.

    The source (except for "CH density porosity", "CH neutron porosity",
    "OH density porosity" and "OH neutron porosity") of the values and
    the descriptions is the POSC V2.2 "well log trace class" standard
    instance values, which are documented as "A classification of well
    log traces based on specification of a range of characteristics.
    Traces may be classed according to the type of physical
    characteristic they are meant to measure."

    :cvar ACCELERATION: Output from an accelerometer on a logging tool.
    :cvar ACOUSTIC_CALIPER: A well log that uses an acoustic device to
        measure hole diameter.
    :cvar ACOUSTIC_CASING_COLLAR_LOCATOR: The signal measured by an
        acoustic device at the location of casing collars and other
        features (e.g., perforations).
    :cvar ACOUSTIC_IMPEDANCE: Seismic velocity multiplied by density.
    :cvar ACOUSTIC_POROSITY: Porosity calculated from an acoustic log.
    :cvar ACOUSTIC_VELOCITY: The velocity of an acoustic wave.
    :cvar ACOUSTIC_WAVE_MATRIX_TRAVEL_TIME: The time it takes for an
        acoustic wave to traverse a fixed distance of a given material
        or matrix. In this case the material or matrix is a specific,
        zero-porosity rock, e.g., sandstone, limestone or dolomite.
    :cvar ACOUSTIC_WAVE_TRAVEL_TIME: The time it takes for an acoustic
        wave to traverse a fixed distance.
    :cvar AMPLITUDE: Any measurement of the maximum departure of a wave
        from an average value.
    :cvar AMPLITUDE_OF_ACOUSTIC_WAVE: The extent of departure of an
        acoustic wave measured from the mean position.
    :cvar AMPLITUDE_OF_E_M_WAVE: The extent of departure of an
        electromagnetic wave measured from the mean position.
    :cvar AMPLITUDE_RATIO: The ratio of two amplitudes.
    :cvar AREA: A particular extent of space or surface.
    :cvar ATTENUATION: The amount of reduction in the amplitude of a
        wave.
    :cvar ATTENUATION_OF_ACOUSTIC_WAVE: The amount of reduction in the
        amplitude of an acoustic wave.
    :cvar ATTENUATION_OF_E_M_WAVE: The amount of reduction in the
        amplitude of an electromagnetic wave.
    :cvar AUXILIARY: A general classification for measurements, which
        are very specialized and not normally accessed by
        petrophysicists.
    :cvar AVERAGE_POROSITY: The pore volume of a rock averaged using
        various well log or core porosity measurements.
    :cvar AZIMUTH: In the horizontal plane, it is the clockwise angle of
        departure from magnetic north (while looking down hole).
    :cvar BARITE_MUD_CORRECTION: A trace that has been corrected for the
        effects of barite in the borehole fluid.
    :cvar BED_THICKNESS_CORRECTION: A trace that has been corrected for
        bed thickness effects.
    :cvar BIT_SIZE: The diameter of the drill bit used to drill the
        hole.
    :cvar BLOCKED: A well log trace that has been edited to reflect
        sharp bed boundaries.  The trace has a square wave appearance.
    :cvar BOREHOLE_ENVIRONMENT_CORRECTION: A trace that has been
        corrected for the effects of the borehole environment, e.g.,
        borehole size.
    :cvar BOREHOLE_FLUID_CORRECTION: A trace that has been corrected for
        the effects of borehole fluid; e.g., a mud cake correction.
    :cvar BOREHOLE_SIZE_CORRECTION: A trace that has been corrected for
        the effects of borehole size.
    :cvar BROMIDE_MUD_CORRECTION: A trace that has been corrected for
        the effects of bromide in the borehole fluid.
    :cvar BULK_COMPRESSIBILITY: The relative compressibility of a
        material.
    :cvar BULK_DENSITY: The measured density of a rock with the pore
        volume filled with fluid.  The pore fluid is generally assumed
        to be water.
    :cvar BULK_VOLUME: A quantity-per-unit volume.
    :cvar BULK_VOLUME_GAS: The quantity of gas present in a unit volume
        of rock.  The product of gas saturation and total porosity.
    :cvar BULK_VOLUME_HYDROCARBON: The quantity of hydrocarbon present
        in a unit volume of rock.  The product of hydrocarbon saturation
        and total porosity.
    :cvar BULK_VOLUME_OIL: The quantity of oil present in a unit volume
        of rock.  The product of oil saturation and total porosity.
    :cvar BULK_VOLUME_WATER: The quantity of formation water present in
        a unit volume of rock.  The product of water saturation and
        total porosity.
    :cvar C_O_RATIO: The ratio of the carbon measurement to the oxygen
        measurement.
    :cvar CALIPER: A well log used to record hole diameter (open or
        cased).
    :cvar CASED_HOLE_CORRECTION: A trace that has been corrected for the
        effects of being recorded in a cased hole, e.g., corrected for
        casing weight and thickness.
    :cvar CASING_COLLAR_LOCATOR: The signal measured by a device at the
        location of casing collars and other features (e.g.,
        perforations).
    :cvar CASING_CORRECTION: A trace that has been corrected for the
        effects of casing; this includes things such as casing weight,
        thickness and diameter.
    :cvar CASING_DIAMETER_CORRECTION: A trace that has been corrected
        for the effects of casing diameter.
    :cvar CASING_INSPECTION: Any of the measurements made for the
        purpose of determining the properties of the well casing.
    :cvar CASING_THICKNESS_CORRECTION: A trace that has been corrected
        for the effects of casing thickness.
    :cvar CASING_WEIGHT_CORRECTION: A trace that has been corrected for
        the effects of casing weight.
    :cvar CEMENT_CORRECTION: A trace that has been corrected for the
        effects of the cement surrounding the casing; this includes
        cement thickness, density and type.
    :cvar CEMENT_DENSITY_CORRECTION: A trace that has been corrected for
        the effects of cement density.
    :cvar CEMENT_EVALUATION: Any of the measurements made to determine
        the presence and quality of the cement bond to casing or to
        formation.
    :cvar CEMENT_THICKNESS_CORRECTION: A trace that  has been corrected
        for the effects of cement thickness.
    :cvar CEMENT_TYPE_CORRECTION: A trace that has been corrected for
        the effects of the type of cement used.
    :cvar CH_DENSITY_POROSITY:
    :cvar CH_DOLOMITE_DENSITY_POROSITY: Porosity calculated from the
        bulk density measurement of a cased hole density log using a
        dolomite matrix density.
    :cvar CH_DOLOMITE_NEUTRON_POROSITY: Porosity calculated from a cased
        hole neutron log using a dolomite matrix.
    :cvar CH_LIMESTONE_DENSITY_POROSITY: Porosity calculated from the
        bulk density measurement of a cased hole density log using a
        limestone matrix density.
    :cvar CH_LIMESTONE_NEUTRON_POROSITY: Porosity calculated from a
        cased-hole neutron log using a limestone matrix.
    :cvar CH_NEUTRON_POROSITY:
    :cvar CH_SANDSTONE_DENSITY_POROSITY: Porosity calculated from the
        bulk density measurement of a cased-hole density log using a
        sandstone matrix density.
    :cvar CH_SANDSTONE_NEUTRON_POROSITY: Porosity calculated from an
        openhole neutron log using a sandstone matrix.
    :cvar COMPRESSIONAL_WAVE_DOLOMITE_POROSITY: Porosity calculated from
        a compressional wave acoustic log using a dolomite matrix.
    :cvar COMPRESSIONAL_WAVE_LIMESTONE_POROSITY: Porosity calculated
        from a compressional wave acoustic log using a limestone matrix
    :cvar COMPRESSIONAL_WAVE_MATRIX_TRAVEL_TIME: The time it takes for a
        compressional acoustic wave to traverse a fixed distance of a
        given material or matrix. In this case the material or matrix is
        a specific, zero porosity rock, e.g. sandstone, limestone or
        dolomite.
    :cvar COMPRESSIONAL_WAVE_SANDSTONE_POROSITY: Porosity calculated
        from a compressional wave acoustic log using a sandstone matrix.
    :cvar COMPRESSIONAL_WAVE_TRAVEL_TIME: The time it takes for a
        compressional acoustic wave to traverse a fixed distance.
    :cvar CONDUCTIVITY: The property of a medium (solid or fluid) that
        allows the medium to conduct a form of energy; e.g., electrical
        conductivity or thermal conductivity.
    :cvar CONDUCTIVITY_FROM_ATTENUATION: Conductivity calculated from
        the attenuation of an electromagnetic wave. Generally recorded
        from a LWD resistivity tool.
    :cvar CONDUCTIVITY_FROM_PHASE_SHIFT: Conductivity calculated from
        the phase shift of an electromagnetic wave. Generally recorded
        from a LWD resistivity tool.
    :cvar CONNATE_WATER_CONDUCTIVITY: The conductivity of the water
        entrapped in the interstices of the rock.
    :cvar CONNATE_WATER_RESISTIVITY: The resistivity of the water
        entrapped in the interstices of the rock.
    :cvar CONVENTIONAL_CORE_POROSITY: Porosity from a measurement made
        on a conventional core.
    :cvar CORE_MATRIX_DENSITY: The density of a rock matrix measured on
        a core sample.
    :cvar CORE_PERMEABILITY: The permeability derived from a core.
    :cvar CORE_POROSITY: Porosity from a core measurement.
    :cvar CORRECTED: A trace that has had corrections applied; e.g.
        environmental corrections.
    :cvar COUNT_RATE: The rate of occurrences; e.g. the far counts from
        a density tool..
    :cvar COUNT_RATE_RATIO: The ratio of two count rates.
    :cvar CROSS_PLOT_POROSITY: The pore volume of a rock calculated from
        cross plotting two or more well log porosity measurements.
    :cvar DECAY_TIME: The time it takes for a population to decay,
        generally expressed as a half life.
    :cvar DEEP_CONDUCTIVITY: The conductivity that represents a
        measurement made several feet into the formation; generally
        considered a measurement of the undisturbed formation.
    :cvar DEEP_INDUCTION_CONDUCTIVITY: The conductivity, measured by an
        induction log, which represents a measurement made several feet
        into the formation; generally considered a measurement of the
        undisturbed formation.
    :cvar DEEP_INDUCTION_RESISTIVITY: The resistivity, measured by an
        induction log, which represents a measurement made several feet
        into the formation; generally considered a measurement of the
        undisturbed formation.
    :cvar DEEP_LATEROLOG_CONDUCTIVITY: The conductivity, measured by a
        laterolog, which represents a measurement made several feet into
        the formation; generally considered a measurement of the
        undisturbed formation.
    :cvar DEEP_LATEROLOG_RESISTIVITY: The resistivity, measured by a
        laterolog, which represents a measurement made several feet into
        the formation; generally considered a measurement of the
        undisturbed formation.
    :cvar DEEP_RESISTIVITY: The resistivity, which represents a
        measurement made several feet into the formation; generally
        considered a measurement of the undisturbed formation.
    :cvar DENSITY: Mass per unit Volume; well logging units are usually
        gm/cc.
    :cvar DENSITY_POROSITY: Porosity calculated using the bulk density
        measurement from a density log.
    :cvar DEPTH: The distance to a point in a wellbore.
    :cvar DEPTH_ADJUSTED: The process of depth correcting a trace by
        depth matching it to a reference trace.
    :cvar DEPTH_DERIVED_FROM_VELOCITY: The depth calculated from
        velocity information.
    :cvar DEVIATION: Departure of a borehole from vertical.  Also, the
        angle measured between the tool axis and vertical.
    :cvar DIELECTRIC: Relative permittivity.
    :cvar DIFFUSION_CORRECTION: A trace that  has been corrected for the
        effects of diffusion.
    :cvar DIP: The angle that a structural surface, e.g. a bedding or
        fault plane, makes with the horizontal, measured perpendicular
        to the strike of the structure.
    :cvar DIPMETER: Any of a number of measurements produced by a tool
        designed to measure formation dip and borehole characteristics
        through direct and indirect measurements.
    :cvar DIPMETER_CONDUCTIVITY: The conductivity, measured by a
        dipmeter, which represents a measurement made approximately one
        to two feet into the formation; generally considered to measure
        the formation where it contains fluids that are comprised
        primarily of mud filtrate.
    :cvar DIPMETER_RESISTIVITY: The resistivity, measured by a dipmeter,
        which represents a measurement made approximately one to two
        feet into the formation; generally considered to measure the
        formation where it contains fluids that are comprised primarily
        of mud filtrate.
    :cvar DOLOMITE_ACOUSTIC_POROSITY: Porosity calculated from an
        acoustic log using a dolomite matrix.
    :cvar DOLOMITE_DENSITY_POROSITY: Porosity calculated from the bulk
        density measurement of a density log using a dolomite matrix
        density.
    :cvar DOLOMITE_NEUTRON_POROSITY: Porosity calculated from a neutron
        log using a dolomite matrix.
    :cvar EDITED: A well log trace which has been corrected or adjusted
        through an editing process.
    :cvar EFFECTIVE_POROSITY: The interconnected pore volume occupied by
        free fluids.
    :cvar ELECTRIC_CURRENT: The flow of electric charge.
    :cvar ELECTRIC_POTENTIAL: The difference in electrical energy
        between two systems.
    :cvar ELECTROMAGNETIC_WAVE_MATRIX_TRAVEL_TIME: The time it takes for
        an electromagnetic wave to traverse a fixed distance of a given
        material or matrix. In this case the material or matrix is a
        specific, zero porosity rock, e.g. sandstone, limestone or
        dolomite.
    :cvar ELECTROMAGNETIC_WAVE_TRAVEL_TIME: The time it takes for an
        electromagnetic wave to traverse a fixed distance.
    :cvar ELEMENT: The elemental composition, generally in weight
        percent, of a formation as calculated from information obtained
        from a geochemical logging pass; e.g., weight percent of Al, Si,
        Ca, Fe, etc.
    :cvar ELEMENTAL_RATIO: The ratio of two different elemental
        measurements; e.g. K/U.
    :cvar ENHANCED: A well log trace that has been filtered to improve
        its value; e.g. inverse filtering for better resolution.
    :cvar FILTERED: A well log trace which has had a filter applied to
        it.
    :cvar FLOWMETER: A logging tool to measure the rate and/or direction
        of fluid flow in a wellbore.
    :cvar FLUID_DENSITY: The quantity per unit volume of fluid.
    :cvar FLUID_VELOCITY: The velocity of a flowing fluid.
    :cvar FLUID_VISCOSITY: The amount of a fluid resistance to flow.
    :cvar FLUSHED_ZONE_CONDUCTIVITY: The conductivity of the zone
        immediately behind the mud cake and which is considered to be
        flushed by mud filtrate, i.e., it is considered to have all
        mobile formation fluids displaced from it.
    :cvar FLUSHED_ZONE_RESISTIVITY: The resistivity of the zone
        immediately behind the mud cake and which is considered to be
        flushed by mud filtrate, i.e., it is considered to have all
        mobile formation fluids displaced from it.
    :cvar FLUSHED_ZONE_SATURATION: The fraction or percentage of pore
        volume of rock occupied by drilling mud or mud filtrate in the
        flushed zone.
    :cvar FORCE: Energy exerted or brought to bear.
    :cvar FORMATION_DENSITY_CORRECTION: A trace that has been corrected
        for formation density effects.
    :cvar FORMATION_PROPERTIES_CORRECTION: A trace that has been
        corrected for formation properties; e.g., salinity.
    :cvar FORMATION_SALINITY_CORRECTION: A trace that has been corrected
        for the salinity effects from the water in the formation.
    :cvar FORMATION_SATURATION_CORRECTION: A trace that has been
        corrected for formation saturation effects.
    :cvar FORMATION_VOLUME_FACTOR_CORRECTION: A trace that has been
        corrected for the effects of the hydrocarbon formation volume
        factor.
    :cvar FORMATION_WATER_DENSITY_CORRECTION: A trace that has been
        corrected for the effects of the density of the formation water.
    :cvar FORMATION_WATER_SATURATION_CORRECTION: A trace that has been
        corrected for water saturation effects.
    :cvar FREE_FLUID_INDEX: The percent of the bulk volume occupied by
        fluids that are free to flow as measured by the nuclear
        magnetism log.
    :cvar FRICTION_EFFECT_CORRECTION: A trace that has been corrected
        for the effects of friction.
    :cvar GAMMA_RAY: The measurement of naturally occurring gamma ray
        radiation being released by radioisotopes in clay or other
        minerals in the formation.
    :cvar GAMMA_RAY_MINUS_URANIUM: The measurement of the naturally
        occurring gamma radiation less the radiation attributed to
        uranium.
    :cvar GAS_SATURATION: The fraction or percentage of pore volume of
        rock occupied by gas.
    :cvar GRADIOMANOMETER: The measurement of the average density of
        fluids in a wellbore.
    :cvar HIGH_FREQUENCY_CONDUCTIVITY: A measurement of the conductivity
        of the formation, by a high frequency electromagnetic tool,
        within the first few cubic inches of the borehole wall.
    :cvar HIGH_FREQUENCY_ELECTROMAGNETIC: High frequency electromagnetic
        measurements, e.g. from a dielectric logging tool.
    :cvar HIGH_FREQUENCY_ELECTROMAGNETIC_POROSITY: Porosity calculated
        using a high frequency electromagnetic measurement as input.
    :cvar HIGH_FREQUENCY_E_M_PHASE_SHIFT: The amount of change in the
        phase of a high frequency electromagnetic wave.
    :cvar HIGH_FREQUENCY_RESISTIVITY: A measurement of the resistivity
        of the formation, by a high frequency electromagnetic tool,
        within the first few cubic inches of the borehole wall.
    :cvar HYDROCARBON_CORRECTION: A trace that has been corrected for
        the effects of hydrocarbons.
    :cvar HYDROCARBON_DENSITY_CORRECTION: A trace that has been
        corrected for the effects of hydrocarbon density.
    :cvar HYDROCARBON_GRAVITY_CORRECTION: A trace that has been
        corrected for the effects of hydrocarbon gravity.
    :cvar HYDROCARBON_SATURATION: The fraction or percentage of pore
        volume of rock occupied by hydrocarbon.
    :cvar HYDROCARBON_VISCOSITY_CORRECTION: A trace that has been
        corrected for the effects of hydrocarbon viscosity.
    :cvar IMAGE: The likeness of an object produced by an electrical
        device.
    :cvar INTERPRETATION_VARIABLE: A variable in a well log
        interpretation equation.
    :cvar IRON_MUD_CORRECTION: A trace that has been corrected for the
        effects of iron in the borehole fluid.
    :cvar JOINED: A well log trace that has had two or more runs spliced
        together to make a single trace.
    :cvar KCL_MUD_CORRECTION: A trace that has been corrected for the
        effects of KCl in the borehole fluid.
    :cvar LENGTH: A measured distance or dimension.
    :cvar LIMESTONE_ACOUSTIC_POROSITY: Porosity calculated from an
        acoustic log using a limestone matrix.
    :cvar LIMESTONE_DENSITY_POROSITY: Porosity calculated from the bulk
        density measurement of a density log using a limestone matrix
        density.
    :cvar LIMESTONE_NEUTRON_POROSITY: Porosity calculated from a neutron
        log using a limestone matrix.
    :cvar LITHOLOGY_CORRECTION: A trace that has been corrected for
        lithology effects.
    :cvar LOG_DERIVED_PERMEABILITY: The permeability derived from a well
        log.
    :cvar LOG_MATRIX_DENSITY: The density of a rock matrix used with, or
        derived from, the bulk density from a well log. The matrix is
        assumed to have zero porosity.
    :cvar MAGNETIC_CASING_COLLAR_LOCATOR: The signal measured by a
        magnetic device at the location of casing collars and other
        features (e.g., perforations).
    :cvar MATRIX_DENSITY: The density of a rock matrix.  In this case,
        the matrix is assumed to have zero porosity.
    :cvar MATRIX_TRAVEL_TIME: The time it takes for an electromagnetic
        or acoustic wave to traverse a fixed distance of a given
        material or matrix. In this case the material or matrix is a
        specific, zero porosity rock, e.g. sandstone, limestone or
        dolomite.
    :cvar MEASURED_DEPTH: The distance measured along the path of a
        wellbore.
    :cvar MECHANICAL_CALIPER: A well log which uses a mechanical device
        to measure hole diameter.
    :cvar MECHANICAL_CASING_COLLAR_LOCATOR: The signal measured by a
        mechanical device at the location of casing collars and other
        features (e.g., perforations).
    :cvar MEDIUM_CONDUCTIVITY: The conductivity which represents a
        measurement made approximately two to three feet into the
        formation; generally considered to measure the formation where
        it contain fluids which are a mixture of mud filtrate, connate
        water and possibly hydrocarbons.
    :cvar MEDIUM_INDUCTION_CONDUCTIVITY: The conductivity, made by an
        induction log, which represents a measurement made approximately
        two to three feet into the formation.
    :cvar MEDIUM_INDUCTION_RESISTIVITY: The resistivity, made by an
        induction log, which represents a measurement made approximately
        two to three feet into the formation.
    :cvar MEDIUM_LATEROLOG_CONDUCTIVITY: The conductivity, measured by a
        laterolog, which represents a measurement made approximately two
        to three feet into the formation.
    :cvar MEDIUM_LATEROLOG_RESISTIVITY: The resistivity, measured by a
        laterolog, which represents a measurement made approximately two
        to three feet into the formation.
    :cvar MEDIUM_RESISTIVITY: The resistivity which represents a
        measurement made approximately two to three feet into the
        formation; generally considered to measure the formation where
        it contain fluids which are a mixture of mud filtrate, connate
        water and possibly hydrocarbons.
    :cvar MICRO_CONDUCTIVITY: A measurement of the conductivity of the
        formation within the first few cubic inches of the borehole
        wall.
    :cvar MICRO_INVERSE_CONDUCTIVITY: A conductivity measurement made by
        a micro log tool which measures within the first few cubic
        inches of the borehole wall.
    :cvar MICRO_INVERSE_RESISTIVITY: A resistivity measurement made by a
        micro log tool which measures within the first few cubic inches
        of the borehole wall.
    :cvar MICRO_LATEROLOG_CONDUCTIVITY: A measurement of the
        conductivity of the formation, by a laterolog, within the first
        few cubic inches of the borehole wall.
    :cvar MICRO_LATEROLOG_RESISTIVITY: A measurement of the resistivity
        of the formation, by a laterolog, within the first few cubic
        inches of the borehole wall.
    :cvar MICRO_NORMAL_CONDUCTIVITY: A conductivity measurement made by
        a micro log tool which measures within the first few cubic
        inches of the borehole wall.
    :cvar MICRO_NORMAL_RESISTIVITY: A resistivity measurement made by a
        micro log tool which measures within the first few cubic inches
        of the borehole wall.
    :cvar MICRO_RESISTIVITY: A measurement of the resistivity of the
        formation within the first few cubic inches of the borehole
        wall.
    :cvar MICRO_SPHERICALLY_FOCUSED_CONDUCTIVITY: A measurement of the
        conductivity of the formation, by a spherically focused tool,
        within the first few cubic inches of the borehole wall.
    :cvar MICRO_SPHERICALLY_FOCUSED_RESISTIVITY: A measurement of the
        resistivity of the formation, by a spherically focused tool,
        within the first few cubic inches of the borehole wall.
    :cvar MINERAL: The mineral composition, generally in weight percent,
        of a formation as calculated from elemental information obtained
        from a geochemical logging pass; e.g., weight percent of
        dolomite, calcite, illite, quartzite, etc.
    :cvar MUD_CAKE_CONDUCTIVITY: The conductivity of the filter cake,
        the residue deposited on the borehole wall as mud loses filtrate
        into porous and permeable rock.
    :cvar MUD_CAKE_CORRECTION: A trace which has been corrected for the
        effects of mud cake; e.g., mud cake thickness and/or density.
    :cvar MUD_CAKE_DENSITY_CORRECTION: A trace which has been corrected
        for the effects of mud cake density.
    :cvar MUD_CAKE_RESISTIVITY: The resistivity of the filter cake, the
        residue deposited on the borehole wall as mud loses filtrate
        into porous and permeable rock.
    :cvar MUD_CAKE_RESISTIVITY_CORRECTION: A trace which has been
        corrected for the effects of mud cake resistivity.
    :cvar MUD_CAKE_THICKNESS_CORRECTION: A trace which has been
        corrected for the effects of mud cake thickness.
    :cvar MUD_COMPOSITION_CORRECTION: A trace which has been corrected
        for the effects of borehole fluid composition; e.g., a
        correction for KCl in the borehole fluid.
    :cvar MUD_CONDUCTIVITY: The conductivity of the continuous phase
        liquid used for the drilling of the well.
    :cvar MUD_FILTRATE_CONDUCTIVITY: The conductivity of the effluent of
        the continuous phase liquid of the drilling mud which permeates
        porous and permeable rock.
    :cvar MUD_FILTRATE_CORRECTION: A trace which has been corrected for
        the effects of mud filtrate.  This includes things such as
        filtrate salinity.
    :cvar MUD_FILTRATE_DENSITY_CORRECTION: A trace which has been
        corrected for the effects of mud filtrate density.
    :cvar MUD_FILTRATE_RESISTIVITY: The resistivity of the effluent of
        the continuous phase liquid of the drilling mud which permeates
        porous and permeable rock.
    :cvar MUD_FILTRATE_RESISTIVITY_CORRECTION: A trace which has been
        corrected for the effects of mud filtrate resistivity.
    :cvar MUD_FILTRATE_SALINITY_CORRECTION: A trace which has been
        corrected for the effects of mud filtrate salinity.
    :cvar MUD_RESISTIVITY: The resistivity of the continuous phase
        liquid used for the drilling of the well.
    :cvar MUD_SALINITY_CORRECTION: A trace which has been corrected for
        the effects of salinity in the borehole fluid.
    :cvar MUD_VISCOSITY_CORRECTION: A trace which has been corrected for
        the effects of the viscosity of the borehole fluid.
    :cvar MUD_WEIGHT_CORRECTION: A trace which has been corrected for
        the effects of weighting the borehole fluid.
    :cvar NEUTRON_DIE_AWAY_TIME: The time it takes for a neutron
        population to die away to half value.
    :cvar NEUTRON_POROSITY: Porosity from a neutron log.
    :cvar NUCLEAR_CALIPER: A well log which uses a nuclear device to
        measure hole diameter.
    :cvar NUCLEAR_MAGNETIC_DECAY_TIME: The decay time of a nuclear
        magnetic signal.
    :cvar NUCLEAR_MAGNETISM_LOG_PERMEABILITY: The permeability derived
        from a nuclear magnetism log.
    :cvar NUCLEAR_MAGNETISM_POROSITY: Porosity calculated using the
        measurements from a nuclear magnetism logging pass.
    :cvar OH_DENSITY_POROSITY:
    :cvar OH_DOLOMITE_DENSITY_POROSITY: Porosity calculated from the
        bulk density measurement of an open hole density log using a
        dolomite matrix density.
    :cvar OH_DOLOMITE_NEUTRON_POROSITY: Porosity calculated from an open
        hole neutron log using a dolomite matrix.
    :cvar OH_LIMESTONE_DENSITY_POROSITY: Porosity calculated from the
        bulk density measurement of an open hole density log using a
        limestone matrix density.
    :cvar OH_LIMESTONE_NEUTRON_POROSITY: Porosity calculated from an
        open hole neutron log using a limestone matrix.
    :cvar OH_NEUTRON_POROSITY:
    :cvar OH_SANDSTONE_DENSITY_POROSITY: Porosity calculated from the
        bulk density measurement of an open hole density log using a
        sandstone matrix density.
    :cvar OH_SANDSTONE_NEUTRON_POROSITY: Porosity calculated from an
        open hole neutron log using a sandstone matrix.
    :cvar OIL_BASED_MUD_CORRECTION: A trace which has been corrected for
        the effects of oil based borehole fluid.
    :cvar OIL_SATURATION: The fraction or percentage of pore volume of
        rock occupied by oil.
    :cvar PERFORATING: The procedure for introducing holes through
        casing into a formation so that formation fluids can enter into
        the casing.
    :cvar PERMEABILITY: The permeability of the surrounding formation.
    :cvar PHASE_SHIFT: A change or variation according to a harmonic law
        from a standard position or instant of starting.
    :cvar PHOTOELECTRIC_ABSORPTION: The effect measured by the density
        log and produced by the process of a photon colliding with an
        atom, and then being completely absorbed and its total energy
        used to eject one of the orbital electrons from those
        surrounding the nucleus.
    :cvar PHOTOELECTRIC_ABSORPTION_CORRECTION: The correction that is to
        be made to the photoelectric absorption curve.
    :cvar PHYSICAL_MEASUREMENT_CORRECTION: A trace which has been
        corrected for various physical measurement effects; e.g.
        spreading loss.
    :cvar PLANE_ANGLE: An angle formed by two intersecting lines.
    :cvar POROSITY: The total pore volume occupied by fluid in a rock.
        Includes isolated nonconnecting pores and volume occupied by
        absorbed, immobile fluid.
    :cvar POROSITY_CORRECTION: A trace which has been corrected for
        porosity effects.
    :cvar POTASSIUM: The measurement of gamma radiation emitted by
        potassium.
    :cvar PRESSURE: The force or thrust exerted upon a surface divided
        by the area of the surface.
    :cvar PRESSURE_CORRECTION: A trace which has been corrected for the
        effects of pressure in the borehole.
    :cvar PROCESSED: A well log trace which has been processed in some
        way; e.g., depth adjusted or environmentally corrected.
    :cvar PULSED_NEUTRON_POROSITY: Porosity calculated from a pulsed
        neutron log.
    :cvar QUALITY: Degree of excellence.
    :cvar RATIO: A relationship between two values usually expressed as
        a fraction.
    :cvar RAW: A well log trace which has not had any processing.  In
        other words, a trace which has not been depth adjusted or
        environmentally corrected.
    :cvar RELATIVE_BEARING: While looking down hole, it is the clockwise
        angle from the upper side of the sonde to the reference pad or
        electrode.
    :cvar RESISTIVITY: The property measuring the resistance to flow of
        an electrical current.
    :cvar RESISTIVITY_FACTOR_CORRECTION: A trace which has been
        corrected for resistivity factor effects.
    :cvar RESISTIVITY_FROM_ATTENUATION: Resistivity calculated from the
        attenuation of an electromagnetic wave. Generally recorded from
        a LWD resistivity tool.
    :cvar RESISTIVITY_FROM_PHASE_SHIFT: Resistivity calculated from the
        phase shift of an electromagnetic wave. Generally recorded from
        a LWD resistivity tool.
    :cvar RESISTIVITY_PHASE_SHIFT: The amount of change in the phase of
        an electrical wave.
    :cvar RESISTIVITY_RATIO: The ratio of two resistivity values.
    :cvar SALINITY: The concentration of ions in solution.
    :cvar SAMPLING: To take a sample of or from something.
    :cvar SANDSTONE_ACOUSTIC_POROSITY: Porosity calculated from an
        acoustic log using a sandstone matrix.
    :cvar SANDSTONE_DENSITY_POROSITY: Porosity calculated from the bulk
        density measurement of a density log using a sandstone matrix
        density.
    :cvar SANDSTONE_NEUTRON_POROSITY: Porosity calculated from a neutron
        log using a sandstone matrix.
    :cvar SATURATION: The fraction or percentage of the pore volume of a
        rock.
    :cvar SHALE_VOLUME: An estimate of the amount of shale present in
        the formation. Frequently calculated from a gamma ray or SP
        curve.
    :cvar SHALLOW_CONDUCTIVITY: The conductivity which represents a
        measurement made approximately one to two feet into the
        formation; generally considered to measure the formation where
        it contains fluids which are comprised primarily of mud
        filtrate.
    :cvar SHALLOW_INDUCTION_CONDUCTIVITY: The conductivity, measured by
        an induction log, which represents a measurement made
        approximately one to two feet into the formation; generally
        considered to measure the formation where it contains fluids
        which are comprised primarily of mud filtrate.
    :cvar SHALLOW_INDUCTION_RESISTIVITY: The resistivity, measured by an
        induction log, which represents a measurement made approximately
        one to two feet into the formation; generally considered to
        measure the formation where it contains fluids which are
        comprised primarily of mud filtrate.
    :cvar SHALLOW_LATEROLOG_CONDUCTIVITY: The conductivity, measured by
        a laterolog, which represents a measurement made approximately
        one to two feet into the formation; generally considered to
        measure the formation where it contains fluids which are
        comprised primarily of mud filtrate.
    :cvar SHALLOW_LATEROLOG_RESISTIVITY: The resistivity, measured by a
        laterolog, which represents a measurement made approximately one
        to two feet into the formation; generally considered to measure
        the formation where it contains fluids which are comprised
        primarily of mud filtrate.
    :cvar SHALLOW_RESISTIVITY: The resistivity which represents a
        measurement made approximately one to two feet into the
        formation; generally considered to measure the formation where
        it contains fluids which are comprised primarily of mud
        filtrate.
    :cvar SHEAR_WAVE_DOLOMITE_POROSITY: Porosity calculated from a shear
        wave acoustic log using a dolomite matrix.
    :cvar SHEAR_WAVE_LIMESTONE_POROSITY: Porosity calculated from a
        shear wave acoustic log using a limestone matrix.
    :cvar SHEAR_WAVE_MATRIX_TRAVEL_TIME: The time it takes for a shear
        acoustic wave to traverse a fixed distance of a given material
        or matrix. In this case the material or matrix is a specific,
        zero porosity rock, e.g. sandstone, limestone or dolomite.
    :cvar SHEAR_WAVE_SANDSTONE_POROSITY: Porosity calculated from a
        shear wave acoustic log using a sandstone matrix.
    :cvar SHEAR_WAVE_TRAVEL_TIME: The time it takes for a shear acoustic
        wave to traverse a fixed distance.
    :cvar SHIFTED: A well log trace which has had its original values
        shifted by some factor; e.g., added or multiplied by a constant.
    :cvar SIDEWALL_CORE_POROSITY: Porosity from a measurement made on a
        sidewall core.
    :cvar SIGMA: The macroscopic capture cross section, i.e. the
        effective cross-sectional area per unit volume for the capture
        of neutrons.
    :cvar SIGMA_FORMATION: The macroscopic capture cross section, i.e.
        the effective cross-sectional area per unit volume, of the
        formation for the capture of neutrons.
    :cvar SIGMA_GAS: The macroscopic capture cross section, i.e. the
        effective cross-sectional area per unit volume, of gas for the
        capture of neutrons.
    :cvar SIGMA_HYDROCARBON: The macroscopic capture cross section, i.e.
        the effective cross-sectional area per unit volume, of
        hydrocarbon for the capture of neutrons.
    :cvar SIGMA_MATRIX: The macroscopic capture cross section, i.e. the
        effective cross-sectional area per unit volume, of the rock
        matrix for the capture of neutrons.
    :cvar SIGMA_OIL: The macroscopic capture cross section, i.e. the
        effective cross-sectional area per unit volume, of oil for the
        capture of neutrons.
    :cvar SIGMA_WATER: The macroscopic capture cross section, i.e. the
        effective cross-sectional area per unit volume, of water for the
        capture of neutrons.
    :cvar SLIPPAGE_VELOCITY_CORRECTION: A trace which has been corrected
        for slippage velocity.
    :cvar SMOOTHED: A well log trace which has been filtered to smooth,
        or average the trace.
    :cvar SPECTRAL_GAMMA_RAY: The measurement of all the naturally
        occurring gamma radiation separated by energy windows.
    :cvar SPHERICALLY_FOCUSED_CONDUCTIVITY: The conductivity, measured
        by a spherically focused log, which represents the resistivity
        approximately one to two feet into the formation.
    :cvar SPHERICALLY_FOCUSED_RESISTIVITY: The resistivity, measured by
        a spherically focused log, which represents the resistivity
        approximately one to two feet into the formation.
    :cvar SPONTANEOUS_POTENTIAL: The difference in potential (DC
        Voltage) between a moveable electrode in the borehole and a
        distant reference electrode usually at the surface.
    :cvar SPREADING_LOSS_CORRECTION: A trace which has been corrected
        for the effects of spreading loss.
    :cvar SYNTHETIC_WELL_LOG_TRACE: A well log trace which has been
        artificially created, as opposed to an actual measurement, from
        associated measurements or information.
    :cvar TEMPERATURE: A temperature measurement.
    :cvar TEMPERATURE_CORRECTION: A trace which has been corrected for
        the effects of the temperature in the borehole.
    :cvar TENSION: The tension on the wireline cable while logging.
    :cvar TH_K_RATIO: The ratio of the Thorium measurement to the
        Potassium measurement.
    :cvar THORIUM: The measurement of gamma radiation emitted by
        thorium.
    :cvar TIME: A measured or measurable period.
    :cvar TOOL_DIAMETER_CORRECTION: A trace which has been corrected for
        the tool diameter.
    :cvar TOOL_ECCENTRICITY_CORRECTION: A trace which has been corrected
        for the effects of the tool not being centered in the borehole.
    :cvar TOTAL_GAMMA_RAY: The measurement of all the naturally
        occurring gamma radiation.
    :cvar TOTAL_POROSITY: The total pore volume occupied by fluid in a
        rock.
    :cvar TRACER_SURVEY: A well log used for the purpose of monitoring a
        traceable material; e.g. a radioactive isotope.
    :cvar TRAVEL_TIME: The time it takes for an acoustic or
        electromagnetic wave to traverse a specific distance.
    :cvar TRUE_CONDUCTIVITY: The conductivity of fluid-filled rock where
        fluid distributions and saturations are representative of those
        in the uninvaded, undisturbed part of the formation.
    :cvar TRUE_RESISTIVITY: The resistivity of fluid-filled rock where
        fluid distributions and saturations are representative of those
        in the uninvaded, undisturbed part of the formation.
    :cvar TRUE_VERTICAL_DEPTH: The distance along a straight, vertical
        path.  Usually computed from a measured depth and deviation
        information.
    :cvar TUBE_WAVE_DOLOMITE_POROSITY: Porosity calculated from a tube
        wave acoustic log using a dolomite matrix.
    :cvar TUBE_WAVE_LIMESTONE_POROSITY: Porosity calculated from a tube
        wave acoustic log using a limestone matrix.
    :cvar TUBE_WAVE_MATRIX_TRAVEL_TIME: The time it takes for a
        acoustic tube wave to traverse a fixed distance of a given
        material or matrix. In this case the material or matrix is a
        specific, zero porosity rock, e.g. sandstone, limestone or
        dolomite.
    :cvar TUBE_WAVE_SANDSTONE_POROSITY: Porosity calculated from a tube
        wave acoustic log using a sandstone matrix.
    :cvar TUBE_WAVE_TRAVEL_TIME: The time it takes for a tube acoustic
        wave to traverse a fixed distance.
    :cvar URANIUM: The measurement of gamma radiation emitted by
        uranium.
    :cvar VELOCITY: directional speed
    :cvar VOLUME: cubic capacity
    :cvar WATER_BASED_FLUID_CORRECTION: A trace which has been corrected
        for the effects of the components in a water based borehole
        fluid system; e.g., a correction for KCL in the mud.
    :cvar WATER_HOLDUP_CORRECTION: A trace which has been corrected for
        water holdup.
    :cvar WATER_SATURATED_CONDUCTIVITY: The conductivity of rock
        completely saturated with connate water.
    :cvar WATER_SATURATED_RESISTIVITY: The resistivity of rock
        completely saturated with connate water.
    :cvar WATER_SATURATION: The fraction or percentage of pore volume of
        rock occupied by water.
    """

    ACCELERATION = "acceleration"
    ACOUSTIC_CALIPER = "acoustic caliper"
    ACOUSTIC_CASING_COLLAR_LOCATOR = "acoustic casing collar locator"
    ACOUSTIC_IMPEDANCE = "acoustic impedance"
    ACOUSTIC_POROSITY = "acoustic porosity"
    ACOUSTIC_VELOCITY = "acoustic velocity"
    ACOUSTIC_WAVE_MATRIX_TRAVEL_TIME = "acoustic wave matrix travel time"
    ACOUSTIC_WAVE_TRAVEL_TIME = "acoustic wave travel time"
    AMPLITUDE = "amplitude"
    AMPLITUDE_OF_ACOUSTIC_WAVE = "amplitude of acoustic wave"
    AMPLITUDE_OF_E_M_WAVE = "amplitude of E-M wave"
    AMPLITUDE_RATIO = "amplitude ratio"
    AREA = "area"
    ATTENUATION = "attenuation"
    ATTENUATION_OF_ACOUSTIC_WAVE = "attenuation of acoustic wave"
    ATTENUATION_OF_E_M_WAVE = "attenuation of E-M wave"
    AUXILIARY = "auxiliary"
    AVERAGE_POROSITY = "average porosity"
    AZIMUTH = "azimuth"
    BARITE_MUD_CORRECTION = "barite mud correction"
    BED_THICKNESS_CORRECTION = "bed thickness correction"
    BIT_SIZE = "bit size"
    BLOCKED = "blocked"
    BOREHOLE_ENVIRONMENT_CORRECTION = "borehole environment correction"
    BOREHOLE_FLUID_CORRECTION = "borehole fluid correction"
    BOREHOLE_SIZE_CORRECTION = "borehole size correction"
    BROMIDE_MUD_CORRECTION = "bromide mud correction"
    BULK_COMPRESSIBILITY = "bulk compressibility"
    BULK_DENSITY = "bulk density"
    BULK_VOLUME = "bulk volume"
    BULK_VOLUME_GAS = "bulk volume gas"
    BULK_VOLUME_HYDROCARBON = "bulk volume hydrocarbon"
    BULK_VOLUME_OIL = "bulk volume oil"
    BULK_VOLUME_WATER = "bulk volume water"
    C_O_RATIO = "C/O ratio"
    CALIPER = "caliper"
    CASED_HOLE_CORRECTION = "cased hole correction"
    CASING_COLLAR_LOCATOR = "casing collar locator"
    CASING_CORRECTION = "casing correction"
    CASING_DIAMETER_CORRECTION = "casing diameter correction"
    CASING_INSPECTION = "casing inspection"
    CASING_THICKNESS_CORRECTION = "casing thickness correction"
    CASING_WEIGHT_CORRECTION = "casing weight correction"
    CEMENT_CORRECTION = "cement correction"
    CEMENT_DENSITY_CORRECTION = "cement density correction"
    CEMENT_EVALUATION = "cement evaluation"
    CEMENT_THICKNESS_CORRECTION = "cement thickness correction"
    CEMENT_TYPE_CORRECTION = "cement type correction"
    CH_DENSITY_POROSITY = "CH density porosity"
    CH_DOLOMITE_DENSITY_POROSITY = "CH dolomite density porosity"
    CH_DOLOMITE_NEUTRON_POROSITY = "CH dolomite neutron porosity"
    CH_LIMESTONE_DENSITY_POROSITY = "CH limestone density porosity"
    CH_LIMESTONE_NEUTRON_POROSITY = "CH limestone neutron porosity"
    CH_NEUTRON_POROSITY = "CH neutron porosity"
    CH_SANDSTONE_DENSITY_POROSITY = "CH sandstone density porosity"
    CH_SANDSTONE_NEUTRON_POROSITY = "CH sandstone neutron porosity"
    COMPRESSIONAL_WAVE_DOLOMITE_POROSITY = (
        "compressional wave dolomite porosity"
    )
    COMPRESSIONAL_WAVE_LIMESTONE_POROSITY = (
        "compressional wave limestone porosity"
    )
    COMPRESSIONAL_WAVE_MATRIX_TRAVEL_TIME = (
        "compressional wave matrix travel time"
    )
    COMPRESSIONAL_WAVE_SANDSTONE_POROSITY = (
        "compressional wave sandstone porosity"
    )
    COMPRESSIONAL_WAVE_TRAVEL_TIME = "compressional wave travel time"
    CONDUCTIVITY = "conductivity"
    CONDUCTIVITY_FROM_ATTENUATION = "conductivity from attenuation"
    CONDUCTIVITY_FROM_PHASE_SHIFT = "conductivity from phase shift"
    CONNATE_WATER_CONDUCTIVITY = "connate water conductivity"
    CONNATE_WATER_RESISTIVITY = "connate water resistivity"
    CONVENTIONAL_CORE_POROSITY = "conventional core porosity"
    CORE_MATRIX_DENSITY = "core matrix density"
    CORE_PERMEABILITY = "core permeability"
    CORE_POROSITY = "core porosity"
    CORRECTED = "corrected"
    COUNT_RATE = "count rate"
    COUNT_RATE_RATIO = "count rate ratio"
    CROSS_PLOT_POROSITY = "cross plot porosity"
    DECAY_TIME = "decay time"
    DEEP_CONDUCTIVITY = "deep conductivity"
    DEEP_INDUCTION_CONDUCTIVITY = "deep induction conductivity"
    DEEP_INDUCTION_RESISTIVITY = "deep induction resistivity"
    DEEP_LATEROLOG_CONDUCTIVITY = "deep laterolog conductivity"
    DEEP_LATEROLOG_RESISTIVITY = "deep laterolog resistivity"
    DEEP_RESISTIVITY = "deep resistivity"
    DENSITY = "density"
    DENSITY_POROSITY = "density porosity"
    DEPTH = "depth"
    DEPTH_ADJUSTED = "depth adjusted"
    DEPTH_DERIVED_FROM_VELOCITY = "depth derived from velocity"
    DEVIATION = "deviation"
    DIELECTRIC = "dielectric"
    DIFFUSION_CORRECTION = "diffusion correction"
    DIP = "dip"
    DIPMETER = "dipmeter"
    DIPMETER_CONDUCTIVITY = "dipmeter conductivity"
    DIPMETER_RESISTIVITY = "dipmeter resistivity"
    DOLOMITE_ACOUSTIC_POROSITY = "dolomite acoustic porosity"
    DOLOMITE_DENSITY_POROSITY = "dolomite density porosity"
    DOLOMITE_NEUTRON_POROSITY = "dolomite neutron porosity"
    EDITED = "edited"
    EFFECTIVE_POROSITY = "effective porosity"
    ELECTRIC_CURRENT = "electric current"
    ELECTRIC_POTENTIAL = "electric potential"
    ELECTROMAGNETIC_WAVE_MATRIX_TRAVEL_TIME = (
        "electromagnetic wave matrix travel time"
    )
    ELECTROMAGNETIC_WAVE_TRAVEL_TIME = "electromagnetic wave travel time"
    ELEMENT = "element"
    ELEMENTAL_RATIO = "elemental ratio"
    ENHANCED = "enhanced"
    FILTERED = "filtered"
    FLOWMETER = "flowmeter"
    FLUID_DENSITY = "fluid density"
    FLUID_VELOCITY = "fluid velocity"
    FLUID_VISCOSITY = "fluid viscosity"
    FLUSHED_ZONE_CONDUCTIVITY = "flushed zone conductivity"
    FLUSHED_ZONE_RESISTIVITY = "flushed zone resistivity"
    FLUSHED_ZONE_SATURATION = "flushed zone saturation"
    FORCE = "force"
    FORMATION_DENSITY_CORRECTION = "formation density correction"
    FORMATION_PROPERTIES_CORRECTION = "formation properties correction"
    FORMATION_SALINITY_CORRECTION = "formation salinity correction"
    FORMATION_SATURATION_CORRECTION = "formation saturation correction"
    FORMATION_VOLUME_FACTOR_CORRECTION = "formation volume factor correction"
    FORMATION_WATER_DENSITY_CORRECTION = "formation water density correction"
    FORMATION_WATER_SATURATION_CORRECTION = (
        "formation water saturation correction"
    )
    FREE_FLUID_INDEX = "free fluid index"
    FRICTION_EFFECT_CORRECTION = "friction effect correction"
    GAMMA_RAY = "gamma ray"
    GAMMA_RAY_MINUS_URANIUM = "gamma ray minus uranium"
    GAS_SATURATION = "gas saturation"
    GRADIOMANOMETER = "gradiomanometer"
    HIGH_FREQUENCY_CONDUCTIVITY = "high frequency conductivity"
    HIGH_FREQUENCY_ELECTROMAGNETIC = "high frequency electromagnetic"
    HIGH_FREQUENCY_ELECTROMAGNETIC_POROSITY = (
        "high frequency electromagnetic porosity"
    )
    HIGH_FREQUENCY_E_M_PHASE_SHIFT = "high frequency E-M phase shift"
    HIGH_FREQUENCY_RESISTIVITY = "high frequency resistivity"
    HYDROCARBON_CORRECTION = "hydrocarbon correction"
    HYDROCARBON_DENSITY_CORRECTION = "hydrocarbon density correction"
    HYDROCARBON_GRAVITY_CORRECTION = "hydrocarbon gravity correction"
    HYDROCARBON_SATURATION = "hydrocarbon saturation"
    HYDROCARBON_VISCOSITY_CORRECTION = "hydrocarbon viscosity correction"
    IMAGE = "image"
    INTERPRETATION_VARIABLE = "interpretation variable"
    IRON_MUD_CORRECTION = "iron mud correction"
    JOINED = "joined"
    KCL_MUD_CORRECTION = "KCl mud correction"
    LENGTH = "length"
    LIMESTONE_ACOUSTIC_POROSITY = "limestone acoustic porosity"
    LIMESTONE_DENSITY_POROSITY = "limestone density porosity"
    LIMESTONE_NEUTRON_POROSITY = "limestone neutron porosity"
    LITHOLOGY_CORRECTION = "lithology correction"
    LOG_DERIVED_PERMEABILITY = "log derived permeability"
    LOG_MATRIX_DENSITY = "log matrix density"
    MAGNETIC_CASING_COLLAR_LOCATOR = "magnetic casing collar locator"
    MATRIX_DENSITY = "matrix density"
    MATRIX_TRAVEL_TIME = "matrix travel time"
    MEASURED_DEPTH = "measured depth"
    MECHANICAL_CALIPER = "mechanical caliper"
    MECHANICAL_CASING_COLLAR_LOCATOR = "mechanical casing collar locator"
    MEDIUM_CONDUCTIVITY = "medium conductivity"
    MEDIUM_INDUCTION_CONDUCTIVITY = "medium induction conductivity"
    MEDIUM_INDUCTION_RESISTIVITY = "medium induction resistivity"
    MEDIUM_LATEROLOG_CONDUCTIVITY = "medium laterolog conductivity"
    MEDIUM_LATEROLOG_RESISTIVITY = "medium laterolog resistivity"
    MEDIUM_RESISTIVITY = "medium resistivity"
    MICRO_CONDUCTIVITY = "micro conductivity"
    MICRO_INVERSE_CONDUCTIVITY = "micro inverse conductivity"
    MICRO_INVERSE_RESISTIVITY = "micro inverse resistivity"
    MICRO_LATEROLOG_CONDUCTIVITY = "micro laterolog conductivity"
    MICRO_LATEROLOG_RESISTIVITY = "micro laterolog resistivity"
    MICRO_NORMAL_CONDUCTIVITY = "micro normal conductivity"
    MICRO_NORMAL_RESISTIVITY = "micro normal resistivity"
    MICRO_RESISTIVITY = "micro resistivity"
    MICRO_SPHERICALLY_FOCUSED_CONDUCTIVITY = (
        "micro spherically focused conductivity"
    )
    MICRO_SPHERICALLY_FOCUSED_RESISTIVITY = (
        "micro spherically focused resistivity"
    )
    MINERAL = "mineral"
    MUD_CAKE_CONDUCTIVITY = "mud cake conductivity"
    MUD_CAKE_CORRECTION = "mud cake correction"
    MUD_CAKE_DENSITY_CORRECTION = "mud cake density correction"
    MUD_CAKE_RESISTIVITY = "mud cake resistivity"
    MUD_CAKE_RESISTIVITY_CORRECTION = "mud cake resistivity correction"
    MUD_CAKE_THICKNESS_CORRECTION = "mud cake thickness correction"
    MUD_COMPOSITION_CORRECTION = "mud composition correction"
    MUD_CONDUCTIVITY = "mud conductivity"
    MUD_FILTRATE_CONDUCTIVITY = "mud filtrate conductivity"
    MUD_FILTRATE_CORRECTION = "mud filtrate correction"
    MUD_FILTRATE_DENSITY_CORRECTION = "mud filtrate density correction"
    MUD_FILTRATE_RESISTIVITY = "mud filtrate resistivity"
    MUD_FILTRATE_RESISTIVITY_CORRECTION = "mud filtrate resistivity correction"
    MUD_FILTRATE_SALINITY_CORRECTION = "mud filtrate salinity correction"
    MUD_RESISTIVITY = "mud resistivity"
    MUD_SALINITY_CORRECTION = "mud salinity correction"
    MUD_VISCOSITY_CORRECTION = "mud viscosity correction"
    MUD_WEIGHT_CORRECTION = "mud weight correction"
    NEUTRON_DIE_AWAY_TIME = "neutron die away time"
    NEUTRON_POROSITY = "neutron porosity"
    NUCLEAR_CALIPER = "nuclear caliper"
    NUCLEAR_MAGNETIC_DECAY_TIME = "nuclear magnetic decay time"
    NUCLEAR_MAGNETISM_LOG_PERMEABILITY = "nuclear magnetism log permeability"
    NUCLEAR_MAGNETISM_POROSITY = "nuclear magnetism porosity"
    OH_DENSITY_POROSITY = "OH density porosity"
    OH_DOLOMITE_DENSITY_POROSITY = "OH dolomite density porosity"
    OH_DOLOMITE_NEUTRON_POROSITY = "OH dolomite neutron porosity"
    OH_LIMESTONE_DENSITY_POROSITY = "OH limestone density porosity"
    OH_LIMESTONE_NEUTRON_POROSITY = "OH limestone neutron porosity"
    OH_NEUTRON_POROSITY = "OH neutron porosity"
    OH_SANDSTONE_DENSITY_POROSITY = "OH sandstone density porosity"
    OH_SANDSTONE_NEUTRON_POROSITY = "OH sandstone neutron porosity"
    OIL_BASED_MUD_CORRECTION = "oil based mud correction"
    OIL_SATURATION = "oil saturation"
    PERFORATING = "perforating"
    PERMEABILITY = "permeability"
    PHASE_SHIFT = "phase shift"
    PHOTOELECTRIC_ABSORPTION = "photoelectric absorption"
    PHOTOELECTRIC_ABSORPTION_CORRECTION = "photoelectric absorption correction"
    PHYSICAL_MEASUREMENT_CORRECTION = "physical measurement correction"
    PLANE_ANGLE = "plane angle"
    POROSITY = "porosity"
    POROSITY_CORRECTION = "porosity correction"
    POTASSIUM = "potassium"
    PRESSURE = "pressure"
    PRESSURE_CORRECTION = "pressure correction"
    PROCESSED = "processed"
    PULSED_NEUTRON_POROSITY = "pulsed neutron porosity"
    QUALITY = "quality"
    RATIO = "ratio"
    RAW = "raw"
    RELATIVE_BEARING = "relative bearing"
    RESISTIVITY = "resistivity"
    RESISTIVITY_FACTOR_CORRECTION = "resistivity factor correction"
    RESISTIVITY_FROM_ATTENUATION = "resistivity from attenuation"
    RESISTIVITY_FROM_PHASE_SHIFT = "resistivity from phase shift"
    RESISTIVITY_PHASE_SHIFT = "resistivity phase shift"
    RESISTIVITY_RATIO = "resistivity ratio"
    SALINITY = "salinity"
    SAMPLING = "sampling"
    SANDSTONE_ACOUSTIC_POROSITY = "sandstone acoustic porosity"
    SANDSTONE_DENSITY_POROSITY = "sandstone density porosity"
    SANDSTONE_NEUTRON_POROSITY = "sandstone neutron porosity"
    SATURATION = "saturation"
    SHALE_VOLUME = "shale volume"
    SHALLOW_CONDUCTIVITY = "shallow conductivity"
    SHALLOW_INDUCTION_CONDUCTIVITY = "shallow induction conductivity"
    SHALLOW_INDUCTION_RESISTIVITY = "shallow induction resistivity"
    SHALLOW_LATEROLOG_CONDUCTIVITY = "shallow laterolog conductivity"
    SHALLOW_LATEROLOG_RESISTIVITY = "shallow laterolog resistivity"
    SHALLOW_RESISTIVITY = "shallow resistivity"
    SHEAR_WAVE_DOLOMITE_POROSITY = "shear wave dolomite porosity"
    SHEAR_WAVE_LIMESTONE_POROSITY = "shear wave limestone porosity"
    SHEAR_WAVE_MATRIX_TRAVEL_TIME = "shear wave matrix travel time"
    SHEAR_WAVE_SANDSTONE_POROSITY = "shear wave sandstone porosity"
    SHEAR_WAVE_TRAVEL_TIME = "shear wave travel time"
    SHIFTED = "shifted"
    SIDEWALL_CORE_POROSITY = "sidewall core porosity"
    SIGMA = "sigma"
    SIGMA_FORMATION = "sigma formation"
    SIGMA_GAS = "sigma gas"
    SIGMA_HYDROCARBON = "sigma hydrocarbon"
    SIGMA_MATRIX = "sigma matrix"
    SIGMA_OIL = "sigma oil"
    SIGMA_WATER = "sigma water"
    SLIPPAGE_VELOCITY_CORRECTION = "slippage velocity correction"
    SMOOTHED = "smoothed"
    SPECTRAL_GAMMA_RAY = "spectral gamma ray"
    SPHERICALLY_FOCUSED_CONDUCTIVITY = "spherically focused conductivity"
    SPHERICALLY_FOCUSED_RESISTIVITY = "spherically focused resistivity"
    SPONTANEOUS_POTENTIAL = "spontaneous potential"
    SPREADING_LOSS_CORRECTION = "spreading loss correction"
    SYNTHETIC_WELL_LOG_TRACE = "synthetic well log trace"
    TEMPERATURE = "temperature"
    TEMPERATURE_CORRECTION = "temperature correction"
    TENSION = "tension"
    TH_K_RATIO = "Th/K ratio"
    THORIUM = "thorium"
    TIME = "time"
    TOOL_DIAMETER_CORRECTION = "tool diameter correction"
    TOOL_ECCENTRICITY_CORRECTION = "tool eccentricity correction"
    TOTAL_GAMMA_RAY = "total gamma ray"
    TOTAL_POROSITY = "total porosity"
    TRACER_SURVEY = "tracer survey"
    TRAVEL_TIME = "travel time"
    TRUE_CONDUCTIVITY = "true conductivity"
    TRUE_RESISTIVITY = "true resistivity"
    TRUE_VERTICAL_DEPTH = "true vertical depth"
    TUBE_WAVE_DOLOMITE_POROSITY = "tube wave dolomite porosity"
    TUBE_WAVE_LIMESTONE_POROSITY = "tube wave limestone porosity"
    TUBE_WAVE_MATRIX_TRAVEL_TIME = "tube wave matrix travel time"
    TUBE_WAVE_SANDSTONE_POROSITY = "tube wave sandstone porosity"
    TUBE_WAVE_TRAVEL_TIME = "tube wave travel time"
    URANIUM = "uranium"
    VELOCITY = "velocity"
    VOLUME = "volume"
    WATER_BASED_FLUID_CORRECTION = "water based fluid correction"
    WATER_HOLDUP_CORRECTION = "water holdup correction"
    WATER_SATURATED_CONDUCTIVITY = "water saturated conductivity"
    WATER_SATURATED_RESISTIVITY = "water saturated resistivity"
    WATER_SATURATION = "water saturation"


class MudType(Enum):
    """
    Specifies the class of a drilling fluid.

    :cvar OIL_BASED:
    :cvar WATER_BASED:
    :cvar OTHER: A drilling fluid in which neither water nor oil is the
        continuous phase.
    :cvar PNEUMATIC: A drilling fluid which is gas-based.
    """

    OIL_BASED = "oil-based"
    WATER_BASED = "water-based"
    OTHER = "other"
    PNEUMATIC = "pneumatic"


@dataclass
class MudDensityStatistics:
    """
    Mud density readings at average or channel.

    :ivar average: Average mud density through the interval.
    :ivar channel: Log channel from which the mud density statistics
        were calculated.
    """

    average: Optional[str] = field(
        default=None,
        metadata={
            "name": "Average",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class MudLogParameter:
    """Information around the mud log: type, time taken, top and bottom depth, pressure gradient, etc.

    :ivar md_interval: Measured depth interval that is the focus of this
        parameter.
    :ivar citation: An ISO 19115 EIP-derived set of metadata attached to
        ensure the traceability of the MudLogParameter.
    :ivar comments: Description or secondary qualifier pertaining to
        MudlogParameter or to Value attribute.
    :ivar uid: Unique identifier for this instance of MudLogParameter.
    """

    md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    citation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Citation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MudLogReport:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class MudLogStringParameterKind(Enum):
    """
    Specifies values for mud log parameters that are described by character
    strings.
    """

    BIT_PARAMETERS = "bit parameters"
    BIT_TYPE_COMMENT = "bit type comment"
    CASING_POINT_COMMENT = "casing point comment"
    CHROMATOGRAPH_COMMENT = "chromatograph comment"
    CIRCULATION_SYSTEM_COMMENT = "circulation system comment"
    CORE_INTERVAL_COMMENT = "core interval comment"
    DRILLING_DATA_COMMENT = "drilling data comment"
    GAS_PEAKS_COMMENT = "gas peaks comment"
    GAS_RATIO_COMMENT = "gas ratio comment"
    GENERAL_ENGINEERING_COMMENT = "general engineering comment"
    LITHLOG_COMMENT = "lithlog comment"
    LWD_COMMENT = "LWD comment"
    MARKER_OR_FORMATION_TOP_COMMENT = "marker or formation top comment"
    MIDNIGHT_DEPTH_DATE = "midnight depth date"
    MUD_CHECK_COMMENT = "mud check comment"
    MUD_DATA_COMMENT = "mud data comment"
    MUDLOG_COMMENT = "mudlog comment"
    PRESSURE_DATA_COMMENT = "pressure data comment"
    SHALE_DENSITY_COMMENT = "shale density comment"
    SHORT_TRIP_COMMENT = "short trip comment"
    SHOW_REPORT_COMMENT = "show report comment"
    SIDEWALL_CORE_COMMENT = "sidewall core comment"
    SLIDING_INTERVAL = "sliding Interval"
    STEAM_STILL_RESULTS_COMMENT = "steam still results comment"
    SURVEY_COMMENT = "survey comment"
    TEMPERATURE_DATA_COMMENT = "temperature data comment"
    TEMPERATURE_TREND_COMMENT = "temperature trend comment"
    UNKNOWN = "unknown"
    WIRELINE_LOG_COMMENT = "wireline log comment"


@dataclass
class MudLosses:
    """
    Operations Mud Losses Schema.Captures volumes of mud lost for specific
    activities or onsite locations and total volumes for surface and down hole.

    :ivar vol_lost_shaker_surf: Volume of mud lost at shakers (at
        surface).
    :ivar vol_lost_mud_cleaner_surf: Volume of mud lost in mud cleaning
        equipment (at surface).
    :ivar vol_lost_pits_surf: Volume of mud lost in pit room (at
        surface).
    :ivar vol_lost_tripping_surf: Volume of mud lost while tripping (at
        surface).
    :ivar vol_lost_other_surf: Surface volume lost other location.
    :ivar vol_tot_mud_lost_surf: Total volume of mud lost at surface.
    :ivar vol_lost_circ_hole: Mud volume lost downhole while
        circulating.
    :ivar vol_lost_csg_hole: Mud volume lost downhole while running
        casing.
    :ivar vol_lost_cmt_hole: Mud volume lost downhole while cementing.
    :ivar vol_lost_bhd_csg_hole: Mud volume lost downhole behind casing.
    :ivar vol_lost_abandon_hole: Mud volume lost downhole during
        abandonment.
    :ivar vol_lost_other_hole: Mud volume lost downhole from other
        location.
    :ivar vol_tot_mud_lost_hole: Total volume of mud lost downhole.
    """

    vol_lost_shaker_surf: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolLostShakerSurf",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_lost_mud_cleaner_surf: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolLostMudCleanerSurf",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_lost_pits_surf: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolLostPitsSurf",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_lost_tripping_surf: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolLostTrippingSurf",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_lost_other_surf: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolLostOtherSurf",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_tot_mud_lost_surf: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolTotMudLostSurf",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_lost_circ_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolLostCircHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_lost_csg_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolLostCsgHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_lost_cmt_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolLostCmtHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_lost_bhd_csg_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolLostBhdCsgHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_lost_abandon_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolLostAbandonHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_lost_other_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolLostOtherHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_tot_mud_lost_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolTotMudLostHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class MudSubType(Enum):
    """
    The name of a data extension.
    """

    AERATED_MUD = "aerated mud"
    AIR = "air"
    BRACKISH_WATER = "brackish water"
    BRINE = "brine"
    CAESIUM_FORMATE = "caesium formate"
    DIESEL_OIL_BASED = "diesel oil-based"
    ESTER_SYNTHETIC_BASED = "ester synthetic-based"
    FRESHWATER = "freshwater"
    GLYCOL_MUD = "glycol mud"
    GYP_MUD = "gyp mud"
    INTERNAL_OLEFIN_SYNTHETIC_BASED = "internal-olefin synthetic-based"
    LIGHTLY_TREATED_NON_DISPERSED = "lightly treated non-dispersed"
    LIGNITE_LIGNOSULFONATE_MUD = "lignite/lignosulfonate mud"
    LIME_MUD = "lime mud"
    LINEAR_PARAFFIN_SYNTHETIC_BASED = "linear paraffin synthetic-based"
    LINEAR_ALPHA_OLEFIN_SYNTHETIC_BASED = "linear-alpha-olefin synthetic-based"
    LOW_SOLIDS = "low solids"
    LOW_TOXICITY_MINERAL_OIL_BASED = "low toxicity mineral oil-based"
    MINERAL_OIL_BASED = "mineral oil-based"
    MIST = "mist"
    MIXED_METAL_OXIDE_MUD = "mixed-metal oxide mud"
    NATIVE_NATURAL_MUD = "native/natural mud"
    NATURAL_GAS = "natural gas"
    NITROGEN_AERATED_MUD = "nitrogen-aerated mud"
    NON_AQUEOUS_INVERT_EMULSION_DRILLING_FLUIDS = (
        "non-aqueous (invert emulsion) drilling fluids"
    )
    NON_DISPERSED = "non-dispersed"
    PNEUMATIC_GASEOUS_DRILLING_FLUIDS = "pneumatic (gaseous) drilling fluids"
    POLYMER_MUD = "polymer mud"
    POTASSIUM_FORMATE = "potassium formate"
    POTASSIUM_TREATED_MUD = "potassium-treated mud"
    SALT_WATER_MUD = "salt water mud"
    SATURATED_SALT_MUD = "saturated salt mud"
    SEA_WATER = "sea water"
    SEAWATER_MUD = "seawater mud"
    SILICATE_MUD = "silicate mud"
    SODIUM_FORMATE = "sodium formate"
    SPUD_MUD = "spud mud"
    STABLE_FOAM = "stable foam"
    STIFF_FOAM = "stiff foam"
    WATER_BASED_DRILLING_FLUIDS = "water-based drilling fluids"


@dataclass
class MudlogReportInterval:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class NameTagLocation(Enum):
    """
    Specifies the values for the locations where an equipment tag might be found.
    """

    BODY = "body"
    BOX = "box"
    OTHER = "other"
    PIN = "pin"


class NameTagNumberingScheme(Enum):
    """
    Specifies the values of the specifications for creating equipment tags.
    """

    ANSI_AIM_BC10 = "ANSI/AIM-BC10"
    ANSI_AIM_BC2 = "ANSI/AIM-BC2"
    ANSI_AIM_BC6 = "ANSI/AIM-BC6"
    EAN_UCC = "EAN.UCC"
    EPC64 = "EPC64"
    EPC96 = "EPC96"
    F2_F = "F2F"
    MFM = "MFM"
    MSRCID = "MSRCID"
    SERIAL_NUMBER = "serial number"


class NameTagTechnology(Enum):
    """
    Specifies the values for the mechanisms for attaching an equipment tag to an
    item.
    """

    INTRINSIC = "intrinsic"
    LABELED = "labeled"
    PAINTED = "painted"
    STAMPED = "stamped"
    TAGGED = "tagged"
    TEMPORARY = "temporary"


class NozzleType(Enum):
    """
    Specifies the type of nozzle.
    """

    EXTENDED = "extended"
    NORMAL = "normal"


@dataclass
class OsdutubularAssemblyStatus:
    """
    OSDU Tubular Assembly Status information.

    :ivar date: Date the status has been established.
    :ivar description: Used to describe the reason of Activity - such as
        cut/pull, pulling.
    :ivar status_type: Status type.
    """

    class Meta:
        name = "OSDUTubularAssemblyStatus"

    date: Optional[str] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    status_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "StatusType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class ObjectSequence:
    """
    Defines a sequence number with an optional description attribute.

    :ivar description: The description of this object sequence.
    """

    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class OpsReport:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class OtherConnectionTypes(Enum):
    """
    Specifies the values for other types of connections.
    """

    CEMENTED_IN_PLACE = "cemented-in-place"
    DOGSCOMPRESSIONFIT_SEALED = "dogscompressionfit-sealed"


@dataclass
class PpfgchannelOsduintegration:
    """
    Information about a PPFGChannel that is relevant for OSDU integration but does
    not have a natural place in a PPFGChannel object.

    :ivar record_date: The date that the PPFG channel was created by the
        PPFG practitioner or contractor.
    """

    class Meta:
        name = "PPFGChannelOSDUIntegration"

    record_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "RecordDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class PpfgchannelSetOsduintegration:
    """
    Information about a PPFGChannelSet that is relevant for OSDU integration but
    does not have a natural place in a PPFGChanneSet object.

    :ivar record_date: The date that the PPFGChanneSet was created by
        the PPFG practitioner or contractor.
    """

    class Meta:
        name = "PPFGChannelSetOSDUIntegration"

    record_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "RecordDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class PpfgdataDerivation(Enum):
    """
    Specifies the source of PPFG data.

    :cvar BASIN_MODEL: Data resulting from general basin modeling.
    :cvar ESTIMATED: Data built as an estimation from another
        datasource.
    :cvar INFERRED: Data inferred from parent data.
    :cvar MEASURED: Data resulting from raw measurement on site.
    :cvar POST_DRILL_INTERPRETATION: Data resulting from a PostDrill
        Interpretation.
    :cvar PRE_DRILL_INTERPRETATION: Data resulting from a PreDrill
        Interpretation.
    :cvar REAL_TIME: Raw dataset resulting from real-time acquisition.
    :cvar TRANSFORMED: Data resulting from a transformation.
    """

    BASIN_MODEL = "basin model"
    ESTIMATED = "estimated"
    INFERRED = "inferred"
    MEASURED = "measured"
    POST_DRILL_INTERPRETATION = "post-drill interpretation"
    PRE_DRILL_INTERPRETATION = "pre-drill interpretation"
    REAL_TIME = "real time"
    TRANSFORMED = "transformed"


class PpfgdataProcessing(Enum):
    """
    The type and level of data processing that has been applied to PPFG data.
    """

    CALIBRATED = "calibrated"
    CORRECTED = "corrected"
    FILTERED = "filtered"
    INTERPOLATED = "interpolated"
    INTERPRETED = "interpreted"
    NORMALIZED = "normalized"
    SMOOTHED = "smoothed"
    TRANSFORMED = "transformed"


class Ppfgfamily(Enum):
    """The Family Type of the PPFG quantity measured, for example 'pore pressure
    from corrected drilling exponent'.

    An individual quantity that belongs to a Main Family.
    """

    ACHIEVABLE_FRACTURE_GRADIENT = "achievable fracture gradient"
    BREAKOUT_WIDTH = "breakout width"
    CORRECTED_TEMPERATURE = "corrected temperature"
    EFFECTIVE_STRESS = "effective stress"
    EFFECTIVE_STRESS_GRADIENT = "effective stress gradient"
    FORMATION_TEMPERATURE = "formation temperature"
    FRACTURE_BREAKDOWN_GRADIENT = "fracture breakdown gradient"
    FRACTURE_BREAKDOWN_PRESSURE = "fracture breakdown pressure"
    FRACTURE_CLOSURE_GRADIENT = "fracture closure gradient"
    FRACTURE_CLOSURE_PRESSURE = "fracture closure pressure"
    FRACTURE_GRADIENT = "fracture gradient"
    FRACTURE_INITIATION_PRESSURE = "fracture initiation pressure"
    FRACTURE_INITIATION_PRESSURE_GRADIENT = (
        "fracture initiation pressure gradient"
    )
    FRACTURE_PRESSURE = "fracture pressure"
    FRACTURE_PROPAGATION_PRESSURE = "fracture propagation pressure"
    FRACTURE_PROPAGATION_PRESSURE_GRADIENT = (
        "fracture propagation pressure gradient"
    )
    FRICTION_ANGLE_FAILURE_CRITERIA = "friction angle (failure criteria)"
    INTERMEDIATE_PRINCIPLE_STRESS = "intermediate principle stress"
    INTERMEDIATE_PRINCIPLE_STRESS_GRADIENT = (
        "intermediate principle stress gradient"
    )
    LEAST_PRINCIPLE_STRESS = "least principle stress"
    LEAST_PRINCIPLE_STRESS_GRADIENT = "least principle stress gradient"
    MARGIN = "margin"
    MAX_HORIZONTAL_STRESS = "max horizontal stress"
    MAX_HORIZONTAL_STRESS_GRADIENT = "max horizontal stress gradient"
    MAXIMUM_HORIZONTAL_STRESS_AZIMUTH = "maximum horizontal stress azimuth"
    MAXIMUM_PRINCIPLE_STRESS = "maximum principle stress"
    MAXIMUM_PRINCIPLE_STRESS_GRADIENT = "maximum principle stress gradient"
    MEAN_EFFECTIVE_STRESS = "mean effective stress"
    MEAN_EFFECTIVE_STRESS_GRADIENT = "mean effective stress gradient"
    MEAN_STRESS = "mean stress"
    MEAN_STRESS_GRADIENT = "mean stress gradient"
    MEASURED_DEPTH = "measured depth"
    MEASURED_FORMATION_PRESSURE = "measured formation pressure"
    MEASURED_FORMATION_PRESSURE_GRADIENT = (
        "measured formation pressure gradient"
    )
    MINIMUM_HORIZONTAL_STRESS = "minimum horizontal stress"
    MINIMUM_HORIZONTAL_STRESS_GRADIENT = "minimum horizontal stress gradient"
    MODELED_FRACTURE_GRADIENT = "modeled fracture gradient"
    MPD_BACK_PRESSURE = "mpd back pressure"
    NORMAL_COMPACTION_TRENDLINE = "normal compaction trendline"
    NORMAL_COMPACTION_TRENDLINE_CORRECTED_DRILLING_EXPONENT = (
        "normal compaction trendline - corrected drilling exponent"
    )
    NORMAL_COMPACTION_TRENDLINE_DENSITY = (
        "normal compaction trendline - density"
    )
    NORMAL_COMPACTION_TRENDLINE_MECHANICAL_SPECIFIC_ENERGY = (
        "normal compaction trendline - mechanical specific energy"
    )
    NORMAL_COMPACTION_TRENDLINE_RESISTIVITY = (
        "normal compaction trendline - resistivity"
    )
    NORMAL_COMPACTION_TRENDLINE_SONIC = "normal compaction trendline - sonic"
    NORMAL_COMPACTION_TRENDLINE_TOTAL_POROSITY = (
        "normal compaction trendline - total porosity"
    )
    NORMAL_EFFECTIVE_STRESS = "normal effective stress"
    NORMAL_EFFECTIVE_STRESS_GRADIENT = "normal effective stress gradient"
    NORMAL_HYDROSTATIC_PRESSURE = "normal hydrostatic pressure"
    NORMAL_HYDROSTATIC_PRESSURE_GRADIENT = (
        "normal hydrostatic pressure gradient"
    )
    OVERBURDEN_GRADIENT = "overburden gradient"
    OVERBURDEN_PRESSURE = "overburden pressure"
    OVERPRESSURE = "overpressure"
    OVERPRESSURE_GRADIENT = "overpressure gradient"
    PORE_PRESSURE = "pore  pressure"
    PORE_PRESSURE_ESTIMATED_FROM_CONNECTION_GAS = (
        "pore pressure estimated from connection gas"
    )
    PORE_PRESSURE_ESTIMATED_FROM_DENSITY = (
        "pore pressure estimated from density"
    )
    PORE_PRESSURE_ESTIMATED_FROM_DRILL_GAS = (
        "pore pressure estimated from drill gas"
    )
    PORE_PRESSURE_ESTIMATED_FROM_DRILLING_PARAMETER = (
        "pore pressure estimated from drilling parameter"
    )
    PORE_PRESSURE_ESTIMATED_FROM_LOG = "pore pressure estimated from log"
    PORE_PRESSURE_ESTIMATED_FROM_RESISTIVITY = (
        "pore pressure estimated from resistivity"
    )
    PORE_PRESSURE_ESTIMATED_FROM_SEISMIC_VELOCITY = (
        "pore pressure estimated from seismic velocity"
    )
    PORE_PRESSURE_ESTIMATED_FROM_SONIC = "pore pressure estimated from sonic"
    PORE_PRESSURE_ESTIMATED_FROM_TOTAL_POROSITY = (
        "pore pressure estimated from total porosity"
    )
    PORE_PRESSURE_FROM_BASIN_MODEL = "pore pressure from basin model"
    PORE_PRESSURE_FROM_CORRECTED_DRILLING_EXPONENT = (
        "pore pressure from corrected drilling exponent"
    )
    PORE_PRESSURE_FROM_MECHANICAL_SPECIFIC_ENERGY = (
        "pore pressure from mechanical specific energy"
    )
    PORE_PRESSURE_GRADIENT = "pore pressure gradient"
    PORE_PRESSURE_GRADIENT_ESTIMATED_FROM_CONNECTION_GAS = (
        "pore pressure gradient estimated from connection gas"
    )
    PORE_PRESSURE_GRADIENT_ESTIMATED_FROM_DENSITY = (
        "pore pressure gradient estimated from density"
    )
    PORE_PRESSURE_GRADIENT_ESTIMATED_FROM_DRILL_GAS = (
        "pore pressure gradient estimated from drill gas"
    )
    PORE_PRESSURE_GRADIENT_ESTIMATED_FROM_DRILLING_PARAMETER = (
        "pore pressure gradient estimated from drilling parameter"
    )
    PORE_PRESSURE_GRADIENT_ESTIMATED_FROM_LOG = (
        "pore pressure gradient estimated from log"
    )
    PORE_PRESSURE_GRADIENT_ESTIMATED_FROM_RESISTIVITY = (
        "pore pressure gradient estimated from resistivity"
    )
    PORE_PRESSURE_GRADIENT_ESTIMATED_FROM_SEISMIC_VELOCITY = (
        "pore pressure gradient estimated from seismic velocity"
    )
    PORE_PRESSURE_GRADIENT_ESTIMATED_FROM_SONIC = (
        "pore pressure gradient estimated from sonic"
    )
    PORE_PRESSURE_GRADIENT_ESTIMATED_FROM_TOTAL_POROSITY = (
        "pore pressure gradient estimated from total porosity"
    )
    PORE_PRESSURE_GRADIENT_FROM_BASIN_MODEL = (
        "pore pressure gradient from basin model"
    )
    PORE_PRESSURE_GRADIENT_FROM_CORRECTED_DRILLING_EXPONENT = (
        "pore pressure gradient from corrected drilling exponent"
    )
    PORE_PRESSURE_GRADIENT_FROM_MECHANICAL_SPECIFIC_ENERGY = (
        "pore pressure gradient from mechanical specific energy"
    )
    PORE_FRAC_WINDOW = "pore-frac window"
    SAFE_DRILLING_MARGIN = "safe drilling margin"
    SEDIMENTATION_RATE = "sedimentation rate"
    SHEAR_FAILURE_PRESSURE_COLLAPSE_PRESSURE = (
        "shear failure pressure (collapse pressure)"
    )
    SHEAR_FAILURE_PRESSURE_GRADIENT_COLLAPSE_PRESSURE_GRADIENT = (
        "shear failure pressure gradient (collapse pressure gradient)"
    )
    STRENGTHENED_FRACTURE_GRADIENT = "strengthened fracture gradient"
    STRUCTURALLY_ADJUSTED_PORE_PRESSURE = "structurally adjusted pore pressure"
    STRUCTURALLY_ADJUSTED_PORE_PRESSURE_GRADIENT = (
        "structurally adjusted pore pressure gradient"
    )
    SUBNORMAL_PRESSURE = "subnormal pressure"
    TEMPERATURE_ANNULAR = "temperature annular"
    TEMPERATURE_BHA = "temperature bha"
    TRUE_VERTICAL_DEPTH = "true vertical depth"
    TWO_WAY_TIME = "two way time"
    UNCONFINED_COMPRESSIVE_STRENGTH = "unconfined compressive strength"
    VERTICAL_EFFECTIVE_STRESS = "vertical effective stress"
    VERTICAL_EFFECTIVE_STRESS_GRADIENT = "vertical effective stress gradient"
    VERTICAL_STRESS = "vertical stress"
    VERTICAL_STRESS_GRADIENT = "vertical stress gradient"


class PpfgfamilyMnemonic(Enum):
    """
    The mnemonic for the Family Type of the PPFG quantity measured.
    """

    BOANGLE = "BOAngle"
    ES = "ES"
    ESG = "ESG"
    ESN = "ESN"
    FA = "FA"
    FBP = "FBP"
    FBPG = "FBPG"
    FCP = "FCP"
    FCPG = "FCPG"
    FG = "FG"
    FG_ACHIV = "FG ACHIV"
    FG_BM = "FG BM"
    FG_STREN = "FG STREN"
    FIP = "FIP"
    FIPG = "FIPG"
    FP = "FP"
    FPP = "FPP"
    FPPG = "FPPG"
    FTEMP = "FTEMP"
    IPS = "IPS"
    IPSG = "IPSG"
    LPS = "LPS"
    LPSG = "LPSG"
    MD = "MD"
    MES = "MES"
    MESG = "MESG"
    MPD_BP = "MPD BP"
    MPS = "MPS"
    MPSG = "MPSG"
    MRGN = "MRGN"
    MS = "MS"
    MSG = "MSG"
    NCT = "NCT"
    NCT_DT = "NCT DT"
    NCT_DXC = "NCT DXC"
    NCT_MSE = "NCT MSE"
    NCT_PHIT = "NCT PHIT"
    NCT_RES = "NCT RES"
    NCT_RHOB = "NCT RHOB"
    NESG = "NESG"
    OB = "OB"
    OBG = "OBG"
    OP = "OP"
    OPG = "OPG"
    PFW = "PFW"
    PNORM = "PNORM"
    PNORMG = "PNORMG"
    PP = "PP"
    PP_BM = "PP BM"
    PP_CG = "PP CG"
    PP_DG = "PP DG"
    PP_DP = "PP DP"
    PP_DT = "PP DT"
    PP_DXC = "PP DXC"
    PP_LOG = "PP LOG"
    PP_MEAS = "PP MEAS"
    PP_MSE = "PP MSE"
    PP_PHIT = "PP PHIT"
    PP_RES = "PP RES"
    PP_RHOB = "PP RHOB"
    PP_VSEIS = "PP VSEIS"
    PP_ZADJ = "PP ZADJ"
    PPG = "PPG"
    PPG_BM = "PPG BM"
    PPG_CG = "PPG CG"
    PPG_DG = "PPG DG"
    PPG_DP = "PPG DP"
    PPG_DT = "PPG DT"
    PPG_DX_C = "PPG DxC"
    PPG_EST = "PPG EST"
    PPG_MEAS = "PPG MEAS"
    PPG_MSE = "PPG MSE"
    PPG_PHIT = "PPG PHIT"
    PPG_RES = "PPG RES"
    PPG_RHOB = "PPG RHOB"
    PPG_VSEIS = "PPG VSEIS"
    PPG_ZADJ = "PPG ZADJ"
    PSNORM = "PSNORM"
    SDM = "SDM"
    SEDRT = "SEDRT"
    SFP = "SFP"
    SFPG = "SFPG"
    SHAZ = "SHAZ"
    SHMAX = "SHmax"
    SHMAX_G = "SHmaxG"
    SHMIN = "Shmin"
    SHMIN_G = "ShminG"
    SV = "SV"
    SVG = "SVG"
    TEMP_A = "TEMP A"
    TEMP_BHA = "TEMP BHA"
    TEMP_C = "TEMP C"
    TVD = "TVD"
    TWT = "TWT"
    UCS = "UCS"
    VES = "VES"
    VESG = "VESG"


@dataclass
class PpfglogOsduintegration:
    """
    Information about a PPFGLog that is relevant for OSDU integration but does not
    have a natural place in a PPFGLog object.

    :ivar record_date: The date that the PPFG channel set was created by
        the PPFG practitioner or contractor.
    """

    class Meta:
        name = "PPFGLogOSDUIntegration"

    record_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "RecordDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class PpfgmainFamily(Enum):
    """The Main Family Type of the PPFG quantity measured, for example 'pore
    pressure'.

    Primarily used for high level data classification.
    """

    COMPACTION_TRENDLINE = "compaction trendline"
    EFFECTIVE_STRESS = "effective stress"
    EFFECTIVE_STRESS_GRADIENT = "effective stress gradient"
    FORMATION_PRESSURE = "formation pressure"
    FORMATION_PRESSURE_GRADIENT = "formation pressure gradient"
    FRACTURE_PRESSURE = "fracture pressure"
    FRACTURE_PRESSURE_GRADIENT = "fracture pressure gradient"
    GEOMECHNANICS = "geomechnanics"
    MARGIN = "margin"
    MPD = "mpd"
    OVERPRESSURE = "overpressure"
    OVERPRESSURE_GRADIENT = "overpressure gradient"
    PORE_PRESSURE = "pore pressure"
    PORE_PRESSURE_GRADIENT = "pore pressure gradient"
    REFERENCE = "reference"
    SEDIMENTATION_RATE = "sedimentation rate"
    STRESS = "stress"
    STRESS_GRADIENT = "stress gradient"
    TEMPERATURE = "temperature"
    TRANSFORM_MODEL_PARAMETER = "transform model parameter"
    WINDOW = "window"


class PpfgmodeledLithology(Enum):
    """
    Specifies the type of lithology modeled in PPFG data.
    """

    CARBONATE = "carbonate"
    COMPOSITE = "composite"
    IGNEOUS = "igneous"
    SALT = "salt"
    SAND = "sand"
    SHALE = "shale"


class PpfgtectonicSetting(Enum):
    """
    Specifies the source of PPFG data.
    """

    COMPRESSIONAL = "compressional"
    EXTENSIONAL = "extensional"
    STRIKE_SLIP = "strike slip"
    TRANSPRESSIONAL = "transpressional"
    TRANSTENSIONAL = "transtensional"


class PpfgtransformModelType(Enum):
    """
    Empirical calibrated models used for pressure calculations from a petrophysical
    channel (sonic or resistivity).
    """

    APPARENT_POISSON_S_RATIO = "apparent poisson's ratio"
    BOWERS = "bowers"
    DIAGENETIC = "diagenetic"
    EATON = "eaton"
    EATON_DAINES = "eaton-daines"
    EQUIVALENT_DEPTH = "equivalent depth"
    K0 = "k0"
    STRESS_PATH = "stress path"


class PpfguncertaintyType(Enum):
    """
    Specifies class of uncertainty for PPFG data.
    """

    HIGH = "high"
    LOW = "low"
    MAXIMUM = "maximum"
    MEAN = "mean"
    MID = "mid"
    MINIMUM = "minimum"
    MOST_LIKELY = "most likely"
    P10 = "p10"
    P50 = "p50"
    P90 = "p90"


@dataclass
class Parameter:
    formula: Optional[str] = field(
        default=None,
        metadata={
            "name": "Formula",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "name": "Title",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class PassDetail:
    """
    Details about an individual pass when using PassIndexedDepth.

    :ivar pass_value: The pass number.
    :ivar description: Description of pass such as Calibration Pass,
        Main Pass, Repeated Pass.
    """

    pass_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "Pass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class PassDirection(Enum):
    """
    :cvar UP: The tool is moving up (decreasing depth).
    :cvar HOLDING_STEADY: The tools is not moving up or down (depth is
        not changing).
    :cvar DOWN: The tool is moving down (increasing depth).
    """

    UP = "up"
    HOLDING_STEADY = "holding steady"
    DOWN = "down"


class PerfConveyanceMethod(Enum):
    """Information on how perforation is conveyed: slick line, wireline, tubing"""

    SLICK_LINE = "slick line"
    TUBING_CONVEYED = "tubing conveyed"
    WIRELINE = "wireline"


@dataclass
class PerfHole:
    """
    Information on the perforated hole.

    :ivar md_interval: Measured depth interval for the perforation hole.
    :ivar tvd_interval: The true vertical depth that describes the hole.
    :ivar hole_diameter: The diameter of the hole.
    :ivar hole_angle: The angle of the holes.
    :ivar hole_pattern: The pattern of the holes.
    :ivar remarks: Remarks and comments about this perforated hole.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar hole_density: The density of the holes.
    :ivar hole_count: The number of holes.
    :ivar uid: Unique identifier for this instance of PerfHole.
    """

    md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_diameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "HoleDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "HoleAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_pattern: Optional[str] = field(
        default=None,
        metadata={
            "name": "HolePattern",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    remarks: Optional[str] = field(
        default=None,
        metadata={
            "name": "Remarks",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_density: Optional[str] = field(
        default=None,
        metadata={
            "name": "HoleDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "HoleCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PerfSlot:
    """
    Information on slot resulting from a perforation.

    :ivar slot_height: The height of slot.
    :ivar slot_width: The width of the slot.
    :ivar slot_center_distance: Distance from center point.
    :ivar slot_count: The number of the slots.
    :ivar remarks: Remarks and comments about this perforation slot.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of PerfSlot.
    """

    slot_height: Optional[str] = field(
        default=None,
        metadata={
            "name": "SlotHeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    slot_width: Optional[str] = field(
        default=None,
        metadata={
            "name": "SlotWidth",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    slot_center_distance: Optional[str] = field(
        default=None,
        metadata={
            "name": "SlotCenterDistance",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    slot_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "SlotCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    remarks: Optional[str] = field(
        default=None,
        metadata={
            "name": "Remarks",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class PerforationStatus(Enum):
    """
    Specifies the set of values for the status of a perforation.
    """

    OPEN = "open"
    PROPOSED = "proposed"
    SQUEEZED = "squeezed"


class PerforationToolType(Enum):
    """
    Species the values for the type of perforation tool used to create the perfs.
    """

    CASING_GUN = "casing gun"
    COILED_TUBING_JET_TOOL = "coiled tubing jet tool"
    DRILLED = "drilled"
    MANDREL = "mandrel"
    N_A = "n/a"
    SLOTS_MACHINE_CUT = "slots-machine cut"
    SLOTS_UNDERCUT = "slots-undercut"
    STRIP_GUN = "strip gun"
    TCP_GUN = "tcp gun"
    THROUGH_TUBING_GUN = "through tubing gun"


@dataclass
class Personnel:
    """Operations Personnel Component Schema.

    List each company on the rig at the time of the report and key
    information about each company, for example, name, type of service,
    and number of personnel.

    :ivar company: Pointer to a BusinessAssociate representing the
        company.
    :ivar type_service: Service provided by the company.
    :ivar num_people: Number of people on board for that company.
    :ivar total_time: Total time worked by the company (commonly in
        hours).
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Personnel.
    """

    company: Optional[str] = field(
        default=None,
        metadata={
            "name": "Company",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_service: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeService",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_people: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumPeople",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    total_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "TotalTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class PhysicalStatus(Enum):
    """
    Specifies the values for the physical status of an interval.
    """

    CLOSED = "closed"
    OPEN = "open"
    PROPOSED = "proposed"


class PitType(Enum):
    """
    Specfies the type of pit.

    :cvar BULK:
    :cvar CHEMICAL:
    :cvar DRILLING:
    :cvar MIX:
    :cvar MUD_CLEANING:
    :cvar SAND_TRAP:
    :cvar SLUG: The pit in the active pit system located immediately
        downstream of the shale shakers, whose primary purpose is to
        allow the settling and disposal of the larger drilled cuttings
        not removed by the shale shakers. It is also called a settling
        tank".
    :cvar STORAGE:
    :cvar SURGE_TANK:
    :cvar TRIP_TANK:
    """

    BULK = "bulk"
    CHEMICAL = "chemical"
    DRILLING = "drilling"
    MIX = "mix"
    MUD_CLEANING = "mud cleaning"
    SAND_TRAP = "sand trap"
    SLUG = "slug"
    STORAGE = "storage"
    SURGE_TANK = "surge tank"
    TRIP_TANK = "trip tank"


@dataclass
class PitVolume:
    """
    Pit Volume Component Schema.

    :ivar pit: This is a pointer to the corresponding pit on the rig
        containing the volume being described.
    :ivar dtim: Date and time the information is related to.
    :ivar vol_pit: Volume of fluid in the pit.
    :ivar dens_fluid: Density of fluid in the pit.
    :ivar desc_fluid: Description of the fluid in the pit.
    :ivar vis_funnel: Funnel viscosity (in seconds).
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of PitVolume.
    """

    pit: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_pit: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolPit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    dens_fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "DensFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    desc_fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "DescFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vis_funnel: Optional[str] = field(
        default=None,
        metadata={
            "name": "VisFunnel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class PresTestType(Enum):
    """
    Specifies the types of pressure test(s) conducted during a drilling report
    period.

    :cvar LEAK_OFF_TEST: A leakoff test (LOT) is usually conducted
        immediately after drilling below a new casing shoe. The test
        indicates the strength of the wellbore at the casing seat,
        typically considered one of the weakest points in any interval.
        The data gathered during the LOT is used to prevent lost
        circulations while drilling. During the test, the well is shut
        in and fluid is pumped into the wellbore gradually to increase
        the pressure on the formation.
    :cvar FORMATION_INTEGRITY_TEST: To avoid breaking down the
        formation, many operators perform a formation integrity test
        (FIT) at the casing seat to determine if the wellbore will
        tolerate the maximum mud weight anticipated while drilling the
        interval. If the casing seat holds pressure that is equivalent
        to the prescribed mud density, the test is considered successful
        and drilling resumes.
    """

    LEAK_OFF_TEST = "leak off test"
    FORMATION_INTEGRITY_TEST = "formation integrity test"


class PressureGradientParameterKind(Enum):
    """
    Specifies values for mud log parameters that are measured in units of pressure
    gradient.
    """

    DIRECT_PORE_PRESSURE_GRADIENT_MEASUREMENT = (
        "direct pore pressure gradient measurement"
    )
    FRACTURE_PRESSURE_GRADIENT_ESTIMATE = "fracture pressure gradient estimate"
    KICK_PRESSURE_GRADIENT = "kick pressure gradient"
    LOST_RETURNS = "lost returns"
    OVERBURDEN_GRADIENT = "overburden gradient"
    PORE_PRESSURE_GRADIENT_ESTIMATE = "pore pressure gradient estimate"


class PressureParameterKind(Enum):
    """
    Specifies values for mud log parameters that are measured in units of pressure.
    """

    DIRECT_FRACTURE_PRESSURE_MEASUREMENT = (
        "direct fracture pressure measurement"
    )
    PORE_PRESSURE_ESTIMATE_WHILE_DRILLING = (
        "pore pressure estimate while drilling"
    )


class ProppantAgentKind(Enum):
    """Specifies the type of proppant agent: ceramic, resin, sand, etc."""

    CERAMIC = "ceramic"
    RESIN_COATED_CERAMIC = "resin coated ceramic"
    RESIN_COATED_SAND = "resin coated sand"
    SAND = "sand"


class PumpOpType(Enum):
    """
    Specifies type of well operation being conducted while this pump was in use.
    """

    DRILLING = "drilling"
    REAMING = "reaming"
    CIRCULATING = "circulating"
    SLOW_PUMP = "slow pump"


class PumpType(Enum):
    """
    Specifies the type of pump.

    :cvar CENTRIFUGAL: Centrifugal mud pump.
    :cvar DUPLEX: Duplex mud mump, two cylinders.
    :cvar TRIPLEX: Triplex mud pump, three cylinders.
    """

    CENTRIFUGAL = "centrifugal"
    DUPLEX = "duplex"
    TRIPLEX = "triplex"


class ReadingKind(Enum):
    """
    Specifies if the reading was measured or estimated.

    :cvar MEASURED: The reading was measured.
    :cvar ESTIMATED: The reading was estimated.
    :cvar UNKNOWN: The value is not known. Avoid using this value. All
        reasonable attempts should be made to determine the appropriate
        value. Use of this value may result in rejection in some
        situations.
    """

    MEASURED = "measured"
    ESTIMATED = "estimated"
    UNKNOWN = "unknown"


@dataclass
class ReferenceContainer:
    """
    Information on containing or contained components.

    :ivar string: DownholeString reference.
    :ivar equipment: Equipment reference.
    :ivar accesory_equipment: Reference to the equipment for this
        accessory.
    :ivar comment: Comment or remarks on this container reference.
    :ivar uid: Unique identifier for this instance of
        ReferenceContainer.
    """

    string: Optional[str] = field(
        default=None,
        metadata={
            "name": "String",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    equipment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Equipment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    accesory_equipment: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccesoryEquipment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class RheometerViscosity:
    """
    Viscosity reading of the rheometer.

    :ivar speed: Rotational speed of the rheometer, typically in RPM.
    :ivar viscosity: The raw reading from a rheometer. This could be ,
        but is not necessarily, a viscosity.
    :ivar uid: Unique identifier for this instance of
        RheometerViscosity.
    """

    speed: Optional[str] = field(
        default=None,
        metadata={
            "name": "Speed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    viscosity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Viscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Rig:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class RigUtilization:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class Risk:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class RodConnectionTypes(Enum):
    """
    Specifies the values for the connection type of rod.
    """

    EATING_NIPPLE_CUP = "eating nipple-cup"
    LATCHED = "latched"
    SEATING_NIPPLE_MECHANICAL = "seating nipple-mechanical"
    SLIPFIT_SEALED = "slipfit sealed"
    THREADED = "threaded"
    WELDED = "welded"


@dataclass
class RopStatistics:
    """
    Measurements on minimum, average and maximum rates of penetration (ROP) and the
    channel from which this data was calculated.

    :ivar average: Average rate of penetration through the interval.
    :ivar minimum: Minimum rate of penetration through the interval.
    :ivar maximum: Maximum rate of penetration through the interval.
    :ivar channel: Log channel from which the ROP statistics were
        calculated.
    """

    average: Optional[str] = field(
        default=None,
        metadata={
            "name": "Average",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    minimum: Optional[str] = field(
        default=None,
        metadata={
            "name": "Minimum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    maximum: Optional[str] = field(
        default=None,
        metadata={
            "name": "Maximum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class RpmStatistics:
    """
    Measurement of the average turn rate and the channel from which the data was
    calculated.

    :ivar average: Average bit turn rate through the interval.
    :ivar channel: Log channel from which the turn rate statistics were
        calculated.
    """

    average: Optional[str] = field(
        default=None,
        metadata={
            "name": "Average",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class ScaleType(Enum):
    """
    Specifies the main line scale types.
    """

    LINEAR = "linear"
    LOGARITHMIC = "logarithmic"


class ScrType(Enum):
    """
    Specifies the type of slow circulation rate.

    :cvar STRING_ANNULUS:
    :cvar STRING_KILL_LINE:
    :cvar STRING_CHOKE_LINE:
    :cvar UNKNOWN: The value is not known. Avoid using this value. All
        reasonable attempts should be made to determine the appropriate
        value. Use of this value may result in rejection in some
        situations.
    """

    STRING_ANNULUS = "string annulus"
    STRING_KILL_LINE = "string kill line"
    STRING_CHOKE_LINE = "string choke line"
    UNKNOWN = "unknown"


@dataclass
class ShakerScreen:
    """
    Operations Shaker Screen Component Schema.

    :ivar dtim_start: Date and time that activities started.
    :ivar dtim_end: Date and time activities were completed.
    :ivar num_deck: Deck number the mesh is installed on.
    :ivar mesh_x: Mesh size in the X direction.
    :ivar mesh_y: Mesh size in the Y direction.
    :ivar manufacturer: Pointer to a BusinessAssociate representing the
        manufacturer or supplier of the item.
    :ivar model: Manufacturers designated model.
    :ivar cut_point: Shaker screen cut point, which is the maximum size
        cuttings that will pass through the screen.
    """

    dtim_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_deck: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumDeck",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mesh_x: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeshX",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mesh_y: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeshY",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    model: Optional[str] = field(
        default=None,
        metadata={
            "name": "Model",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cut_point: Optional[str] = field(
        default=None,
        metadata={
            "name": "CutPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class ShowEvaluation:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class ShowEvaluationInterval:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class ShowFluorescence(Enum):
    """
    Specifies the intensity and color of the show.
    """

    FAINT = "faint"
    BRIGHT = "bright"
    NONE = "none"


class ShowLevel(Enum):
    """Specifies another qualifier for the show: blooming or streaming."""

    BLOOMING = "blooming"
    STREAMING = "streaming"


class ShowRating(Enum):
    """
    Specifies the quality of the fluid showing at this interval.
    """

    NONE = "none"
    VERY_POOR = "very poor"
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    VERY_GOOD = "very good"


class ShowSpeed(Enum):
    """Specifies an indication of both the solubility of the oil and the
    permeability of the show.

    The speed can vary from instantaneous to very slow.
    """

    SLOW = "slow"
    MODERATELY_FAST = "moderately fast"
    FAST = "fast"
    INSTANTANEOUS = "instantaneous"
    NONE = "none"


@dataclass
class SourceTrajectoryStation:
    """A reference to a trajectoryStation in a wellbore.

    The trajectoryStation may be defined within the context of another
    wellbore. This value represents a foreign key from one element to
    another.

    :ivar station_reference: A pointer to the trajectoryStation within
        the parent trajectory. StationReference is a special case where
        WITSML only uses a UID for the pointer.The natural identity of a
        station is its physical characteristics (e.g., md).
    :ivar trajectory:
    """

    station_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "StationReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    trajectory: Optional[str] = field(
        default=None,
        metadata={
            "name": "Trajectory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


class StateDetailActivity(Enum):
    """
    Specifies the state of a drilling activity (DrillActivity).

    :cvar INJURY: Personnel injury in connection with drilling and/or
        drilling related operations.
    :cvar OPERATION_FAILED: Operation failed to achieve objective.
    :cvar KICK: Formation fluid invading the wellbore.
    :cvar CIRCULATION_LOSS: Circulation lost to the formation.
    :cvar MUD_LOSS: Circulation impossible due to plugging or failure of
        equipment.
    :cvar STUCK_EQUIPMENT: Equipment got stuck in the hole.
    :cvar EQUIPMENT_FAILURE: Equipment failure occurred.
    :cvar EQUIPMENT_HANG: Operations had to be aborted due to an
        equipment issue
    :cvar SUCCESS: Operation achieved  the objective.
    """

    INJURY = "injury"
    OPERATION_FAILED = "operation failed"
    KICK = "kick"
    CIRCULATION_LOSS = "circulation loss"
    MUD_LOSS = "mud loss"
    STUCK_EQUIPMENT = "stuck equipment"
    EQUIPMENT_FAILURE = "equipment failure"
    EQUIPMENT_HANG = "equipment hang"
    SUCCESS = "success"


class StimAdditiveKind(Enum):
    """
    Specifies the type of stimulation additive added to the fluid used in the stim
    job.
    """

    ACID = "acid"
    ACTIVATOR = "activator"
    BIOCIDE = "biocide"
    BREAKER = "breaker"
    BREAKER_AID = "breaker aid"
    BUFFER = "buffer"
    CLAY_STABILIZER = "clay stabilizer"
    CORROSION_INHIBITOR = "corrosion inhibitor"
    CORROSION_INHIBITOR_AID = "corrosion inhibitor aid"
    CROSSLINKER = "crosslinker"
    DELAYING_AGENT = "delaying agent"
    FIBERS = "fibers"
    FLUID_LOSS_ADDITIVE = "fluid loss additive"
    FOAMER = "foamer"
    FRICTION_REDUCER = "friction reducer"
    GELLING_AGENT = "gelling agent"
    IRON_CONTROL_ADDITIVE = "iron control additive"
    MUTUAL_SOLVENT = "mutual solvent"
    SALT = "salt"
    STABILIZER = "stabilizer"
    SURFACTANT = "surfactant"


@dataclass
class StimEvent:
    """
    Provides a mechanism to capture general events that occurred during a stage of
    a stimulation job.

    :ivar number: Event number.
    :ivar dtim: Date and time of this event.
    :ivar comment: A short description of the event.
    :ivar num_step: Step number. Use it to reference an existing job
        step entry.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of StimEvent.
    """

    number: Optional[str] = field(
        default=None,
        metadata={
            "name": "Number",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_step: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class StimFetTestAnalysisMethod(Enum):
    """
    Specifies the types of stimulation FET analysis methods.
    """

    AVERAGE = "average"
    DELTA_PRESSURE_OVER_G_TIME = "delta pressure over g-time"
    DELTA_PRESSURE_OVER_LINEAR_TIME = "delta pressure over linear time"
    DELTA_PRESSURE_OVER_RADIAL_TIME = "delta pressure over radial time"
    GDK_2_D = "gdk 2-d"
    HORNER = "horner"
    LINEAR = "linear"
    LOG_LOG = "log-log"
    NOLTE = "nolte"
    OTHER = "other"
    PDL_COEFFICIENT = "pdl coefficient"
    PERKINS_AND_KERN_2_D = "perkins and kern 2-d"
    RADIAL_2_D = "radial 2-d"
    SQUARE_ROOT = "square root"
    THIRD_PARTY_SOFTWARE = "third-party software"


class StimFlowPathType(Enum):
    """
    Specifies the type of flow paths used in a stimulation job.

    :cvar ANNULUS: Fluid is conducted through the annulus.
    :cvar CASING: Fluid is conducted through the casing (no tubing
        present).
    :cvar DRILL_PIPE: Fluid is conducted through the drill pipe.
    :cvar OPEN_HOLE: Fluid is conducted through the open hole.
    :cvar TUBING: Fluid is conducted through tubing.
    :cvar TUBING_AND_ANNULUS: Fluid is conducted through tubing and the
        annulus.
    """

    ANNULUS = "annulus"
    CASING = "casing"
    DRILL_PIPE = "drill pipe"
    OPEN_HOLE = "open hole"
    TUBING = "tubing"
    TUBING_AND_ANNULUS = "tubing and annulus"


class StimFluidKind(Enum):
    """
    Specifies the fluid type.

    :cvar ACID_BASED: A fluid in which the primary fluid medium of
        mixing and transport is acidic (substance which reacts with a
        base; aqueous acids have a pH less than 7).
    :cvar GAS: A carrier medium in which gas is the primary medium of
        mixing and transport.
    :cvar OIL_BASED: A fluid in which oil is the primary fluid medium of
        mixing and transport.
    :cvar WATER_BASED:
    """

    ACID_BASED = "acid-based"
    GAS = "gas"
    OIL_BASED = "oil-based"
    WATER_BASED = "water-based"


class StimFluidSubtype(Enum):
    """
    Specifies the secondary qualifier for fluid type, e.g., acid, base, condensate,
    etc.
    """

    ACID = "acid"
    BASE = "base"
    CARBON_DIOXIDE = "carbon dioxide"
    CARBON_DIOXIDE_AND_NITROGEN = "carbon dioxide and nitrogen"
    CARBON_DIOXIDE_AND_WATER = "carbon dioxide and water"
    CONDENSATE = "condensate"
    CROSS_LINKED_GEL = "cross-linked gel"
    CRUDE_OIL = "crude oil"
    DIESEL = "diesel"
    FOAM = "foam"
    FRACTURING_OIL = "fracturing oil"
    FRESH_WATER = "fresh water"
    GELLED_ACID = "gelled acid"
    GELLED_CONDENSATE = "gelled condensate"
    GELLED_CRUDE = "gelled crude"
    GELLED_DIESEL = "gelled diesel"
    GELLED_OIL = "gelled oil"
    GELLED_SALT_WATER = "gelled salt water"
    HOT_CONDENSATE = "hot condensate"
    HOT_FRESH_WATER = "hot fresh water"
    HOT_OIL = "hot oil"
    HOT_SALT_WATER = "hot salt water"
    HYBRID = "hybrid"
    LINEAR_GEL = "linear gel"
    LIQUEFIED_PETROLEUM_GAS = "liquefied petroleum gas"
    NITROGEN = "nitrogen"
    OIL = "oil"
    OTHER = "other"
    PRODUCED_WATER = "produced water"
    SALT_WATER = "salt water"
    SLICK_WATER = "slick water"


@dataclass
class StimIso135035Point:
    """
    A stress, conductivity, permeability, and temperature data point.

    :ivar conductivity: The conductivity under stress.
    :ivar temperature: The temperature at the time measurements were
        taken.
    :ivar permeability: The permeability under stress.
    :ivar stress: The amount of stress applied.
    :ivar uid: Unique identifier for this instance of
        StimISO13503_5Point
    """

    class Meta:
        name = "StimISO13503_5Point"

    conductivity: Optional[str] = field(
        default=None,
        metadata={
            "name": "Conductivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "Temperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    permeability: Optional[str] = field(
        default=None,
        metadata={
            "name": "Permeability",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    stress: Optional[str] = field(
        default=None,
        metadata={
            "name": "Stress",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimJob:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class StimJobDiversionMethod(Enum):
    """
    Specifies the type of diversion used during a stimulation job.
    """

    BALL_SEALER = "ball sealer"
    BANDS = "bands"
    CHEMICAL = "chemical"
    FIBERS = "fibers"
    OTHER = "other"
    PACKER = "packer"
    SOLID_PARTICLE = "solid particle"
    STRADDLE_PACKER = "straddle packer"


@dataclass
class StimJobLogCatalog:
    """
    A group of logs from a stimulation job, one log per stage.
    """

    job_log: List[str] = field(
        default_factory=list,
        metadata={
            "name": "JobLog",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class StimJobStage:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class StimMaterialKind(Enum):
    """
    Specifies the type of stimulation material.
    """

    ADDITIVE = "additive"
    BRINE = "brine"
    CO2 = "CO2"
    GEL = "gel"
    N2 = "N2"
    OTHER = "other"
    PROPPANT_AGENT = "proppant agent"
    WATER = "water"


@dataclass
class StimMaterialQuantity:
    """
    Stimulation material used.

    :ivar density: The density of material used.
    :ivar mass: The mass of material used.  This should be used without
        specifying any of the other material measures (e.g. volume,
        standard volume, etc.).
    :ivar mass_flow_rate: Rate at which mass of material is flowing.
    :ivar std_volume: The standard volume of material used. Standard
        volume is the volume measured under the same conditions. This
        should be used without specifying any of the other material
        measures (e.g., mass, volume, etc.).
    :ivar volume: The volume of material used.  This should be used
        without specifying any of the other material measures (e.g.
        mass, standard volume, etc.).
    :ivar volume_concentration: The volume per volume measure of
        material used.  This should be used without specifying any of
        the other material measures (e.g. mass, density, standard
        volume, etc.).
    :ivar volumetric_flow_rate: Rate at which the volume of material is
        flowing.
    :ivar material: This is a reference to the UID of the StimMaterial
        in the StimJobMaterialCatalog.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        StimMaterialQuantity
    """

    density: Optional[str] = field(
        default=None,
        metadata={
            "name": "Density",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mass: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mass_flow_rate: Optional[str] = field(
        default=None,
        metadata={
            "name": "MassFlowRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    std_volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "StdVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "Volume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    volume_concentration: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolumeConcentration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    volumetric_flow_rate: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolumetricFlowRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    material: Optional[str] = field(
        default=None,
        metadata={
            "name": "Material",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimPerforationCluster:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class StimPressureFlowRate:
    """
    In an injection step test, the injection rate at a particular pressure.

    :ivar pressure: The pressure of the step test.
    :ivar bottomhole_rate: The flow of the fluid at the bottomhole.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        StimPressureFlowRate.
    """

    pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bottomhole_rate: Optional[str] = field(
        default=None,
        metadata={
            "name": "BottomholeRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimPumpFlowBackTestStep:
    """
    In a step-down pump diagnostics test, this object contains all the data for a
    particular step in that test.

    :ivar dtim: Time stamp of the pressure measurement.
    :ivar flowback_volume: Volume of flowback since the start of the
        test.
    :ivar flowback_volume_rate: Flowback rate.
    :ivar number: The number of the step. Identifies the step within the
        step down test.
    :ivar bottomhole_rate: Bottomhole flow rate for the specific step.
    :ivar pres: Surface pressure measured for the specific step.
    :ivar pipe_friction: Calculated pipe friction for the specific step.
    :ivar entry_friction: Calculated entry friction accounting for
        perforation and near wellbore restrictions for the specific
        step.
    :ivar perf_friction: Calculated perforation friction for the
        specific step.
    :ivar near_wellbore_friction: Calculated near-wellbore friction
        loss.
    :ivar surface_rate: Surface rate entering the well for the specific
        step.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        StimPumpFlowBackTestStep.
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowback_volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowbackVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowback_volume_rate: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowbackVolumeRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    number: Optional[str] = field(
        default=None,
        metadata={
            "name": "Number",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    bottomhole_rate: Optional[str] = field(
        default=None,
        metadata={
            "name": "BottomholeRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pipe_friction: Optional[str] = field(
        default=None,
        metadata={
            "name": "PipeFriction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    entry_friction: Optional[str] = field(
        default=None,
        metadata={
            "name": "EntryFriction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perf_friction: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerfFriction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    near_wellbore_friction: Optional[str] = field(
        default=None,
        metadata={
            "name": "NearWellboreFriction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    surface_rate: Optional[str] = field(
        default=None,
        metadata={
            "name": "SurfaceRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimReservoirInterval:
    """
    Description of a reservoir interval.

    :ivar lith_md_interval: Lithology measured depth interval.
    :ivar lith_formation_permeability: Formation permeability, a
        measurement of the ability of a fluid to flow through a rock.
        Commonly measured in milliDarcys (1m2 = 0.000000000000986923
        Darcy).
    :ivar lith_youngs_modulus: Young's modulus (E) is a measure of the
        stiffness of an isotropic elastic material. It is also known as
        the Young modulus, modulus of elasticity, elastic modulus
        (though Young's modulus is actually one  of several elastic
        moduli such as the bulk modulus and the shear modulus) or
        tensile modulus. It is  defined as the ratio of the uniaxial
        stress over the uniaxial strain.
    :ivar lith_pore_pres: Refers to the pressure of fluids held within a
        soil or rock, in gaps between particles’ formation porosity.
    :ivar lith_net_pay_thickness: Net pay is computed. It is the
        thickness of rock that can deliver hydrocarbons to the wellbore
        formation.
    :ivar lith_name: A name for the formation lithology.
    :ivar gross_pay_md_interval: Measured depth of the bottom of the
        formation.
    :ivar gross_pay_thickness: The total thickness of the interval being
        treated, whether or not it is productive.
    :ivar net_pay_thickness: The thickness of the most productive part
        of the interval. Net pay is a subset of the gross.
    :ivar net_pay_pore_pres: The pore pressure of the net pay.
    :ivar net_pay_fluid_compressibility: The volume change of the fluid
        in the net pay when pressure is applied.
    :ivar net_pay_fluid_viscosity: With respect to the net pay, a
        measurement of the internal resistance of a fluid to flow
        against itself. Expressed as the ratio of shear stress to shear
        rate.
    :ivar net_pay_name: The name used for the net pay zone.
    :ivar net_pay_formation_permeability: The permeability of the net
        pay of the formation.
    :ivar lith_poissons_ratio: The ratio of the relative contraction
        strain, or transverse strain (normal to the applied load),
        divided by the relative extension strain, or axial strain (in
        the direction of the applied load).
    :ivar net_pay_formation_porosity: The porosity of the net pay
        formation.
    :ivar formation_permeability: Permeability of the formation.
    :ivar formation_porosity: Porosity of the formation.
    :ivar name_formation: Name of the formation.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        StimReservoirInterval
    """

    lith_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "LithMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lith_formation_permeability: Optional[str] = field(
        default=None,
        metadata={
            "name": "LithFormationPermeability",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lith_youngs_modulus: Optional[str] = field(
        default=None,
        metadata={
            "name": "LithYoungsModulus",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lith_pore_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "LithPorePres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lith_net_pay_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "LithNetPayThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lith_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LithName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gross_pay_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "GrossPayMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gross_pay_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "GrossPayThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    net_pay_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "NetPayThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    net_pay_pore_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "NetPayPorePres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    net_pay_fluid_compressibility: Optional[str] = field(
        default=None,
        metadata={
            "name": "NetPayFluidCompressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    net_pay_fluid_viscosity: Optional[str] = field(
        default=None,
        metadata={
            "name": "NetPayFluidViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    net_pay_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "NetPayName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    net_pay_formation_permeability: Optional[str] = field(
        default=None,
        metadata={
            "name": "NetPayFormationPermeability",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lith_poissons_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "LithPoissonsRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    net_pay_formation_porosity: Optional[str] = field(
        default=None,
        metadata={
            "name": "NetPayFormationPorosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    formation_permeability: Optional[str] = field(
        default=None,
        metadata={
            "name": "FormationPermeability",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    formation_porosity: Optional[str] = field(
        default=None,
        metadata={
            "name": "FormationPorosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name_formation: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameFormation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimShutInPressure:
    """
    A pressure measurement taken at a certain time after the well has been shut in.

    :ivar pressure: The shut-in pressure.
    :ivar time_after_shutin: The time span after shut in at which the
        pressure was measured.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        StimShutInPressure.
    """

    pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    time_after_shutin: Optional[str] = field(
        default=None,
        metadata={
            "name": "TimeAfterShutin",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimTubular:
    """
    In a production enhancement job, this item constitutes the data for a tubular
    in the hole.

    :ivar type_value: The type of tubular (e.g., casing, tubing, liner,
        packer, open hole, other).
    :ivar id: The inside diameter of the tubular used.
    :ivar od: The outside diameter of the tubular used.
    :ivar weight: The weight per length of the tubular.
    :ivar tubular_md_interval: Measured depth interval over which the
        tubular was used.
    :ivar tubular_tvd_interval: True vertical depth interval over which
        the tubular was used.
    :ivar volume_factor: The volume per length of the tubular.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of StimTubular.
    """

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od: Optional[str] = field(
        default=None,
        metadata={
            "name": "Od",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    weight: Optional[str] = field(
        default=None,
        metadata={
            "name": "Weight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "TubularMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "TubularTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    volume_factor: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolumeFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StnTrajCorUsed:
    """
    Captures information about corrections applied to a trajectory station.

    :ivar grav_axial_accel_cor: Calculated gravitational field strength
        correction.
    :ivar grav_tran1_accel_cor: The correction applied to a cross-axial
        (direction 1) component of the Earth's gravitational field.
    :ivar grav_tran2_accel_cor: The correction applied to a cross-axial
        (direction 2) component of the Earth's gravitational field.
    :ivar mag_axial_drlstr_cor: Axial magnetic drill string correction.
    :ivar mag_tran1_drlstr_cor: Cross-axial (direction 1) magnetic
        correction.
    :ivar mag_tran2_drlstr_cor: Cross-axial (direction 2) magnetic
        correction.
    :ivar mag_tran1_msacor: Cross-axial (direction 1) magnetic
        correction due to a multi-station analysis process.
    :ivar mag_tran2_msacor: Cross-axial (direction 2) magnetic
        correction due to a multi-station analysis process.
    :ivar mag_axial_msacor: Axial magnetic correction due to a multi-
        station analysis process.
    :ivar sag_inc_cor: Calculated sag correction to the inclination.
    :ivar sag_azi_cor: Calculated cosag correction to the azimuth.
    :ivar stn_mag_decl_used: Magnetic declination used to correct a
        Magnetic North referenced azimuth to a True North azimuth.
        Magnetic declination angles are measured positive clockwise from
        True North to Magnetic North (or negative in the anti-clockwise
        direction). To convert a Magnetic azimuth to a True North
        azimuth, the magnetic declination should be added.
    :ivar stn_grid_con_used: The angle  used to correct a true north
        referenced azimuth to a grid north azimuth. WITSML follows the
        Gauss-Bomford convention in which convergence angles are
        measured positive clockwise from true north to grid north (or
        negative in the anti-clockwise direction). To convert a true
        north referenced azimuth to a grid north azimuth, the
        convergence angle must be subtracted from true north. If this
        value is not provided, then GridConUsed applies to all grid-
        north referenced stations.
    :ivar stn_grid_scale_factor_used: A multiplier to change geodetic
        distances based on the Earth model (ellipsoid) to distances on
        the grid plane. This is the number which was already used to
        correct lateral distances. Provide it only if it is used in your
        trajectory stations. If StnGridScaleFactorUsed is not provided,
        then the value in the parent Trajectory applies to all
        trajectory stations. The grid scale factor applies to the
        DispEw, DispNs and Closure elements on trajectory stations.
    :ivar dir_sensor_offset: Offset relative to the bit.
    """

    grav_axial_accel_cor: Optional[str] = field(
        default=None,
        metadata={
            "name": "GravAxialAccelCor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    grav_tran1_accel_cor: Optional[str] = field(
        default=None,
        metadata={
            "name": "GravTran1AccelCor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    grav_tran2_accel_cor: Optional[str] = field(
        default=None,
        metadata={
            "name": "GravTran2AccelCor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mag_axial_drlstr_cor: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagAxialDrlstrCor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mag_tran1_drlstr_cor: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagTran1DrlstrCor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mag_tran2_drlstr_cor: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagTran2DrlstrCor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mag_tran1_msacor: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagTran1MSACor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mag_tran2_msacor: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagTran2MSACor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mag_axial_msacor: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagAxialMSACor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sag_inc_cor: Optional[str] = field(
        default=None,
        metadata={
            "name": "SagIncCor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sag_azi_cor: Optional[str] = field(
        default=None,
        metadata={
            "name": "SagAziCor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    stn_mag_decl_used: Optional[str] = field(
        default=None,
        metadata={
            "name": "StnMagDeclUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    stn_grid_con_used: Optional[str] = field(
        default=None,
        metadata={
            "name": "StnGridConUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    stn_grid_scale_factor_used: Optional[str] = field(
        default=None,
        metadata={
            "name": "StnGridScaleFactorUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dir_sensor_offset: Optional[str] = field(
        default=None,
        metadata={
            "name": "DirSensorOffset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class StnTrajMatrixCov:
    """
    Captures validation information for a covariance matrix.

    :ivar variance_nn: Covariance north north.
    :ivar variance_ne: Crossvariance north east.
    :ivar variance_nvert: Crossvariance north vertical.
    :ivar variance_ee: Covariance east east.
    :ivar variance_evert: Crossvariance east vertical.
    :ivar variance_vert_vert: Covariance vertical vertical.
    :ivar bias_n: Bias north.
    :ivar bias_e: Bias east.
    :ivar bias_vert: Bias vertical. The coordinate system is set up in a
        right-handed configuration, which makes the vertical direction
        increasing (i.e., positive) downwards.
    :ivar sigma: The sigma which is appropriate for all the other values
        in this class.
    """

    variance_nn: Optional[str] = field(
        default=None,
        metadata={
            "name": "VarianceNN",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    variance_ne: Optional[str] = field(
        default=None,
        metadata={
            "name": "VarianceNE",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    variance_nvert: Optional[str] = field(
        default=None,
        metadata={
            "name": "VarianceNVert",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    variance_ee: Optional[str] = field(
        default=None,
        metadata={
            "name": "VarianceEE",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    variance_evert: Optional[str] = field(
        default=None,
        metadata={
            "name": "VarianceEVert",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    variance_vert_vert: Optional[str] = field(
        default=None,
        metadata={
            "name": "VarianceVertVert",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    bias_n: Optional[str] = field(
        default=None,
        metadata={
            "name": "BiasN",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    bias_e: Optional[str] = field(
        default=None,
        metadata={
            "name": "BiasE",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    bias_vert: Optional[str] = field(
        default=None,
        metadata={
            "name": "BiasVert",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    sigma: Optional[float] = field(
        default=None,
        metadata={
            "name": "Sigma",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class StnTrajRawData:
    """
    Captures raw data for a trajectory station.

    :ivar grav_axial_raw: Uncorrected gravitational field strength
        measured in the axial direction.
    :ivar grav_tran1_raw: Uncorrected gravitational field strength
        measured in the transverse direction.
    :ivar grav_tran2_raw: Uncorrected gravitational field strength
        measured in the transverse direction, approximately normal to
        tran1.
    :ivar mag_axial_raw: Uncorrected magnetic field strength measured in
        the axial direction.
    :ivar mag_tran1_raw: Uncorrected magnetic field strength measured in
        the transverse direction.
    :ivar mag_tran2_raw: Uncorrected magnetic field strength measured in
        the transverse direction, approximately normal to tran1.
    """

    grav_axial_raw: Optional[str] = field(
        default=None,
        metadata={
            "name": "GravAxialRaw",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    grav_tran1_raw: Optional[str] = field(
        default=None,
        metadata={
            "name": "GravTran1Raw",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    grav_tran2_raw: Optional[str] = field(
        default=None,
        metadata={
            "name": "GravTran2Raw",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mag_axial_raw: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagAxialRaw",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mag_tran1_raw: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagTran1Raw",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mag_tran2_raw: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagTran2Raw",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class StnTrajValid:
    """
    Captures validation information for a survey.

    :ivar mag_total_field_calc: Calculated total intensity of the
        geomagnetic field as sum of BGGM, IFR and local field.
    :ivar mag_dip_angle_calc: Calculated magnetic dip (inclination), the
        angle between the horizontal and the geomagnetic field (positive
        down, res .001).
    :ivar grav_total_field_calc: Calculated total gravitational field.
    """

    mag_total_field_calc: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagTotalFieldCalc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mag_dip_angle_calc: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagDipAngleCalc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    grav_total_field_calc: Optional[str] = field(
        default=None,
        metadata={
            "name": "GravTotalFieldCalc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class SubStringType(Enum):
    """
    Specifies the values  to further qualify a string type.
    """

    ABANDONED_JUNK_FISH = "abandoned junk/fish"
    CAPILLARY_STRING_INSIDE_TUBING = "capillary string (inside tubing)"
    CAPILLARY_STRING_TUBING_CASING_ANNULUS = (
        "capillary string (tubing/casing annulus)"
    )
    CONDUCTOR_CASING = "conductor casing"
    DRILL_STRING = "drill string"
    FLOWLINE = "flowline"
    GEOLOGICAL_OBJECTS = "geological objects"
    INNER_LINER = "inner liner"
    INTERMEDIATE_CASING = "intermediate casing"
    PRODUCTION_CASING = "production casing"
    PRODUCTION_LINER = "production liner"
    PROTECTIVE_CASING = "protective casing"
    SURFACE_CASING = "surface casing"
    WELLBORE_NOTES = "wellbore notes"
    Y_TOOL_STRING = "y-tool string"


class SupportCraftType(Enum):
    """
    Specifies the type of support craft.
    """

    BARGE = "barge"
    STANDBY_BOAT = "standby boat"
    HELICOPTER = "helicopter"
    SUPPLY_BOAT = "supply boat"
    TRUCK = "truck"
    CREW_VEHICLE = "crew vehicle"
    TUG_BOAT = "tug boat"


class SurfEquipType(Enum):
    """
    Specifies the type of surface equipment.

    :cvar IADC:
    :cvar CUSTOM:
    :cvar COILED_TUBING:
    :cvar UNKNOWN: The value is not known. Avoid using this value. All
        reasonable attempts should be made to determine the appropriate
        value. Use of this value may result in rejection in some
        situations.
    """

    IADC = "IADC"
    CUSTOM = "custom"
    COILED_TUBING = "coiled tubing"
    UNKNOWN = "unknown"


@dataclass
class SurveyProgram:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class SurveySection:
    """
    Survey Section Component Schema.

    :ivar sequence: Order in which the program sections are or were
        executed.
    :ivar name: Name of the survey program section.
    :ivar md_interval:
    :ivar survey_company: Pointer to a BusinessAssociate representing
        the company who will run or has run the survey tool.
    :ivar name_tool: Name of survey tool used in this section.
    :ivar type_tool: Type of tool used.
    :ivar model_error: Error model used to calculate the ellipses of
        uncertainty.
    :ivar overwrite: Higher index trajectory takes precedence over
        overlapping section of previous trajectory?   Values are "true"
        (or "1") and "false" (or "0"). Normally, this is true.
    :ivar frequency_mx: Maximum allowable depth frequency for survey
        stations for this survey run.
    :ivar item_state: The item state for the data object.
    :ivar comments: Comments and remarks.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier of this instance of SurveySection.
    """

    sequence: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sequence",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    survey_company: Optional[str] = field(
        default=None,
        metadata={
            "name": "SurveyCompany",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    name_tool: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameTool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    type_tool: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeTool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    model_error: Optional[str] = field(
        default=None,
        metadata={
            "name": "ModelError",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    overwrite: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Overwrite",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    frequency_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "FrequencyMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    item_state: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemState",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Target:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class TargetSectionScope(Enum):
    """
    These values represent the type of scope of a section that describes a target.

    :cvar ARC: continuous curve
    :cvar LINE: straight line
    """

    ARC = "arc"
    LINE = "line"


@dataclass
class TimestampedCommentString:
    """
    A timestamped textual description.

    :ivar d_tim: The timestamp of the time-qualified comment.
    """

    d_tim: Optional[str] = field(
        default=None,
        metadata={
            "name": "dTim",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ToolErrorModel:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class ToolErrorModelDictionary:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class TorqueCurrentStatistics:
    """
    Measurement of the  average electric current and the channel from which the
    data was calculated.

    :ivar average: Average electric current through the interval
    :ivar channel: Log channel from which the electric current
        statistics were calculated.
    """

    average: Optional[str] = field(
        default=None,
        metadata={
            "name": "Average",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class TorqueStatistics:
    """
    Measurement of average torque and the channel from which the data was
    calculated.

    :ivar average: Average torque through the interval.
    :ivar channel: Log channel from which the torque statistics were
        calculated.
    """

    average: Optional[str] = field(
        default=None,
        metadata={
            "name": "Average",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class TrajStationType(Enum):
    """
    Specifies the type of directional survey station.

    :cvar AZIMUTH_ON_PLANE: Section terminates at a given azimuth on a
        given plane target; requires target ID.
    :cvar BUILDRATE_TO_DELTA_MD: Section follows a given build rate to a
        specified delta measured depth.
    :cvar BUILDRATE_TO_INCL: Section follows a given build rate to a
        specified inclination.
    :cvar BUILDRATE_TO_MD: Section follows a given build rate to a
        specified measured depth.
    :cvar BUILDRATE_AND_TURNRATE_TO_AZI: Section follows a given build
        rate and turn rate to a specified azimuth.
    :cvar BUILDRATE_AND_TURNRATE_TO_DELTA_MD: Section follows a given
        build rate and turn rate to a specified delta measured depth.
    :cvar BUILDRATE_AND_TURNRATE_TO_INCL: Section follows a given build
        rate and turn rate to a specified inclination.
    :cvar BUILDRATE_AND_TURNRATE_TO_INCL_AND_AZI: Section follows a
        given build rate and turn rate to a specified inclination and
        azimuth.
    :cvar BUILDRATE_AND_TURNRATE_TO_MD: Section follows a given build
        rate and turn rate to a specified measured depth.
    :cvar BUILDRATE_AND_TURNRATE_TO_TVD: Section follows a given build
        rate and turn rate to a specified TVD.
    :cvar BUILDRATE_TVD: Section follows a given build rate to a
        specified TVD.
    :cvar CASING_MD: Measured depth casing point; can also be inserted
        within actual survey stations.
    :cvar CASING_TVD: TVD casing point; can also be inserted within
        actual survey stations.
    :cvar DLS: Section follows a given dogleg severity.
    :cvar DLS_TO_AZI_AND_MD: Section follows a given dogleg severity to
        a specified measured depth and azimuth.
    :cvar DLS_TO_AZI_TVD: Section follows a given dogleg severity until
        a specified TVD and azimuth.
    :cvar DLS_TO_INCL: Section follows a given dogleg severity until a
        specified inclination.
    :cvar DLS_TO_INCL_AND_AZI: Section follows a given dogleg severity
        to a specified inclination and azimuth.
    :cvar DLS_TO_INCL_AND_MD: Section follows a given dogleg severity to
        a specified measured depth and inclination.
    :cvar DLS_TO_INCL_AND_TVD: Section follows a given dogleg severity
        until a specified TVD and inclination.
    :cvar DLS_TO_NS: Section follows a given dogleg severity for a given
        north, south distance.
    :cvar DLS_AND_TOOLFACE_TO_AZI: Section follows a given toolface
        angle and  dogleg severity to a specified azimuth.
    :cvar DLS_AND_TOOLFACE_TO_DELTA_MD: Section follows a given toolface
        angle and dogleg severity to a specified delta measured depth.
    :cvar DLS_AND_TOOLFACE_TO_INCL: Section follows a given toolface
        angle and dogleg severity to a specified inclination.
    :cvar DLS_AND_TOOLFACE_TO_INCL_AZI: Section follows a given toolface
        angle and dogleg severity to a specified inclination and
        azimuth.
    :cvar DLS_AND_TOOLFACE_TO_MD: Section follows a given toolface angle
        and dogleg severity to a specified measured depth.
    :cvar DLS_AND_TOOLFACE_TO_TVD: Section follows a given toolface
        angle and dogleg severity to a specified TVD.
    :cvar EXTRAPOLATED: Derived by extrapolating beyond the first or
        last station (either planned or surveyed).
    :cvar FORMATION_MD: Measured depth formation; can be inserted within
        actual survey stations also .
    :cvar FORMATION_TVD: TVD formation; can be inserted within actual
        survey stations also.
    :cvar HOLD_TO_DELTA_MD: Section holds angle and azimuth to a
        specified delta measured depth.
    :cvar HOLD_TO_MD: Section holds angle and azimuth to a specified
        measured depth.
    :cvar HOLD_TO_TVD: Section holds angle and azimuth to a specified
        TVD.
    :cvar INCL_AZI_AND_TVD: Section follows a continuous curve to a
        specified inclination, azimuth and true vertical depth.
    :cvar INTERPOLATED: Derived by interpolating between stations with
        entered values (either planned or surveyed).
    :cvar MARKER_MD: Measured depth marker; can be inserted within
        actual survey stations also.
    :cvar MARKER_TVD: TVD marker; can be inserted within actual survey
        stations also.
    :cvar MD_AND_INCL: An old style drift indicator by Totco /
        inclination-only survey.
    :cvar MD_INCL_AND_AZI: A normal MWD / gyro survey.
    :cvar N_E_AND_TVD: A point on a computed trajectory with northing,
        easting and true vertical depth.
    :cvar NS_EW_AND_TVD: Specified as TVD, NS, EW; could be used for
        point or drilling target (non-geological target).
    :cvar TARGET_CENTER: Specified as TVD, NS, EW of target center;
        requires target ID association.
    :cvar TARGET_OFFSET: Specified as TVD, NS, EW of target offset;
        requires target ID association.
    :cvar TIE_IN_POINT: Tie-in point for the survey.
    :cvar TURNRATE_TO_AZI: Section follows a given turn rate to an
        azimuth.
    :cvar TURNRATE_TO_DELTA_MD: Section follows a given turn rate to a
        given delta measured depth.
    :cvar TURNRATE_TO_MD: Section follows a given turn rate to a given
        measured depth.
    :cvar TURNRATE_TO_TVD: Section follows a given turn rate to a given
        TVD.
    :cvar UNKNOWN: The value is not known. Avoid using this value. All
        reasonable attempts should be made to determine the appropriate
        value. Use of this value may result in rejection in some
        situations.
    """

    AZIMUTH_ON_PLANE = "azimuth on plane"
    BUILDRATE_TO_DELTA_MD = "buildrate to delta-MD"
    BUILDRATE_TO_INCL = "buildrate to INCL"
    BUILDRATE_TO_MD = "buildrate to MD"
    BUILDRATE_AND_TURNRATE_TO_AZI = "buildrate and turnrate to AZI"
    BUILDRATE_AND_TURNRATE_TO_DELTA_MD = "buildrate and turnrate to delta-MD"
    BUILDRATE_AND_TURNRATE_TO_INCL = "buildrate and turnrate to INCL"
    BUILDRATE_AND_TURNRATE_TO_INCL_AND_AZI = (
        "buildrate and turnrate to INCL and AZI"
    )
    BUILDRATE_AND_TURNRATE_TO_MD = "buildrate and turnrate to MD"
    BUILDRATE_AND_TURNRATE_TO_TVD = "buildrate and turnrate to TVD"
    BUILDRATE_TVD = "buildrate TVD"
    CASING_MD = "casing MD"
    CASING_TVD = "casing TVD"
    DLS = "DLS"
    DLS_TO_AZI_AND_MD = "DLS to AZI and MD"
    DLS_TO_AZI_TVD = "DLS to AZI-TVD"
    DLS_TO_INCL = "DLS to INCL"
    DLS_TO_INCL_AND_AZI = "DLS to INCL and AZI"
    DLS_TO_INCL_AND_MD = "DLS to INCL and MD"
    DLS_TO_INCL_AND_TVD = "DLS to INCL and TVD"
    DLS_TO_NS = "DLS to NS"
    DLS_AND_TOOLFACE_TO_AZI = "DLS and toolface to AZI"
    DLS_AND_TOOLFACE_TO_DELTA_MD = "DLS and toolface to delta-MD"
    DLS_AND_TOOLFACE_TO_INCL = "DLS and toolface to INCL"
    DLS_AND_TOOLFACE_TO_INCL_AZI = "DLS and toolface to INCL-AZI"
    DLS_AND_TOOLFACE_TO_MD = "DLS and toolface to MD"
    DLS_AND_TOOLFACE_TO_TVD = "DLS and toolface to TVD"
    EXTRAPOLATED = "extrapolated"
    FORMATION_MD = "formation MD"
    FORMATION_TVD = "formation TVD"
    HOLD_TO_DELTA_MD = "hold to delta-MD"
    HOLD_TO_MD = "hold to MD"
    HOLD_TO_TVD = "hold to TVD"
    INCL_AZI_AND_TVD = "INCL AZI and TVD"
    INTERPOLATED = "interpolated"
    MARKER_MD = "marker MD"
    MARKER_TVD = "marker TVD"
    MD_AND_INCL = "MD and INCL"
    MD_INCL_AND_AZI = "MD INCL and AZI"
    N_E_AND_TVD = "N E and TVD"
    NS_EW_AND_TVD = "NS EW and TVD"
    TARGET_CENTER = "target center"
    TARGET_OFFSET = "target offset"
    TIE_IN_POINT = "tie in point"
    TURNRATE_TO_AZI = "turnrate to AZI"
    TURNRATE_TO_DELTA_MD = "turnrate to delta-MD"
    TURNRATE_TO_MD = "turnrate to MD"
    TURNRATE_TO_TVD = "turnrate to TVD"
    UNKNOWN = "unknown"


class TrajStnCalcAlgorithm(Enum):
    """
    Specifies the trajectory station calculation algorithm.
    """

    AVERAGE_ANGLE = "average angle"
    BALANCED_TANGENTIAL = "balanced tangential"
    CONSTANT_TOOL_FACE = "constant tool face"
    CUSTOM = "custom"
    INERTIAL = "inertial"
    MINIMUM_CURVATURE = "minimum curvature"
    RADIUS_OF_CURVATURE = "radius of curvature"
    TANGENTIAL = "tangential"


@dataclass
class Trajectory:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class TrajectoryOsduintegration:
    """
    Information about a Trajectory that is relevant for OSDU integration but does
    not have a natural place in a Trajectory object.

    :ivar active_indicator: Active Survey Indicator. Distinct from
        ActiveStatus on Trajectory.
    :ivar applied_operation: The audit trail of operations applied to
        the station coordinates from the original state to the current
        state. The list may contain operations applied prior to
        ingestion as well as the operations applied to produce the
        Wgs84Coordinates. The text elements refer to ESRI style CRS and
        Transformation names, which may have to be translated to EPSG
        standard names.
    :ivar intermediary_service_company: Pointer to a BusinessAssociate
        that represents the company who engaged the service company
        (ServiceCompany) to perform the surveying.
    :ivar survey_tool_type: The type of tool or equipment used to
        acquire this Directional Survey.
    :ivar trajectory_version: The version of the wellbore survey
        deliverable received from the service provider - as given by
        this provider. Distinct from objectVersion.
    """

    class Meta:
        name = "TrajectoryOSDUIntegration"

    active_indicator: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ActiveIndicator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    applied_operation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AppliedOperation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    intermediary_service_company: Optional[str] = field(
        default=None,
        metadata={
            "name": "IntermediaryServiceCompany",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    survey_tool_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SurveyToolType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    trajectory_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "TrajectoryVersion",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class TrajectoryStation:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class TrajectoryStationOsduintegration:
    """
    Information about a TrajectoryStation that is relevant for OSDU integration but
    does not have a natural place in a TrajectoryStation object.

    :ivar easting: The easting value of the point in the directional
        survey. Local CRS must be defined.
    :ivar northing: The northing value of the point in the directional
        survey. Local CRS must be defined.
    :ivar radius_of_uncertainty: The radius of uncertainty distance of
        this trajectory station.
    """

    class Meta:
        name = "TrajectoryStationOSDUIntegration"

    easting: Optional[str] = field(
        default=None,
        metadata={
            "name": "Easting",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    northing: Optional[str] = field(
        default=None,
        metadata={
            "name": "Northing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    radius_of_uncertainty: Optional[str] = field(
        default=None,
        metadata={
            "name": "RadiusOfUncertainty",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class TubingConnectionTypes(Enum):
    """
    Specifies the values for the connection types of tubing.
    """

    DOGSCOMPRESSIONFIT_NOTSEALED = "dogscompressionfit-notsealed"
    LANDED = "landed"
    LATCHED = "latched"
    RADIAL = "radial"
    SELFSEALING_THREADED = "selfsealing-threaded"
    SLIPFIT_SEALED = "slipfit-sealed"
    THREADED = "threaded"


@dataclass
class Tubular:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class TubularComponentOsduintegration:
    """
    Information about a TubularComponent that is relevant for OSDU integration but
    does not have a natural place in a TubularComponent.

    :ivar packer_set_depth_tvd: The depth the packer equipment was set
        to seal the casing or tubing.
    :ivar pilot_hole_size: Size of the Pilot Hole.
    :ivar section_type: Identifier of the Section Type.
    :ivar shoe_depth_tvd: Depth of the tubing shoe measured from the
        surface.
    :ivar tubular_component_base_md: The measured depth of the base from
        the specific component.
    :ivar tubular_component_base_reported_tvd: Depth of the base of the
        component measured from the Well-Head.
    :ivar tubular_component_bottom_connection_type: The Bottom
        Connection Type.
    :ivar tubular_component_box_pin_config: Type of collar used to
        couple the tubular with another tubing string.
    :ivar tubular_component_material_type: Specifies the material type
        constituting the component.
    :ivar tubular_component_top_connection_type: The Top Connection
        Type.
    :ivar tubular_component_top_md: The measured depth of the top from
        the specific component.
    :ivar tubular_component_top_reported_tvd: Depth of the top of the
        component measured from the Well-Head.
    """

    class Meta:
        name = "TubularComponentOSDUIntegration"

    packer_set_depth_tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "PackerSetDepthTvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pilot_hole_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "PilotHoleSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    section_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SectionType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    shoe_depth_tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "ShoeDepthTvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_component_base_md: Optional[str] = field(
        default=None,
        metadata={
            "name": "TubularComponentBaseMd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_component_base_reported_tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "TubularComponentBaseReportedTvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_component_bottom_connection_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TubularComponentBottomConnectionType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_component_box_pin_config: Optional[str] = field(
        default=None,
        metadata={
            "name": "TubularComponentBoxPinConfig",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_component_material_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TubularComponentMaterialType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_component_top_connection_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TubularComponentTopConnectionType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_component_top_md: Optional[str] = field(
        default=None,
        metadata={
            "name": "TubularComponentTopMd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_component_top_reported_tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "TubularComponentTopReportedTvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class TubularComponentType(Enum):
    """Specifies the types of components that can be used in a tubular string.

    These are used to specify the type of component and multiple
    components are used to define a tubular string (Tubular).
    """

    ACCELERATOR = "accelerator"
    ADJUSTABLE_KICKOFF = "adjustable kickoff"
    BIT_CORE_DIAMOND = "bit core diamond"
    BIT_CORE_PDC = "bit core PDC"
    BIT_DIAMOND_FIXED_CUT = "bit diamond fixed cut"
    BIT_HOLE_OPENER = "bit hole opener"
    BIT_INSERT_ROLLER_CONE = "bit insert roller cone"
    BIT_MILL_TOOTH_ROLLER_CONE = "bit mill tooth roller cone"
    BIT_PDC_FIXED_CUTTER = "bit PDC fixed cutter"
    BIT_UNDER_REAMER = "bit under reamer"
    BRIDGE_PLUG = "bridge plug"
    BULL_PLUG = "bull plug"
    BULLNOSE = "bullnose"
    CASING = "casing"
    CASING_CROSSOVER = "casing crossover"
    CASING_CUTTER = "casing cutter"
    CASING_HEAD = "casing head"
    CASING_INFLATABLE_PACKER = "casing inflatable packer"
    CASING_SHOE_SCREW_IN = "casing shoe screw-in"
    CATCH_ASSEMBLY = "catch assembly"
    COILED_TUBING_IN_HOLE = "coiled tubing in hole"
    COILED_TUBING_ON_COIL = "coiled tubing on coil"
    CORE_BARREL = "core barrel"
    CORE_ORIENTATION_BARREL = "core orientation barrel"
    DIE_COLLAR = "die collar"
    DIE_COLLAR_LH = "die collar LH"
    DIRECTIONAL_GUIDANCE_SYSTEM = "directional guidance system"
    DRILL_COLLAR = "drill collar"
    DRILL_COLLAR_SHORT = "drill collar short"
    DRILL_PIPE = "drill pipe"
    DRILL_PIPE_COMPRESSIVE = "drill pipe compressive"
    DRILL_PIPE_LH = "drill pipe LH"
    DRILL_STEM_TEST_BHA = "drill stem test BHA"
    DRIVE_PIPE = "drive pipe"
    DUAL_CATCH_ASSEMBLY = "dual catch assembly"
    EXTENSION_BOWL_OVERSHOT = "extension bowl overshot"
    EXTENSION_SUB_OVERSHOT = "extension sub-overshot"
    FLOAT_COLLAR = "float collar"
    FLOAT_SHOE = "float shoe"
    FLOW_HEAD = "flow head"
    GUIDE_SHOE = "guide shoe"
    HANGER_CASING_SUBSEA = "hanger casing subsea"
    HANGER_CASING_SURFACE = "hanger casing surface"
    HANGER_LINER = "hanger liner"
    HANGER_MUD_LINE = "hanger mud line"
    HANGER_TUBING = "hanger tubing"
    HEAVY_WEIGHT_DRILL_PIPE = "heavy weight drill pipe"
    HEAVY_WEIGHT_DRILL_PIPE_LH = "heavy weight drill pipe LH"
    JAR = "jar"
    JUNK_BASKET = "junk basket"
    JUNK_BASKET_REVERSE_CIRCULATION = "junk basket reverse circulation"
    KELLY = "kelly"
    KEYSEAT_WIPER_TOOL = "keyseat wiper tool"
    LANDING_FLOAT_COLLAR = "landing float collar"
    LEAD_IMPRESSION_BLOCK = "lead impression block"
    LINER = "liner"
    LOGGING_WHILE_DRILLING_TOOL = "logging while drilling tool"
    MAGNET = "magnet"
    MILL_CASING_CUTTING = "mill casing cutting"
    MILL_DRESS = "mill dress"
    MILL_FLAT_BOTTOM = "mill flat bottom"
    MILL_HOLLOW = "mill hollow"
    MILL_PACKER_PICKER_ASSEMBLY = "mill packer picker assembly"
    MILL_PILOT = "mill pilot"
    MILL_POLISH = "mill polish"
    MILL_SECTION = "mill section"
    MILL_TAPER = "mill taper"
    MILL_WASHOVER = "mill washover"
    MILL_WATERMELON = "mill watermelon"
    MILLOUT_EXTENSION = "millout extension"
    MOTOR = "motor"
    MOTOR_INSTRUMENTED = "motor instrumented"
    MOTOR_STEERABLE = "motor steerable"
    MULE_SHOE = "mule shoe"
    MULTILATERAL_HANGER_RUNNING_TOOL = "multilateral hanger running tool"
    MWD_HANG_OFF_SUB = "MWD hang off sub"
    MWD_PULSER = "MWD pulser"
    NON_MAGNETIC_COLLAR = "non-magnetic collar"
    NON_MAGNETIC_STABILIZER = "non-magnetic stabilizer"
    OTHER = "other"
    OVERSHOT = "overshot"
    OVERSHOT_LH = "overshot LH"
    OVERSIZE_LIP_GUIDE_OVERSHOT = "oversize lip guide overshot"
    PACKER = "packer"
    PACKER_RETRIEVE_TT_SQUEEZE = "packer retrieve TT squeeze"
    PACKER_RTTS = "packer RTTS"
    PACKER_STORM_VALVE_RTTS = "packer storm valve RTTS"
    PIPE_CUTTER = "pipe cutter"
    POLISHED_BORE_RECEPTACLE = "polished bore receptacle"
    PORTED_STINGER = "ported stinger"
    PREPACKED_SCREENS = "prepacked screens"
    REAMER = "reamer"
    REVERSING_TOOL = "reversing tool"
    RISER_HIGH_PRESSURE = "riser high pressure"
    RISER_MARINE = "riser marine"
    RISER_PRODUCTION = "riser production"
    ROTARY_STEERING_TOOL = "rotary steering tool"
    RUNNING_TOOL = "running tool"
    SAFETY_JOINT = "safety joint"
    SAFETY_JOINT_LH = "safety joint LH"
    SCAB_LINER_BIT_GUIDE = "scab liner bit guide"
    SCRAPER = "scraper"
    SCRATCHERS = "scratchers"
    SLOTTED_LINER = "slotted liner"
    SPEAR = "spear"
    STABILIZER = "stabilizer"
    STABILIZER_INLINE = "stabilizer inline"
    STABILIZER_NEAR_BIT = "stabilizer near bit"
    STABILIZER_NEAR_BIT_ROLLER_REAMER = "stabilizer near bit roller reamer"
    STABILIZER_NON_ROTATING = "stabilizer non-rotating"
    STABILIZER_STEERABLE = "stabilizer steerable"
    STABILIZER_STRING = "stabilizer string"
    STABILIZER_STRING_ROLLER_REAMER = "stabilizer string roller reamer"
    STABILIZER_TURBO_BACK = "stabilizer turbo back"
    STABILIZER_VARIABLE_BLADE = "stabilizer variable blade"
    STAGE_CEMENT_COLLAR = "stage cement collar"
    SUB_BAR_CATCHER = "sub-bar catcher"
    SUB_BENT = "sub-bent"
    SUB_BIT = "sub-bit"
    SUB_BUMPER = "sub-bumper"
    SUB_CATCHER = "sub-catcher"
    SUB_CIRCULATION = "sub-circulation"
    SUB_CONE = "sub-cone"
    SUB_CROSSOVER = "sub-crossover"
    SUB_DART = "sub-dart"
    SUB_FILTER = "sub-filter"
    SUB_FLOAT = "sub-float"
    SUB_JETTING = "sub-jetting"
    SUB_JUNK = "sub-junk"
    SUB_ORIENTING = "sub-orienting"
    SUB_PORTED = "sub-ported"
    SUB_PRESSURE_RELIEF = "sub-pressure relief"
    SUB_PUMP_OUT = "sub-pump out"
    SUB_RESTRICTOR = "sub-restrictor"
    SUB_SAVER = "sub-saver"
    SUB_SHOCK = "sub-shock"
    SUB_SIDE_ENTRY = "sub-side entry"
    SUB_STOP = "sub-stop"
    SURFACE_PIPE = "surface pipe"
    TAPER_TAP = "taper tap"
    TAPER_TAP_LH = "taper tap LH"
    THRUSTER = "thruster"
    TIEBACK_POLISHED_BORE_RECEPTACLE = "tieback polished bore receptacle"
    TIEBACK_STINGER = "tieback stinger"
    TUBING = "tubing"
    TUBING_CONVEYED_PERFORATING_GUN = "tubing-conveyed perforating gun"
    TURBINE = "turbine"
    UNKNOWN = "unknown"
    WASHOVER_PIPE = "washover pipe"
    WHIPSTOCK = "whipstock"
    WHIPSTOCK_ANCHOR = "whipstock anchor"


@dataclass
class TubularUmbilicalCut:
    """
    Information about a cut in a TubularUmbilical.

    :ivar cut_date: The date the cut happened.
    :ivar cut_md: Measured Depth at which the cut has happened.
    :ivar is_accidental: Flag indicating whether the cut is accidental
        or not.
    """

    cut_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "CutDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cut_md: Optional[str] = field(
        default=None,
        metadata={
            "name": "CutMd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_accidental: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAccidental",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class TubularUmbilicalOsduintegration:
    """
    Information about a TubularUmbilical that is relevant for OSDU integration but
    does not have a natural place in a TubularUmbilical.

    :ivar wellhead_outlet_key: The Wellhead Outlet the Umbilical is
        connected to.
    """

    class Meta:
        name = "TubularUmbilicalOSDUIntegration"

    wellhead_outlet_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellheadOutletKey",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


class TypeSurveyTool(Enum):
    """
    Specifies values for the type of directional survey tool; a very generic
    classification.
    """

    GYROSCOPIC_INERTIAL = "gyroscopic inertial"
    GYROSCOPIC_MWD = "gyroscopic MWD"
    GYROSCOPIC_NORTH_SEEKING = "gyroscopic north seeking"
    MAGNETIC_MULTIPLE_SHOT = "magnetic multiple-shot"
    MAGNETIC_MWD = "magnetic MWD"
    MAGNETIC_SINGLE_SHOT = "magnetic single-shot"


@dataclass
class Weather:
    """
    Operations Weather Component Schema.

    :ivar dtim: Date and time the information is related to.
    :ivar agency: Pointer to a BusinessAssociate representing the
        company that supplied the weather data.
    :ivar barometric_pressure: Atmospheric pressure.
    :ivar beaufort_scale_number: The Beaufort wind force scale is a
        system used to estimate and report wind speeds when no measuring
        apparatus is available. It was invented in the early 19th
        century by Admiral Sir Francis Beaufort of the British Navy as a
        way to interpret winds from conditions. Values range from 0
        (calm) to 12 (hurricane force).
    :ivar temp_surface_mn: Minimum temperature above ground. Temperature
        of the atmosphere.
    :ivar temp_surface_mx: Maximum temperature above ground.
    :ivar temp_wind_chill: A measure of the combined chilling effect of
        wind and low temperature on living things, also named chill
        factor, e.g., according to the US weather service table, an air
        temperature of 30 degF with a 10 mph corresponds to a windchill
        of 22 degF.
    :ivar tempsea: Sea temperature.
    :ivar visibility: Horizontal visibility.
    :ivar azi_wave: The direction from which the waves are coming,
        measured from true north.
    :ivar ht_wave: Average height of the waves.
    :ivar significant_wave: An average of the higher 1/3 of the wave
        heights passing during a  sample period (typically 20 to 30
        minutes).
    :ivar max_wave: The maximum wave height.
    :ivar period_wave: The elapsed time between the passing of two wave
        tops.
    :ivar azi_wind: The direction from which the wind is blowing,
        measured from true north.
    :ivar vel_wind: Wind speed.
    :ivar type_precip: Type of precipitation.
    :ivar amt_precip: Amount of precipitation.
    :ivar cover_cloud: Description of cloud cover.
    :ivar ceiling_cloud: Height of cloud cover.
    :ivar current_sea: The speed of the ocean current.
    :ivar azi_current_sea: Azimuth of current.
    :ivar comments: Comments and remarks.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Weather
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    agency: Optional[str] = field(
        default=None,
        metadata={
            "name": "Agency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    barometric_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "BarometricPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    beaufort_scale_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "BeaufortScaleNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "pattern": r".+",
        },
    )
    temp_surface_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempSurfaceMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_surface_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempSurfaceMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_wind_chill: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempWindChill",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tempsea: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tempsea",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    visibility: Optional[str] = field(
        default=None,
        metadata={
            "name": "Visibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    azi_wave: Optional[str] = field(
        default=None,
        metadata={
            "name": "AziWave",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ht_wave: Optional[str] = field(
        default=None,
        metadata={
            "name": "HtWave",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    significant_wave: Optional[str] = field(
        default=None,
        metadata={
            "name": "SignificantWave",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_wave: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxWave",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    period_wave: Optional[str] = field(
        default=None,
        metadata={
            "name": "PeriodWave",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    azi_wind: Optional[str] = field(
        default=None,
        metadata={
            "name": "AziWind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vel_wind: Optional[str] = field(
        default=None,
        metadata={
            "name": "VelWind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_precip: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypePrecip",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    amt_precip: Optional[str] = field(
        default=None,
        metadata={
            "name": "AmtPrecip",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cover_cloud: Optional[str] = field(
        default=None,
        metadata={
            "name": "CoverCloud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ceiling_cloud: Optional[str] = field(
        default=None,
        metadata={
            "name": "CeilingCloud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    current_sea: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurrentSea",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    azi_current_sea: Optional[str] = field(
        default=None,
        metadata={
            "name": "AziCurrentSea",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class WeightingFunction:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class WeightingFunctionDictionary:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class Well:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class WellCmledger:
    class Meta:
        name = "WellCMLedger"
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class WellCompletion:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class WellControlIncidentType(Enum):
    """
    Specifies the type of a well control incident.

    :cvar SHALLOW_GAS_KICK: Shallow gas is flowing incidentally into a
        well being drilled.
    :cvar WATER_KICK: Water is flowing incidentally into a well being
        drilled.
    :cvar OIL_KICK: Crude oil is flowing incidentally into a well being
        drilled.
    :cvar GAS_KICK: Gas is flowing incidentally into a well being
        drilled.
    """

    SHALLOW_GAS_KICK = "shallow gas kick"
    WATER_KICK = "water kick"
    OIL_KICK = "oil kick"
    GAS_KICK = "gas kick"


class WellKillingProcedureType(Enum):
    """Specifies the type of procedure used to stop (kill) the flow of formation
    fluids into a well.

    A well-killing procedure may be planned or unplanned. The particular
    situation determines what type of procedure is used.

    :cvar DRILLERS_METHOD: Prescribes circulating the kick fluids out of
        the well and then circulating a higher density kill mud into the
        well through a kill line with an adjustable choke.
    :cvar WAIT_AND_WEIGHT: Prescribes circulating heavier kill mud while
        a constant downhole pressure is maintained by pressure relief
        through a choke.
    :cvar BULLHEADING: Prescribes pumping kill-weight fluid down the
        tubing and forcing the wellbore fluids back into the formation
        through the perforations.
    :cvar LUBRICATE_AND_BLEED: Prescribes this process: 1) Pump a volume
        of killing fluid corresponding to half the volume of the well
        tubing into the well. 2) Observe the well for 30 to 60 minutes
        and wait for the tubing head pressure to drop. 3) Pump
        additional killing fluid into the well. 4) When the wellhead
        pressure drops below 200 psi above observed tubing head
        pressure, bleed off gas from the tubing at high rate.
    :cvar FORWARD_CIRCULATION: Prescribes circulating drilling fluid
        down the tubing, through a circulation device (or out the end of
        a workstring/coiled tubing) and up the annulus.
    :cvar REVERSE_CIRCULATION: Prescribes circulating a drilling fluid
        down the completion annulus, workstring annulus, or pipe annulus
        and taking returns up the tubing, workstring, or pipe.
    """

    DRILLERS_METHOD = "drillers method"
    WAIT_AND_WEIGHT = "wait and weight"
    BULLHEADING = "bullheading"
    LUBRICATE_AND_BLEED = "lubricate and bleed"
    FORWARD_CIRCULATION = "forward circulation"
    REVERSE_CIRCULATION = "reverse circulation"


class WellPurpose(Enum):
    """
    Specifies values that represent the classification of a well or wellbore by the
    purpose for which it was initially drilled.

    :cvar APPRAISAL: A well drilled into a formation shown to be
        potentially productive of oil or gas by an earlier well for the
        purpose of obtaining more information about the reservoir. Also
        known as a delineation well.
    :cvar APPRAISAL_CONFIRMATION_APPRAISAL: An appraisal well, generally
        drilled in a location interpreted to be in the reservoir, whose
        purpose is to confirm the interpretation.
    :cvar APPRAISAL_EXPLORATORY_APPRAISAL: An appraisal well, generally
        drilled in an area unknown to be part of the reservoir, whose
        purpose is to determine the extent of the reservoir.
    :cvar EXPLORATION: An exploratory well drilled in an unproved area
        to test for a new field, a new pay, a deeper reservoir, or a
        shallower reservoir. Also known as a wildcat.
    :cvar EXPLORATION_DEEPER_POOL_WILDCAT: An exploratory well drilled
        to search for additional pools of hydrocarbon near known pools
        of hydrocarbon but at deeper stratigraphic levels than known
        pools.
    :cvar EXPLORATION_NEW_FIELD_WILDCAT: An exploratory well drilled to
        search for an occurrence of hydrocarbon at a relatively
        considerable distance outside the limits of known pools of
        hydrocarbon, as those limits were understood at the time.
    :cvar EXPLORATION_NEW_POOL_WILDCAT: An exploratory well drilled to
        search for additional pools of hydrocarbon near and at the same
        stratigraphic level as known pools.
    :cvar EXPLORATION_OUTPOST_WILDCAT: An exploratory well drilled to
        search for additional pools of hydrocarbon or to extend the
        limits of a known pool by searching in the same interval at some
        distance from a known pool.
    :cvar EXPLORATION_SHALLOWER_POOL_WILDCAT: An exploratory well
        drilled to search for additional pools of hydrocarbon near but
        at a shallower stratigraphic levels than known pools.
    :cvar DEVELOPMENT: A well drilled in a zone in an area already
        proved productive.
    :cvar DEVELOPMENT_INFILL_DEVELOPMENT: A development well drilled to
        fill in between established wells, usually as part of a drilling
        program to reduce the spacing between wells to increase
        production.
    :cvar DEVELOPMENT_INJECTOR: A development well drilled with the
        intent of injecting fluids into the reservoir for the purpose of
        improving reservoir production.
    :cvar DEVELOPMENT_PRODUCER: A development well drilled with the
        intent of producing fluids.
    :cvar FLUID_STORAGE: A well drilled for storing fluids - generally
        either hydrocarbons or waste disposal.
    :cvar FLUID_STORAGE_GAS_STORAGE: A well drilled with the intent of
        injecting gas into the reservoir rock as a storage facility.
    :cvar GENERAL_SRVC: A well drilled with the intent of providing a
        general service as opposed to producing or injecting fluids.
        Examples of such services are geologic tests, pressure relief
        (for blowouts), and monitoring and observation.
    :cvar GENERAL_SRVC_BOREHOLE_RE_ACQUISITION: A service well drilled
        to intersect another well below the surface for the purpose of
        extending the life of a well whose surface borehole has been
        lost or damaged.
    :cvar GENERAL_SRVC_OBSERVATION: A service well drilled for the
        purpose of monitoring fluids in a reservoir, or observing some
        other subsurface phenomena. Also called a monitor well.
    :cvar GENERAL_SRVC_RELIEF: A service well drilled with the specific
        purpose to provide communication at some point below the surface
        to another well that is out of control.
    :cvar GENERAL_SRVC_RESEARCH: A well drilled with the purpose of
        obtaining information on the stratigraphy, on drilling
        practices, for logging tests, or other such purpose. It is not
        expected to find economic reserves of hydrocarbons.
    :cvar GENERAL_SRVC_RESEARCH_DRILL_TEST: A research well drilled to
        test the suitablity of a particular type of equipment or
        drilling practice.
    :cvar GENERAL_SRVC_RESEARCH_STRAT_TEST: A research well drilled for
        the purpose of gathering geologic information on the
        stratigraphy of an area. A C.O.S.T. well would be included in
        this category.
    :cvar GENERAL_SRVC_WASTE_DISPOSAL: A service well drilled for the
        purpose of injection of sewage, industrial waste, or other waste
        fluids into the subsurface for disposal.
    :cvar MINERAL: A non-oil and gas well drilled for the purpose of
        locating and/or extracting a mineral from the subsurface,
        usually through the injection and/or extraction of mineral-
        bearing fluids.
    """

    APPRAISAL = "appraisal"
    APPRAISAL_CONFIRMATION_APPRAISAL = "appraisal -- confirmation appraisal"
    APPRAISAL_EXPLORATORY_APPRAISAL = "appraisal -- exploratory appraisal"
    EXPLORATION = "exploration"
    EXPLORATION_DEEPER_POOL_WILDCAT = "exploration -- deeper-pool wildcat"
    EXPLORATION_NEW_FIELD_WILDCAT = "exploration -- new-field wildcat"
    EXPLORATION_NEW_POOL_WILDCAT = "exploration -- new-pool wildcat"
    EXPLORATION_OUTPOST_WILDCAT = "exploration -- outpost wildcat"
    EXPLORATION_SHALLOWER_POOL_WILDCAT = (
        "exploration -- shallower-pool wildcat"
    )
    DEVELOPMENT = "development"
    DEVELOPMENT_INFILL_DEVELOPMENT = "development -- infill development"
    DEVELOPMENT_INJECTOR = "development -- injector"
    DEVELOPMENT_PRODUCER = "development -- producer"
    FLUID_STORAGE = "fluid storage"
    FLUID_STORAGE_GAS_STORAGE = "fluid storage -- gas storage"
    GENERAL_SRVC = "general srvc"
    GENERAL_SRVC_BOREHOLE_RE_ACQUISITION = (
        "general srvc -- borehole re-acquisition"
    )
    GENERAL_SRVC_OBSERVATION = "general srvc -- observation"
    GENERAL_SRVC_RELIEF = "general srvc -- relief"
    GENERAL_SRVC_RESEARCH = "general srvc -- research"
    GENERAL_SRVC_RESEARCH_DRILL_TEST = "general srvc -- research -- drill test"
    GENERAL_SRVC_RESEARCH_STRAT_TEST = "general srvc -- research -- strat test"
    GENERAL_SRVC_WASTE_DISPOSAL = "general srvc -- waste disposal"
    MINERAL = "mineral"


class WellTestType(Enum):
    """
    Specifies the type of well test conducted.

    :cvar DRILL_STEM_TEST: Determines the productive capacity, pressure,
        permeability or extent (or a combination of these) of a
        hydrocarbon reservoir, with the drill string still in the hole.
    :cvar PRODUCTION_TEST: Determines the daily rate of oil, gas, and
        water production from a (potential) reservoir.
    """

    DRILL_STEM_TEST = "drill stem test"
    PRODUCTION_TEST = "production test"


@dataclass
class Wellbore:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class WellboreCompletion:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class WellboreFluidLocation(Enum):
    """
    Specified the location where cement job fluid can be found.
    """

    ANNULUS = "annulus"
    DEADEND = "deadend"
    IN_PIPE = "in pipe"
    RAT_HOLE = "rat hole"


@dataclass
class WellboreGeology:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class WellboreGeometry:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class WellboreGeometrySection:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class WellboreMarker:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


@dataclass
class WellboreMarkerSet:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"


class WellboreType(Enum):
    """
    Specifies the values for the classification of a wellbore with respect to its
    parent well/wellbore.

    :cvar BYPASS: The original wellbore had to be abandoned before its
        final usage. This wellbore is being drilled as a different
        wellbore, but one which has the same target as the one that was
        abandoned.
    :cvar INITIAL: This is the first wellbore that has been drilled, or
        attempted, in a given well.
    :cvar REDRILL: The wellbore is being redrilled.
    :cvar REENTRY: The wellbore is being reentered after a period of
        abandonment.
    :cvar RESPUD: The wellbore is part of an existing regulatory well.
        The original borehole did not reach the target depth. This
        borehole required the well to be respudded (drilled from a
        different surface position).
    :cvar SIDETRACK: The wellbore is a deviation from a given wellbore
        that produces a different borehole from the others, and whose
        bottomhole differs from any previously existing wellbore
        bottomholes.
    """

    BYPASS = "bypass"
    INITIAL = "initial"
    REDRILL = "redrill"
    REENTRY = "reentry"
    RESPUD = "respud"
    SIDETRACK = "sidetrack"


@dataclass
class WobStatistics:
    """
    Measurement of average weight on bit and channel from which the data was
    calculated.

    :ivar average: Average weight on bit through the interval.
    :ivar channel: Log channel from which the WOB statistics were
        calculated.
    """

    average: Optional[str] = field(
        default=None,
        metadata={
            "name": "Average",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class XyAccelerometer:
    cant_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "CantAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    switching: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Switching",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class AcidizeFracExtension(AbstractEventExtension):
    """
    Information on fractionation event.

    :ivar stim_job_id: Reference to a StimJob.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    stim_job_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "StimJobID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class Authorization:
    approval_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "ApprovalAuthority",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    approved_by: Optional[str] = field(
        default=None,
        metadata={
            "name": "ApprovedBy",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    approved_on: Optional[str] = field(
        default=None,
        metadata={
            "name": "ApprovedOn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    checked_by: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckedBy",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    checked_on: Optional[str] = field(
        default=None,
        metadata={
            "name": "CheckedOn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    revision_comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "RevisionComment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    revision_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "RevisionDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    status: Optional[AuthorizationStatus] = field(
        default=None,
        metadata={
            "name": "Status",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class AzimuthFormula:
    formula: Optional[str] = field(
        default=None,
        metadata={
            "name": "Formula",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    parameter: List[Parameter] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class Bhpextension(AbstractEventExtension):
    """
    Information on bottom hole pressure during this event.

    :ivar bhpref_id: Reference to bottom hole pressure
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    class Meta:
        name = "BHPExtension"

    bhpref_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "BHPRefID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class BendAngle(AbstractRotarySteerableTool):
    """
    Used with point-the-bit type of rotary steerable system tools; describes the
    angle of the bit.

    :ivar bend_angle: The angle of the bend.
    """

    bend_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "BendAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class BendOffset(AbstractRotarySteerableTool):
    """
    Used with point-the-bit type of rotary steerable system tools; describes the
    angle of the bit.

    :ivar bend_offset: Offset distance from the bottom connection to the
        bend.
    """

    bend_offset: Optional[str] = field(
        default=None,
        metadata={
            "name": "BendOffset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class BitRecord:
    """Bit Record Component Schema.

    Captures information that describes the bit and problems with the
    bit. Many of the problems are classified using IADC codes that are
    specified as enumerated lists in WITSML.

    :ivar num_bit: Bit number and rerun number, e.g., "4.1" for the
        first rerun of bit 4.
    :ivar dia_bit: Diameter of the drilled hole.
    :ivar dia_pass_thru: Minimum hole or tubing diameter that the bit
        will pass through (for bi-center bits).
    :ivar dia_pilot: Diameter of the pilot bit (for bi-center bits).
    :ivar manufacturer: Pointer to a BusinessAssociate representing the
        manufacturer or supplier of the item.
    :ivar type_bit: Type of bit.
    :ivar code_mfg: The manufacturer's code for the bit.
    :ivar code_iadc: IADC bit code.
    :ivar cond_init_inner: Initial condition of the inner tooth rows
        (inner 2/3 of the bit) (0-8).
    :ivar cond_init_outer: Initial condition of the outer tooth rows
        (outer 1/3 of bit) (0-8).
    :ivar cond_init_dull: Initial dull condition from the IADC bit-wear
        2-character codes.
    :ivar cond_init_location: Initial row and cone numbers for items
        that need location information (e.g., cracked cone, lost cone,
        etc).
    :ivar cond_init_bearing: Initial condition of the bit bearings
        (integer 0-8 or E, F, N or X).
    :ivar cond_init_gauge: Initial condition of the bit gauge in 1/16 of
        an inch. I = in gauge, else the number of 16ths out of gauge.
    :ivar cond_init_other: Other comments on initial bit condition from
        the IADC list (BitDullCode enumerated list).
    :ivar cond_init_reason: Initial reason the bit was pulled from IADC
        codes (BitReasonPulled enumerated list).
    :ivar cond_final_inner: Final condition of the inner tooth rows
        (inner 2/3 of bit) (0-8).
    :ivar cond_final_outer: Final condition of the outer tooth rows
        (outer 1/3 of bit) (0-8).
    :ivar cond_final_dull: Final dull condition from the IADC bit-wear
        2-character codes.
    :ivar cond_final_location: Final conditions for row and cone numbers
        for items that need location information (e.g., cracked cone,
        lost cone, etc).
    :ivar cond_final_bearing: Final condition of the bit bearings
        (integer 0-8 or E, F, N or X).
    :ivar cond_final_gauge: Final condition of the bit gauge in 1/16 of
        a inch. I = in gauge, else number of 16ths out of gauge.
    :ivar cond_final_other: Other final comments on bit condition from
        the IADC list (BitDullCode enumerated list).
    :ivar cond_final_reason: Final reason the bit was pulled from IADC
        codes (BitReasonPulled enumerated list).
    :ivar drive: Bit drive type (motor, rotary table, etc.).
    :ivar bit_class: N = new, U = used.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar cost:
    :ivar uid: Unique identifier for this instance of BitRecord.
    """

    num_bit: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumBit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_bit: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaBit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    dia_pass_thru: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaPassThru",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_pilot: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaPilot",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_bit: Optional[BitType] = field(
        default=None,
        metadata={
            "name": "TypeBit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    code_mfg: Optional[str] = field(
        default=None,
        metadata={
            "name": "CodeMfg",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    code_iadc: Optional[str] = field(
        default=None,
        metadata={
            "name": "CodeIADC",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_init_inner: Optional[IadcIntegerCode] = field(
        default=None,
        metadata={
            "name": "CondInitInner",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_init_outer: Optional[IadcIntegerCode] = field(
        default=None,
        metadata={
            "name": "CondInitOuter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_init_dull: Optional[BitDullCode] = field(
        default=None,
        metadata={
            "name": "CondInitDull",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_init_location: Optional[str] = field(
        default=None,
        metadata={
            "name": "CondInitLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_init_bearing: Optional[IadcBearingWearCode] = field(
        default=None,
        metadata={
            "name": "CondInitBearing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_init_gauge: Optional[str] = field(
        default=None,
        metadata={
            "name": "CondInitGauge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_init_other: Optional[str] = field(
        default=None,
        metadata={
            "name": "CondInitOther",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_init_reason: Optional[BitReasonPulled] = field(
        default=None,
        metadata={
            "name": "CondInitReason",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_final_inner: Optional[IadcIntegerCode] = field(
        default=None,
        metadata={
            "name": "CondFinalInner",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_final_outer: Optional[IadcIntegerCode] = field(
        default=None,
        metadata={
            "name": "CondFinalOuter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_final_dull: Optional[BitDullCode] = field(
        default=None,
        metadata={
            "name": "CondFinalDull",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_final_location: Optional[str] = field(
        default=None,
        metadata={
            "name": "CondFinalLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_final_bearing: Optional[IadcBearingWearCode] = field(
        default=None,
        metadata={
            "name": "CondFinalBearing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_final_gauge: Optional[str] = field(
        default=None,
        metadata={
            "name": "CondFinalGauge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_final_other: Optional[str] = field(
        default=None,
        metadata={
            "name": "CondFinalOther",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cond_final_reason: Optional[BitReasonPulled] = field(
        default=None,
        metadata={
            "name": "CondFinalReason",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    drive: Optional[str] = field(
        default=None,
        metadata={
            "name": "Drive",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bit_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "BitClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cost: Optional[str] = field(
        default=None,
        metadata={
            "name": "Cost",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class BopComponent:
    """
    Blowout Preventer Component Schema.

    :ivar type_bop_comp: Type of ram or preventer.
    :ivar desc_comp: Description of the component.
    :ivar id_pass_thru: Inner diameter that tubulars can pass through.
    :ivar pres_work: Working rating pressure of the component.
    :ivar dia_close_mn: Minimum diameter of the component it will seal.
    :ivar dia_close_mx: Maximum diameter of the component it will seal.
    :ivar nomenclature: Arrangement nomenclature for the blowout
        preventer stack (e.g., S, R, A).
    :ivar is_variable: Is ram bore variable or single size? Defaults to
        false. Values are "true" (or "1") and "false" (or "0").
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of BopComponent
    """

    type_bop_comp: Optional[BopType] = field(
        default=None,
        metadata={
            "name": "TypeBopComp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    desc_comp: Optional[str] = field(
        default=None,
        metadata={
            "name": "DescComp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_pass_thru: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdPassThru",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_work: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresWork",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_close_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaCloseMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_close_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaCloseMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nomenclature: Optional[str] = field(
        default=None,
        metadata={
            "name": "Nomenclature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_variable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsVariable",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class BottomHoleCirculatingTemperature(AbstractBottomHoleTemperature):
    """
    Circulating temperature at the bottom of the hole.
    """


@dataclass
class BottomHoleStaticTemperature(AbstractBottomHoleTemperature):
    """
    Static temperature at the bottom of the hole.

    :ivar etim_static: Elapsed time since circulation stopped.
    """

    etim_static: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimStatic",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class CasingConnectionType(AbstractConnectionType):
    """
    Container element for casing connections or collection of all casing
    connections information.

    :ivar casing_connection_type: Connection of type casing.
    """

    casing_connection_type: Optional[CasingConnectionTypes] = field(
        default=None,
        metadata={
            "name": "CasingConnectionType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class CementExtension(AbstractEventExtension):
    """
    Information on cement job event.

    :ivar cement_job: Reference to a cementJob.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    cement_job: Optional[str] = field(
        default=None,
        metadata={
            "name": "CementJob",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class CleanFillExtension(AbstractEventExtension):
    """
    Information on clean fill event.

    :ivar fill_cleaning_method: method of fill and cleaning
    :ivar tool_size: the size of the tool
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    fill_cleaning_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "FillCleaningMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tool_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "ToolSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class CompletionStatusHistory:
    """
    Information on the collection of Completion StatusHistory.

    :ivar status: Completion status.
    :ivar start_date: The start date of the status.
    :ivar end_date: The end date of the status.
    :ivar perforation_md_interval: Measured depth interval between the
        top and the base of the perforations.
    :ivar comment: Comments or remarks on the status.
    :ivar uid: Unique identifier for this instance of
        CompletionStatusHistory.
    """

    status: Optional[CompletionStatus] = field(
        default=None,
        metadata={
            "name": "Status",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    start_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Connection:
    """Tubular Connection Component Schema.

    Describes dimensions and properties of a connection between
    tubulars.

    :ivar id: Inside diameter of the connection.
    :ivar od: Outside diameter of the body of the item.
    :ivar len: Length of the item.
    :ivar type_thread: Thread type from API RP7G, 5CT.
    :ivar size_thread: Thread size.
    :ivar tens_yield: Yield stress of steel: worn stress.
    :ivar tq_yield: Torque at which yield occurs.
    :ivar position: Where connected.
    :ivar critical_cross_section: For bending stiffness ratio.
    :ivar pres_leak: Leak pressure rating.
    :ivar tq_makeup: Make-up torque.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Connection.
    """

    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od: Optional[str] = field(
        default=None,
        metadata={
            "name": "Od",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len: Optional[str] = field(
        default=None,
        metadata={
            "name": "Len",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_thread: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeThread",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    size_thread: Optional[str] = field(
        default=None,
        metadata={
            "name": "SizeThread",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tens_yield: Optional[str] = field(
        default=None,
        metadata={
            "name": "TensYield",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tq_yield: Optional[str] = field(
        default=None,
        metadata={
            "name": "TqYield",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    position: Optional[ConnectionPosition] = field(
        default=None,
        metadata={
            "name": "Position",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    critical_cross_section: Optional[str] = field(
        default=None,
        metadata={
            "name": "CriticalCrossSection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_leak: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresLeak",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tq_makeup: Optional[str] = field(
        default=None,
        metadata={
            "name": "TqMakeup",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class CustomOperatingRange(AbstractOperatingRange):
    title: Optional[str] = field(
        default=None,
        metadata={
            "name": "Title",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "Uom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class CuttingsIntervalShow:
    """A set of measurements or observations on cuttings samples describing the
    evaluation of a hydrocarbon show based on observation of hydrocarbon staining
    and fluorescence.

    For information on procedures for show evaluation, see the WITSML
    Technical Usage Guide.

    :ivar citation: An ISO 19115 EIP-derived set of metadata attached to
        ensure the traceability of the CuttingsIntervalShow.
    :ivar show_rating: Show Rating.
    :ivar stain_color: Visible stain color.
    :ivar stain_distr: Visible stain distribution.
    :ivar stain_pc: Visible stain (commonly in percent).
    :ivar cut_speed: Cut speed.
    :ivar cut_color: Cut color.
    :ivar cut_strength: Cut strength.
    :ivar cut_form: Cut formulation.
    :ivar cut_level: Cut level (faint, bright, etc.).
    :ivar cut_flor_form: Cut fluorescence form.
    :ivar cut_flor_color: Cut fluorescence color.
    :ivar cut_flor_strength: Cut fluorescence strength.
    :ivar cut_flor_speed: Cut fluorescence speed.
    :ivar cut_flor_level: Cut fluorescence level.
    :ivar nat_flor_color: Natural fluorescence color.
    :ivar nat_flor_pc: Natural fluorescence (commonly in percent).
    :ivar nat_flor_level: Natural fluorescence level.
    :ivar nat_flor_desc: Natural fluorescence description.
    :ivar residue_color: Residue color.
    :ivar impregnated_litho: Impregnated lithology.
    :ivar odor: Description of any hydrocarbon type odors smelled.
    :ivar cutting_fluid: Description of the cutting solvent used to
        treat the cuttings.
    :ivar uid: Unique identifier for this instance of
        CuttingsIntervalShow.
    """

    citation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Citation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    show_rating: Optional[ShowRating] = field(
        default=None,
        metadata={
            "name": "ShowRating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    stain_color: Optional[str] = field(
        default=None,
        metadata={
            "name": "StainColor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    stain_distr: Optional[str] = field(
        default=None,
        metadata={
            "name": "StainDistr",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    stain_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "StainPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cut_speed: Optional[ShowSpeed] = field(
        default=None,
        metadata={
            "name": "CutSpeed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cut_color: Optional[str] = field(
        default=None,
        metadata={
            "name": "CutColor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cut_strength: Optional[str] = field(
        default=None,
        metadata={
            "name": "CutStrength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cut_form: Optional[ShowLevel] = field(
        default=None,
        metadata={
            "name": "CutForm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cut_level: Optional[str] = field(
        default=None,
        metadata={
            "name": "CutLevel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cut_flor_form: Optional[ShowLevel] = field(
        default=None,
        metadata={
            "name": "CutFlorForm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cut_flor_color: Optional[str] = field(
        default=None,
        metadata={
            "name": "CutFlorColor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cut_flor_strength: Optional[str] = field(
        default=None,
        metadata={
            "name": "CutFlorStrength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cut_flor_speed: Optional[ShowSpeed] = field(
        default=None,
        metadata={
            "name": "CutFlorSpeed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cut_flor_level: Optional[ShowFluorescence] = field(
        default=None,
        metadata={
            "name": "CutFlorLevel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nat_flor_color: Optional[str] = field(
        default=None,
        metadata={
            "name": "NatFlorColor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nat_flor_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "NatFlorPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nat_flor_level: Optional[ShowFluorescence] = field(
        default=None,
        metadata={
            "name": "NatFlorLevel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nat_flor_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "NatFlorDesc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    residue_color: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResidueColor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    impregnated_litho: Optional[str] = field(
        default=None,
        metadata={
            "name": "ImpregnatedLitho",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    odor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Odor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cutting_fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "CuttingFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DepthRegCalibrationPoint:
    """A mapping of pixel positions on the log image to rectified or depth-
    registered positions on the log image.

    Specifically, pixels along the depth track are tagged with the
    matching measured depth for that position.

    :ivar index: The index (depth or time) for the calibration point.
        The UOM value must be consistent with the indexType.
    :ivar track: A pointer to the track containing the point.
    :ivar role: The horizontal position on the grid that the calibration
        point represents.
    :ivar curve_name: Facilitates searching for logs based on curve
        type.
    :ivar fraction: An intermediate point from the left edge to the
        right edge. Required when CalibrationPointRole is "fraction";
        otherwise, not allowed otherwise.) Used to extrapolate the
        rectified position of a track boundary that has wandered off the
        edge of the image.
    :ivar comment: Comments about the log section.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar parameter:
    :ivar point:
    :ivar uid: Unique identifier for the calibration point.
    """

    index: Optional[str] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    track: Optional[str] = field(
        default=None,
        metadata={
            "name": "Track",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    role: Optional[CalibrationPointRole] = field(
        default=None,
        metadata={
            "name": "Role",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    curve_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurveName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fraction: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    parameter: List[DepthRegParameter] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    point: Optional[DepthRegPoint] = field(
        default=None,
        metadata={
            "name": "Point",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DepthRegRectangle:
    """Uses 4 corner points (Ul, Ur, Ll, Lr) to define the position (pixel) of a
    rectangular area of an image, using x-y coordinates.

    Most objects point to this object because most are rectangles, and
    use this schema to define each rectangle.

    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar ul: The upper left point of a rectangular region.
    :ivar ur: The upper right point of a rectangular region.
    :ivar ll: The lower left point of a rectangular region.
    :ivar lr: The lower right point of a rectangular region.
    :ivar uid: Unique identifier for the rectangular area.
    """

    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ul: Optional[DepthRegPoint] = field(
        default=None,
        metadata={
            "name": "Ul",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ur: Optional[DepthRegPoint] = field(
        default=None,
        metadata={
            "name": "Ur",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ll: Optional[DepthRegPoint] = field(
        default=None,
        metadata={
            "name": "Ll",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lr: Optional[DepthRegPoint] = field(
        default=None,
        metadata={
            "name": "Lr",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DirectionalSurveyExtension(AbstractEventExtension):
    """
    Information on directional survey event.

    :ivar trajectory: Reference to trajectory
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    trajectory: Optional[str] = field(
        default=None,
        metadata={
            "name": "Trajectory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class DownholeComponentReference:
    """
    Reference to a downhole component identifier.

    :ivar string_equipment: Reference to string equipment
    :ivar perforation_set: Reference to perforation set
    :ivar borehole_string_reference:
    :ivar downhole_string_reference:
    """

    string_equipment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StringEquipment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_set: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PerforationSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    borehole_string_reference: List[BoreholeStringReference] = field(
        default_factory=list,
        metadata={
            "name": "BoreholeStringReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    downhole_string_reference: List[DownholeStringReference] = field(
        default_factory=list,
        metadata={
            "name": "DownholeStringReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class DownholeExtension(AbstractEventExtension):
    """
    Information on downhole related to this event.

    :ivar downhole_component: Reference to downhole component
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    downhole_component: Optional[str] = field(
        default=None,
        metadata={
            "name": "DownholeComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class DrillActivity:
    """
    Operations Activity Component Schema.

    :ivar dtim_start: Date and time that activities started.
    :ivar proprietary_code:
    :ivar dtim_end: Date and time that activities ended.
    :ivar duration: The activity duration (commonly in hours).
    :ivar md: The measured depth to the drilling activity/operation.
    :ivar tvd: True vertical depth to the drilling activity/operation.
    :ivar phase: Phase refers to a large activity classification, e.g.,
        drill surface hole.
    :ivar activity_code: A code used to define rig activity.
    :ivar detail_activity: Custom string to further define an activity.
    :ivar type_activity_class: Classifier (planned, unplanned,
        downtime).
    :ivar activity_md_interval: Measured depth interval over which the
        activity was conducted.
    :ivar activity_tvd_interval: True vertical depth interval over which
        the activity was conducted.
    :ivar bit_md_interval: Range of bit measured depths over which the
        activity occurred.
    :ivar state: Finish, interrupted, failed, etc.
    :ivar state_detail_activity: The outcome of the detailed activity.
    :ivar operator: Pointer to a BusinessAssociate representing the
        operator.
    :ivar optimum: Is the activity optimum.? Values are "true" (or "1")
        and "false" (or "0").
    :ivar productive: Does activity bring closer to objective?  Values
        are "true" (or "1") and "false" (or "0").
    :ivar item_state: The item state for the data object.
    :ivar comments: Comments and remarks.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar bha_run: A pointer to the bhaRun object related to this
        activity
    :ivar tubular:
    :ivar uid: Unique identifier for this instance of DrillActivity.
    """

    dtim_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    proprietary_code: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProprietaryCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    duration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md: Optional[str] = field(
        default=None,
        metadata={
            "name": "Md",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    phase: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phase",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    activity_code: Optional[DrillActivityCode] = field(
        default=None,
        metadata={
            "name": "ActivityCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    detail_activity: Optional[str] = field(
        default=None,
        metadata={
            "name": "DetailActivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_activity_class: Optional[DrillActivityTypeType] = field(
        default=None,
        metadata={
            "name": "TypeActivityClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    activity_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "ActivityMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    activity_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "ActivityTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bit_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "BitMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    state: Optional[str] = field(
        default=None,
        metadata={
            "name": "State",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    state_detail_activity: Optional[StateDetailActivity] = field(
        default=None,
        metadata={
            "name": "StateDetailActivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    operator: Optional[str] = field(
        default=None,
        metadata={
            "name": "Operator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    optimum: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Optimum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    productive: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Productive",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    item_state: Optional[ItemState] = field(
        default=None,
        metadata={
            "name": "ItemState",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bha_run: Optional[str] = field(
        default=None,
        metadata={
            "name": "BhaRun",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tubular",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportControlIncidentInfo:
    """
    Information about a well control incident that occurred during the drill report
    period.

    :ivar dtim: Date and time of the well control incident.
    :ivar md_inflow: The measured depth to the well inflow entry point.
    :ivar tvd_inflow: The true vertical depth to the well inflow entry
        point.
    :ivar phase: Phase is large activity classification, e.g. drill
        surface hole.
    :ivar activity_code: A code used to define rig activity.
    :ivar detail_activity: Custom string to further define an activity.
    :ivar etim_lost: The amount of time lost because of the well control
        incident. Commonly specified in hours.
    :ivar dtim_regained: The date and time at which control of the well
        was regained.
    :ivar dia_bit: The drill bit nominal outside diameter at the time of
        the well control incident.
    :ivar md_bit: The measured depth of the bit at the time of the the
        well control incident.
    :ivar wt_mud: The density of the drilling fluid at the time of the
        well control incident.
    :ivar pore_pressure: The equivalent mud weight value of the pore
        pressure reading.
    :ivar dia_csg_last: Diameter of the last installed casing.
    :ivar md_csg_last: Measured depth of the last casing joint.
    :ivar vol_mud_gained: The gained volume of drilling fluid due to the
        well kick.
    :ivar pres_shut_in_casing: The shut in casing pressure.
    :ivar pres_shut_in_drill: The actual pressure in the drill pipe when
        the rams were closed around it.
    :ivar incident_type: The type of well control incident.
    :ivar killing_type: The type of procedure used to kill the well.
    :ivar formation: The lithological description of the geological
        formation at the incident depth.
    :ivar temp_bottom: The temperature at the bottom of the wellbore.
    :ivar pres_max_choke: The maximum pressure that the choke valve can
        be exposed to.
    :ivar description: A description of the well control incident.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar proprietary_code: A proprietary code used to define rig
        activity. The name of the proprietary system should be defined
        in the namingSystem attribute.
    :ivar uid: Unique identifier for this instance of
        DrillReportControlIncidentInfo.
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_inflow: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdInflow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_inflow: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdInflow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    phase: Optional[str] = field(
        default=None,
        metadata={
            "name": "Phase",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    activity_code: Optional[DrillActivityCode] = field(
        default=None,
        metadata={
            "name": "ActivityCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    detail_activity: Optional[str] = field(
        default=None,
        metadata={
            "name": "DetailActivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_lost: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimLost",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_regained: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimRegained",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_bit: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaBit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_bit: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdBit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wt_mud: Optional[str] = field(
        default=None,
        metadata={
            "name": "WtMud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pore_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "PorePressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    dia_csg_last: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaCsgLast",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_csg_last: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdCsgLast",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_mud_gained: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolMudGained",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_shut_in_casing: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresShutInCasing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_shut_in_drill: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresShutInDrill",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    incident_type: Optional[WellControlIncidentType] = field(
        default=None,
        metadata={
            "name": "IncidentType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    killing_type: Optional[WellKillingProcedureType] = field(
        default=None,
        metadata={
            "name": "KillingType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    formation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Formation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_bottom: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempBottom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_max_choke: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresMaxChoke",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    proprietary_code: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProprietaryCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportCoreInfo:
    """
    General information about a core taken during the drill report period.

    :ivar dtim: Date and time that the core was completed.
    :ivar core_number: Core identification number.
    :ivar cored_md_interval: Cored interval expressed as measured depth.
    :ivar cored_tvd_interval: Cored interval expressed as true vertical
        depth.
    :ivar len_recovered: Length of the core recovered.
    :ivar recover_pc: The relative amount of core recovered.
    :ivar len_barrel: Length of  the core barrel.
    :ivar inner_barrel_type: Core inner barrel type.
    :ivar core_description: General core description.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        DrillReportCoreInfo.
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    core_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CoreNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cored_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "CoredMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cored_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "CoredTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_recovered: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenRecovered",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    recover_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "RecoverPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_barrel: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenBarrel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    inner_barrel_type: Optional[InnerBarrelType] = field(
        default=None,
        metadata={
            "name": "InnerBarrelType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    core_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "CoreDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportGasReadingInfo:
    """
    General information about a gas reading taken during the drill report period.

    :ivar dtim: Date and time of the gas reading.
    :ivar reading_type: Type of gas reading.
    :ivar gas_reading_md_interval: Measured depth interval over which
        the gas reading was conducted.
    :ivar gas_reading_tvd_interval: True vertical depth interval over
        which the gas reading was conducted.
    :ivar gas_high: The highest gas reading.
    :ivar gas_low: The lowest gas reading.
    :ivar meth: Methane (C1) concentration.
    :ivar eth: Ethane (C2) concentration.
    :ivar prop: Propane (C3) concentration.
    :ivar ibut: Iso-butane (iC4) concentration.
    :ivar nbut: Nor-butane (nC4) concentration.
    :ivar ipent: Iso-pentane (iC5) concentration.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        DrillReportGasReadingInfo.
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    reading_type: Optional[GasPeakType] = field(
        default=None,
        metadata={
            "name": "ReadingType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gas_reading_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "GasReadingMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gas_reading_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "GasReadingTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gas_high: Optional[str] = field(
        default=None,
        metadata={
            "name": "GasHigh",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gas_low: Optional[str] = field(
        default=None,
        metadata={
            "name": "GasLow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    meth: Optional[str] = field(
        default=None,
        metadata={
            "name": "Meth",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    eth: Optional[str] = field(
        default=None,
        metadata={
            "name": "Eth",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    prop: Optional[str] = field(
        default=None,
        metadata={
            "name": "Prop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ibut: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ibut",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nbut: Optional[str] = field(
        default=None,
        metadata={
            "name": "Nbut",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ipent: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ipent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportLogInfo:
    """
    General information about a log conducted during the drill report period.

    :ivar dtim: The date and time that the log was completed.
    :ivar run_number: Log run number. For measurement while drilling,
        this should be the bottom hole assembly number.
    :ivar service_company: Pointer to a BusinessAssociate representing
        the contractor who provided the service.
    :ivar logged_md_interval: Measured depth interval from the top to
        the base of the interval logged.
    :ivar logged_tvd_interval: True vertical depth interval from the top
        to the base of the interval logged.
    :ivar tool: A pointer to the logging tool kind for the logging tool.
    :ivar md_temp_tool: Measured depth to the temperature measurement
        tool.
    :ivar tvd_temp_tool: True vertical depth to the temperature
        measurement tool.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar bottom_hole_temperature:
    :ivar uid: Unique identifier for this instance of
        DrillReportLogInfo.
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    run_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RunNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    service_company: Optional[str] = field(
        default=None,
        metadata={
            "name": "ServiceCompany",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    logged_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "LoggedMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    logged_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "LoggedTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tool: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_temp_tool: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdTempTool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_temp_tool: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdTempTool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bottom_hole_temperature: Optional[AbstractBottomHoleTemperature] = field(
        default=None,
        metadata={
            "name": "BottomHoleTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportPorePressure:
    """
    General information about pore pressure related to the drill report period.

    :ivar reading_kind: Indicate if the reading was estimated or
        measured.
    :ivar equivalent_mud_weight: The equivalent mud weight value of the
        pore pressure reading.
    :ivar dtim: Date and time at the reading was recorded.
    :ivar md: Measured depth where the readings were recorded.
    :ivar tvd: True vertical depth where the readings were recorded.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        DrillReportPorePressure.
    """

    reading_kind: Optional[ReadingKind] = field(
        default=None,
        metadata={
            "name": "ReadingKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    equivalent_mud_weight: Optional[str] = field(
        default=None,
        metadata={
            "name": "EquivalentMudWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md: Optional[str] = field(
        default=None,
        metadata={
            "name": "Md",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportStatusInfo:
    """
    General status information for the drill report period.

    :ivar dtim: The date and time for which the well status is reported.
    :ivar md: Wellbore measured depth at the end of the report period.
    :ivar tvd: Wellbore true vertical depth at the end of the report.
    :ivar md_plug_top: The measured plug back depth.
    :ivar dia_hole: Hole nominal inside diameter.
    :ivar md_dia_hole_start: Measured depth to the start of the current
        hole diameter.
    :ivar dia_pilot: Pilot hole nominal inside diameter.
    :ivar md_dia_pilot_plan: The planned measured depth of the pilot
        hole.
    :ivar tvd_dia_pilot_plan: The planned true vertical depth of the
        pilot hole.
    :ivar type_wellbore: Type of wellbore.
    :ivar md_kickoff: Measured depth to the kickoff point of the
        wellbore.
    :ivar tvd_kickoff: True vertical depth to the kickoff point of the
        wellbore.
    :ivar strength_form: The measured formation strength. This should be
        the final measurement before the end of the report period.
    :ivar md_strength_form: The measured depth of the formation strength
        measurement.
    :ivar tvd_strength_form: The true vertical depth of the formation
        strength measurement.
    :ivar dia_csg_last: Diameter of the last casing joint.
    :ivar md_csg_last: Measured depth of the last casing joint.
    :ivar tvd_csg_last: True vertical depth of last casing joint.
    :ivar pres_test_type: The type of pressure test that was run.
    :ivar md_planned: The measured depth planned to be reached.
    :ivar dist_drill: Distance drilled.  This should be measured along
        the centerline of the wellbore.
    :ivar sum24_hr: A summary of the activities performed and the status
        of the ongoing activities.
    :ivar forecast24_hr: A summary of  planned activities for the next
        reporting period.
    :ivar rop_current: Rate of penetration at the end of the reporting
        period.
    :ivar rig_utilization: A pointer to the rig used.
    :ivar etim_start: Time from the start of operations (commonly in
        days).
    :ivar etim_spud: Time since the bit broke ground (commonly in days).
    :ivar etim_loc: Time the rig has been on location (commonly in
        days).
    :ivar etim_drill: Drilling time.
    :ivar rop_av: Average rate of penetration.
    :ivar supervisor: Name of the operator's rig supervisor.
    :ivar engineer: Name of the operator's drilling engineer.
    :ivar geologist: Name of operator's wellsite geologist.
    :ivar etim_drill_rot: Time spent rotary drilling.
    :ivar etim_drill_slid: Time spent slide drilling from the start of
        the bit run.
    :ivar etim_circ: Time spent circulating from the start of the bit
        run.
    :ivar etim_ream: Time spent reaming from the start of the bit run.
    :ivar etim_hold: Time spent with no directional drilling work
        (commonly in hours).
    :ivar etim_steering: Time spent steering the bottomhole assembly
        (commonly in hours).
    :ivar dist_drill_rot: Distance drilled: rotating.
    :ivar dist_drill_slid: Distance drilled: sliding.
    :ivar dist_ream: Distance reamed.
    :ivar dist_hold: Distance covered while holding angle with a
        steerable drilling assembly.
    :ivar dist_steering: Distance covered while actively steering with a
        steerable drilling assembly.
    :ivar num_pob: Total number of personnel on board the rig.
    :ivar num_contract: Number of contractor personnel on the rig.
    :ivar num_operator: Number of operator personnel on the rig.
    :ivar num_service: Number of service company personnel on the rig.
    :ivar num_afe: Authorization for expenditure (AFE) number that this
        cost item applies to.
    :ivar condition_hole: Description of the hole condition.
    :ivar tvd_lot: True vertical depth of a leak off test point.
    :ivar pres_lot_emw: Leak off test equivalent mud weight.
    :ivar pres_kick_tol: Kick tolerance pressure.
    :ivar vol_kick_tol: Kick tolerance volume.
    :ivar maasp: Maximum allowable shut-in casing pressure.
    :ivar tubular: A pointer to the tubular (assembly) used in this
        report period.
    :ivar parent_wellbore: References to the parent wellbore(s). These
        are the wellbore(s) from which the current wellbore (indirectly)
        kickedoff.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar elev_kelly:
    :ivar cost_day:
    :ivar cost_day_mud:
    :ivar uid: Unique identifier for this instance of
        DrillReportStatusInfo.
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md: Optional[str] = field(
        default=None,
        metadata={
            "name": "Md",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_plug_top: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdPlugTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_dia_hole_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdDiaHoleStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_pilot: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaPilot",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_dia_pilot_plan: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdDiaPilotPlan",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_dia_pilot_plan: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdDiaPilotPlan",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_wellbore: Optional[WellboreType] = field(
        default=None,
        metadata={
            "name": "TypeWellbore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_kickoff: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdKickoff",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_kickoff: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdKickoff",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    strength_form: Optional[str] = field(
        default=None,
        metadata={
            "name": "StrengthForm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_strength_form: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdStrengthForm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_strength_form: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdStrengthForm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_csg_last: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaCsgLast",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_csg_last: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdCsgLast",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_csg_last: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdCsgLast",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_test_type: Optional[PresTestType] = field(
        default=None,
        metadata={
            "name": "PresTestType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_planned: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdPlanned",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_drill: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistDrill",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sum24_hr: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sum24Hr",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    forecast24_hr: Optional[str] = field(
        default=None,
        metadata={
            "name": "Forecast24Hr",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rop_current: Optional[str] = field(
        default=None,
        metadata={
            "name": "RopCurrent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rig_utilization: Optional[str] = field(
        default=None,
        metadata={
            "name": "RigUtilization",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_spud: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimSpud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_loc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimLoc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_drill: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimDrill",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rop_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "RopAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    supervisor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Supervisor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    engineer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Engineer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    geologist: Optional[str] = field(
        default=None,
        metadata={
            "name": "Geologist",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_drill_rot: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimDrillRot",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_drill_slid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimDrillSlid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_circ: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimCirc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_ream: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimReam",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_hold: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimHold",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_steering: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimSteering",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_drill_rot: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistDrillRot",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_drill_slid: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistDrillSlid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_ream: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistReam",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_hold: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistHold",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_steering: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistSteering",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_pob: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumPob",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_contract: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumContract",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_operator: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumOperator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_service: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumService",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_afe: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumAFE",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    condition_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConditionHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_lot: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdLot",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_lot_emw: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresLotEmw",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_kick_tol: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresKickTol",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_kick_tol: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolKickTol",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    maasp: Optional[str] = field(
        default=None,
        metadata={
            "name": "Maasp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tubular",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    parent_wellbore: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ParentWellbore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    elev_kelly: Optional[str] = field(
        default=None,
        metadata={
            "name": "ElevKelly",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cost_day: Optional[str] = field(
        default=None,
        metadata={
            "name": "CostDay",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cost_day_mud: Optional[str] = field(
        default=None,
        metadata={
            "name": "CostDayMud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillReportSurveyStationReport:
    """
    Captures information for a report including drill report survey stations.

    :ivar acquisition_remark: Remarks related to acquisition context
        which is not the same as Description, which is a summary of the
        trajectory.
    :ivar mag_decl_used: Magnetic declination used to correct a Magnetic
        North referenced azimuth to a True North azimuth.  Magnetic
        declination angles are measured positive clockwise from True
        North to Magnetic North (or negative in the anti-clockwise
        direction). To convert a Magnetic azimuth to a True North
        azimuth, the magnetic declination should be added. Starting
        value if stations have individual values.
    :ivar md_max_extrapolated: The measured depth to which the survey
        segment was extrapolated.
    :ivar md_max_measured: Measured depth within the wellbore of the
        LAST trajectory station with recorded data. If a trajectory has
        been extrapolated to a deeper depth than the last surveyed
        station then that is MdMaxExtrapolated and not MdMaxMeasured.
    :ivar md_tie_on: Tie-point depth measured along the wellbore from
        the measurement reference datum to the trajectory station -
        where tie point is the place on the originating trajectory where
        the current trajectory intersecst it.
    :ivar nominal_calc_algorithm: The nominal type of algorithm used in
        the position calculation in trajectory stations. Individual
        stations may use different algorithms.
    :ivar nominal_type_survey_tool: The nominal type of tool used for
        the trajectory station measurements. Individual stations may
        have a different tool type.
    :ivar nominal_type_traj_station: The nominal type of survey station
        for the trajectory stations. Individual stations may have a
        different type.
    :ivar trajectory_osduintegration: Information about a Trajectory
        that is relevant for OSDU integration but does not have a
        natural place in a Trajectory object.
    :ivar grid_con_used: The angle  used to correct a true north
        referenced azimuth to a grid north azimuth. WITSML follows the
        Gauss-Bomford convention in which convergence angles are
        measured positive clockwise from true north to grid north (or
        negative in the anti-clockwise direction). To convert a true
        north referenced azimuth to a grid north azimuth, the
        convergence angle must be subtracted from true north. If
        StnGridConUsed is not provided, then this value applies to all
        grid-north referenced stations.
    :ivar grid_scale_factor_used: A multiplier to change geodetic
        distances based on the Earth model (ellipsoid) to distances on
        the grid plane. This is the number which was already used to
        correct lateral distances. Provide it only if it is used in your
        trajectory stations. If StnGridScaleFactorUsed is not provided,
        then this value applies to all trajectory stations. The grid
        scale factor applies to the DispEw, DispNs and Closure elements
        on trajectory stations.
    :ivar azi_vert_sect: Azimuth used for vertical section
        plot/computations.
    :ivar disp_ns_vert_sect_orig: Origin north-south used for vertical
        section plot/computations.
    :ivar disp_ew_vert_sect_orig: Origin east-west used for vertical
        section plot/computations.
    :ivar azi_ref: Specifies the definition of north. While this is
        optional because of legacy data, it is strongly recommended that
        this always be specified.
    :ivar drill_report_survey_station:
    """

    acquisition_remark: Optional[str] = field(
        default=None,
        metadata={
            "name": "AcquisitionRemark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mag_decl_used: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagDeclUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_max_extrapolated: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdMaxExtrapolated",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_max_measured: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdMaxMeasured",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_tie_on: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdTieOn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nominal_calc_algorithm: Optional[Union[TrajStnCalcAlgorithm, str]] = field(
        default=None,
        metadata={
            "name": "NominalCalcAlgorithm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nominal_type_survey_tool: Optional[Union[TypeSurveyTool, str]] = field(
        default=None,
        metadata={
            "name": "NominalTypeSurveyTool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nominal_type_traj_station: Optional[Union[TrajStationType, str]] = field(
        default=None,
        metadata={
            "name": "NominalTypeTrajStation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    trajectory_osduintegration: Optional[TrajectoryOsduintegration] = field(
        default=None,
        metadata={
            "name": "TrajectoryOSDUIntegration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    grid_con_used: Optional[str] = field(
        default=None,
        metadata={
            "name": "GridConUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    grid_scale_factor_used: Optional[str] = field(
        default=None,
        metadata={
            "name": "GridScaleFactorUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    azi_vert_sect: Optional[str] = field(
        default=None,
        metadata={
            "name": "AziVertSect",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    disp_ns_vert_sect_orig: Optional[str] = field(
        default=None,
        metadata={
            "name": "DispNsVertSectOrig",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    disp_ew_vert_sect_orig: Optional[str] = field(
        default=None,
        metadata={
            "name": "DispEwVertSectOrig",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    azi_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "AziRef",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    drill_report_survey_station: List[DrillReportSurveyStation] = field(
        default_factory=list,
        metadata={
            "name": "DrillReportSurveyStation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class DrillReportWellTestInfo:
    """
    General information about a production well test conducted during the drill
    report period.

    :ivar dtim: Date and time that the well test was completed.
    :ivar test_type: The type of well test.
    :ivar test_number: The number of the well test.
    :ivar test_md_interval: Test interval expressed as a measured depth.
    :ivar test_tvd_interval: Test interval expressed as a true vertical
        depth.
    :ivar choke_orifice_size: The diameter of the choke opening.
    :ivar density_oil: The density of the produced oil.
    :ivar density_water: The density of the produced water.
    :ivar density_gas: The density of the produced gas.
    :ivar flow_rate_oil: The maximum rate at which oil was produced.
    :ivar flow_rate_water: The maximum rate at which water was produced.
    :ivar flow_rate_gas: The maximum rate at which gas was produced.
    :ivar pres_shut_in: The final shut-in pressure.
    :ivar pres_flowing: The final flowing pressure.
    :ivar pres_bottom: The final bottomhole pressure.
    :ivar gas_oil_ratio: The ratio of the volume of gas to the volume of
        oil.
    :ivar water_oil_ratio: The relative amount of water per amount of
        oil.
    :ivar chloride: The relative amount of chloride in the produced
        water.
    :ivar carbon_dioxide: The relative amount of CO2 gas.
    :ivar hydrogen_sulfide: The relative amount of H2S gas.
    :ivar vol_oil_total: The total amount of oil produced. This includes
        oil that was disposed of (e.g., burned).
    :ivar vol_gas_total: The total amount of gas produced. This includes
        gas that was disposed of (e.g., burned).
    :ivar vol_water_total: The total amount of water produced. This
        includes water that was disposed of.
    :ivar vol_oil_stored: The total amount of produced oil that was
        stored.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of
        DrillReportWellTestInfo.
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    test_type: Optional[WellTestType] = field(
        default=None,
        metadata={
            "name": "TestType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    test_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    test_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    test_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    choke_orifice_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChokeOrificeSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    density_oil: Optional[str] = field(
        default=None,
        metadata={
            "name": "DensityOil",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    density_water: Optional[str] = field(
        default=None,
        metadata={
            "name": "DensityWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    density_gas: Optional[str] = field(
        default=None,
        metadata={
            "name": "DensityGas",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flow_rate_oil: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowRateOil",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flow_rate_water: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowRateWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flow_rate_gas: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowRateGas",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_shut_in: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresShutIn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_flowing: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresFlowing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_bottom: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresBottom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gas_oil_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "GasOilRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    water_oil_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "WaterOilRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    chloride: Optional[str] = field(
        default=None,
        metadata={
            "name": "Chloride",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    carbon_dioxide: Optional[str] = field(
        default=None,
        metadata={
            "name": "CarbonDioxide",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hydrogen_sulfide: Optional[str] = field(
        default=None,
        metadata={
            "name": "HydrogenSulfide",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_oil_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolOilTotal",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_gas_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolGasTotal",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_water_total: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolWaterTotal",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_oil_stored: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolOilStored",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DrillingParameters:
    """Information regarding drilling: ROP, WOB, torque, etc.

    :ivar rop: Rate of penetration through the interval.
    :ivar average_weight_on_bit: Surface weight on bit: average through
        the interval.
    :ivar average_torque: Average torque through the interval.
    :ivar average_torque_current: Average torque current through the
        interval. This is the raw measurement from which the average
        torque can be calculated.
    :ivar average_turn_rate: Average turn rate through the interval
        (commonly in rpm).
    :ivar average_mud_density: Average mud density through the interval.
    :ivar average_ecd_at_td: Average effective circulating density at TD
        through the interval.
    :ivar average_drilling_coefficient: Average drilling exponent
        through the interval.
    """

    rop: Optional[RopStatistics] = field(
        default=None,
        metadata={
            "name": "Rop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    average_weight_on_bit: Optional[WobStatistics] = field(
        default=None,
        metadata={
            "name": "AverageWeightOnBit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    average_torque: Optional[TorqueStatistics] = field(
        default=None,
        metadata={
            "name": "AverageTorque",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    average_torque_current: Optional[TorqueCurrentStatistics] = field(
        default=None,
        metadata={
            "name": "AverageTorqueCurrent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    average_turn_rate: Optional[RpmStatistics] = field(
        default=None,
        metadata={
            "name": "AverageTurnRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    average_mud_density: Optional[MudDensityStatistics] = field(
        default=None,
        metadata={
            "name": "AverageMudDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    average_ecd_at_td: Optional[EcdStatistics] = field(
        default=None,
        metadata={
            "name": "AverageEcdAtTd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    average_drilling_coefficient: Optional[DxcStatistics] = field(
        default=None,
        metadata={
            "name": "AverageDrillingCoefficient",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class DrillingParams:
    """
    The bottomhole assembly drilling parameters schema, which contains statistical
    and calculated operations data for the run, related to depths, activities,
    temperature, pressure, flow rates, torque, etc.

    :ivar etim_op_bit: Operating time spent by bit for run. BUSINESS
        RULE: When reporting an actual as opposed to design, this is
        required.
    :ivar md_hole_start: Measured depth at start of the run.
    :ivar md_hole_stop: Measured depth at the end of the run.
    :ivar hkld_rot: Hookload: rotating.
    :ivar over_pull: Overpull = HkldUp - HkldRot
    :ivar slack_off: Slackoff = HkldRot  - HkdDown.
    :ivar hkld_up: Hookload when the string is moving up.
    :ivar hkld_dn: Hookload when the string is moving down.
    :ivar tq_on_bot_av: Average Torque: on bottom.
    :ivar tq_on_bot_mx: Maximum torque: on bottom.
    :ivar tq_on_bot_mn: Minimum torque: on bottom.
    :ivar tq_off_bot_av: Average torque: off bottom.
    :ivar tq_dh_av: Average torque: downhole.
    :ivar wt_above_jar: Weight of the string above the jars.
    :ivar wt_below_jar: Weight  of the string below the jars.
    :ivar wt_mud: Drilling fluid density.
    :ivar flowrate_pump_av: Average mud pump flow rate.
    :ivar flowrate_pump_mx: Maximum mud pump flow rate.
    :ivar flowrate_pump_mn: Minimum mud pump flow rate.
    :ivar vel_nozzle_av: Bit nozzle average velocity.
    :ivar pow_bit: Bit hydraulic.
    :ivar pres_drop_bit: Pressure drop in bit.
    :ivar ctim_hold: Time spent on hold from start of bit run.
    :ivar ctim_steering: Time spent steering from start of bit run.
    :ivar ctim_drill_rot: Time spent rotary drilling from start of bit
        run.
    :ivar ctim_drill_slid: Time spent slide drilling from start of bit
        run.
    :ivar ctim_circ: Time spent circulating from start of bit run.
    :ivar ctim_ream: Time spent reaming from start of bit run.
    :ivar dist_drill_rot: Distance drilled - rotating.
    :ivar dist_drill_slid: Distance drilled - sliding
    :ivar dist_ream: Distance reamed.
    :ivar dist_hold: Distance covered while holding angle with a
        steerable drilling assembly.
    :ivar dist_steering: Distance covered while actively steering with a
        steerable drilling assembly.
    :ivar rpm_av: Average turn rate (commonly in rpm) through Interval.
    :ivar rpm_mx: Maximum turn rate (commonly in rpm).
    :ivar rpm_mn: Minimum turn rate (commonly in rpm).
    :ivar rpm_av_dh: Average turn rate (commonly in rpm) downhole.
    :ivar rop_av: Average rate of penetration through Interval.
    :ivar rop_mx: Maximum rate of penetration through Interval.
    :ivar rop_mn: Minimum rate of penetration through Interval.
    :ivar wob_av: Surface weight on bit - average through interval.
    :ivar wob_mx: Weight on bit - maximum.
    :ivar wob_mn: Weight on bit - minimum.
    :ivar wob_av_dh: Weight on bit - average downhole.
    :ivar reason_trip: Reason for trip.
    :ivar objective_bha: Objective of bottom hole assembly.
    :ivar azi_top: Azimuth at start measured depth.
    :ivar azi_bottom: Azimuth at stop measured depth.
    :ivar incl_start: Inclination at start measured depth.
    :ivar incl_mx: Maximum inclination.
    :ivar incl_mn: Minimum inclination.
    :ivar incl_stop: Inclination at stop measured depth.
    :ivar temp_mud_dh_mx: Maximum mud temperature downhole during run.
    :ivar pres_pump_av: Average pump pressure.
    :ivar flowrate_bit: Flow rate at bit.
    :ivar mud_class: The class of the drilling fluid.
    :ivar mud_sub_class: Mud Subtype at event occurrence.
    :ivar comments: Comments and remarks.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar tubular: A pointer to the tubular assembly.
    :ivar uid: Unique identifier for the parameters
    """

    etim_op_bit: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimOpBit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_hole_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdHoleStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_hole_stop: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdHoleStop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    hkld_rot: Optional[str] = field(
        default=None,
        metadata={
            "name": "HkldRot",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    over_pull: Optional[str] = field(
        default=None,
        metadata={
            "name": "OverPull",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    slack_off: Optional[str] = field(
        default=None,
        metadata={
            "name": "SlackOff",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hkld_up: Optional[str] = field(
        default=None,
        metadata={
            "name": "HkldUp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hkld_dn: Optional[str] = field(
        default=None,
        metadata={
            "name": "HkldDn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tq_on_bot_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "TqOnBotAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tq_on_bot_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "TqOnBotMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tq_on_bot_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "TqOnBotMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tq_off_bot_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "TqOffBotAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tq_dh_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "TqDhAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wt_above_jar: Optional[str] = field(
        default=None,
        metadata={
            "name": "WtAboveJar",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wt_below_jar: Optional[str] = field(
        default=None,
        metadata={
            "name": "WtBelowJar",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wt_mud: Optional[str] = field(
        default=None,
        metadata={
            "name": "WtMud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_pump_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowratePumpAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_pump_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowratePumpMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_pump_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowratePumpMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vel_nozzle_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "VelNozzleAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pow_bit: Optional[str] = field(
        default=None,
        metadata={
            "name": "PowBit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_drop_bit: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresDropBit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ctim_hold: Optional[str] = field(
        default=None,
        metadata={
            "name": "CTimHold",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ctim_steering: Optional[str] = field(
        default=None,
        metadata={
            "name": "CTimSteering",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ctim_drill_rot: Optional[str] = field(
        default=None,
        metadata={
            "name": "CTimDrillRot",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ctim_drill_slid: Optional[str] = field(
        default=None,
        metadata={
            "name": "CTimDrillSlid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ctim_circ: Optional[str] = field(
        default=None,
        metadata={
            "name": "CTimCirc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ctim_ream: Optional[str] = field(
        default=None,
        metadata={
            "name": "CTimReam",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_drill_rot: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistDrillRot",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_drill_slid: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistDrillSlid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_ream: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistReam",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_hold: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistHold",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_steering: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistSteering",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rpm_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "RpmAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rpm_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "RpmMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rpm_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "RpmMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rpm_av_dh: Optional[str] = field(
        default=None,
        metadata={
            "name": "RpmAvDh",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rop_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "RopAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rop_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "RopMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rop_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "RopMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wob_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "WobAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wob_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "WobMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wob_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "WobMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wob_av_dh: Optional[str] = field(
        default=None,
        metadata={
            "name": "WobAvDh",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    reason_trip: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReasonTrip",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    objective_bha: Optional[str] = field(
        default=None,
        metadata={
            "name": "ObjectiveBha",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    azi_top: Optional[str] = field(
        default=None,
        metadata={
            "name": "AziTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    azi_bottom: Optional[str] = field(
        default=None,
        metadata={
            "name": "AziBottom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    incl_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "InclStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    incl_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "InclMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    incl_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "InclMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    incl_stop: Optional[str] = field(
        default=None,
        metadata={
            "name": "InclStop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_mud_dh_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempMudDhMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_pump_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresPumpAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_bit: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateBit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mud_class: Optional[MudType] = field(
        default=None,
        metadata={
            "name": "MudClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mud_sub_class: Optional[MudSubType] = field(
        default=None,
        metadata={
            "name": "MudSubClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tubular",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Equipment:
    """Information on a piece of equipment.

    Each kind of equipment in the set has a type (what it is) and
    attributes common across all instances of that type of equipment.
    The String Equipment then references these common attributes.

    :ivar equipment_name: The name of the piece of equipment.
    :ivar equipment_type: The equipment type etc. bridge plug, bull
        plug. capillary tubing.
    :ivar manufacturer: Pointer to a BusinessAssociate representing the
        manufacturer of this equipment.
    :ivar model: The model of the equipment.
    :ivar catalog_id: Catalog where equipment can be found.
    :ivar catalog_name: Name of equipment as found in the catalog.
    :ivar brand_name: The equipment's brand name.
    :ivar model_type: The equipment's model type.
    :ivar series: Series number.
    :ivar is_serialized: A flag that indicates the equipment has a
        serial number.
    :ivar serial_number: Serial number.
    :ivar part_no: Number that identifies this part.
    :ivar surface_condition: Surface condition.
    :ivar material: Material that the equipment is made from.
    :ivar grade: Grade level of this piece of material.
    :ivar unit_weight: The weight per length of this equipment.
    :ivar coating_liner_applied: Flag indicating whether equipment has a
        coating.
    :ivar outside_coating: Equipment's outside coating based on
        enumeration value.
    :ivar inside_coating: Equipment's inner coating based on enumeration
        value.
    :ivar unit_length: The length of this equipment.
    :ivar major_od: The major outside diameter of this equipment.
    :ivar minor_od: The minor outside diameter of this equipment.
    :ivar od: The outside diameter of this equipment.
    :ivar max_od: The maximum outside diameter of this equipment.
    :ivar min_od: The minimum outside diameter of this equipment.
    :ivar major_id: The major inside diameter of this equipment.
    :ivar minor_id: The minor inside diameter of this equipment.
    :ivar id: The inside diameter of this equipment.
    :ivar max_id: The maximum inside diameter of this equipment.
    :ivar min_id: The minimum inside diameter of this equipment.
    :ivar drift: The drift diameter is the minimum inside diameter of
        pipe through which another tool or string can be pulled.
    :ivar nominal_size: The nominal size of this equipment.
    :ivar name_service: Sweet or sour service.
    :ivar description: The description of this equipment.
    :ivar description_permanent: The description of this equipment to be
        permanently kept.
    :ivar remark: Remarks about this equipment property.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar property:
    :ivar slot_as_manufactured:
    :ivar hole_as_manufactured:
    :ivar uid: Unique identifier for this instance of Equipment.
    """

    equipment_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "EquipmentName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    equipment_type: Optional[Union[EquipmentType, str]] = field(
        default=None,
        metadata={
            "name": "EquipmentType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    model: Optional[str] = field(
        default=None,
        metadata={
            "name": "Model",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    catalog_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "CatalogId",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    catalog_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CatalogName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    brand_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "BrandName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    model_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ModelType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    series: Optional[str] = field(
        default=None,
        metadata={
            "name": "Series",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_serialized: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsSerialized",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    part_no: Optional[str] = field(
        default=None,
        metadata={
            "name": "PartNo",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    surface_condition: Optional[str] = field(
        default=None,
        metadata={
            "name": "SurfaceCondition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    material: Optional[str] = field(
        default=None,
        metadata={
            "name": "Material",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    grade: Optional[GradeType] = field(
        default=None,
        metadata={
            "name": "Grade",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    unit_weight: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    coating_liner_applied: Optional[bool] = field(
        default=None,
        metadata={
            "name": "CoatingLinerApplied",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    outside_coating: Optional[Coating] = field(
        default=None,
        metadata={
            "name": "OutsideCoating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    inside_coating: Optional[Coating] = field(
        default=None,
        metadata={
            "name": "InsideCoating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    unit_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    major_od: Optional[str] = field(
        default=None,
        metadata={
            "name": "MajorOd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    minor_od: Optional[str] = field(
        default=None,
        metadata={
            "name": "MinorOd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od: Optional[str] = field(
        default=None,
        metadata={
            "name": "Od",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_od: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxOd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    min_od: Optional[str] = field(
        default=None,
        metadata={
            "name": "MinOd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    major_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "MajorId",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    minor_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "MinorId",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxId",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    min_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "MinId",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    drift: Optional[str] = field(
        default=None,
        metadata={
            "name": "Drift",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nominal_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "NominalSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name_service: Optional[str] = field(
        default=None,
        metadata={
            "name": "NameService",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description_permanent: Optional[str] = field(
        default=None,
        metadata={
            "name": "DescriptionPermanent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    remark: Optional[str] = field(
        default=None,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    property: List[ExtPropNameValue] = field(
        default_factory=list,
        metadata={
            "name": "Property",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    slot_as_manufactured: List[PerfSlot] = field(
        default_factory=list,
        metadata={
            "name": "SlotAsManufactured",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_as_manufactured: List[PerfHole] = field(
        default_factory=list,
        metadata={
            "name": "HoleAsManufactured",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EventInfo:
    """
    Event information type.

    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar begin_event:
    :ivar end_event:
    """

    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    begin_event: Optional[EventRefInfo] = field(
        default=None,
        metadata={
            "name": "BeginEvent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_event: Optional[EventRefInfo] = field(
        default=None,
        metadata={
            "name": "EndEvent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class EventType:
    """
    The type of the referencing event.

    :ivar class_value: The type of the event (job, daily report, etc.)
    """

    class_value: Optional[EventTypeType] = field(
        default=None,
        metadata={
            "name": "Class",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class FluidLocation:
    """
    Location of fluid in the wellbore.

    :ivar fluid: Reference to fluid used in the CementJob.
    :ivar mdfluid_base: Measured depth of the base of the cement.
    :ivar mdfluid_top: Measured depth at the top of the interval.
    :ivar volume: Volume of fluid at this location.
    :ivar location_type:
    :ivar uid: Unique identifier for this instance of FluidLocation.
    """

    fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    mdfluid_base: Optional[str] = field(
        default=None,
        metadata={
            "name": "MDFluidBase",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    mdfluid_top: Optional[str] = field(
        default=None,
        metadata={
            "name": "MDFluidTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "Volume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    location_type: Optional[WellboreFluidLocation] = field(
        default=None,
        metadata={
            "name": "LocationType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class FluidReportExtension(AbstractEventExtension):
    """
    Information on fluid report event.

    :ivar fluids_report: Reference to the fluid report
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    fluids_report: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidsReport",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class GasPeak:
    """
    Readings at maximum gas production.

    :ivar peak_type: Type of gas peak
    :ivar md_peak: Measured depth at which the gas reading was taken.
    :ivar average_gas: Average total gas.
    :ivar peak_gas: Peak gas reading.
    :ivar background_gas: Background gas reading.
    :ivar channel:
    """

    peak_type: Optional[GasPeakType] = field(
        default=None,
        metadata={
            "name": "PeakType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    md_peak: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdPeak",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    average_gas: Optional[str] = field(
        default=None,
        metadata={
            "name": "AverageGas",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    peak_gas: Optional[str] = field(
        default=None,
        metadata={
            "name": "PeakGas",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    background_gas: Optional[str] = field(
        default=None,
        metadata={
            "name": "BackgroundGas",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class GeologyFeature:
    """
    Geology features found in the location of the borehole string.

    :ivar name: Name of the feature.
    :ivar geology_type: Aquifer or reservoir.
    :ivar feature_md_interval: Measured depth interval for this feature.
    :ivar feature_tvd_interval: True vertical depth interval for this
        feature.
    :ivar geologic_unit_interpretation: Reference to a RESQML geologic
        unit interpretation for this feature.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of GeologyFeature.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    geology_type: Optional[GeologyType] = field(
        default=None,
        metadata={
            "name": "GeologyType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    feature_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "FeatureMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    feature_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "FeatureTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    geologic_unit_interpretation: Optional[str] = field(
        default=None,
        metadata={
            "name": "GeologicUnitInterpretation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class HoleOpener:
    """Hole Opener Component Schema.

    Describes the hole-opener tool (often called a ‘reamer’) used on the
    tubular string.

    :ivar type_hole_opener: Under reamer or fixed blade.
    :ivar num_cutter: Number of cutters on the tool.
    :ivar manufacturer: Pointer to a BusinessAssociate representing the
        manufacturer or supplier of the tool.
    :ivar dia_hole_opener: Diameter of the reamer.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    type_hole_opener: Optional[HoleOpenerType] = field(
        default=None,
        metadata={
            "name": "TypeHoleOpener",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_cutter: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumCutter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_hole_opener: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaHoleOpener",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class Hse:
    """Operations Health, Safety and Environment Schema.

    Captures data related to HSE events (e.g., tests, inspections,
    meetings, and drills), test values (e.g., pressure tested to),
    and/or incidents (e.g., discharges, non-compliance notices received,
    etc.).

    :ivar days_inc_free: Incident free duration (commonly in days).
    :ivar last_csg_pres_test: Last casing pressure test date and time.
    :ivar pres_last_csg: Last casing pressure test pressure.
    :ivar last_bop_pres_test: Last blow out preventer pressure test.
    :ivar next_bop_pres_test: Next blow out preventer pressure test.
    :ivar pres_std_pipe: Standpipe manifold pressure tested to.
    :ivar pres_kelly_hose: Kelly hose pressure tested to.
    :ivar pres_diverter: Blow out preventer diverter pressure tested to.
    :ivar pres_annular: Blow out preventer annular preventer pressure
        tested to.
    :ivar pres_rams: Blow out preventer ram pressure tested to.
    :ivar pres_choke_line: Choke line pressure tested to.
    :ivar pres_choke_man: Choke line manifold pressure tested to.
    :ivar last_fire_boat_drill: Last fire or life boat drill.
    :ivar last_abandon_drill: Last abandonment drill.
    :ivar last_rig_inspection: Last rig inspection/check.
    :ivar last_safety_meeting: Last safety meeting.
    :ivar last_safety_inspection: Last safety inspection.
    :ivar last_trip_drill: Last trip drill.
    :ivar last_diverter_drill: Last diverter drill.
    :ivar last_bop_drill: Last blow out preventer drill.
    :ivar reg_agency_insp: Governmental regulatory inspection agency
        inspection? Values are "true" (or "1") and "false" (or "0").
    :ivar non_compliance_issued: Inspection non-compliance notice
        served? Values are "true" (or "1") and "false" (or "0").
    :ivar num_stop_cards: Number of health, safety and environment
        incidents reported.
    :ivar fluid_discharged: Daily whole mud discarded.
    :ivar vol_ctg_discharged: Volume of cuttings discharged.
    :ivar vol_oil_ctg_discharge: Oil on cuttings daily discharge.
    :ivar waste_discharged: Volume of sanitary waste discharged.
    :ivar comments: Comments and remarks.
    :ivar incident:
    """

    days_inc_free: Optional[str] = field(
        default=None,
        metadata={
            "name": "DaysIncFree",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    last_csg_pres_test: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastCsgPresTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_last_csg: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresLastCsg",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    last_bop_pres_test: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastBopPresTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    next_bop_pres_test: Optional[str] = field(
        default=None,
        metadata={
            "name": "NextBopPresTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_std_pipe: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresStdPipe",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_kelly_hose: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresKellyHose",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_diverter: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresDiverter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_annular: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresAnnular",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_rams: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresRams",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_choke_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresChokeLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_choke_man: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresChokeMan",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    last_fire_boat_drill: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastFireBoatDrill",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    last_abandon_drill: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastAbandonDrill",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    last_rig_inspection: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastRigInspection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    last_safety_meeting: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastSafetyMeeting",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    last_safety_inspection: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastSafetyInspection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    last_trip_drill: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastTripDrill",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    last_diverter_drill: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastDiverterDrill",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    last_bop_drill: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastBopDrill",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    reg_agency_insp: Optional[bool] = field(
        default=None,
        metadata={
            "name": "RegAgencyInsp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    non_compliance_issued: Optional[bool] = field(
        default=None,
        metadata={
            "name": "NonComplianceIssued",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_stop_cards: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumStopCards",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_discharged: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidDischarged",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_ctg_discharged: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolCtgDischarged",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_oil_ctg_discharge: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolOilCtgDischarge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    waste_discharged: Optional[str] = field(
        default=None,
        metadata={
            "name": "WasteDischarged",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    incident: List[Incident] = field(
        default_factory=list,
        metadata={
            "name": "Incident",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class InterpretedIntervalLithology:
    """The description of a single rock type that is used within
    InterpretedGeologyInterval.

    There can only be one of these in each InterpretedGeologyInterval.

    :ivar kind: The geological name for the type of lithology from the
        enum table listing a subset of the OneGeology / CGI defined
        formation types.
    :ivar citation: An ISO 19115 EIP-derived set of metadata attached to
        ensure the traceability of the InterpretedIntervalLithology
    :ivar code_lith: An optional custom lithology encoding scheme. If
        used, it is recommended that the scheme follows the NPD required
        usage. With the numeric values noted in the enum tables, which
        was the original intent for this item. The NPD Coding System
        assigns a digital code to the main lithologies as per the
        Norwegian Blue Book data standards. The code was then derived by
        lithology = (main lithology * 10) + cement + (modifier / 100).
        Example: Calcite cemented silty micaceous sandstone: (33 * 10) +
        1 + (21 / 100) gives a numeric code of 331.21. However, the NPD
        is also working through Energistics/Caesar to potentially change
        this usage.) This scheme should not be used for mnemonics,
        because those vary by operator, and if an abbreviation is
        required, a local look-up table should be used by the rendering
        client, based on Lithology Type.
    :ivar color: STRUCTURED DESCRIPTION USAGE. Lithology color
        description, from Shell 1995 4.3.3.1 and 4.3.3.2 Colors with the
        addition of: frosted. e.g., black, blue, brown, buff, green,
        grey, olive, orange, pink, purple, red, translucent, frosted,
        white, yellow; modified by: dark, light, moderate, medium,
        mottled, variegated, slight, weak, strong, and vivid.
    :ivar texture: STRUCTURED DESCRIPTION USAGE. Lithology matrix
        texture description from Shell 1995 4.3.2.6: crystalline, (often
        "feather-edge" appearance on breaking), friable, dull, earthy,
        chalky, (particle size less than 20m; often exhibits capillary
        imbibition) visibly particulate, granular, sucrosic, (often
        exhibits capillary imbibition). Examples: compact interlocking,
        particulate, (Gradational textures are quite common.) chalky
        matrix with sucrosic patches, (Composite textures also occur).
    :ivar hardness: STRUCTURED DESCRIPTION USAGE. Mineral hardness.
        Typically, this element is rarely used because mineral hardness
        is not typically recorded. What typically is recorded is
        compaction. However, this element is retained for use defined as
        per Mohs scale of mineral hardness.
    :ivar compaction: STRUCTURED DESCRIPTION USAGE. Lithology compaction
        from Shell 1995 4.3.1.5, which includes: not compacted, slightly
        compacted, compacted, strongly compacted, friable, indurated,
        hard.
    :ivar size_grain: STRUCTURED DESCRIPTION USAGE. Lithology grain size
        description. Defined from Shell 4.3.1.1. (Wentworth) modified to
        remove the ambiguous term pelite. Size ranges in millimeter (or
        micrometer) and inches. LT 256 mm        LT 10.1 in
        "boulder" 64-256 mm        2.5–10.1 in        "cobble"; 32–64 mm
        1.26–2.5 in       "very coarse gravel" 16–32 mm        0.63–1.26
        in        "coarse gravel" 8–16 mm            0.31–0.63 in
        "medium gravel" 4–8 mm            0.157–0.31 in        "fine
        gravel" 2–4 mm            0.079–0.157 in     "very fine gravel"
        1–2 mm           0.039–0.079 in    "very coarse sand" 0.5–1 mm
        0.020–0.039 in        "coarse sand" 0.25–0.5 mm
        0.010–0.020 in     "medium sand" 125–250 um        0.0049–0.010
        in        "fine sand" 62.5–125 um      .0025–0.0049 in   "very
        fine sand" 3.90625–62.5 um        0.00015–0.0025 in    "silt" LT
        3.90625 um        LT 0.00015 in        "clay" LT 1 um
        LT 0.000039 in        "colloid"
    :ivar roundness: STRUCTURED DESCRIPTION USAGE. Lithology roundness
        description from Shell 4.3.1.3. Roundness refers to modal size
        class: very angular, angular, subangular, subrounded, rounded,
        well rounded.
    :ivar sorting: STRUCTURED DESCRIPTION USAGE. Lithology sorting
        description from Shell 4.3.1.2 Sorting: very poorly sorted,
        unsorted, poorly sorted, poorly to moderately well sorted,
        moderately well sorted, well sorted, very well sorted,
        unimodally sorted, bimodally sorted.
    :ivar sphericity: STRUCTURED DESCRIPTION USAGE. Lithology sphericity
        description for the modal size class of grains in the sample,
        defined as per Shell 4.3.1.4 Sphericity: very elongated,
        elongated, slightly elongated, slightly spherical, spherical,
        very spherical.
    :ivar matrix_cement: STRUCTURED DESCRIPTION USAGE. Lithology
        matrix/cement description. Terms will be as defined in the
        enumeration table. e.g., "calcite" (Common) "dolomite",
        "ankerite" (e.g., North Sea HPHT reservoirs such as Elgin and
        Franklin have almost pure ankerite cementation) "siderite"
        (Sherwood sandstones, southern UK typical Siderite cements),
        "quartz" (grain-to-grain contact cementation or secondary quartz
        deposition), "kaolinite", "illite" (e.g., Village Fields North
        Sea), "smectite","chlorite" (Teg, Algeria.).
    :ivar porosity_visible: STRUCTURED DESCRIPTION USAGE. Lithology
        visible porosity description. Defined after BakerHughes
        definitions, as opposed to Shell, which has no linkage to actual
        numeric estimates.
    :ivar porosity_fabric: STRUCTURED DESCRIPTION USAGE. Visible
        porosity fabric description from after Shell 4.3.2.1 and
        4.3.2.2: intergranular (particle size greater than 20m), fine
        interparticle (particle size less than 20m), intercrystalline,
        intragranular, intraskeletal, intracrystalline, mouldic,
        fenestral, shelter, framework, stylolitic, replacement,
        solution, vuggy, channel, cavernous.
    :ivar permeability: STRUCTURED DESCRIPTION USAGE. Lithology
        permeability description from Shell 4.3.2.5. In the future,
        these values would benefit from quantification, e.g., tight,
        slightly, fairly, highly.
    :ivar qualifier:
    :ivar uid: Unique identifier for this instance of
        InterpretedIntervalLithology.
    """

    kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    citation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Citation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    code_lith: Optional[str] = field(
        default=None,
        metadata={
            "name": "CodeLith",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    color: Optional[str] = field(
        default=None,
        metadata={
            "name": "Color",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    texture: Optional[str] = field(
        default=None,
        metadata={
            "name": "Texture",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hardness: Optional[str] = field(
        default=None,
        metadata={
            "name": "Hardness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    compaction: Optional[str] = field(
        default=None,
        metadata={
            "name": "Compaction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    size_grain: Optional[str] = field(
        default=None,
        metadata={
            "name": "SizeGrain",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    roundness: Optional[str] = field(
        default=None,
        metadata={
            "name": "Roundness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sorting: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sorting",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sphericity: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sphericity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    matrix_cement: Optional[str] = field(
        default=None,
        metadata={
            "name": "MatrixCement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    porosity_visible: Optional[str] = field(
        default=None,
        metadata={
            "name": "PorosityVisible",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    porosity_fabric: Optional[str] = field(
        default=None,
        metadata={
            "name": "PorosityFabric",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    permeability: Optional[str] = field(
        default=None,
        metadata={
            "name": "Permeability",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    qualifier: List[LithologyQualifier] = field(
        default_factory=list,
        metadata={
            "name": "Qualifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class IntervalStatusHistory:
    """
    Information on the status history in the interval.

    :ivar physical_status: The physical status of an interval (e.g.,
        open, closed, proposed).
    :ivar start_date: The start date of  the status and allocation
        factor.
    :ivar end_date: The end date of status and allocation factor.
    :ivar status_md_interval: Measured depth interval over which this
        status is valid for the given time frame.
    :ivar allocation_factor: Defines the proportional amount of fluid
        from the well completion that is flowing through this interval
        within a wellbore.
    :ivar comment: Comments and remarks about the interval over this
        period of time.
    :ivar uid: Unique identifier for this instance of
        IntervalStatusHistory.
    """

    physical_status: Optional[PhysicalStatus] = field(
        default=None,
        metadata={
            "name": "PhysicalStatus",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    start_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    status_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "StatusMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    allocation_factor: Optional[str] = field(
        default=None,
        metadata={
            "name": "AllocationFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "pattern": r".+",
        },
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Inventory:
    """
    Inventory Component Schema.

    :ivar name: Name or type of inventory item.
    :ivar item_wt_or_vol_per_unit: Item weight or volume per unit.
    :ivar price_per_unit: Price per item unit, assume same currency for
        all items.
    :ivar qty_start: Start quantity for report interval.
    :ivar qty_adjustment: Daily quantity adjustment/correction.
    :ivar qty_received: Quantity received at the site.
    :ivar qty_returned: Quantity returned to base from site.
    :ivar qty_used: Quantity used for the report interval.
    :ivar cost_item: Cost for the product for the report interval.
    :ivar qty_on_location: Amount of the item remaining on location
        after all adjustments for the report interval.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Inventory.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    item_wt_or_vol_per_unit: Optional[AbstractItemWtOrVolPerUnit] = field(
        default=None,
        metadata={
            "name": "ItemWtOrVolPerUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    price_per_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "PricePerUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    qty_start: Optional[float] = field(
        default=None,
        metadata={
            "name": "QtyStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    qty_adjustment: Optional[float] = field(
        default=None,
        metadata={
            "name": "QtyAdjustment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    qty_received: Optional[float] = field(
        default=None,
        metadata={
            "name": "QtyReceived",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    qty_returned: Optional[float] = field(
        default=None,
        metadata={
            "name": "QtyReturned",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    qty_used: Optional[float] = field(
        default=None,
        metadata={
            "name": "QtyUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cost_item: Optional[str] = field(
        default=None,
        metadata={
            "name": "CostItem",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    qty_on_location: Optional[float] = field(
        default=None,
        metadata={
            "name": "QtyOnLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ItemVolPerUnit(AbstractItemWtOrVolPerUnit):
    """
    Item volume per unit.

    :ivar item_vol_per_unit: Item volume per unit.
    """

    item_vol_per_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemVolPerUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class ItemWtPerUnit(AbstractItemWtOrVolPerUnit):
    """
    Item weight per unit.

    :ivar item_wt_per_unit: Item weight per unit.
    """

    item_wt_per_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemWtPerUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class Jar:
    """WITSML - Tubular Jar Component Schema. Captures information about jars, which are mechanical or hydraulic devices used in the drill stem to deliver an impact load to another component of the drill stem, especially when that component is stuck.

    :ivar for_up_set: Up set force.
    :ivar for_down_set: Down set force.
    :ivar for_up_trip: Up trip force.
    :ivar for_down_trip: Down trip force.
    :ivar for_pmp_open: Pump open force.
    :ivar for_seal_fric: Seal friction force.
    :ivar type_jar: The kind of jar.
    :ivar jar_action: The jar action.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    for_up_set: Optional[str] = field(
        default=None,
        metadata={
            "name": "ForUpSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    for_down_set: Optional[str] = field(
        default=None,
        metadata={
            "name": "ForDownSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    for_up_trip: Optional[str] = field(
        default=None,
        metadata={
            "name": "ForUpTrip",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    for_down_trip: Optional[str] = field(
        default=None,
        metadata={
            "name": "ForDownTrip",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    for_pmp_open: Optional[str] = field(
        default=None,
        metadata={
            "name": "ForPmpOpen",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    for_seal_fric: Optional[str] = field(
        default=None,
        metadata={
            "name": "ForSealFric",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_jar: Optional[JarType] = field(
        default=None,
        metadata={
            "name": "TypeJar",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    jar_action: Optional[JarAction] = field(
        default=None,
        metadata={
            "name": "JarAction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class JobExtension(AbstractEventExtension):
    """
    Information on the job event.

    :ivar job_reason: Comment on the reason for the job
    :ivar job_status: Status of job
    :ivar primary_motivation_for_job: The primary reason for doing this
        job.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    job_reason: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobReason",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    job_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "JobStatus",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    primary_motivation_for_job: Optional[str] = field(
        default=None,
        metadata={
            "name": "PrimaryMotivationForJob",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class LostCirculationExtension(AbstractEventExtension):
    """
    Information on lost circulation event.

    :ivar volume_lost: Volume lost
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    volume_lost: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolumeLost",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class MemberObject:
    """
    Defines a member of an objectGroup.

    :ivar index_kind: For a log object, this specifies the kind of the
        index curve for the log. This is only relevant for a
        systematically growing object.
    :ivar index_interval: The growing-object index value range that
        applies to this group. The significance of this range is defined
        by the groupType.
    :ivar mnemonic_list: A comma delimited list of log curve mnemonics.
        Each mnemonic should only occur once in the list. If not
        specified then the group applies to all curves in the log.
    :ivar reference_depth: A measured depth related to this group. This
        does not necessarily represent an actual depth within a growing-
        object. The significance of this depth is defined by the
        groupType.
    :ivar reference_date_time: A date and time related to this group.
        This does not necessarily represent an actual index within a
        growing-object. The significance of this time is defined by the
        groupType.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar object_reference:
    :ivar sequence1:
    :ivar sequence2:
    :ivar sequence3:
    :ivar uid: Unique identifier for this instance of MemberObject
    """

    index_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "IndexKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    index_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "IndexInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mnemonic_list: Optional[str] = field(
        default=None,
        metadata={
            "name": "MnemonicList",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    reference_depth: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReferenceDepth",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    reference_date_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReferenceDateTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    object_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "ObjectReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    sequence1: Optional[ObjectSequence] = field(
        default=None,
        metadata={
            "name": "Sequence1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    sequence2: Optional[ObjectSequence] = field(
        default=None,
        metadata={
            "name": "Sequence2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    sequence3: Optional[ObjectSequence] = field(
        default=None,
        metadata={
            "name": "Sequence3",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MudLogConcentrationParameter(MudLogParameter):
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    concentration_parameter_kind: Optional[ConcentrationParameterKind] = field(
        default=None,
        metadata={
            "name": "ConcentrationParameterKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class MudLogForceParameter(MudLogParameter):
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    force_parameter_kind: Optional[ForceParameterKind] = field(
        default=None,
        metadata={
            "name": "ForceParameterKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class MudLogPressureGradientParameter(MudLogParameter):
    """
    Describes the kind and value of mud log parameters that are expressed in units
    of pressure gradient.

    :ivar value: The value of the parameter in pressure gradient units.
    :ivar pressure_gradient_parameter_kind:
    """

    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    pressure_gradient_parameter_kind: Optional[
        PressureGradientParameterKind
    ] = field(
        default=None,
        metadata={
            "name": "PressureGradientParameterKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class MudLogPressureParameter(MudLogParameter):
    """
    Describes the kind and value of mud log parameters that are expressed in units
    of pressure.

    :ivar value: The value of the parameter in pressure units.
    :ivar pressure_parameter_kind:
    """

    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    pressure_parameter_kind: Optional[PressureParameterKind] = field(
        default=None,
        metadata={
            "name": "PressureParameterKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class MudLogStringParameter(MudLogParameter):
    """
    Stores the values of parameters that are described by character strings.

    :ivar value: The value of the parameter as a character string.
    :ivar mud_log_string_parameter_kind:
    """

    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    mud_log_string_parameter_kind: Optional[MudLogStringParameterKind] = field(
        default=None,
        metadata={
            "name": "MudLogStringParameterKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class MudVolume:
    """
    Operations Mud Volume Component Schema.

    :ivar vol_tot_mud_start: Total volume of mud at start of report
        interval (including pits and hole).
    :ivar vol_mud_dumped: Volume of mud dumped.
    :ivar vol_mud_received: Volume of mud received from mud warehouse.
    :ivar vol_mud_returned: Volume of mud returned to mud warehouse.
    :ivar vol_mud_built: Volume of mud built.
    :ivar vol_mud_string: Volume of mud contained within active string.
    :ivar vol_mud_casing: Volume of mud contained in casing annulus.
    :ivar vol_mud_hole: Volume of mud contained in the openhole annulus.
    :ivar vol_mud_riser: Volume of mud contained in riser section
        annulus.
    :ivar vol_tot_mud_end: Total volume of mud at the end of the report
        interval (including pits and hole).
    :ivar mud_losses:
    """

    vol_tot_mud_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolTotMudStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_mud_dumped: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolMudDumped",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_mud_received: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolMudReceived",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_mud_returned: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolMudReturned",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_mud_built: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolMudBuilt",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_mud_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolMudString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_mud_casing: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolMudCasing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_mud_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolMudHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_mud_riser: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolMudRiser",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_tot_mud_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolTotMudEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mud_losses: Optional[MudLosses] = field(
        default=None,
        metadata={
            "name": "MudLosses",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class NameTag:
    """WITSML - Equipment NameTag Schema.

    :ivar name: The physical identification string of the equipment tag.
    :ivar numbering_scheme: The format or encoding specification of the
        equipment tag. The tag may contain different pieces of
        information and knowledge of that information is inherent in the
        specification. The "identification string" is a mandatory part
        of the information in a tag.
    :ivar technology: Identifies the general type of identifier on an
        item.  If multiple identifiers exist on an item, a separate
        description set for each identifier should be created.  For
        example, a joint of casing may have a barcode label on it along
        with a painted-on code and an RFID tag attached or embedded into
        the coupling.  The barcode label may in turn be an RFID-equipped
        label. This particular scenario would require populating five
        nameTags to fully describe and decode all the possible
        identifiers as follows: 'tagged' - RFID tag embedded in the
        coupling, 'label'  - Serial number printed on the label,
        'tagged' - RFID tag embedded into the label, 'label'  - Barcode
        printed on the label, 'painted'- Mill number painted on the pipe
        body.
    :ivar location: An indicator of where the tag is attached to the
        item. This is used to assist the user in finding where an
        identifier is located on an item.  This optional field also
        helps to differentiate where an identifier is located when
        multiple identifiers exist on an item. Most downhole components
        have a box (female thread) and pin (male thread) end as well as
        a pipe body in between the ends. Where multiple identifiers are
        used on an item, it is convenient to have a reference as to
        which end, or somewhere in the middle, an identifier may be
        closer to. Some items may have an identifier on a non-standard
        location, such as on the arm of a hole opener.  'other', by
        exclusion, tells a user to look elsewhere than on the body or
        near the ends of an item.  Most non-downhole tools use either
        'body', 'other' or not specified because the location tends to
        lose value with smaller or non threaded items.
    :ivar installation_date: When the tag was installed in or on the
        item.
    :ivar installation_company: Pointer to a BusinessAssociate
        representing the name of the company that installed the tag.
    :ivar mounting_code: Reference to a manufacturer's or installer's
        installation description, code, or method.
    :ivar comment: A comment or remark about the tag.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of NameTag.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    numbering_scheme: Optional[NameTagNumberingScheme] = field(
        default=None,
        metadata={
            "name": "NumberingScheme",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    technology: Optional[NameTagTechnology] = field(
        default=None,
        metadata={
            "name": "Technology",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    location: Optional[NameTagLocation] = field(
        default=None,
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    installation_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "InstallationDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    installation_company: Optional[str] = field(
        default=None,
        metadata={
            "name": "InstallationCompany",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mounting_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "MountingCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Nozzle:
    """
    Nozzle Component Schema.

    :ivar index: Index if this is an indexed object.
    :ivar dia_nozzle: Nozzle diameter.
    :ivar type_nozzle: Nozzle type.
    :ivar len: Length of the nozzle.
    :ivar orientation: Nozzle orientation.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Nozzle
    """

    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_nozzle: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaNozzle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_nozzle: Optional[NozzleType] = field(
        default=None,
        metadata={
            "name": "TypeNozzle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len: Optional[str] = field(
        default=None,
        metadata={
            "name": "Len",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    orientation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Orientation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class OtherConnectionType(AbstractConnectionType):
    """
    Allows you to enter a connection type other than the ones in the standard list.

    :ivar other_connection_type: Connection type other than rod, casing
        or tubing.
    """

    other_connection_type: Optional[OtherConnectionTypes] = field(
        default=None,
        metadata={
            "name": "OtherConnectionType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class Ppfgchannel:
    """A channel object specific to pore pressure and fracture gradient modeling.

    It corresponds roughly to a PPFGDataSetCurve in OSDU.

    :ivar ppfgdata_processing_applied: An array of processing operations
        that have been applied to this channel's data. For example:
        'Smoothed', 'Calibrated', etc.
    :ivar ppfgderivation: Indicates how the PPFG data in the channel was
        derived.
    :ivar ppfgfamily: The PPFG Family of the PPFG quantity measured, for
        example 'Pore Pressure from Corrected Drilling Exponent'. An
        individual channel that belongs to a Main Family.
    :ivar ppfgfamily_mnemonic: The mnemonic of the PPFG Family.
    :ivar ppfgmain_family: The Main Family Type of the PPFG quantity
        measured, for example 'Pore Pressure'. Primarily used for high
        level data classification.
    :ivar ppfgmodeled_lithology: The lithology that this channel was
        modeled on. The assumption is that several different channels
        will be modeled, each for a specific lithology type, and during
        drilling, when it is known which lithologyy the well is
        currently in, users would refer to the channels modeled on the
        appropropriate type of lithology.
    :ivar ppfgtransform_model_type: The empirical calibrated model used
        for pressure calculations from a petrophysical channel (sonic or
        resistivity), for example 'Eaton' and 'Bowers',... .
    :ivar ppfguncertainty_class: The uncertainty class for the channel,
        for example 'most likely' or 'p50'.
    :ivar ppfgchannel_osduintegration: Information about a PPFGChannel
        that is relevant for OSDU integration but does not have a
        natural place in a PPFGChannel object.
    """

    class Meta:
        name = "PPFGChannel"
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"

    ppfgdata_processing_applied: List[Union[PpfgdataProcessing, str]] = field(
        default_factory=list,
        metadata={
            "name": "PPFGDataProcessingApplied",
            "type": "Element",
        },
    )
    ppfgderivation: Optional[Union[PpfgdataDerivation, str]] = field(
        default=None,
        metadata={
            "name": "PPFGDerivation",
            "type": "Element",
        },
    )
    ppfgfamily: Optional[Union[Ppfgfamily, str]] = field(
        default=None,
        metadata={
            "name": "PPFGFamily",
            "type": "Element",
        },
    )
    ppfgfamily_mnemonic: Optional[Union[PpfgfamilyMnemonic, str]] = field(
        default=None,
        metadata={
            "name": "PPFGFamilyMnemonic",
            "type": "Element",
        },
    )
    ppfgmain_family: Optional[Union[PpfgmainFamily, str]] = field(
        default=None,
        metadata={
            "name": "PPFGMainFamily",
            "type": "Element",
        },
    )
    ppfgmodeled_lithology: Optional[Union[PpfgmodeledLithology, str]] = field(
        default=None,
        metadata={
            "name": "PPFGModeledLithology",
            "type": "Element",
        },
    )
    ppfgtransform_model_type: Optional[
        Union[PpfgtransformModelType, str]
    ] = field(
        default=None,
        metadata={
            "name": "PPFGTransformModelType",
            "type": "Element",
        },
    )
    ppfguncertainty_class: Optional[Union[PpfguncertaintyType, str]] = field(
        default=None,
        metadata={
            "name": "PPFGUncertaintyClass",
            "type": "Element",
        },
    )
    ppfgchannel_osduintegration: Optional[PpfgchannelOsduintegration] = field(
        default=None,
        metadata={
            "name": "PPFGChannelOSDUIntegration",
            "type": "Element",
        },
    )


@dataclass
class PpfgchannelSet:
    """A channel set object specific to pore pressure and fracture gradient
    modeling.

    It corresponds roughly to a PPFGDataSet in OSDU.

    :ivar ppfgcomment: Open comments from the PPFG calculation team.
    :ivar ppfgderivation: Nominal indication of how how the PPFG data in
        the channel set was derived. Individual channels may have
        different derivations.
    :ivar ppfggauge_type: Free text to describe the type of gauge used
        for the pressure measurement.
    :ivar ppfgoffset_wellbore: Offset Wellbores included in the context
        and calculations of this PPFG channel set.
    :ivar ppfgtectonic_setting: Tectonic Scenario Setting for Planning
        and Pore Pressure Practitioners. Built into interpretive curves.
        Can be, for example 'Strike Slip'.
    :ivar ppfgchannel_set_osduintegration: Information about a
        PPFGChannelSet that is relevant for OSDU integration but does
        not have a natural place in a PPFGChannelSet object.
    """

    class Meta:
        name = "PPFGChannelSet"
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"

    ppfgcomment: Optional[str] = field(
        default=None,
        metadata={
            "name": "PPFGComment",
            "type": "Element",
        },
    )
    ppfgderivation: Optional[Union[PpfgdataDerivation, str]] = field(
        default=None,
        metadata={
            "name": "PPFGDerivation",
            "type": "Element",
        },
    )
    ppfggauge_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "PPFGGaugeType",
            "type": "Element",
        },
    )
    ppfgoffset_wellbore: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PPFGOffsetWellbore",
            "type": "Element",
        },
    )
    ppfgtectonic_setting: Optional[Union[PpfgtectonicSetting, str]] = field(
        default=None,
        metadata={
            "name": "PPFGTectonicSetting",
            "type": "Element",
        },
    )
    ppfgchannel_set_osduintegration: Optional[
        PpfgchannelSetOsduintegration
    ] = field(
        default=None,
        metadata={
            "name": "PPFGChannelSetOSDUIntegration",
            "type": "Element",
        },
    )


@dataclass
class Ppfglog:
    """
    A log object specific to pore pressure and fracture gradient modeling.

    :ivar ppfgcomment: Open comments from the PPFG calculation team.
    :ivar ppfgderivation: Nominal indication of how how the PPFG data in
        the log was derived. Individual channels may have different
        derivations.
    :ivar ppfggauge_type: Free text to describe the type of gauge used
        for the pressure measurement.
    :ivar ppfgoffset_wellbore: Offset Wellbores included in the context
        and calculations of this PPFG log.
    :ivar ppfgtectonic_setting: Tectonic Scenario Setting for Planning
        and Pore Pressure Practitioners. Built into interpretive curves.
        Can be, for example 'Strike Slip'.
    :ivar ppfglog_osduintegration: Information about a PPFGLog that is
        relevant for OSDU integration but does not have a natural place
        in a PPFGLog object.
    """

    class Meta:
        name = "PPFGLog"
        namespace = "http://www.energistics.org/energyml/data/witsmlv2"

    ppfgcomment: Optional[str] = field(
        default=None,
        metadata={
            "name": "PPFGComment",
            "type": "Element",
        },
    )
    ppfgderivation: Optional[Union[PpfgdataDerivation, str]] = field(
        default=None,
        metadata={
            "name": "PPFGDerivation",
            "type": "Element",
        },
    )
    ppfggauge_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "PPFGGaugeType",
            "type": "Element",
        },
    )
    ppfgoffset_wellbore: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PPFGOffsetWellbore",
            "type": "Element",
        },
    )
    ppfgtectonic_setting: Optional[Union[PpfgtectonicSetting, str]] = field(
        default=None,
        metadata={
            "name": "PPFGTectonicSetting",
            "type": "Element",
        },
    )
    ppfglog_osduintegration: Optional[PpfglogOsduintegration] = field(
        default=None,
        metadata={
            "name": "PPFGLogOSDUIntegration",
            "type": "Element",
        },
    )


@dataclass
class PassIndexedDepth:
    """
    Qualifies measured depth based on pass, direction and depth.

    :ivar pass_value: The pass number. When pass indexed depth values
        are used as primary index values, the pass number MUST change
        any time direction changes. When used as secondary index values,
        this is not required.
    :ivar direction: The direction of the tool in a pass. For primary
        index values, index values within a pass MUST be strictly
        ordered according to the direction. Holding steady MUST NOT be
        used for primary index values; it is only allowed for secondary
        index values.
    :ivar measured_depth: The measured depth of the point.
    """

    pass_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "Pass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    direction: Optional[PassDirection] = field(
        default=None,
        metadata={
            "name": "Direction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    measured_depth: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeasuredDepth",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class Perforating:
    """
    Information on the perforating job.

    :ivar stage_number: index number of stage
    :ivar bottom_packer_set: Perf-Bottom of packer set depth
    :ivar perforation_fluid_type: Perforation fluid type
    :ivar hydrostatic_pressure: hydrostaticPressure
    :ivar surface_pressure: Surface pressure
    :ivar reservoir_pressure: Reservoir pressure
    :ivar fluid_density: The density of fluid
    :ivar fluid_level: Fluid level.
    :ivar conveyance_method: The conveyance method
    :ivar shots_planned: Number of shots planned
    :ivar shots_density: Number of shots per unit length (ft, m)
    :ivar shots_misfired: The number of missed firings from the gun.
    :ivar orientation: orientaton
    :ivar orientation_method: Description of orientaton method
    :ivar perforation_company: Pointer to a BusinessAssociate
        representing the company providing the perforation.
    :ivar carrier_manufacturer: Pointer to a BusinessAssociate
        representing the manufacturer of the carrier.
    :ivar carrier_size: Size of the carrier.
    :ivar carrier_description: Description from carrier
    :ivar charge_manufacturer: Pointer to a BusinessAssociate
        representing the manufacturer of the charge.
    :ivar charge_size: The size of the charge.
    :ivar charge_weight: The weight of the charge.
    :ivar charge_type: The type of the charge.
    :ivar ref_log: Reference to the log
    :ivar gun_centralized: True if centralized, else decentralized.
    :ivar gun_size: The size of the perforation gun.
    :ivar gun_desciption: Description about the perforating gun.
    :ivar gun_left_in_hole: Flag indicating whether the gun is left in
        hole or not.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Perforating
    """

    stage_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "StageNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bottom_packer_set: Optional[str] = field(
        default=None,
        metadata={
            "name": "BottomPackerSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_fluid_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationFluidType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hydrostatic_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "HydrostaticPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    surface_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "SurfacePressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    reservoir_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReservoirPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_density: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_level: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidLevel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    conveyance_method: Optional[PerfConveyanceMethod] = field(
        default=None,
        metadata={
            "name": "ConveyanceMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    shots_planned: Optional[int] = field(
        default=None,
        metadata={
            "name": "ShotsPlanned",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    shots_density: Optional[str] = field(
        default=None,
        metadata={
            "name": "ShotsDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    shots_misfired: Optional[int] = field(
        default=None,
        metadata={
            "name": "ShotsMisfired",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    orientation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Orientation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    orientation_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_company: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationCompany",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    carrier_manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "CarrierManufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    carrier_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "CarrierSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    carrier_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "CarrierDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    charge_manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChargeManufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    charge_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChargeSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    charge_weight: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChargeWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    charge_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChargeType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ref_log: Optional[str] = field(
        default=None,
        metadata={
            "name": "RefLog",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gun_centralized: Optional[str] = field(
        default=None,
        metadata={
            "name": "GunCentralized",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gun_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "GunSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gun_desciption: Optional[str] = field(
        default=None,
        metadata={
            "name": "GunDesciption",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gun_left_in_hole: Optional[bool] = field(
        default=None,
        metadata={
            "name": "GunLeftInHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PerforationStatusHistory:
    """
    Information on the collection of perforation status history.

    :ivar perforation_status: Perforation status.
    :ivar start_date: The start date of the status.
    :ivar end_date: The end date of the status.
    :ivar perforation_md_interval: Overall measured depth interval for
        this perforated interval.
    :ivar perforation_tvd_interval: Overall true vertical depth interval
        for this perforated interval.
    :ivar allocation_factor: Defines the proportional amount of fluid
        from the well completion that is flowing through this interval
        within a wellbore.
    :ivar comment: Remarks and comments about the status.
    :ivar uid: Unique identifier for this instance of
        PerforationStatusHistory.
    """

    perforation_status: Optional[PerforationStatus] = field(
        default=None,
        metadata={
            "name": "PerforationStatus",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    start_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    allocation_factor: Optional[str] = field(
        default=None,
        metadata={
            "name": "AllocationFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "pattern": r".+",
        },
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PlaneAngleOperatingRange(AbstractOperatingRange):
    uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "Uom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class PointMetadata:
    """Used to declare that data points in a specific WITSML log channel may
    contain value attributes (e.g., quality identifiers).

    This declaration is independent from the possibility that ETP may
    have sent ValueAttributes in real time. If an instance of
    PointMetadata is present for a Channel, then the value for that
    point is represented as an array in the bulk data string.

    :ivar name: The name of the point metadata. IMMUTABLE. Set on object
        creation and MUST NOT change thereafter. Customer provided
        changes after creation are an error.
    :ivar data_kind: The kind of point metadata. IMMUTABLE. Set on
        object creation and MUST NOT change thereafter. Customer
        provided changes after creation are an error.
    :ivar description: Free format description of the point metadata.
    :ivar uom: The underlying unit of measure of the value. IMMUTABLE.
        Set on object creation and MUST NOT change thereafter. Customer
        provided changes after creation are an error.
    :ivar metadata_property_kind: An optional value pointing to a
        PropertyKind. Energistics provides a list of standard property
        kinds that represent the basis for the commonly used properties
        in the E&amp;P subsurface workflow. This PropertyKind
        enumeration is in the external PropertyKindDictionary XML file
        in the Common ancillary folder. IMMUTABLE. Set on object
        creation and MUST NOT change thereafter. Customer provided
        changes after creation are an error.
    :ivar axis_definition: IMMUTABLE. Set on object creation and MUST
        NOT change thereafter. Customer provided changes after creation
        are an error. IMMUTABLE. Set on object creation and MUST NOT
        change thereafter. Customer provided changes after creation are
        an error.
    :ivar datum: Defines a vertical datum that point metadata values
        that are measured depth or vertical depth values are referenced
        to. IMMUTABLE. Set on object creation and MUST NOT change
        thereafter. Customer provided changes after creation are an
        error.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    data_kind: Optional[ChannelDataKind] = field(
        default=None,
        metadata={
            "name": "DataKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "Uom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    metadata_property_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "MetadataPropertyKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    axis_definition: List[LogChannelAxis] = field(
        default_factory=list,
        metadata={
            "name": "AxisDefinition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    datum: Optional[str] = field(
        default=None,
        metadata={
            "name": "Datum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class PressureTestExtension(AbstractEventExtension):
    """
    Information on pressure test event.

    :ivar dia_orifice_size: Orifice Size
    :ivar dtime_next_test_date: Next Test Date
    :ivar flowrate_rate_bled: Rate Bled
    :ivar identifier_job: String Being Tested
    :ivar is_success: True if successful
    :ivar max_pressure_duration: Maximum pressure held during test
    :ivar circulating_position: Circulating position
    :ivar fluid_bled_type: Fluid bled type
    :ivar orientation_method: Description of orientaton method
    :ivar test_fluid_type: Test fluid type
    :ivar test_sub_type: Test sub type
    :ivar test_type: Test type
    :ivar annulus_pressure: Annulus pressure
    :ivar well_pressure_used: Well pressure used
    :ivar str10_reference: Reference #
    :ivar uid_assembly: Well (Assembly)
    :ivar volume_bled: Volume Bled
    :ivar volume_lost: Volume Lost
    :ivar volume_pumped: Volume Pumped
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    dia_orifice_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaOrificeSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtime_next_test_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimeNextTestDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_rate_bled: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateRateBled",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    identifier_job: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdentifierJob",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_success: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsSuccess",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_pressure_duration: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxPressureDuration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    circulating_position: Optional[str] = field(
        default=None,
        metadata={
            "name": "CirculatingPosition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_bled_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidBledType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    orientation_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    test_fluid_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestFluidType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    test_sub_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestSubType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    test_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    annulus_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "AnnulusPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    well_pressure_used: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellPressureUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    str10_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "Str10Reference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid_assembly: Optional[str] = field(
        default=None,
        metadata={
            "name": "UidAssembly",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    volume_bled: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolumeBled",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    volume_lost: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolumeLost",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    volume_pumped: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolumePumped",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class PumpOp:
    """
    Operations Pump Component Schema.

    :ivar dtim: Date and time the information is related to.
    :ivar pump: A pointer to the corresponding pump on the rig.
    :ivar type_operation: Type of pump operation.
    :ivar id_liner: Liner inside diameter.
    :ivar len_stroke: Stroke length.
    :ivar rate_stroke: Pump rate (strokes per minute).
    :ivar pressure: Pump pressure recorded.
    :ivar pc_efficiency: Pump efficiency.
    :ivar pump_output: Pump output (included for efficiency).
    :ivar md_bit: Along-hole measured depth of the measurement from the
        drill datum.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of PumpOp.
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pump: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pump",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    type_operation: Optional[PumpOpType] = field(
        default=None,
        metadata={
            "name": "TypeOperation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_liner: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdLiner",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_stroke: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenStroke",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rate_stroke: Optional[str] = field(
        default=None,
        metadata={
            "name": "RateStroke",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    pc_efficiency: Optional[str] = field(
        default=None,
        metadata={
            "name": "PcEfficiency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pump_output: Optional[str] = field(
        default=None,
        metadata={
            "name": "PumpOutput",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_bit: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdBit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Rheometer:
    """Rheometer readings taken during a drill report period.

    A rheometer is viscosimeter use for some fluid measurements,
    particularly when solid suspension properties are needed.

    :ivar temp_rheom: Rheometer temperature.
    :ivar pres_rheom: Rheometer pressure.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar viscosity:
    :ivar uid: Unique identifier for this instance of Rheometer.
    """

    temp_rheom: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempRheom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_rheom: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresRheom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    viscosity: List[RheometerViscosity] = field(
        default_factory=list,
        metadata={
            "name": "Viscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class RigResponse:
    """
    Operations Rig Response Component Schema.

    :ivar rig_heading: Direction, relative to true north, to which the
        rig is facing.
    :ivar rig_heave: Maximum amplitude of the vertical motion of the
        rig.
    :ivar rig_pitch_angle: Measure of the fore-aft rotational movement
        of the rig due to the combined effects of wind and waves;
        measured as the angle from horizontal.
    :ivar rig_roll_angle: Measure of the side-to-side rotational
        movement of the rig due to the combined effects of wind and
        waves; measured as the angle from vertical.
    :ivar riser_angle: Angle of the marine riser with the vertical.
    :ivar riser_direction: Direction of the marine riser.
    :ivar riser_tension: Tension of the marine riser.
    :ivar variable_deck_load: Current temporary load on the rig deck.
    :ivar total_deck_load: Total deck load.
    :ivar guide_base_angle: Direction of the guide base.
    :ivar ball_joint_angle: Angle between the riser and the blowout
        preventer (BOP) at the flex joint.
    :ivar ball_joint_direction: Direction of the ball joint.
    :ivar offset_rig: Horizontal displacement of the rig relative to the
        wellhead.
    :ivar load_leg1: Load carried by one leg of a jackup rig.
    :ivar load_leg2: Load carried by the second leg of a jackup rig.
    :ivar load_leg3: Load carried by the third leg of a jackup rig.
    :ivar load_leg4: Load carried by the fourth leg of a jackup rig.
    :ivar penetration_leg1: Penetration of the first leg into the
        seabed.
    :ivar penetration_leg2: Penetration of the second leg into the
        seabed.
    :ivar penetration_leg3: Penetration of the third leg into the
        seabed.
    :ivar penetration_leg4: Penetration of the fourth leg into the
        seabed.
    :ivar disp_rig: Vessel displacement (in water).
    :ivar mean_draft: Mean draft at mid-section of the vessel.
    :ivar anchor_state:
    """

    rig_heading: Optional[str] = field(
        default=None,
        metadata={
            "name": "RigHeading",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rig_heave: Optional[str] = field(
        default=None,
        metadata={
            "name": "RigHeave",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rig_pitch_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "RigPitchAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rig_roll_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "RigRollAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    riser_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "RiserAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    riser_direction: Optional[str] = field(
        default=None,
        metadata={
            "name": "RiserDirection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    riser_tension: Optional[str] = field(
        default=None,
        metadata={
            "name": "RiserTension",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    variable_deck_load: Optional[str] = field(
        default=None,
        metadata={
            "name": "VariableDeckLoad",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    total_deck_load: Optional[str] = field(
        default=None,
        metadata={
            "name": "TotalDeckLoad",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    guide_base_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "GuideBaseAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ball_joint_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "BallJointAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ball_joint_direction: Optional[str] = field(
        default=None,
        metadata={
            "name": "BallJointDirection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    offset_rig: Optional[str] = field(
        default=None,
        metadata={
            "name": "OffsetRig",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    load_leg1: Optional[str] = field(
        default=None,
        metadata={
            "name": "LoadLeg1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    load_leg2: Optional[str] = field(
        default=None,
        metadata={
            "name": "LoadLeg2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    load_leg3: Optional[str] = field(
        default=None,
        metadata={
            "name": "LoadLeg3",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    load_leg4: Optional[str] = field(
        default=None,
        metadata={
            "name": "LoadLeg4",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    penetration_leg1: Optional[str] = field(
        default=None,
        metadata={
            "name": "PenetrationLeg1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    penetration_leg2: Optional[str] = field(
        default=None,
        metadata={
            "name": "PenetrationLeg2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    penetration_leg3: Optional[str] = field(
        default=None,
        metadata={
            "name": "PenetrationLeg3",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    penetration_leg4: Optional[str] = field(
        default=None,
        metadata={
            "name": "PenetrationLeg4",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    disp_rig: Optional[str] = field(
        default=None,
        metadata={
            "name": "DispRig",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mean_draft: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeanDraft",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    anchor_state: List[AnchorState] = field(
        default_factory=list,
        metadata={
            "name": "AnchorState",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class RodConnectionType(AbstractConnectionType):
    """
    A type of rod connection, e.g., latched, threaded, welded, etc.

    :ivar rod_connection_type: Connection whose type is rod.
    """

    rod_connection_type: Optional[RodConnectionTypes] = field(
        default=None,
        metadata={
            "name": "RodConnectionType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class Scr:
    """
    Operations Slow Circulation Rates (SCR) Component Schema.

    :ivar dtim: Date and time the information is related to.
    :ivar pump: A pointer to the corresponding pump on the rig.
    :ivar type_scr: Type of slow circulation rate.
    :ivar rate_stroke: Pump stroke rate.
    :ivar pres_recorded: Recorded pump pressure for the stroke rate.
    :ivar md_bit: Along hole measured depth of measurement from the
        drill datum.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Scr
    """

    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    pump: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pump",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    type_scr: Optional[ScrType] = field(
        default=None,
        metadata={
            "name": "TypeScr",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    rate_stroke: Optional[str] = field(
        default=None,
        metadata={
            "name": "RateStroke",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    pres_recorded: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresRecorded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    md_bit: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdBit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Sensor:
    """
    Tubular Sensor Component Schema.

    :ivar type_measurement: Type from POSC.
    :ivar offset_bot: Offset from the bottom of the MWD tool.
    :ivar comments: Comments and remarks.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Sensor.
    """

    type_measurement: Optional[MeasurementType] = field(
        default=None,
        metadata={
            "name": "TypeMeasurement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    offset_bot: Optional[str] = field(
        default=None,
        metadata={
            "name": "OffsetBot",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ShakerOp:
    """
    Operations Shaker Component Schema.

    :ivar shaker: A pointer to the shaker that is characterized by this
        report.
    :ivar md_hole: Hole measured depth at the time of measurement.
    :ivar dtim: Date and time the information is related to.
    :ivar hours_run: Hours run the shaker has run for this operation.
    :ivar pc_screen_covered: Percent of screen covered by cuttings.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar shaker_screen:
    :ivar uid: Unique identifier for this instance of ShakerOp
    """

    shaker: Optional[str] = field(
        default=None,
        metadata={
            "name": "Shaker",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    md_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hours_run: Optional[str] = field(
        default=None,
        metadata={
            "name": "HoursRun",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pc_screen_covered: Optional[str] = field(
        default=None,
        metadata={
            "name": "PcScreenCovered",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    shaker_screen: Optional[ShakerScreen] = field(
        default=None,
        metadata={
            "name": "ShakerScreen",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Stabilizer:
    """Tubular Stablizer Component Schema.

    Captures dimension and operation information about stabilizers used
    in the tubular string.

    :ivar len_blade: Length of the blade.
    :ivar len_blade_gauge: Gauge Length of the blade. That is, the
        length of the blade measured at the OdBladeMx.
    :ivar od_blade_mx: Maximum outer diameter of the blade.
    :ivar od_blade_mn: Minimum outer diameter of the blade.
    :ivar dist_blade_bot: Distance of the blade bottom from the bottom
        of the component.
    :ivar shape_blade: Blade shape.
    :ivar fact_fric: Friction factor.
    :ivar type_blade: Blade type.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Stabilizer.
    """

    len_blade: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenBlade",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_blade_gauge: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenBladeGauge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od_blade_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdBladeMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od_blade_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdBladeMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dist_blade_bot: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistBladeBot",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    shape_blade: Optional[BladeShapeType] = field(
        default=None,
        metadata={
            "name": "ShapeBlade",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fact_fric: Optional[float] = field(
        default=None,
        metadata={
            "name": "FactFric",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_blade: Optional[BladeType] = field(
        default=None,
        metadata={
            "name": "TypeBlade",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimFetTest:
    """A diagnostic test that determines fluid efficiency.

    Fluid efficiency test (FET).

    :ivar analysis_method: An analysis method used for this FET.
    :ivar dtim_start: Start time for the FET.
    :ivar dtim_end: End time for the FET.
    :ivar end_pdl_duration: The end of the pressure-dependent leak-off
        portion of the FET.
    :ivar fluid_efficiency: A measurement, derived from a data frac, of
        the efficiency of a particular fluid in creating fracture area
        on a particular formation at a set of conditions.
    :ivar fracture_close_duration: The time at which the fracture
        effectively closes without proppant in place.
    :ivar fracture_close_pres: The pressure at which the fracture
        effectively closes without proppant in place.
    :ivar fracture_extension_pres: The fracture pressure limit for an
        unfractured formation is the fracture initiation pressure. This
        is typically considered the upper bound for the minimum
        horizontal stress or closure pressure. A step-rate test is used
        to determine the fracture extension pressure.
    :ivar fracture_gradient: The fracture gradient.
    :ivar fracture_length: The length of the fracture tip to tip;
        fracture half length is the length of one wing of a fracture
        from the wellbore to the tip.
    :ivar fracture_width: The width of a fracture at the wellbore.
        Hydraulic frac width is generated by frac fluid viscosity and/or
        pump rate (i.e., horsepower).
    :ivar net_pres: The difference between the fracture extension
        pressure and the pressure that exists in the fracture.
    :ivar pdl_coef: The pressure dependent leak-off coefficient.
    :ivar pore_pres: The pressure of the liquids in the formation pores.
    :ivar pseudo_radial_pres: The Horner plot is used to determine if
        pseudo-radial flow developed during pressure decline. If a semi-
        log straight line is observed and the line can be extrapolated
        to a reasonable value of reservoir pressure, then radial or
        pseudo-radial flow may be affecting the decline behavior. This
        suggests that the fracture is already closed and that data
        beyond the point of influence need not be considered in the
        evaluation of closure.
    :ivar residual_permeability: That permeability which remains after a
        fractured formation has closed, allowing the the formation
        fracture face to be pressurized before the fracture is
        mechanically reopened.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of StimFetTest.
    """

    analysis_method: List[StimFetTestAnalysisMethod] = field(
        default_factory=list,
        metadata={
            "name": "AnalysisMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_pdl_duration: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndPdlDuration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_efficiency: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidEfficiency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fracture_close_duration: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureCloseDuration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fracture_close_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureClosePres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fracture_extension_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureExtensionPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fracture_gradient: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureGradient",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fracture_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fracture_width: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureWidth",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    net_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "NetPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pdl_coef: Optional[str] = field(
        default=None,
        metadata={
            "name": "PdlCoef",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pore_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "PorePres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pseudo_radial_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "PseudoRadialPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    residual_permeability: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResidualPermeability",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimFlowPath:
    """
    The fluid flow path for used when pumping a stage in a stimulation job.

    :ivar avg_pmax_pac_pres: PMax prediction allows the tool assembly to
        be designed with expected pressures. It determines maximum
        allowable surface pressure and is typically calculated as a
        single number by which the pressure relief valves are set. This
        variable is the average of all the pmax pressures calculated for
        this flow path.
    :ivar friction_factor_open_hole: The friction factor used to compute
        openhole pressure loss.
    :ivar avg_pmax_weaklink_pres: Average allowable pressure for the
        zone of interest with respect to the bottomhole assembly during
        the stimulation services.
    :ivar break_down_pres: The pressure at which the formation broke.
    :ivar bridge_plug_md: The measured depth of a bridge plug.
    :ivar fracture_gradient: The formation fracture gradient for this
        treatment interval.
    :ivar kind: The type of flow path.
    :ivar max_pmax_pac_pres: PMax prediction allows the tool assembly to
        be designed with expected pressures. It determines maximum
        allowable surface pressure and is typically calculated as a
        single number by which the pressure relief valves are set. This
        variable is the maximum of all the pmax pressures calculated for
        this flow path.
    :ivar max_pmax_weaklink_pres: Maximum allowable pressure for the
        zone of interest with respect to the bottomhole assembly during
        the stimulation services.
    :ivar packer_md: The measured depth of a packer.
    :ivar friction_factor_pipe: The friction factor for the pipe,
        tubing, and/or casing.
    :ivar tubing_bottom_md: The maximum measured depth of the tubing
        used for treatment of a stage.
    :ivar tubular:
    """

    avg_pmax_pac_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgPmaxPacPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    friction_factor_open_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "FrictionFactorOpenHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_pmax_weaklink_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgPmaxWeaklinkPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    break_down_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "BreakDownPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bridge_plug_md: Optional[str] = field(
        default=None,
        metadata={
            "name": "BridgePlugMD",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fracture_gradient: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureGradient",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    kind: Optional[StimFlowPathType] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_pmax_pac_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxPmaxPacPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_pmax_weaklink_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxPmaxWeaklinkPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    packer_md: Optional[str] = field(
        default=None,
        metadata={
            "name": "PackerMD",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    friction_factor_pipe: Optional[str] = field(
        default=None,
        metadata={
            "name": "FrictionFactorPipe",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubing_bottom_md: Optional[str] = field(
        default=None,
        metadata={
            "name": "TubingBottomMD",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular: List[StimTubular] = field(
        default_factory=list,
        metadata={
            "name": "Tubular",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class StimFluid:
    """
    The characteristics and recipe of the stimulation fluid without proppant.

    :ivar name: The name of the fluid.
    :ivar kind: The fluid types.
    :ivar subtype: The fluid subtypes.
    :ivar purpose: The purpose of the fluid.
    :ivar description: The description of the fluid.
    :ivar supplier: The supplier of the fluid.
    :ivar is_kill_fluid: Is the fluid a kill fluid? Values are "true"
        (or "1") and "false" (or "0").
    :ivar volume: Volume of fluid.
    :ivar density: The density of the fluid.
    :ivar fluid_temp: The temperature of the fluid at surface.
    :ivar gel_strength10_min: The shear stress measured at low shear
        rate after a mud has set quiescently for 10 minutes.
    :ivar gel_strength10_sec: The shear stress measured at low shear
        rate after a mud has set quiescently for 10 seconds.
    :ivar specific_gravity: The specific gravity of the fluid at
        surface.
    :ivar viscosity: Viscosity of stimulation fluid.
    :ivar p_h: The pH of the fluid.
    :ivar additive_concentration:
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    kind: Optional[StimFluidKind] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    subtype: Optional[StimFluidSubtype] = field(
        default=None,
        metadata={
            "name": "Subtype",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "name": "Purpose",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    supplier: Optional[str] = field(
        default=None,
        metadata={
            "name": "Supplier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_kill_fluid: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsKillFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "Volume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    density: Optional[str] = field(
        default=None,
        metadata={
            "name": "Density",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_temp: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidTemp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel_strength10_min: Optional[str] = field(
        default=None,
        metadata={
            "name": "GelStrength10Min",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel_strength10_sec: Optional[str] = field(
        default=None,
        metadata={
            "name": "GelStrength10Sec",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    specific_gravity: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecificGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    viscosity: Optional[str] = field(
        default=None,
        metadata={
            "name": "Viscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    p_h: Optional[str] = field(
        default=None,
        metadata={
            "name": "pH",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    additive_concentration: List[StimMaterialQuantity] = field(
        default_factory=list,
        metadata={
            "name": "AdditiveConcentration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class StimIso135032Properties:
    """
    ISO13503-2 properties.

    :ivar absolute_density: The density the material would have if no
        intra-granular porosity is present. (e.g. Boyle’s Law
        porosimetry).
    :ivar clusters_percent: Percentage of undesirable agglomerated
        discrete proppant particles which typically occurs more with
        inefficiently processed natural sand proppants as opposed to
        manufactured ceramic proppants. ISO 13503-2 and API RP19C limit
        the mass of clusters to less than 1%.
    :ivar kvalue: Crush test classification indicating the highest
        stress level at which a proppant generated no more than 10%
        crushed material rounded down to the nearest 1,000 psi during a
        crush test. For example, a value of 14 means ‘14K’ which is
        14000 psi.
    :ivar mean_particle_diameter: The mean diameter of particles in a
        sample of proppant.
    :ivar median_particle_diameter: The median diameter of particles in
        a sample of proppant.
    :ivar specific_gravity: Not formally part of ISO 13503.2 properties,
        the specific gravity is the apparent density of the proppant
        divided by the density of water.
    :ivar roundness: Krumbein Roundness Shape Factor that is a measure
        of the relative sharpness of grain corners or of grain
        curvature. Krumbein and Sloss (1963) are the most widely used
        method of determining shape factors.
    :ivar acid_solubility: The solubility of a proppant in 12:3 HCl:HF
        for 30 minutes at 150°F is an indication of the amount of
        soluble materials (i.e. carbonates, feldspars, iron oxides,
        clays, etc) present in the proppant.
    :ivar apparent_density: Apparent density excludes extra-granular
        porosity by placing a known mass in a volume of fluid and
        determining how much of the fluid is displaced (Archimedes).
    :ivar bulk_density: Bulk density includes both the proppant and the
        porosity. This is measured by filling a known volume with dry
        proppant and measuring the weight.
    :ivar loss_on_ignition: A mass loss (gravimetric) test method
        applied to coated proppants only, which determines the mass of
        resin coating applied to a natural sand or manufactured proppant
        by means of thorough combustion of the flammable resin from the
        nonflammable proppant. Reported as a % of original mass.
    :ivar sphericity: Krumbein Sphericity Shape Factor that is a measure
        of how closely a proppant particle approaches the shape of a
        sphere. Krumbein and Sloss (1963) are the most widely used
        method of determining shape factors.
    :ivar turbidity: A measure of water clarity, how much the material
        suspended in water decreases the passage of light through the
        water. Unit of measure may be Nephelometric Turbidity Unit
        (NTU), but may vary based upon the detector geometry.
    :ivar crush_test_data:
    :ivar sieve_analysis_data:
    :ivar uid: Unique identifier for this instance of
        StimISO13503_2Properties.
    """

    class Meta:
        name = "StimISO13503_2Properties"

    absolute_density: Optional[str] = field(
        default=None,
        metadata={
            "name": "AbsoluteDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    clusters_percent: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClustersPercent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    kvalue: Optional[float] = field(
        default=None,
        metadata={
            "name": "KValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mean_particle_diameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeanParticleDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    median_particle_diameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "MedianParticleDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    specific_gravity: Optional[float] = field(
        default=None,
        metadata={
            "name": "SpecificGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    roundness: Optional[float] = field(
        default=None,
        metadata={
            "name": "Roundness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    acid_solubility: Optional[str] = field(
        default=None,
        metadata={
            "name": "AcidSolubility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    apparent_density: Optional[str] = field(
        default=None,
        metadata={
            "name": "ApparentDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bulk_density: Optional[str] = field(
        default=None,
        metadata={
            "name": "BulkDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    loss_on_ignition: Optional[str] = field(
        default=None,
        metadata={
            "name": "LossOnIgnition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sphericity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Sphericity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    turbidity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Turbidity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    crush_test_data: List[Iso135032CrushTestData] = field(
        default_factory=list,
        metadata={
            "name": "CrushTestData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sieve_analysis_data: List[Iso135032SieveAnalysisData] = field(
        default_factory=list,
        metadata={
            "name": "SieveAnalysisData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimJobDiversion:
    """
    Captures the high-level description of the diversion method used in the
    stimulation job.

    :ivar contractor: Pointer to a BusinessAssociate representing the
        diversion contractor.
    :ivar method: The diversion method used.
    :ivar tool_description: A supplier description of the diversion
        tool, such as its commercial name.
    :ivar element_spacing: Spacing between packer elements.
    """

    contractor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contractor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    method: Optional[StimJobDiversionMethod] = field(
        default=None,
        metadata={
            "name": "Method",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tool_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "ToolDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    element_spacing: Optional[str] = field(
        default=None,
        metadata={
            "name": "ElementSpacing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class StimMaterial:
    """
    Materials as a concept refers to the materials left in the well or consumed in
    the process of making the stimulation; it does not refer the carrier fluid.

    :ivar kind: The material kind.
    :ivar name: The name of the material.
    :ivar supplier: The name of the material supplier.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of StimMaterial.
    """

    kind: Optional[StimMaterialKind] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    supplier: Optional[str] = field(
        default=None,
        metadata={
            "name": "Supplier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimPerforationClusterSet:
    """Provides mechanism for combining perforation clusters into a group.

    This could be used to specify the set of existing perforations
    present in a well before starting a stimulation job, for example,
    for a re-frac job.
    """

    stim_perforation_cluster: List[StimPerforationCluster] = field(
        default_factory=list,
        metadata={
            "name": "StimPerforationCluster",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class StimPumpFlowBackTest:
    """
    Diagnostic test involving flowing a well back after treatment.

    :ivar dtim_end: End time for the test.
    :ivar flow_back_volume: Total volume recovered during a flow back
        test.
    :ivar dtim_start: Start time for the test.
    :ivar fracture_close_duration: The time required for the fracture
        width to become zero.
    :ivar pres_casing: Casing pressure.
    :ivar pres_tubing: Tubing pressure.
    :ivar fracture_close_pres: The pressure when the fracture width
        becomes zero.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar step:
    :ivar uid: Unique identifier for this instance of
        StimPumpFlowBackTest.
    """

    dtim_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flow_back_volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowBackVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fracture_close_duration: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureCloseDuration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_casing: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresCasing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_tubing: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresTubing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fracture_close_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureClosePres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    step: List[StimPumpFlowBackTestStep] = field(
        default_factory=list,
        metadata={
            "name": "Step",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimStepDownTest:
    """
    Diagnostic test involving flowing a well back after treatment.

    :ivar initial_shutin_pres: The initial shutin pressure.
    :ivar bottomhole_fluid_density: The density of the fluid at the
        bottom of the hole adjusting for bottomhole temperature and
        pressure during the step-down test.
    :ivar diameter_entry_hole: Diameter of the injection point or
        perforation.
    :ivar perforation_count: The number of perforations in the interval
        being tested.
    :ivar discharge_coefficient: A coefficient used in the equation for
        calculation of the pressure drop across a perforation set.
    :ivar effective_perfs: The number of perforations in the interval
        being tested that are  calculated to be open to injection, which
        is determined during the step-down test.
    :ivar step: The data related to a particular step in the step-down
        test.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of StimStepDownTest
    """

    initial_shutin_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "InitialShutinPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bottomhole_fluid_density: Optional[str] = field(
        default=None,
        metadata={
            "name": "BottomholeFluidDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    diameter_entry_hole: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiameterEntryHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_count: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    discharge_coefficient: Optional[str] = field(
        default=None,
        metadata={
            "name": "DischargeCoefficient",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    effective_perfs: Optional[str] = field(
        default=None,
        metadata={
            "name": "EffectivePerfs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    step: List[StimPumpFlowBackTestStep] = field(
        default_factory=list,
        metadata={
            "name": "Step",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimStepTest:
    """
    An injection test, plotted pressure against injection rate, where a curve
    deflection and change of slope indicates the fracture breakdown pressure.

    :ivar fracture_extension_pres: The pressure necessary to extend the
        fracture once initiated. The fracture extension pressure may
        rise slightly with increasing fracture length and/or height
        because of friction pressure drop down the length of the
        fracture.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar pres_measurement: A pressure and fluid rate data reading.
    :ivar uid: Unique identifier for this instance of StimStepTest.
    """

    fracture_extension_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureExtensionPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_measurement: List[StimPressureFlowRate] = field(
        default_factory=list,
        metadata={
            "name": "PresMeasurement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class SupportCraft:
    """
    Operations Support Craft Component Schema.

    :ivar name: Human-recognizable context for the support craft.
    :ivar type_support_craft: Type of support craft (e.g., barge,
        helicopter, tug boat, etc.)
    :ivar dtim_arrived: Date and time when the vehicle arrived at the
        rig site.
    :ivar dtim_departed: Date and time when the vehicle departed from
        the rig site.
    :ivar comments: Comments and remarks.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of SupportCraft.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    type_support_craft: Optional[SupportCraftType] = field(
        default=None,
        metadata={
            "name": "TypeSupportCraft",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    dtim_arrived: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimArrived",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_departed: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimDeparted",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class SurfaceEquipment:
    """
    Rig Surface Equipment Schema.

    :ivar description: Description of item and details.
    :ivar pres_rating: Pressure rating of the item.
    :ivar type_surf_equip: Surface equipment type (IADC1-4, Custom,
        Coiled Tubing).
    :ivar use_pump_discharge: Use pump discharge line? Values are "true"
        (or "1") and "false" (or "0").
    :ivar use_standpipe: Use standpipe geometry? Values are "true" (or
        "1") and "false" (or "0").
    :ivar use_hose: Use kelly hose geometry? Values are "true" (or "1")
        and "false" (or "0").
    :ivar use_swivel: Use swivel geometry? Values are "true" (or "1")
        and "false" (or "0").
    :ivar use_kelly: Use kelly geometry? Values are "true" (or "1") and
        "false" (or "0").
    :ivar use_top_stack: Use top stack height? Values are "true" (or
        "1") and "false" (or "0").
    :ivar use_inj_stack: Use injector stack height? Values are "true"
        (or "1") and "false" (or "0").
    :ivar use_surface_iron: Use surface iron description? Values are
        "true" (or "1") and "false" (or "0").
    :ivar id_standpipe: Inner diameter of the standpipe.
    :ivar len_standpipe: Length of the standpipe.
    :ivar id_hose: Inner diameter of the kelly hose.
    :ivar len_hose: Length of the kelly hose.
    :ivar id_swivel: Inner diameter of the swivel.
    :ivar len_swivel: Length of the swivel.
    :ivar id_kelly: Inner diameter of the kelly bushing.
    :ivar len_kelly: Length of the kelly bushing.
    :ivar id_surface_iron: Inner diameter of the surface iron.
    :ivar len_surface_iron: Length of the surface iron.
    :ivar ht_surface_iron: Height of the surface iron.
    :ivar id_discharge_line: Coiled tubing: inner diameter of the pump
        discharge line.
    :ivar len_discharge_line: Coiled tubing: length of the pump
        discharge line.
    :ivar ct_wrap_type: Coiled tubing: the coiled tubing wrap type.
    :ivar od_reel: Coiled tubing: outside diameter of the coiled tubing
        reel.
    :ivar od_core: Coiled tubing: outside diameter of the reel core that
        the coiled tubing is wrapped around.
    :ivar wid_reel_wrap: Coiled tubing: width of the reel core. This is
        the inside dimension.
    :ivar len_reel: Coiled tubing: length of the coiled tubing remaining
        on the reel.
    :ivar inj_stk_up: Coiled tubing: Does it have an injector stack up?
        Values are "true" (or "1") and "false" (or "0").
    :ivar ht_inj_stk: Coiled tubing: The length of tubing from the end
        of the coil reel to the rotary kelly bushing. This length
        includes the tubing in the hole and the tubing on the reel. This
        measurement takes into account the 20 or so feet of tubing that
        is being straightened and pushed through the injector head.
    :ivar umb_inside: Coiled tubing: Umbilical inside, true/false flag
        to account for the wireline inside the coiled tubing. With this
        pressure loss calculation, you can calculate for the strings
        used for logging, wireline coring, etc. Values are "true" (or
        "1") and "false" (or "0").
    :ivar od_umbilical: Coiled tubing: outer diameter of the umbilical.
    :ivar len_umbilical: Coiled tubing: length of the umbilical.
    :ivar id_top_stk: Top drive: inner diameter of the top stack.
    :ivar ht_top_stk: Top drive: The distance that the mud travels from
        the end of the standpipe hose to the drill pipe connection at
        the bottom of the top drive. We are measuring the distance that
        the mud will flow through the top drive.For the top drive. The
        distance that the mud travels from the end of the standpipe hose
        to the drill pipe connection at the bottom of the top drive.
        This is the measurement of the distance that the mud flows
        through the top drive.
    :ivar ht_flange: Height of the flange.
    """

    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_rating: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresRating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_surf_equip: Optional[SurfEquipType] = field(
        default=None,
        metadata={
            "name": "TypeSurfEquip",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    use_pump_discharge: Optional[bool] = field(
        default=None,
        metadata={
            "name": "UsePumpDischarge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    use_standpipe: Optional[bool] = field(
        default=None,
        metadata={
            "name": "UseStandpipe",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    use_hose: Optional[bool] = field(
        default=None,
        metadata={
            "name": "UseHose",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    use_swivel: Optional[bool] = field(
        default=None,
        metadata={
            "name": "UseSwivel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    use_kelly: Optional[bool] = field(
        default=None,
        metadata={
            "name": "UseKelly",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    use_top_stack: Optional[bool] = field(
        default=None,
        metadata={
            "name": "UseTopStack",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    use_inj_stack: Optional[bool] = field(
        default=None,
        metadata={
            "name": "UseInjStack",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    use_surface_iron: Optional[bool] = field(
        default=None,
        metadata={
            "name": "UseSurfaceIron",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_standpipe: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdStandpipe",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_standpipe: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenStandpipe",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_hose: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdHose",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_hose: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenHose",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_swivel: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdSwivel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_swivel: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenSwivel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_kelly: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdKelly",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_kelly: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenKelly",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_surface_iron: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdSurfaceIron",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_surface_iron: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenSurfaceIron",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ht_surface_iron: Optional[str] = field(
        default=None,
        metadata={
            "name": "HtSurfaceIron",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_discharge_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdDischargeLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_discharge_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenDischargeLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ct_wrap_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "CtWrapType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od_reel: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdReel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od_core: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdCore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wid_reel_wrap: Optional[str] = field(
        default=None,
        metadata={
            "name": "WidReelWrap",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_reel: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenReel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    inj_stk_up: Optional[bool] = field(
        default=None,
        metadata={
            "name": "InjStkUp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ht_inj_stk: Optional[str] = field(
        default=None,
        metadata={
            "name": "HtInjStk",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    umb_inside: Optional[bool] = field(
        default=None,
        metadata={
            "name": "UmbInside",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od_umbilical: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdUmbilical",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_umbilical: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenUmbilical",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_top_stk: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdTopStk",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ht_top_stk: Optional[str] = field(
        default=None,
        metadata={
            "name": "HtTopStk",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ht_flange: Optional[str] = field(
        default=None,
        metadata={
            "name": "HtFlange",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class TargetSection:
    """
    WITSML Element Types.

    :ivar sect_number: Sequence number of section, 1,2,3.
    :ivar type_target_section_scope: Section scope: Line or Arc.
    :ivar len_radius: Length of straight line section or radius of arc
        for continuous curve section.
    :ivar angle_arc: Direction of straight line section or radius of arc
        for continuous curve section.
    :ivar thick_above: Height of target above center point at the start
        of the section. In the case of an arc, the thickness above
        should vary linearly with the arc length.
    :ivar thick_below: Depth of target below center point at the start
        of the section. In the case of an arc, the thickness below
        should vary linearly with the arc length.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar location:
    :ivar uid:
    """

    sect_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "SectNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    type_target_section_scope: Optional[TargetSectionScope] = field(
        default=None,
        metadata={
            "name": "TypeTargetSectionScope",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    len_radius: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenRadius",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    angle_arc: Optional[str] = field(
        default=None,
        metadata={
            "name": "AngleArc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    thick_above: Optional[str] = field(
        default=None,
        metadata={
            "name": "ThickAbove",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    thick_below: Optional[str] = field(
        default=None,
        metadata={
            "name": "ThickBelow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    location: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class TrajectoryReport:
    """
    Captures information for a report including trajectory stations.

    :ivar acquisition_remark: Remarks related to acquisition context
        which is not the same as Description, which is a summary of the
        trajectory.
    :ivar mag_decl_used: Magnetic declination used to correct a Magnetic
        North referenced azimuth to a True North azimuth.  Magnetic
        declination angles are measured positive clockwise from True
        North to Magnetic North (or negative in the anti-clockwise
        direction). To convert a Magnetic azimuth to a True North
        azimuth, the magnetic declination should be added. Starting
        value if stations have individual values.
    :ivar md_max_extrapolated: The measured depth to which the survey
        segment was extrapolated.
    :ivar md_max_measured: Measured depth within the wellbore of the
        LAST trajectory station with recorded data. If a trajectory has
        been extrapolated to a deeper depth than the last surveyed
        station then that is MdMaxExtrapolated and not MdMaxMeasured.
    :ivar md_tie_on: Tie-point depth measured along the wellbore from
        the measurement reference datum to the trajectory station -
        where tie point is the place on the originating trajectory where
        the current trajectory intersecst it.
    :ivar nominal_calc_algorithm: The nominal type of algorithm used in
        the position calculation in trajectory stations. Individual
        stations may use different algorithms.
    :ivar nominal_type_survey_tool: The nominal type of tool used for
        the trajectory station measurements. Individual stations may
        have a different tool type.
    :ivar nominal_type_traj_station: The nominal type of survey station
        for the trajectory stations. Individual stations may have a
        different type.
    :ivar trajectory_osduintegration: Information about a Trajectory
        that is relevant for OSDU integration but does not have a
        natural place in a Trajectory object.
    :ivar grid_con_used: The angle  used to correct a true north
        referenced azimuth to a grid north azimuth. WITSML follows the
        Gauss-Bomford convention in which convergence angles are
        measured positive clockwise from true north to grid north (or
        negative in the anti-clockwise direction). To convert a true
        north referenced azimuth to a grid north azimuth, the
        convergence angle must be subtracted from true north. If
        StnGridConUsed is not provided, then this value applies to all
        grid-north referenced stations.
    :ivar grid_scale_factor_used: A multiplier to change geodetic
        distances based on the Earth model (ellipsoid) to distances on
        the grid plane. This is the number which was already used to
        correct lateral distances. Provide it only if it is used in your
        trajectory stations. If StnGridScaleFactorUsed is not provided,
        then this value applies to all trajectory stations. The grid
        scale factor applies to the DispEw, DispNs and Closure elements
        on trajectory stations.
    :ivar azi_vert_sect: Azimuth used for vertical section
        plot/computations.
    :ivar disp_ns_vert_sect_orig: Origin north-south used for vertical
        section plot/computations.
    :ivar disp_ew_vert_sect_orig: Origin east-west used for vertical
        section plot/computations.
    :ivar azi_ref: Specifies the definition of north. While this is
        optional because of legacy data, it is strongly recommended that
        this always be specified.
    :ivar trajectory_station:
    """

    acquisition_remark: Optional[str] = field(
        default=None,
        metadata={
            "name": "AcquisitionRemark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mag_decl_used: Optional[str] = field(
        default=None,
        metadata={
            "name": "MagDeclUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_max_extrapolated: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdMaxExtrapolated",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_max_measured: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdMaxMeasured",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_tie_on: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdTieOn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nominal_calc_algorithm: Optional[Union[TrajStnCalcAlgorithm, str]] = field(
        default=None,
        metadata={
            "name": "NominalCalcAlgorithm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nominal_type_survey_tool: Optional[Union[TypeSurveyTool, str]] = field(
        default=None,
        metadata={
            "name": "NominalTypeSurveyTool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nominal_type_traj_station: Optional[Union[TrajStationType, str]] = field(
        default=None,
        metadata={
            "name": "NominalTypeTrajStation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    trajectory_osduintegration: Optional[TrajectoryOsduintegration] = field(
        default=None,
        metadata={
            "name": "TrajectoryOSDUIntegration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    grid_con_used: Optional[str] = field(
        default=None,
        metadata={
            "name": "GridConUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    grid_scale_factor_used: Optional[str] = field(
        default=None,
        metadata={
            "name": "GridScaleFactorUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    azi_vert_sect: Optional[str] = field(
        default=None,
        metadata={
            "name": "AziVertSect",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    disp_ns_vert_sect_orig: Optional[str] = field(
        default=None,
        metadata={
            "name": "DispNsVertSectOrig",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    disp_ew_vert_sect_orig: Optional[str] = field(
        default=None,
        metadata={
            "name": "DispEwVertSectOrig",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    azi_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "AziRef",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    trajectory_station: List[TrajectoryStation] = field(
        default_factory=list,
        metadata={
            "name": "TrajectoryStation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class TubingConnectionType(AbstractConnectionType):
    """
    Container element for tubing connection types  or collection of tubing
    connection types.

    :ivar tubing_connection_type: Tubing connection type.
    """

    tubing_connection_type: Optional[TubingConnectionTypes] = field(
        default=None,
        metadata={
            "name": "TubingConnectionType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class TubularOsduintegration:
    """
    Information about a Tubular that is relevant for OSDU integration but does not
    have a natural place in a Tubular object.

    :ivar active_indicator: Indicates if the Assembly is activated or
        not.
    :ivar activity_type: Used to describe if it belongs to a RunActivity
        or to a PullActivity.
    :ivar activity_type_reason_description: Used to describe the reason
        of Activity - such as cut/pull, pulling, ...
    :ivar artificial_lift_type: Type of Artificial Lift used (could be
        "Surface Pump" / "Submersible Pump" / "Gas Lift" ...)
    :ivar assembly_base_md: The measured depth of the base from the
        whole assembly.
    :ivar assembly_base_reported_tvd: Depth of the base of the Assembly
        measured from the Well-Head.
    :ivar assembly_top_md: The measured depth of the top from the whole
        assembly.
    :ivar assembly_top_reported_tvd: Depth of the top of the Assembly
        measured from the Well-Head.
    :ivar liner_type: This reference table describes the type of liner
        used in the borehole. For example, slotted, gravel packed or
        pre-perforated etc.
    :ivar osdutubular_assembly_status: Record that reflects the status
        of the Assembly - as 'installed', 'pulled', 'planned',... -
        Applicable to tubing/completions as opposed to drillstrings.
    :ivar parent: Optional - Identifier of the parent assembly (in case
        of side-track, multi-nesting, ...) - The Concentric Tubular
        model is used to identify the Assembly that an Assembly sits
        inside e.g. Surface Casing set inside Conductor, Tubing set
        inside Production Casing, a Bumper Spring set inside a
        Production Tubing Profile Nipple, Liner set inside Casing, etc.
        This is needed to enable a Digital Well Sketch application to
        understand relationships between Assemblies and their parent
        Wellbores.
    :ivar pilot_hole_size: Diameter of the Pilot Hole.
    :ivar sea_floor_penetration_length: The distance that the assembly
        has penetrated below the surface of the sea floor.
    :ivar string_class: Descriptor for Assembly, e.g. Production,
        Surface, Conductor, Intermediate, Drilling.
    :ivar suspension_point_md: In case of multi-nesting of assemblies,
        the 'point' is the Measured Depth of the top of the assembly
        though with PBRs the Suspension Point may not be the top.
    :ivar tubular_assembly_number: Sequence of the TubularAssembly
        (Typically BHA sequence).
    """

    class Meta:
        name = "TubularOSDUIntegration"

    active_indicator: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ActiveIndicator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    activity_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ActivityType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    activity_type_reason_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "ActivityTypeReasonDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    artificial_lift_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ArtificialLiftType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    assembly_base_md: Optional[str] = field(
        default=None,
        metadata={
            "name": "AssemblyBaseMd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    assembly_base_reported_tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "AssemblyBaseReportedTvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    assembly_top_md: Optional[str] = field(
        default=None,
        metadata={
            "name": "AssemblyTopMd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    assembly_top_reported_tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "AssemblyTopReportedTvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    liner_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "LinerType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    osdutubular_assembly_status: Optional[OsdutubularAssemblyStatus] = field(
        default=None,
        metadata={
            "name": "OSDUTubularAssemblyStatus",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    parent: Optional[str] = field(
        default=None,
        metadata={
            "name": "Parent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pilot_hole_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "PilotHoleSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sea_floor_penetration_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "SeaFloorPenetrationLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    string_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "StringClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    suspension_point_md: Optional[str] = field(
        default=None,
        metadata={
            "name": "SuspensionPointMd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_assembly_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "TubularAssemblyNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class TubularUmbilical:
    """An umbilical is any control, power or sensor cable or tube run through an
    outlet on the wellhead down to a particular receptacle on a downhole component
    (power or hydraulic line) or simply to a specific depth (sensors).

    Examples include Gas lift injection tube, Subsea valve control line,
    ESP power cable, iWire for external gauges, external Fiber Optic
    Sensor cable. Umbilicals are run outside of the casing or completion
    assembly and are typically attached by clamps. Umbilicals are run in
    hole same time as the host assembly. Casing Umbilicals may be
    cemented in place e.g. Fiber Optic.

    :ivar connected_tubular_component: The Tubular component the
        umbilical is connected to.
    :ivar cut: A cut in the umbilical.
    :ivar service_type: The Type of Service the umbilical is
        facilitating.
    :ivar tubular_umbilical_osduintegration: Information about a
        TubularUmbilical that is relevant for OSDU integration but does
        not have a natural place in a TubularUmbilical.
    :ivar umbilical_type: The type of umbilical.
    """

    connected_tubular_component: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConnectedTubularComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    cut: List[TubularUmbilicalCut] = field(
        default_factory=list,
        metadata={
            "name": "Cut",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    service_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ServiceType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_umbilical_osduintegration: Optional[
        TubularUmbilicalOsduintegration
    ] = field(
        default=None,
        metadata={
            "name": "TubularUmbilicalOSDUIntegration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    umbilical_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "UmbilicalType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class WaitingOnExtension(AbstractEventExtension):
    """
    Information on waiting event.

    :ivar sub_category: Sub category
    :ivar charge_type_code: Code for charge type
    :ivar business_org_waiting_on: Business organization waiting on
    :ivar is_no_charge_to_producer: Flag indicating whether producer is
        charged or not
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    sub_category: Optional[str] = field(
        default=None,
        metadata={
            "name": "SubCategory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    charge_type_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChargeTypeCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    business_org_waiting_on: Optional[str] = field(
        default=None,
        metadata={
            "name": "BusinessOrgWaitingOn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_no_charge_to_producer: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsNoChargeToProducer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class WellPurposePeriod:
    """
    This class is used to represent a period of time when a facility had a
    consistent WellPurpose.

    :ivar purpose: The facility's purpose.
    :ivar start_date_time: The date and time when the purpose started.
    :ivar end_date_time: The date and time when the purpose ended.
    """

    purpose: Optional[WellPurpose] = field(
        default=None,
        metadata={
            "name": "Purpose",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    start_date_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartDateTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_date_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndDateTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class WellboreGeometryReport:
    """
    Captures information for a report including wellbore geometry.

    :ivar wellbore_geometry_section:
    :ivar depth_water_mean: Water depth.
    :ivar gap_air: Air gap.
    """

    wellbore_geometry_section: List[WellboreGeometrySection] = field(
        default_factory=list,
        metadata={
            "name": "WellboreGeometrySection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    depth_water_mean: Optional[str] = field(
        default=None,
        metadata={
            "name": "DepthWaterMean",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gap_air: Optional[str] = field(
        default=None,
        metadata={
            "name": "GapAir",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class AbstractCementStage:
    """
    Defines the information that is common to the cement job stage design and
    reports.

    :ivar annular_flow_after: Annular flow present after the stage was
        completed?  Values are "true" (or "1") and "false" (or "0").
    :ivar reciprocation_slackoff: Slackoff for reciprocation.
    :ivar bot_plug: Bottom plug used?  Values are "true" (or "1") and
        "false" (or "0").
    :ivar bot_plug_number: Amount of bottom plug used.
    :ivar dia_tail_pipe: Tail pipe size (diameter).
    :ivar displacement_fluid: Reference to displacement fluid
        properties.
    :ivar etim_pres_held: Time the pressure was held.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar flowrate_mud_circ: Rate the mud was circulated during the
        stage.
    :ivar gel10_min: Gels-10Min (in hole at start of job).
    :ivar gel10_sec: Gels-10Sec (in hole at start of job).
    :ivar md_circ_out: Circulate out measured depth.
    :ivar md_coil_tbg: Measured depth of coil tubing (multi-stage cement
        job).
    :ivar md_string: Measured depth of string (multi-stage cement job).
    :ivar md_tool: Measured depth of the tool (multi-stage cement job).
    :ivar mix_method: Mix method.
    :ivar num_stage: Stage number.
    :ivar reciprocation_overpull: Overpull amount for reciprocation.
    :ivar pill_below_plug: Pill below plug?  Values are "true" (or "1")
        and "false" (or "0").
    :ivar plug_catcher: Plug catcher?  Values are "true" (or "1") and
        "false" (or "0").
    :ivar pres_back_pressure: Constant back pressure applied while
        pumping the job (can be superseded by a back pressure per
        pumping stage).
    :ivar pres_bump: Pressure plug bumped.
    :ivar pres_coil_tbg_end: Pressure coiled tubing end.
    :ivar pres_coil_tbg_start: Pressure coiled tubing start
    :ivar pres_csg_end: Casing pressure at the end of the job.
    :ivar pres_csg_start: Casing pressure at the start of the job.
    :ivar pres_displace: Final displacement pressure.
    :ivar pres_held: Pressure held to.
    :ivar pres_mud_circ: Mud circulation pressure.
    :ivar pres_tbg_end: Tubing pressure at the end of the job (not
        coiled tubing).
    :ivar pres_tbg_start: Tubing pressure at the start of the job (not
        coiled tubing).
    :ivar pv_mud: Plastic viscosity (in the hole at the start of the
        job).
    :ivar squeeze_objective: Squeeze objective.
    :ivar stage_md_interval: Measured depth interval for the cement
        stage.
    :ivar tail_pipe_perf: Tail pipe perforated?  Values are "true" (or
        "1") and "false" (or "0").
    :ivar tail_pipe_used: Tail pipe used?  Values are "true" (or "1")
        and "false" (or "0").
    :ivar temp_bhct: Bottomhole temperature: circulating.
    :ivar temp_bhst: Bottomhole temperature: static.
    :ivar top_plug: Top plug used?  Values are "true" (or "1") and
        "false" (or "0").
    :ivar type_original_mud: Type of mud in the hole.
    :ivar type_stage: Stage type.
    :ivar vol_circ_prior: Total volume circulated before starting the
        job/stage.
    :ivar vol_csg_in: Total volume inside the casing for this stage
        placement.
    :ivar vol_csg_out: Total volume outside casing for this stage
        placement.
    :ivar vol_displace_fluid: Volume of displacement fluid.
    :ivar vol_excess: Excess volume.
    :ivar vol_excess_method: Method to estimate excess volume.
    :ivar vol_mud_lost: Total mud lost.
    :ivar vol_returns: Volume of returns.
    :ivar wt_mud: Mud density.
    :ivar yp_mud: Yield point (in the hole at the start of the job).
    :ivar step:
    :ivar original_fluid_location:
    :ivar ending_fluid_location:
    """

    annular_flow_after: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AnnularFlowAfter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    reciprocation_slackoff: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReciprocationSlackoff",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bot_plug: Optional[bool] = field(
        default=None,
        metadata={
            "name": "BotPlug",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bot_plug_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "BotPlugNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_tail_pipe: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaTailPipe",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    displacement_fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "DisplacementFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_pres_held: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimPresHeld",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_mud_circ: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateMudCirc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel10_min: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel10Min",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel10_sec: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel10Sec",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_circ_out: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdCircOut",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_coil_tbg: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdCoilTbg",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_tool: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdTool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mix_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "MixMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_stage: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumStage",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    reciprocation_overpull: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReciprocationOverpull",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pill_below_plug: Optional[bool] = field(
        default=None,
        metadata={
            "name": "PillBelowPlug",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    plug_catcher: Optional[bool] = field(
        default=None,
        metadata={
            "name": "PlugCatcher",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_back_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresBackPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_bump: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresBump",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_coil_tbg_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresCoilTbgEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_coil_tbg_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresCoilTbgStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_csg_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresCsgEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_csg_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresCsgStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_displace: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresDisplace",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_held: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresHeld",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_mud_circ: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresMudCirc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_tbg_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresTbgEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_tbg_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresTbgStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pv_mud: Optional[str] = field(
        default=None,
        metadata={
            "name": "PvMud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    squeeze_objective: Optional[str] = field(
        default=None,
        metadata={
            "name": "SqueezeObjective",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    stage_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "StageMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tail_pipe_perf: Optional[bool] = field(
        default=None,
        metadata={
            "name": "TailPipePerf",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tail_pipe_used: Optional[bool] = field(
        default=None,
        metadata={
            "name": "TailPipeUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_bhct: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempBHCT",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_bhst: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempBHST",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    top_plug: Optional[bool] = field(
        default=None,
        metadata={
            "name": "TopPlug",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_original_mud: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeOriginalMud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_stage: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeStage",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    vol_circ_prior: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolCircPrior",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_csg_in: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolCsgIn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_csg_out: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolCsgOut",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_displace_fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolDisplaceFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_excess: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolExcess",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_excess_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolExcessMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_mud_lost: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolMudLost",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_returns: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolReturns",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wt_mud: Optional[str] = field(
        default=None,
        metadata={
            "name": "WtMud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    yp_mud: Optional[str] = field(
        default=None,
        metadata={
            "name": "YpMud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    step: List[CementPumpScheduleStep] = field(
        default_factory=list,
        metadata={
            "name": "Step",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    original_fluid_location: List[FluidLocation] = field(
        default_factory=list,
        metadata={
            "name": "OriginalFluidLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ending_fluid_location: List[FluidLocation] = field(
        default_factory=list,
        metadata={
            "name": "EndingFluidLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class AzimuthRange(PlaneAngleOperatingRange):
    """
    :ivar is_magnetic_north: True = magnetic north, False = True North
    """

    is_magnetic_north: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsMagneticNorth",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class Bop:
    """
    Rig blowout preventer (BOP) schema.

    :ivar manufacturer: Pointer to a BusinessAssociate representing the
        manufacturer or supplier of the item.
    :ivar model: Manufacturer's designated model.
    :ivar dtim_install: Date and time the BOP was installed.
    :ivar dtim_remove: Date and time of the BOP was removed.
    :ivar name_tag: An identification tag for the blowout preventer. A
        serial number is a type of identification tag; however, some
        tags contain many pieces of information.This element only
        identifies the tag and does not describe the contents.
    :ivar type_connection_bop: Type of connection to the blowout
        preventer.
    :ivar size_connection_bop: Size of the connection to the blowout
        preventer.
    :ivar pres_bop_rating: Maximum pressure rating of the blowout
        preventer.
    :ivar size_bop_sys: Maximum tubulars passable through the blowout
        preventer.
    :ivar rot_bop: Is this a rotating blowout preventer? Values are
        "true" (or "1") and "false" (or "0").
    :ivar id_booster_line: Inner diameter of the booster line.
    :ivar od_booster_line: Outer diameter of the booster line.
    :ivar len_booster_line: Length of the booster line along the riser.
    :ivar id_surf_line: Inner diameter of the surface line.
    :ivar od_surf_line: Outer diameter of the surface line.
    :ivar len_surf_line: Length of the surface line the along riser.
    :ivar id_chk_line: Inner diameter of the choke line.
    :ivar od_chk_line: Outer diameter of the choke line.
    :ivar len_chk_line: Length of the choke line along the riser.
    :ivar id_kill_line: Inner diameter of the kill line.
    :ivar od_kill_line: Outer diameter of the kill line.
    :ivar len_kill_line: Length of the kill line.
    :ivar type_diverter: Diverter description.
    :ivar dia_diverter: Diameter of the diverter.
    :ivar pres_work_diverter: Working rating pressure of the component.
    :ivar accumulator: Type of accumulator/description.
    :ivar cap_acc_fluid: Accumulator fluid capacity.
    :ivar pres_acc_pre_charge: Accumulator pre-charge pressure.
    :ivar vol_acc_pre_charge: Accumulator pre-charge volume
    :ivar pres_acc_op_rating: Accumulator operating pressure rating.
    :ivar type_control_manifold: The blowout preventer control system.
    :ivar desc_control_manifold: Description of the control system.
    :ivar type_choke_manifold: Type of choke manifold.
    :ivar pres_choke_manifold: Choke manifold pressure.
    :ivar bop_component:
    """

    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    model: Optional[str] = field(
        default=None,
        metadata={
            "name": "Model",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_install: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimInstall",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_remove: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimRemove",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name_tag: List[NameTag] = field(
        default_factory=list,
        metadata={
            "name": "NameTag",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_connection_bop: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeConnectionBop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    size_connection_bop: Optional[str] = field(
        default=None,
        metadata={
            "name": "SizeConnectionBop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_bop_rating: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresBopRating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    size_bop_sys: Optional[str] = field(
        default=None,
        metadata={
            "name": "SizeBopSys",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    rot_bop: Optional[bool] = field(
        default=None,
        metadata={
            "name": "RotBop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_booster_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdBoosterLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od_booster_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdBoosterLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_booster_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenBoosterLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_surf_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdSurfLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od_surf_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdSurfLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_surf_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenSurfLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_chk_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdChkLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od_chk_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdChkLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_chk_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenChkLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_kill_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdKillLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od_kill_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdKillLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_kill_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenKillLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_diverter: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeDiverter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_diverter: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaDiverter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_work_diverter: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresWorkDiverter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    accumulator: Optional[str] = field(
        default=None,
        metadata={
            "name": "Accumulator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cap_acc_fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "CapAccFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_acc_pre_charge: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresAccPreCharge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_acc_pre_charge: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolAccPreCharge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_acc_op_rating: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresAccOpRating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_control_manifold: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeControlManifold",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    desc_control_manifold: Optional[str] = field(
        default=None,
        metadata={
            "name": "DescControlManifold",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_choke_manifold: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeChokeManifold",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_choke_manifold: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresChokeManifold",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bop_component: List[BopComponent] = field(
        default_factory=list,
        metadata={
            "name": "BopComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class Borehole:
    """
    Information on the borehole.

    :ivar name: The name of the borehole.
    :ivar type_borehole: Type of borehole. etc. cavern, cavity, normal
        borehole, under ream, etc.
    :ivar md_interval: Measured depth interval for the borehole.
    :ivar tvd_interval: True vertical depth interval for the borehole.
    :ivar borehole_diameter: Borehole diameter.
    :ivar description_permanent: The description of this equipment to be
        permanently kept.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar equipment_event_history:
    :ivar uid: Unique identifier for this instance of Borehole.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_borehole: Optional[BoreholeType] = field(
        default=None,
        metadata={
            "name": "TypeBorehole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    borehole_diameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "BoreholeDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description_permanent: Optional[str] = field(
        default=None,
        metadata={
            "name": "DescriptionPermanent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    equipment_event_history: Optional[EventInfo] = field(
        default=None,
        metadata={
            "name": "EquipmentEventHistory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class CementingFluid:
    """
    Cementing Fluid Component Schema.

    :ivar etim_transitions: The elapsed time between the development of
        100lbf/100sq ft gel strength and 500lbf/100 sq ft gel strength.
    :ivar etim_zero_gel: The elapsed time from initiation of the static
        portion of the test until the slurry attains a gel strength of
        100lbf/100sq ft.
    :ivar type_fluid: Fluid type: Mud, Wash, Spacer, Slurry.
    :ivar fluid_index: Fluid Index: 1: first fluid pumped (= original
        mud), last - 1 = tail cement, last = displacement mud.
    :ivar desc_fluid: Fluid description.
    :ivar purpose: Purpose description.
    :ivar class_slurry_dry_blend: Slurry class.
    :ivar slurry_placement_interval: Measured depth interval between the
        top and base of the slurry placement.
    :ivar source_water: Water source description.
    :ivar vol_water: Volume of water.
    :ivar vol_cement: Volume of cement.
    :ivar ratio_mix_water: Mix-water ratio.
    :ivar vol_fluid: Fluid/slurry volume.
    :ivar excess_pc: Excess percent.
    :ivar vol_yield: Slurry yield.
    :ivar density: Fluid density.
    :ivar solid_volume_fraction: Equals 1 - Porosity.
    :ivar vol_pumped: Volume pumped.
    :ivar vol_other: Other volume.
    :ivar fluid_rheological_model: Specify one of these models:
        Newtonian, Bingham, Power Law, and Herschel Bulkley.
    :ivar viscosity: Viscosity (if Newtonian model) or plastic viscosity
        (if Bingham model).
    :ivar yp: Yield point (Bingham and Herschel Bulkley models).
    :ivar n: Power Law index (Power Law and Herschel Bulkley models).
    :ivar k: Consistency index (Power Law and Herschel Bulkley models).
    :ivar gel10_sec_reading: Gel reading after 10 seconds.
    :ivar gel10_sec_strength: Gel strength after 10 seconds.
    :ivar gel1_min_reading: Gel reading after 1 minute.
    :ivar gel1_min_strength: Gel strength after 1 minute.
    :ivar gel10_min_reading: Gel reading after 10 minutes.
    :ivar gel10_min_strength: Gel strength after 10 minutes.
    :ivar type_base_fluid: Type of base fluid: fresh water, sea water,
        brine, brackish water.
    :ivar dens_base_fluid: Density of base fluid.
    :ivar dry_blend_name: Name of dry blend.
    :ivar dry_blend_description: Description of dry blend.
    :ivar mass_dry_blend: Mass of dry blend: the blend is made of
        different solid additives: the volume is not constant.
    :ivar dens_dry_blend: Density of dry blend.
    :ivar mass_sack_dry_blend: Weight of a sack of dry blend.
    :ivar foam_used: Foam used?  Values are "true" (or "1") and "false"
        (or "0").
    :ivar type_gas_foam: Gas type used for foam job.
    :ivar vol_gas_foam: Volume of gas used for foam job.
    :ivar ratio_const_gas_method_av: Constant gas ratio method ratio.
    :ivar dens_const_gas_method: Constant gas ratio method: average
        density.
    :ivar ratio_const_gas_method_start: Constant gas ratio method:
        initial method ratio.
    :ivar ratio_const_gas_method_end: Constant gas ratio method: final
        method ratio.
    :ivar dens_const_gas_foam: Constant gas ratio method: average
        density.
    :ivar etim_thickening: Test thickening time.
    :ivar temp_thickening: Test thickening temperature.
    :ivar pres_test_thickening: Test thickening pressure.
    :ivar cons_test_thickening: Test thickening consistency/slurry
        viscosity: Bearden Consistency (Bc) 0 to 100.
    :ivar pc_free_water: Test free water na: = mL/250ML.
    :ivar temp_free_water: Test free water temperature.
    :ivar vol_test_fluid_loss: Test fluid loss.
    :ivar temp_fluid_loss: Test fluid loss temperature.
    :ivar pres_test_fluid_loss: Test fluid loss pressure.
    :ivar time_fluid_loss: Test fluid loss: dehydrating test period,
        used to compute the API fluid loss.
    :ivar vol_apifluid_loss: API fluid loss = 2 * volTestFluidLoss *
        SQRT(30/timefluidloss).
    :ivar etim_compr_stren1: Compressive strength time 1.
    :ivar etim_compr_stren2: Compressive strength time 2.
    :ivar pres_compr_stren1: Compressive strength pressure 1.
    :ivar pres_compr_stren2: Compressive strength pressure 2.
    :ivar temp_compr_stren1: Compressive strength temperature 1.
    :ivar temp_compr_stren2: Compressive strength temperature 2.
    :ivar dens_at_pres: Slurry density at pressure.
    :ivar vol_reserved: Volume reserved.
    :ivar vol_tot_slurry: Total Slurry Volume.
    :ivar cement_additive:
    :ivar rheometer:
    :ivar uid: Unique identifier for this cementing fluid.
    """

    etim_transitions: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimTransitions",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_zero_gel: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimZeroGel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_index: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    desc_fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "DescFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "name": "Purpose",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    class_slurry_dry_blend: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClassSlurryDryBlend",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    slurry_placement_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "SlurryPlacementInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    source_water: Optional[str] = field(
        default=None,
        metadata={
            "name": "SourceWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_water: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_cement: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolCement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ratio_mix_water: Optional[str] = field(
        default=None,
        metadata={
            "name": "RatioMixWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    excess_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExcessPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_yield: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolYield",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    density: Optional[str] = field(
        default=None,
        metadata={
            "name": "Density",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    solid_volume_fraction: Optional[str] = field(
        default=None,
        metadata={
            "name": "SolidVolumeFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_pumped: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolPumped",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_other: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolOther",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_rheological_model: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidRheologicalModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    viscosity: Optional[str] = field(
        default=None,
        metadata={
            "name": "Viscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    yp: Optional[str] = field(
        default=None,
        metadata={
            "name": "Yp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    n: Optional[str] = field(
        default=None,
        metadata={
            "name": "N",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    k: Optional[str] = field(
        default=None,
        metadata={
            "name": "K",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel10_sec_reading: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel10SecReading",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel10_sec_strength: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel10SecStrength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel1_min_reading: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel1MinReading",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel1_min_strength: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel1MinStrength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel10_min_reading: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel10MinReading",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel10_min_strength: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel10MinStrength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_base_fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeBaseFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dens_base_fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "DensBaseFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dry_blend_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "DryBlendName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dry_blend_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "DryBlendDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mass_dry_blend: Optional[str] = field(
        default=None,
        metadata={
            "name": "MassDryBlend",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dens_dry_blend: Optional[str] = field(
        default=None,
        metadata={
            "name": "DensDryBlend",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mass_sack_dry_blend: Optional[str] = field(
        default=None,
        metadata={
            "name": "MassSackDryBlend",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    foam_used: Optional[bool] = field(
        default=None,
        metadata={
            "name": "FoamUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_gas_foam: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeGasFoam",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_gas_foam: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolGasFoam",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ratio_const_gas_method_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "RatioConstGasMethodAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dens_const_gas_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "DensConstGasMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ratio_const_gas_method_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "RatioConstGasMethodStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ratio_const_gas_method_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "RatioConstGasMethodEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dens_const_gas_foam: Optional[str] = field(
        default=None,
        metadata={
            "name": "DensConstGasFoam",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_thickening: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimThickening",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_thickening: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempThickening",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_test_thickening: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresTestThickening",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cons_test_thickening: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConsTestThickening",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pc_free_water: Optional[str] = field(
        default=None,
        metadata={
            "name": "PcFreeWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_free_water: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempFreeWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_test_fluid_loss: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolTestFluidLoss",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_fluid_loss: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempFluidLoss",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_test_fluid_loss: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresTestFluidLoss",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    time_fluid_loss: Optional[str] = field(
        default=None,
        metadata={
            "name": "TimeFluidLoss",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_apifluid_loss: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolAPIFluidLoss",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_compr_stren1: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimComprStren1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_compr_stren2: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimComprStren2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_compr_stren1: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresComprStren1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_compr_stren2: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresComprStren2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_compr_stren1: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempComprStren1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_compr_stren2: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempComprStren2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dens_at_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "DensAtPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_reserved: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolReserved",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_tot_slurry: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolTotSlurry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cement_additive: List[CementAdditive] = field(
        default_factory=list,
        metadata={
            "name": "CementAdditive",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rheometer: List[Rheometer] = field(
        default_factory=list,
        metadata={
            "name": "Rheometer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Centrifuge:
    """
    Rig Centrifuge Schema.

    :ivar manufacturer: Pointer to a BusinessAssociate representing the
        manufacturer or supplier of the item.
    :ivar model: Manufacturer's designated model.
    :ivar dtim_install: Date and time the centrifuge was installed.
    :ivar dtim_remove: Date and time the centrifuge was removed.
    :ivar type_value: Description for the type of object.
    :ivar cap_flow: Maximum pump rate at which the unit efficiently
        operates.
    :ivar owner: Pointer to a BusinessAssociate representing the
        contractor/owner.
    :ivar name_tag: An identification tag for the centrifuge. A serial
        number is a type of identification tag; however, some tags
        contain many pieces of information.This element only identifies
        the tag and does not describe the contents.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Centrifuge.
    """

    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    model: Optional[str] = field(
        default=None,
        metadata={
            "name": "Model",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_install: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimInstall",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_remove: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimRemove",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cap_flow: Optional[str] = field(
        default=None,
        metadata={
            "name": "CapFlow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    owner: Optional[str] = field(
        default=None,
        metadata={
            "name": "Owner",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name_tag: List[NameTag] = field(
        default_factory=list,
        metadata={
            "name": "NameTag",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ContinuousAzimuthFormula(AzimuthFormula):
    gyro_axis: Optional[GyroAxisCombination] = field(
        default=None,
        metadata={
            "name": "GyroAxis",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class ContinuousGyro:
    axis_combination: Optional[GyroAxisCombination] = field(
        default=None,
        metadata={
            "name": "AxisCombination",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gyro_reinitialization_distance: Optional[str] = field(
        default=None,
        metadata={
            "name": "GyroReinitializationDistance",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    noise_reduction_factor: Optional[float] = field(
        default=None,
        metadata={
            "name": "NoiseReductionFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    range: Optional[PlaneAngleOperatingRange] = field(
        default=None,
        metadata={
            "name": "Range",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    speed: Optional[str] = field(
        default=None,
        metadata={
            "name": "Speed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    initialization: Optional[str] = field(
        default=None,
        metadata={
            "name": "Initialization",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class CuttingsIntervalLithology:
    """The description of a single rock type in this interval.

    Can include one or more CuttingsIntervalShow objects for hydrocarbon
    show evaluation of the individual lithology.

    :ivar kind: The geological name for the type of lithology from the
        enum table listing a subset of the OneGeology/CGI defined
        formation types.
    :ivar lith_pc: Lithology percent. Represents the portion of the
        sampled interval this lithology type relates to. The total of
        the lithologies within an interval should add up to 100 percent.
        If LithologySource in geology is: - "interpreted" only 100% is
        allowed. - "core" or "cuttings" then recommended usage is that
        the creating application uses blocks of 10%. i.e. 10, 20, 30,
        40, 50, 60, 70, 80, 90, 100. Ideally the input application
        should enforce a total of 100% for each defined depth interval.
        If the total for a depth interval does not add up to 100%, then
        use the "undifferentiated" code to fill out to 100%.
    :ivar citation: An ISO 19115 EIP-derived set of metadata attached to
        ensure the traceability of the CuttingsIntervalLithology.
    :ivar code_lith: An optional custom lithology encoding scheme. If
        used, it is recommended that the scheme follows the NPD required
        usage. With the numeric values noted in the enum tables, which
        was the original intent for this item. The NPD Coding System
        assigns a digital code to the main lithologies as per the
        Norwegian Blue Book data standards. The code was then derived by
        lithology = (main lithology * 10) + cement + (modifier / 100).
        Example: Calcite cemented silty micaceous sandstone: (33 * 10) +
        1 + (21 / 100) gives a numeric code of 331.21. However, the NPD
        is also working through Energistics/Caesar to potentially change
        this usage.) This scheme should not be used for mnemonics,
        because those vary by operator, and if an abbreviation is
        required, a local look-up table should be used by the rendering
        client, based on Lithology Type.
    :ivar color: STRUCTURED DESCRIPTION USAGE. Lithology color
        description, from Shell 1995 4.3.3.1 and 4.3.3.2 colors with the
        addition of: frosted. e.g., black, blue, brown, buff, green,
        grey, olive, orange, pink, purple, red, translucent, frosted,
        white, yellow; modified by: dark, light, moderate, medium,
        mottled, variegated, slight, weak, strong, and vivid.
    :ivar texture: STRUCTURED DESCRIPTION USAGE. Lithology matrix
        texture description from Shell 1995 4.3.2.6: crystalline, (often
        "feather-edge" appearance on breaking), friable, dull, earthy,
        chalky, (particle size less than 20m; often exhibits capillary
        imbibition) visibly particulate, granular, sucrosic, (often
        exhibits capillary imbibition). Examples: compact interlocking,
        particulate, (Gradational textures are quite common.) chalky
        matrix with sucrosic patches, (Composite textures also occur).
    :ivar hardness: STRUCTURED DESCRIPTION USAGE. Mineral hardness.
        Typically, this element is rarely used because mineral hardness
        is not typically recorded. What typically is recorded is
        compaction. However, this element is retained for use defined as
        per Mohs scale of mineral hardness.
    :ivar compaction: STRUCTURED DESCRIPTION USAGE. Lithology compaction
        from Shell 1995 4.3.1.5, which includes: not compacted, slightly
        compacted, compacted, strongly compacted, friable, indurated,
        hard.
    :ivar size_grain: STRUCTURED DESCRIPTION USAGE. Lithology grain size
        description. Defined from Shell 4.3.1.1.(Wentworth) modified to
        remove the ambiguous term pelite. Size ranges in millimeter (or
        micrometer) and inches. LT 256 mm        LT 10.1 in
        "boulder" 64-256 mm        2.5–10.1 in        "cobble"; 32–64 mm
        1.26–2.5 in       "very coarse gravel" 16–32 mm        0.63–1.26
        in        "coarse gravel" 8–16 mm            0.31–0.63 in
        "medium gravel" 4–8 mm            0.157–0.31 in        "fine
        gravel" 2–4 mm            0.079–0.157 in     "very fine gravel"
        1–2 mm           0.039–0.079 in    "very coarse sand" 0.5–1 mm
        0.020–0.039 in        "coarse sand" 0.25–0.5 mm
        0.010–0.020 in     "medium sand" 125–250 um        0.0049–0.010
        in        "fine sand" 62.5–125 um      .0025–0.0049 in   "very
        fine sand" 3.90625–62.5 um        0.00015–0.0025 in    "silt" LT
        3.90625 um        LT 0.00015 in        "clay" LT 1 um
        LT 0.000039 in        "colloid"
    :ivar roundness: STRUCTURED DESCRIPTION USAGE. Lithology roundness
        description from Shell 4.3.1.3. Roundness refers to modal size
        class: very angular, angular, subangular, subrounded, rounded,
        well rounded.
    :ivar sphericity: STRUCTURED DESCRIPTION USAGE. Lithology sphericity
        description for the modal size class of grains in the sample,
        defined as per Shell 4.3.1.4 Sphericity: very elongated,
        elongated, slightly elongated, slightly spherical, spherical,
        very spherical.
    :ivar sorting: STRUCTURED DESCRIPTION USAGE. Lithology sorting
        description from Shell 4.3.1.2 Sorting: very poorly sorted,
        unsorted, poorly sorted, poorly to moderately well sorted,
        moderately well sorted, well sorted, very well sorted,
        unimodally sorted, bimodally sorted.
    :ivar matrix_cement: STRUCTURED DESCRIPTION USAGE. Lithology
        matrix/cement description. Terms will be as defined in the
        enumeration table. e.g., "calcite" (Common) "dolomite",
        "ankerite" (e.g., North Sea HPHT reservoirs such as Elgin and
        Franklin have almost pure ankerite cementation) "siderite"
        (Sherwood sandstones, southern UK typical Siderite cements),
        "quartz" (grain-to-grain contact cementation or secondary quartz
        deposition), "kaolinite", "illite" (e.g., Village Fields North
        Sea), "smectite","chlorite" (Teg, Algeria.).
    :ivar porosity_visible: STRUCTURED DESCRIPTION USAGE. Lithology
        visible porosity description. Defined after BakerHughes
        definitions, as opposed to Shell, which has no linkage to actual
        numeric estimates. The theoretical maximum porosity for a
        clastic rock is about 26%, which is normally much reduced by
        other factors. When estimating porosities use: more than 15%
        "good"; 10 to 15% "fair"; 5 to 10% "poor"; less than 5% "trace";
        0 "none".
    :ivar porosity_fabric: STRUCTURED DESCRIPTION USAGE. Visible
        porosity fabric description from after Shell 4.3.2.1 and
        4.3.2.2: intergranular (particle size greater than 20m), fine
        interparticle (particle size less than 20m), intercrystalline,
        intragranular, intraskeletal, intracrystalline, mouldic,
        fenestral, shelter, framework, stylolitic, replacement,
        solution, vuggy, channel, cavernous.
    :ivar permeability: STRUCTURED DESCRIPTION USAGE. Lithology
        permeability description from Shell 4.3.2.5. In the future,
        these values would benefit from quantification, e.g., tight,
        slightly, fairly, highly.
    :ivar shows:
    :ivar qualifier:
    :ivar uid: Unique identifier for this instance of
        CuttingsIntervalLithology.
    """

    kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    lith_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "LithPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    citation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Citation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    code_lith: Optional[str] = field(
        default=None,
        metadata={
            "name": "CodeLith",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    color: Optional[str] = field(
        default=None,
        metadata={
            "name": "Color",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    texture: Optional[str] = field(
        default=None,
        metadata={
            "name": "Texture",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hardness: Optional[str] = field(
        default=None,
        metadata={
            "name": "Hardness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    compaction: Optional[str] = field(
        default=None,
        metadata={
            "name": "Compaction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    size_grain: Optional[str] = field(
        default=None,
        metadata={
            "name": "SizeGrain",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    roundness: Optional[str] = field(
        default=None,
        metadata={
            "name": "Roundness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sphericity: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sphericity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sorting: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sorting",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    matrix_cement: Optional[str] = field(
        default=None,
        metadata={
            "name": "MatrixCement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    porosity_visible: Optional[str] = field(
        default=None,
        metadata={
            "name": "PorosityVisible",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    porosity_fabric: Optional[str] = field(
        default=None,
        metadata={
            "name": "PorosityFabric",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    permeability: Optional[str] = field(
        default=None,
        metadata={
            "name": "Permeability",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    shows: List[CuttingsIntervalShow] = field(
        default_factory=list,
        metadata={
            "name": "Shows",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    qualifier: List[LithologyQualifier] = field(
        default_factory=list,
        metadata={
            "name": "Qualifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class DayCost:
    """Day Cost SchemaSchema.

    Captures daily cost information for the object (cost item) to which
    it is attached.

    :ivar num_afe: AFE number that this cost item applies to.
    :ivar cost_group: Cost group code.
    :ivar cost_class: Cost class code.
    :ivar cost_code: Cost code.
    :ivar cost_sub_code: Cost subcode.
    :ivar cost_item_description: Description of the cost item.
    :ivar item_kind: The kind of cost item specified (e.g., rig dayrate,
        joints casing).
    :ivar item_size: Size of one cost item.
    :ivar qty_item: Number of cost items used that day, e.g., 1 rig
        dayrate, 30 joints of casing.
    :ivar num_invoice: Invoice number for cost item; the  bill is sent
        to the operator.
    :ivar num_po: Purchase order number provided by the operator.
    :ivar num_ticket: The field ticket number issued by the service
        company on location.
    :ivar is_carry_over: Is this item carried from day to day? Values
        are "true" (or "1") and "false" (or "0").
    :ivar is_rental: Is this item a rental? Values are "true" (or "1")
        and "false" (or "0").
    :ivar name_tag: An identification tag for the item. A serial number
        is a type of identification tag; however, some tags contain many
        pieces of information. This element only identifies the tag and
        does not describe the contents.
    :ivar num_serial: Serial number.
    :ivar vendor: Pointer to a BusinessAssociate representing the
        vendor.
    :ivar num_vendor: Vendor number.
    :ivar pool: Name of pool/reservoir that this cost item can be
        accounted to.
    :ivar estimated: Is this an estimated cost? Values are "true" (or
        "1") and "false" (or "0").
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar cost_amount: Cost for the item for this record.
    :ivar cost_per_item: Cost of each cost item, assume same currency.
    :ivar uid: Unique identifier for this instance of DayCost
    """

    num_afe: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumAFE",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cost_group: Optional[str] = field(
        default=None,
        metadata={
            "name": "CostGroup",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cost_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "CostClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    cost_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CostCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    cost_sub_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CostSubCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cost_item_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "CostItemDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    item_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "ItemKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    item_size: Optional[float] = field(
        default=None,
        metadata={
            "name": "ItemSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    qty_item: Optional[float] = field(
        default=None,
        metadata={
            "name": "QtyItem",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_invoice: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumInvoice",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_po: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumPO",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_ticket: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumTicket",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_carry_over: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsCarryOver",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_rental: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsRental",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name_tag: List[NameTag] = field(
        default_factory=list,
        metadata={
            "name": "NameTag",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_serial: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumSerial",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vendor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Vendor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_vendor: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumVendor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pool: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    estimated: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Estimated",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cost_amount: Optional[str] = field(
        default=None,
        metadata={
            "name": "CostAmount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cost_per_item: Optional[str] = field(
        default=None,
        metadata={
            "name": "CostPerItem",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Degasser:
    """
    Rig Degasser Schema.

    :ivar manufacturer: Pointer to a BusinessAssociate representing the
        manufacturer or supplier of the item.
    :ivar model: Manufacturer's designated model.
    :ivar dtim_install: Date and time the degasser was installed.
    :ivar dtim_remove: Date and time the degasser was removed.
    :ivar type_value: Description for the type of object.
    :ivar owner: Pointer to a BusinessAssociate representing the
        contractor/owner.
    :ivar height: Height of the separator.
    :ivar len: Length of the separator.
    :ivar id: Internal diameter of the object.
    :ivar cap_flow: Maximum pump rate at which the unit efficiently
        operates.
    :ivar area_separator_flow: Flow area of the separator.
    :ivar ht_mud_seal: Depth of trip-tank fluid level to provide back
        pressure against the separator flow.
    :ivar id_inlet: Internal diameter of the inlet line.
    :ivar id_vent_line: Internal diameter of the vent line.
    :ivar len_vent_line: Length of the vent line.
    :ivar cap_gas_sep: Safe gas-separating capacity.
    :ivar cap_blowdown: Gas vent rate at which the vent line pressure
        drop exceeds the hydrostatic head because of the mud seal.
    :ivar pres_rating: Pressure rating of the item.
    :ivar temp_rating: Temperature rating of the separator.
    :ivar name_tag: An identification tag for the degasser. A serial
        number is a type of identification tag; however, some tags
        contain many pieces of information.This element only identifies
        the tag and does not describe the contents.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of degasser
    """

    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    model: Optional[str] = field(
        default=None,
        metadata={
            "name": "Model",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_install: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimInstall",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_remove: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimRemove",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    owner: Optional[str] = field(
        default=None,
        metadata={
            "name": "Owner",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    height: Optional[str] = field(
        default=None,
        metadata={
            "name": "Height",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len: Optional[str] = field(
        default=None,
        metadata={
            "name": "Len",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cap_flow: Optional[str] = field(
        default=None,
        metadata={
            "name": "CapFlow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    area_separator_flow: Optional[str] = field(
        default=None,
        metadata={
            "name": "AreaSeparatorFlow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ht_mud_seal: Optional[str] = field(
        default=None,
        metadata={
            "name": "HtMudSeal",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_inlet: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdInlet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_vent_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdVentLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_vent_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenVentLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cap_gas_sep: Optional[str] = field(
        default=None,
        metadata={
            "name": "CapGasSep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cap_blowdown: Optional[str] = field(
        default=None,
        metadata={
            "name": "CapBlowdown",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_rating: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresRating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_rating: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempRating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name_tag: List[NameTag] = field(
        default_factory=list,
        metadata={
            "name": "NameTag",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DepthRegLogRect:
    """
    A region of an image containing a log rectangle.

    :ivar type_value: A region of an image containing a log section
        image.
    :ivar name: The name of a rectangular section.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar position:
    :ivar uid: Unique identifier for the log section.
    """

    type_value: Optional[LogRectangleType] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    position: Optional[DepthRegRectangle] = field(
        default=None,
        metadata={
            "name": "Position",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DepthRegTrackCurve:
    """
    Descriptions of the actual curve, including elements such as line weight,
    color, and style, within a log track.

    :ivar curve_info: Curve mnemonic
    :ivar line_style: Image line style
    :ivar line_weight: Description of line graveness
    :ivar line_color: Color of this line
    :ivar curve_scale_type: Scale linearity
    :ivar curve_unit: Unit of data represented
    :ivar curve_left_scale_value: Scale value on the left axis
    :ivar curve_right_scale_value: Scale value on the right axis
    :ivar curve_backup_scale_type: Scale of the backup curve
    :ivar curve_scale_rect: Coordinates of rectangle representing the
        area describing the scale.
    :ivar description: Details of the line
    :ivar uid: Unique identifier for the curve.
    """

    curve_info: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurveInfo",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    line_style: Optional[LineStyle] = field(
        default=None,
        metadata={
            "name": "LineStyle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    line_weight: Optional[str] = field(
        default=None,
        metadata={
            "name": "LineWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    line_color: Optional[str] = field(
        default=None,
        metadata={
            "name": "LineColor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    curve_scale_type: Optional[ScaleType] = field(
        default=None,
        metadata={
            "name": "CurveScaleType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    curve_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurveUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    curve_left_scale_value: Optional[float] = field(
        default=None,
        metadata={
            "name": "CurveLeftScaleValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    curve_right_scale_value: Optional[float] = field(
        default=None,
        metadata={
            "name": "CurveRightScaleValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    curve_backup_scale_type: Optional[BackupScaleType] = field(
        default=None,
        metadata={
            "name": "CurveBackupScaleType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    curve_scale_rect: List[DepthRegRectangle] = field(
        default_factory=list,
        metadata={
            "name": "CurveScaleRect",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EquipmentConnection(Connection):
    """
    Information detailing the connection between two components.

    :ivar equipment: Reference to the string equipment.
    :ivar radial_offset: Measurement of radial offset.
    :ivar connection_form: The form of connection: box or pin.
    :ivar connection_upset: Connection upset.
    :ivar connection_type:
    """

    equipment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Equipment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    radial_offset: Optional[str] = field(
        default=None,
        metadata={
            "name": "RadialOffset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    connection_form: Optional[ConnectionFormType] = field(
        default=None,
        metadata={
            "name": "ConnectionForm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    connection_upset: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConnectionUpset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    connection_type: Optional[AbstractConnectionType] = field(
        default=None,
        metadata={
            "name": "ConnectionType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class EquipmentSet:
    """
    Information on the collection of equipment.
    """

    equipment: List[Equipment] = field(
        default_factory=list,
        metadata={
            "name": "Equipment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class Fluid:
    """
    Fluid component schema.

    :ivar type_value: Description for the type of fluid.
    :ivar location_sample: Sample location.
    :ivar dtim: The time when fluid readings were recorded.
    :ivar md: The measured depth where the fluid readings were recorded.
    :ivar tvd: The true vertical depth where the fluid readings were
        recorded.
    :ivar ecd: Equivalent circulating density where fluid reading was
        recorded.
    :ivar kick_tolerance_volume: Assumed kick volume for calculation of
        kick tolerance based on the kick intensity where the fluid
        reading was recorded.
    :ivar kick_tolerance_intensity: Assumed kick density for calculation
        of kick tolerance where the fluid reading was recorded.
    :ivar temp_flow_line: Flow line temperature measurement where the
        fluid reading was recorded.
    :ivar pres_bop_rating: Maximum pressure rating of the blow out
        preventer.
    :ivar mud_class: The class of the drilling fluid.
    :ivar density: Fluid density.
    :ivar vis_funnel: Funnel viscosity in seconds.
    :ivar temp_vis: Funnel viscosity temperature.
    :ivar pv: Plastic viscosity.
    :ivar yp: Yield point (Bingham and Herschel Bulkley models).
    :ivar gel3_sec: Three-second gels.
    :ivar gel6_sec: Six-second gels.
    :ivar gel10_sec: Ten-second gels.
    :ivar gel10_min: Ten-minute gels.
    :ivar gel30_min: Thirty-minute gels.
    :ivar filter_cake_ltlp: Filter cake thickness at low (normal)
        temperature and pressure.
    :ivar filtrate_ltlp: API water loss (low temperature and pressure
        mud filtrate measurement) (volume per 30 min).
    :ivar temp_hthp: High temperature high pressure (HTHP) temperature.
    :ivar pres_hthp: High temperature high pressure (HTHP) pressure.
    :ivar filtrate_hthp: High temperature high pressure (HTHP) filtrate
        (volume per 30 min).
    :ivar filter_cake_hthp: High temperature high pressure (HTHP) filter
        cake thickness.
    :ivar solids_pc: Solids percentage from retort.
    :ivar water_pc: Water content percent.
    :ivar oil_pc: Percent oil content from retort.
    :ivar sand_pc: Sand content percent.
    :ivar solids_low_grav_pc: Low gravity solids percent.
    :ivar solids_low_grav: Solids low gravity content.
    :ivar solids_calc_pc: Percent calculated solids content.
    :ivar barite_pc: Barite content percent.
    :ivar lcm: Lost circulation material.
    :ivar mbt: Cation exchange capacity (CEC) of the mud sample as
        measured by methylene blue titration (MBT).
    :ivar ph: Mud pH.
    :ivar temp_ph: Mud pH measurement temperature.
    :ivar pm: Phenolphthalein alkalinity of whole mud.
    :ivar pm_filtrate: Phenolphthalein alkalinity of mud filtrate.
    :ivar mf: Methyl orange alkalinity of filtrate.
    :ivar alkalinity_p1: Mud alkalinity P1 from alternate alkalinity
        method (volume in ml of 0.02N acid to reach the phenolphthalein
        endpoint).
    :ivar alkalinity_p2: Mud alkalinity P2 from alternate alkalinity
        method (volume in ml of 0.02N acid to titrate, the reagent
        mixture to the phenolphthalein endpoint).
    :ivar chloride: Chloride content.
    :ivar calcium: Calcium content.
    :ivar magnesium: Magnesium content.
    :ivar potassium: Potassium content.
    :ivar brine_pc: Percent brine content.
    :ivar brine_density: Density of water phase of NAF.
    :ivar brine_class: Class of Brine.
    :ivar lime: Lime content.
    :ivar elect_stab: Measurement of the emulsion stability and oil-
        wetting capability in oil-based muds.
    :ivar calcium_chloride_pc: Calcium chloride percent.
    :ivar calcium_chloride: Calcium chloride content.
    :ivar company: Pointer to a BusinessAssociate representing the
        company.
    :ivar engineer: Engineer name
    :ivar asg: Average specific gravity of solids.
    :ivar solids_hi_grav_pc: Solids high gravity percent.
    :ivar solids_hi_grav: Solids high gravity content.
    :ivar polymer: Polymers present in the mud system.
    :ivar poly_type: Type of polymers present in the mud system.
    :ivar sol_cor_pc: Solids corrected for chloride content percent.
    :ivar oil_ctg: Oil on cuttings.
    :ivar oil_ctg_dry: Oil on dried cuttings.
    :ivar hardness_ca: Total calcium hardness.
    :ivar sulfide: Sulfide content.
    :ivar average_cutting_size: Average size of the drill cuttings.
    :ivar carbonate: Carbonate content.
    :ivar iron: Iron content.
    :ivar metal_recovered: Metal recovered from the wellbore.
    :ivar turbidity: Turbidity units to measure the cloudiness or
        haziness of a fluid.
    :ivar oil_grease: Oil and grease content.
    :ivar salt: Salt content.
    :ivar salt_pc: Salt percent.
    :ivar tct: True crystallization temperature.
    :ivar water_phase_salinity: A factor showing the activity level of
        salt in oil-based mud.
    :ivar whole_mud_calcium: Calcium content in the whole mud sample,
        including oil and water phases.
    :ivar whole_mud_chloride: Chloride content in the whole mud sample,
        including oil and water phases.
    :ivar zinc_oxide: Zinc oxide content.
    :ivar sodium_chloride: Sodium chloride content.
    :ivar sodium_chloride_pc: Sodium chloride percent.
    :ivar ppt_spurt_loss: Permeability Plugging Test spurt loss.
    :ivar ppt_pressure: Permeability Plugging Test pressure.
    :ivar ppt_temperature: Permeability Plugging Test temperature.
    :ivar comments: Comments and remarks.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar rheometer:
    :ivar uid: Unique identifier for this instance of Fluid.
    """

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    location_sample: Optional[str] = field(
        default=None,
        metadata={
            "name": "LocationSample",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md: Optional[str] = field(
        default=None,
        metadata={
            "name": "Md",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tvd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ecd: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ecd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    kick_tolerance_volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "KickToleranceVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    kick_tolerance_intensity: Optional[str] = field(
        default=None,
        metadata={
            "name": "KickToleranceIntensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_flow_line: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempFlowLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_bop_rating: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresBopRating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mud_class: Optional[MudType] = field(
        default=None,
        metadata={
            "name": "MudClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    density: Optional[str] = field(
        default=None,
        metadata={
            "name": "Density",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vis_funnel: Optional[str] = field(
        default=None,
        metadata={
            "name": "VisFunnel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_vis: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempVis",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pv: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    yp: Optional[str] = field(
        default=None,
        metadata={
            "name": "Yp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel3_sec: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel3Sec",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel6_sec: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel6Sec",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel10_sec: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel10Sec",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel10_min: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel10Min",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gel30_min: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gel30Min",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    filter_cake_ltlp: Optional[str] = field(
        default=None,
        metadata={
            "name": "FilterCakeLtlp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    filtrate_ltlp: Optional[str] = field(
        default=None,
        metadata={
            "name": "FiltrateLtlp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_hthp: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempHthp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_hthp: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresHthp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    filtrate_hthp: Optional[str] = field(
        default=None,
        metadata={
            "name": "FiltrateHthp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    filter_cake_hthp: Optional[str] = field(
        default=None,
        metadata={
            "name": "FilterCakeHthp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    solids_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SolidsPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    water_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "WaterPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    oil_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "OilPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sand_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SandPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    solids_low_grav_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SolidsLowGravPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    solids_low_grav: Optional[str] = field(
        default=None,
        metadata={
            "name": "SolidsLowGrav",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    solids_calc_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SolidsCalcPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    barite_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "BaritePc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lcm: Optional[str] = field(
        default=None,
        metadata={
            "name": "Lcm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mbt: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mbt",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ph: Optional[float] = field(
        default=None,
        metadata={
            "name": "Ph",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_ph: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempPh",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pm: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pm_filtrate: Optional[str] = field(
        default=None,
        metadata={
            "name": "PmFiltrate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mf: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mf",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    alkalinity_p1: Optional[str] = field(
        default=None,
        metadata={
            "name": "AlkalinityP1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    alkalinity_p2: Optional[str] = field(
        default=None,
        metadata={
            "name": "AlkalinityP2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    chloride: Optional[str] = field(
        default=None,
        metadata={
            "name": "Chloride",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    calcium: Optional[str] = field(
        default=None,
        metadata={
            "name": "Calcium",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    magnesium: Optional[str] = field(
        default=None,
        metadata={
            "name": "Magnesium",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    potassium: Optional[str] = field(
        default=None,
        metadata={
            "name": "Potassium",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    brine_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "BrinePc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    brine_density: Optional[str] = field(
        default=None,
        metadata={
            "name": "BrineDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    brine_class: Optional[Union[BrineType, str]] = field(
        default=None,
        metadata={
            "name": "BrineClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lime: Optional[str] = field(
        default=None,
        metadata={
            "name": "Lime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    elect_stab: Optional[str] = field(
        default=None,
        metadata={
            "name": "ElectStab",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    calcium_chloride_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "CalciumChloridePc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    calcium_chloride: Optional[str] = field(
        default=None,
        metadata={
            "name": "CalciumChloride",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    company: Optional[str] = field(
        default=None,
        metadata={
            "name": "Company",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    engineer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Engineer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    asg: Optional[str] = field(
        default=None,
        metadata={
            "name": "Asg",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    solids_hi_grav_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SolidsHiGravPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    solids_hi_grav: Optional[str] = field(
        default=None,
        metadata={
            "name": "SolidsHiGrav",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    polymer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Polymer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    poly_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "PolyType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sol_cor_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SolCorPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    oil_ctg: Optional[str] = field(
        default=None,
        metadata={
            "name": "OilCtg",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    oil_ctg_dry: Optional[str] = field(
        default=None,
        metadata={
            "name": "OilCtgDry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hardness_ca: Optional[str] = field(
        default=None,
        metadata={
            "name": "HardnessCa",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sulfide: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sulfide",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    average_cutting_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "AverageCuttingSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    carbonate: Optional[str] = field(
        default=None,
        metadata={
            "name": "Carbonate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    iron: Optional[str] = field(
        default=None,
        metadata={
            "name": "Iron",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    metal_recovered: Optional[str] = field(
        default=None,
        metadata={
            "name": "MetalRecovered",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    turbidity: Optional[float] = field(
        default=None,
        metadata={
            "name": "Turbidity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    oil_grease: Optional[str] = field(
        default=None,
        metadata={
            "name": "OilGrease",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    salt: Optional[str] = field(
        default=None,
        metadata={
            "name": "Salt",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    salt_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SaltPc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tct: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tct",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    water_phase_salinity: Optional[str] = field(
        default=None,
        metadata={
            "name": "WaterPhaseSalinity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    whole_mud_calcium: Optional[str] = field(
        default=None,
        metadata={
            "name": "WholeMudCalcium",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    whole_mud_chloride: Optional[str] = field(
        default=None,
        metadata={
            "name": "WholeMudChloride",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    zinc_oxide: Optional[str] = field(
        default=None,
        metadata={
            "name": "ZincOxide",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sodium_chloride: Optional[str] = field(
        default=None,
        metadata={
            "name": "SodiumChloride",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sodium_chloride_pc: Optional[str] = field(
        default=None,
        metadata={
            "name": "SodiumChloridePc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ppt_spurt_loss: Optional[str] = field(
        default=None,
        metadata={
            "name": "PptSpurtLoss",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ppt_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "PptPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    ppt_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "PptTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rheometer: List[Rheometer] = field(
        default_factory=list,
        metadata={
            "name": "Rheometer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class GravelPackInterval:
    """
    The location/interval of the gravel pack, including its history.

    :ivar downhole_string: Reference to the downhole string that denotes
        the interval of the gravel pack.
    :ivar gravel_pack_md_interval: Gravel packed measured depth interval
        for this completion.
    :ivar gravel_pack_tvd_interval: Gravel packed true vertical depth
        interval for this completion.
    :ivar event_history: The contactInterval event information.
    :ivar geology_feature: Reference to a geology feature.
    :ivar geologic_unit_interpretation: Reference to a RESQML geologic
        unit interpretation.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar status_history:
    :ivar uid: Unique identifier for this instance of
        GravelPackInterval.
    """

    downhole_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "DownholeString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gravel_pack_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "GravelPackMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gravel_pack_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "GravelPackTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    event_history: Optional[EventInfo] = field(
        default=None,
        metadata={
            "name": "EventHistory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    geology_feature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GeologyFeature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    geologic_unit_interpretation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GeologicUnitInterpretation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    status_history: List[IntervalStatusHistory] = field(
        default_factory=list,
        metadata={
            "name": "StatusHistory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Hydrocyclone:
    """Rig Hydrocyclones Schema.

    A hydrocyclone is a cone-shaped device for separating fluids and the
    solids dispersed in fluids.

    :ivar manufacturer: Pointer to a BusinessAssociate representing the
        manufacturer or supplier of the item.
    :ivar model: Manufacturer's designated model.
    :ivar dtim_install: Date and time the hydroclone was installed.
    :ivar dtim_remove: Removal date and time the hydroclone was removed.
    :ivar type_value: Description of the type of object.
    :ivar desc_cone: Cone description.
    :ivar owner: Pointer to a BusinessAssociate representing the
        contractor/owner.
    :ivar name_tag: An identification tag for the hydrocyclone. A serial
        number is a type of identification tag; however, some tags
        contain many pieces of information. This element only identifies
        the tag and does not describe the contents.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Hydrocyclone.
    """

    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    model: Optional[str] = field(
        default=None,
        metadata={
            "name": "Model",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_install: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimInstall",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_remove: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimRemove",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    desc_cone: Optional[str] = field(
        default=None,
        metadata={
            "name": "DescCone",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    owner: Optional[str] = field(
        default=None,
        metadata={
            "name": "Owner",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name_tag: List[NameTag] = field(
        default_factory=list,
        metadata={
            "name": "NameTag",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Motor:
    """Tubular Motor Component Schema.

    Used to capture properties about a motor used in a tubular string.

    :ivar offset_tool: Tool offset from bottom.
    :ivar pres_loss_fact: Pressure loss factor.
    :ivar flowrate_mn: Minimum flow rate.
    :ivar flowrate_mx: Maximum flow rate.
    :ivar dia_rotor_nozzle: Diameter of rotor at nozzle.
    :ivar clearance_bear_box: Clearance inside bearing box.
    :ivar lobes_rotor: Number of rotor lobes.
    :ivar lobes_stator: Number of stator lobes.
    :ivar type_bearing: Type of bearing.
    :ivar temp_op_mx: Maximum operating temperature.
    :ivar rotor_catcher: Is rotor catcher present? Values are "true" (or
        "1") and "false" (or "0").
    :ivar dump_valve: Is dump valve present? Values are "true" (or "1")
        and "false" (or "0").
    :ivar dia_nozzle: Nozzle diameter.
    :ivar rotatable: Is motor rotatable? Values are "true" (or "1") and
        "false" (or "0").
    :ivar bend_settings_mn: Minimum bend angle setting.
    :ivar bend_settings_mx: Maximum bend angle setting.
    :ivar sensor:
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    """

    offset_tool: Optional[str] = field(
        default=None,
        metadata={
            "name": "OffsetTool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_loss_fact: Optional[float] = field(
        default=None,
        metadata={
            "name": "PresLossFact",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_rotor_nozzle: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaRotorNozzle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    clearance_bear_box: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClearanceBearBox",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lobes_rotor: Optional[int] = field(
        default=None,
        metadata={
            "name": "LobesRotor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lobes_stator: Optional[int] = field(
        default=None,
        metadata={
            "name": "LobesStator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_bearing: Optional[BearingType] = field(
        default=None,
        metadata={
            "name": "TypeBearing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_op_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempOpMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rotor_catcher: Optional[bool] = field(
        default=None,
        metadata={
            "name": "RotorCatcher",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dump_valve: Optional[bool] = field(
        default=None,
        metadata={
            "name": "DumpValve",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dia_nozzle: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiaNozzle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rotatable: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Rotatable",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bend_settings_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "BendSettingsMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bend_settings_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "BendSettingsMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sensor: List[Sensor] = field(
        default_factory=list,
        metadata={
            "name": "Sensor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class MudGas:
    """
    Information on gas in the mud and gas peak.
    """

    gas_in_mud: Optional[GasInMud] = field(
        default=None,
        metadata={
            "name": "GasInMud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    gas_peak: List[GasPeak] = field(
        default_factory=list,
        metadata={
            "name": "GasPeak",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class MudPump:
    """
    Rig Mud Pump Schema.

    :ivar index: Relative pump number. One-based.
    :ivar manufacturer: Pointer to a BusinessAssociate representing the
        manufacturer or supplier of the item.
    :ivar model: Manufacturer's designated model.
    :ivar dtim_install: Date and time the pump was installed.
    :ivar dtim_remove: Date and time the pump was removed.
    :ivar owner: Pointer to a BusinessAssociate representing the
        contractor/owner.
    :ivar type_pump: Pump type reference list.
    :ivar num_cyl: Number of cylinders (3 = single acting, 2 = double
        acting)
    :ivar od_rod: Rod outer diameter.
    :ivar id_liner: Inner diameter of the pump liner.
    :ivar pump_action: Pump action. 1 = single acting, 2 = double
        acting.
    :ivar eff: Efficiency of the pump.
    :ivar len_stroke: Stroke length.
    :ivar pres_mx: Maximum pump pressure.
    :ivar pow_hyd_mx: Maximum hydraulics horsepower.
    :ivar spm_mx: Maximum speed.
    :ivar displacement: Pump displacement.
    :ivar pres_damp: Pulsation dampener pressure.
    :ivar vol_damp: Pulsation dampener volume.
    :ivar pow_mech_mx: Maximum mechanical power.
    :ivar name_tag: An identification tag for the pump. A serial number
        is a type of identification tag; however, some tags contain many
        pieces of information.This element onlyidentifies the tag and
        does not describe the contents.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of MudPump.
    """

    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    model: Optional[str] = field(
        default=None,
        metadata={
            "name": "Model",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_install: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimInstall",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_remove: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimRemove",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    owner: Optional[str] = field(
        default=None,
        metadata={
            "name": "Owner",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_pump: Optional[PumpType] = field(
        default=None,
        metadata={
            "name": "TypePump",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_cyl: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumCyl",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od_rod: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdRod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_liner: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdLiner",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    pump_action: Optional[str] = field(
        default=None,
        metadata={
            "name": "PumpAction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "pattern": r".+",
        },
    )
    eff: Optional[str] = field(
        default=None,
        metadata={
            "name": "Eff",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_stroke: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenStroke",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pow_hyd_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "PowHydMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    spm_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpmMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    displacement: Optional[str] = field(
        default=None,
        metadata={
            "name": "Displacement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    pres_damp: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresDamp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vol_damp: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolDamp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pow_mech_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "PowMechMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name_tag: List[NameTag] = field(
        default_factory=list,
        metadata={
            "name": "NameTag",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MwdTool:
    """Tubular MWD Tool Component Schema.

    Used to capture operating parameters of the MWD tool.

    :ivar flowrate_mn: Minimum flow rate.
    :ivar flowrate_mx: Maximum flow rate.
    :ivar temp_mx: Maximum Temperature.
    :ivar id_equv: Equivalent inner diameter.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar sensor:
    """

    flowrate_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temp_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "TempMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_equv: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdEquv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    sensor: List[Sensor] = field(
        default_factory=list,
        metadata={
            "name": "Sensor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class OpenHoleInterval:
    """
    The location/interval of the open hole and its history.

    :ivar borehole_string: Reference to a borehole (the as-drilled hole
        through the earth).
    :ivar open_hole_md_interval: Openhole measured depth interval for
        this completion.
    :ivar open_hole_tvd_interval: Openhole true vertical depth interval
        for this completion.
    :ivar event_history: The OpenHoleInterval event information.
    :ivar geology_feature: Reference to a geology feature.
    :ivar geologic_unit_interpretation: Reference to a RESQML geologic
        unit interpretation.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar status_history:
    :ivar uid: Unique identifier for this instance of OpenHoleInterval.
    """

    borehole_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "BoreholeString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    open_hole_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "OpenHoleMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    open_hole_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "OpenHoleTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    event_history: Optional[EventInfo] = field(
        default=None,
        metadata={
            "name": "EventHistory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    geology_feature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GeologyFeature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    geologic_unit_interpretation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GeologicUnitInterpretation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    status_history: List[IntervalStatusHistory] = field(
        default_factory=list,
        metadata={
            "name": "StatusHistory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Participant:
    """
    Information on WITSML objects used.

    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar participant:
    """

    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    participant: List[MemberObject] = field(
        default_factory=list,
        metadata={
            "name": "Participant",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class PassIndexedDepthInterval:
    datum: Optional[str] = field(
        default=None,
        metadata={
            "name": "Datum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    start: Optional[PassIndexedDepth] = field(
        default=None,
        metadata={
            "name": "Start",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    end: Optional[PassIndexedDepth] = field(
        default=None,
        metadata={
            "name": "End",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class PerforatingExtension(AbstractEventExtension):
    """
    Information on the perforating event.

    :ivar perforation_set: The perforationSet reference.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar perforating:
    """

    perforation_set: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforating: List[Perforating] = field(
        default_factory=list,
        metadata={
            "name": "Perforating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class PerforationSet:
    """
    Information regarding a collection of perforations.

    :ivar borehole_string: Reference to the borehole that contains the
        perf set.
    :ivar downhole_string: Reference to the downhole string.
    :ivar md_interval: Measured depth interval for the entire
        perforation set.
    :ivar tvd_interval: The true vertical depth of the entire
        perforation set.
    :ivar hole_diameter: The diameter of the perf holes.
    :ivar hole_angle: The angle of the holes.
    :ivar hole_pattern: The pattern of the holes.
    :ivar hole_density: The density of the holes.
    :ivar hole_count: The number of holes.
    :ivar friction_factor: The friction factor of each perforation set.
    :ivar friction_pres: The friction pressure for the perforation set.
    :ivar discharge_coefficient: A coefficient used in the equation for
        calculation of pressure drop across a perforation set.
    :ivar perforation_tool: The type of perforation tool.
    :ivar perforation_penetration: The penetration length of
        perforation.
    :ivar crush_zone_diameter: The diameter of the crushed zone.
    :ivar crush_damage_ratio: The ratio value of crash damage.
    :ivar perforation_date: The original perforation date.
    :ivar permanent_remarks: Remarks regarding this perforation set.
    :ivar event_history:
    :ivar uid: Unique identifier for this instance of PerforationSet.
    """

    borehole_string: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BoreholeString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    downhole_string: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DownholeString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_diameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "HoleDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "HoleAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_pattern: Optional[str] = field(
        default=None,
        metadata={
            "name": "HolePattern",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_density: Optional[str] = field(
        default=None,
        metadata={
            "name": "HoleDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "HoleCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    friction_factor: Optional[float] = field(
        default=None,
        metadata={
            "name": "FrictionFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    friction_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "FrictionPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    discharge_coefficient: Optional[float] = field(
        default=None,
        metadata={
            "name": "DischargeCoefficient",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_tool: Optional[PerforationToolType] = field(
        default=None,
        metadata={
            "name": "PerforationTool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_penetration: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationPenetration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    crush_zone_diameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "CrushZoneDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    crush_damage_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "CrushDamageRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    permanent_remarks: Optional[str] = field(
        default=None,
        metadata={
            "name": "PermanentRemarks",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    event_history: Optional[EventInfo] = field(
        default=None,
        metadata={
            "name": "EventHistory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PerforationSetInterval:
    """
    The location/interval of the perforation set and its history.

    :ivar perforation_set: Reference to a perforation set.
    :ivar perforation_set_md_interval: Overall measured depth interval
        for this perforation set.
    :ivar perforation_set_tvd_interval: Overall true vertical depth
        interval for this perforation set.
    :ivar event_history: The PerforationSetInterval event information.
    :ivar geology_feature: Reference to a geology feature.
    :ivar geologic_unit_interpretation: Reference to a RESQML geologic
        unit interpretation.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar perforation_status_history:
    :ivar uid: Unique identifier for this instance of
        PerforationSetInterval.
    """

    perforation_set: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_set_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationSetMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_set_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforationSetTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    event_history: Optional[EventInfo] = field(
        default=None,
        metadata={
            "name": "EventHistory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    geology_feature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GeologyFeature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    geologic_unit_interpretation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GeologicUnitInterpretation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_status_history: List[PerforationStatusHistory] = field(
        default_factory=list,
        metadata={
            "name": "PerforationStatusHistory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Pit:
    """
    Rig Pit Schema.

    :ivar index: Relative pit number of all pits on the rig. One-based.
    :ivar dtim_install: Date and time the pit was installed.
    :ivar dtim_remove: Date and time the pit was removed.
    :ivar cap_mx: Maximum pit capacity.
    :ivar owner: Pointer to a BusinessAssociate representing the
        contractor/owner.
    :ivar type_pit: The type of pit.
    :ivar is_active: Flag to indicate if the pit is part of the active
        system. Values are "true" (or "1") and "false" (or "0").
    :ivar name_tag: An identification tag for the pit. A serial number
        is a type of identification tag; however, some tags contain many
        pieces of information. This element only identifies the tag and
        does not describe the contents.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of pit
    """

    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    dtim_install: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimInstall",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_remove: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimRemove",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cap_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "CapMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    owner: Optional[str] = field(
        default=None,
        metadata={
            "name": "Owner",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_pit: Optional[PitType] = field(
        default=None,
        metadata={
            "name": "TypePit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_active: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsActive",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name_tag: List[NameTag] = field(
        default_factory=list,
        metadata={
            "name": "NameTag",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class RotarySteerableTool:
    """Rotary Steerable Tool Component Schema.

    Captures size and performance information about the rotary steerable
    tool used in the tubular string.

    :ivar deflection_method: Method used to direct the deviation of the
        trajectory: point bit or push bit.
    :ivar hole_size_mn: Minimum size of the hole in which the tool can
        operate.
    :ivar hole_size_mx: Maximum size of the hole in which the tool can
        operate.
    :ivar wob_mx: Maximum weight on the bit.
    :ivar operating_speed: Suggested operating speed.
    :ivar speed_mx: Maximum rotation speed.
    :ivar flow_rate_mn: Minimum flow rate for tool operation.
    :ivar flow_rate_mx: Maximum flow rate for tool operation.
    :ivar down_link_flow_rate_mn: Minimum flow rate for programming the
        tool.
    :ivar down_link_flow_rate_mx: Maximum flow rate for programming the
        tool.
    :ivar press_loss_fact: Pressure drop across the tool.
    :ivar pad_count: The number of contact pads.
    :ivar pad_len: Length of the contact pad.
    :ivar pad_width: Width of the contact pad.
    :ivar pad_offset: Offset from the bottom of the pad to the bottom
        connector.
    :ivar open_pad_od: Outside diameter of the tool when the pads are
        activated.
    :ivar close_pad_od: Outside diameter of the tool when the pads are
        closed.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar tool:
    :ivar sensor:
    """

    deflection_method: Optional[DeflectionMethod] = field(
        default=None,
        metadata={
            "name": "DeflectionMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    hole_size_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "HoleSizeMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_size_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "HoleSizeMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wob_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "WobMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    operating_speed: Optional[str] = field(
        default=None,
        metadata={
            "name": "OperatingSpeed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    speed_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpeedMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flow_rate_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowRateMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flow_rate_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowRateMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    down_link_flow_rate_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "DownLinkFlowRateMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    down_link_flow_rate_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "DownLinkFlowRateMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    press_loss_fact: Optional[float] = field(
        default=None,
        metadata={
            "name": "PressLossFact",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pad_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "PadCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pad_len: Optional[str] = field(
        default=None,
        metadata={
            "name": "PadLen",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pad_width: Optional[str] = field(
        default=None,
        metadata={
            "name": "PadWidth",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pad_offset: Optional[str] = field(
        default=None,
        metadata={
            "name": "PadOffset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    open_pad_od: Optional[str] = field(
        default=None,
        metadata={
            "name": "OpenPadOd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    close_pad_od: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClosePadOd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tool: Optional[AbstractRotarySteerableTool] = field(
        default=None,
        metadata={
            "name": "Tool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    sensor: List[Sensor] = field(
        default_factory=list,
        metadata={
            "name": "Sensor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class Shaker:
    """
    Rig Shaker Schema.

    :ivar name: Human-recognizable context for the shaker.
    :ivar manufacturer: Pointer to a BusinessAssociate representing the
        manufacturer or supplier of the item.
    :ivar model: Manufacturer's designated model.
    :ivar dtim_install: Date and time the shaker was installed.
    :ivar dtim_remove: Date and time the shaker was removed.
    :ivar type_value: Description for the type of object.
    :ivar location_shaker: Shaker location on the rig.
    :ivar num_decks: Number of decks.
    :ivar num_casc_level: Number of cascade levels.
    :ivar mud_cleaner: Is part of mud-cleaning assembly as opposed to
        discrete shale shaker? Values are "true" (or "1") and "false"
        (or "0").
    :ivar cap_flow: Maximum pump rate at which the unit efficiently
        operates.
    :ivar owner: Pointer to a BusinessAssociate representing the
        contractor/owner.
    :ivar size_mesh_mn: Minimum mesh size.
    :ivar name_tag: An identification tag for the shaker. A serial
        number is a type of identification tag; however, some tags
        contain many pieces of information. This element only identifies
        the tag and does not describe the contents. .
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar uid: Unique identifier for this instance of Shaker.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    model: Optional[str] = field(
        default=None,
        metadata={
            "name": "Model",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_install: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimInstall",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_remove: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimRemove",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    location_shaker: Optional[str] = field(
        default=None,
        metadata={
            "name": "LocationShaker",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_decks: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumDecks",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_casc_level: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumCascLevel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mud_cleaner: Optional[bool] = field(
        default=None,
        metadata={
            "name": "MudCleaner",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cap_flow: Optional[str] = field(
        default=None,
        metadata={
            "name": "CapFlow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    owner: Optional[str] = field(
        default=None,
        metadata={
            "name": "Owner",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    size_mesh_mn: Optional[str] = field(
        default=None,
        metadata={
            "name": "SizeMeshMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name_tag: List[NameTag] = field(
        default_factory=list,
        metadata={
            "name": "NameTag",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class SlotsInterval:
    """
    The location/interval of the slots and the history.

    :ivar geologic_unit_interpretation: Reference to a RESQML geologic
        unit interpretation.
    :ivar string_equipment: Reference to an equipment string, which is
        the equipment (e.g., tubing, gravel pack screens, etc.) that
        compose the completion.
    :ivar slotted_md_interval: Slotted measured depth interval for this
        completion.
    :ivar slotted_tvd_interval: Slotted true vertical depth interval for
        this completion.
    :ivar event_history: The SlotsInterval event information.
    :ivar geology_feature: Reference to a geology feature.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar status_history:
    :ivar uid: Unique identifier for this instance of SlotsInterval.
    """

    geologic_unit_interpretation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GeologicUnitInterpretation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    string_equipment: Optional[str] = field(
        default=None,
        metadata={
            "name": "StringEquipment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    slotted_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "SlottedMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    slotted_tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "SlottedTvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    event_history: Optional[EventInfo] = field(
        default=None,
        metadata={
            "name": "EventHistory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    geology_feature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GeologyFeature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    status_history: List[IntervalStatusHistory] = field(
        default_factory=list,
        metadata={
            "name": "StatusHistory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StationaryGyro:
    axis_combination: Optional[GyroAxisCombination] = field(
        default=None,
        metadata={
            "name": "AxisCombination",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    range: Optional[PlaneAngleOperatingRange] = field(
        default=None,
        metadata={
            "name": "Range",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class StimAdditive(StimMaterial):
    """
    Provides generic attributes associated with defining an additive used for
    stimulation.

    :ivar additive_kind: Additive type or function from the enumeration
        'StimAdditiveKind'.
    :ivar type_value: The type of additive that is used, which can
        represent a suppliers description or type of AdditiveKind.  For
        example, 5% HCl could be the type when AdditiveKind=acid.
    :ivar supplier_code: A code used to identify the supplier of the
        additive.
    """

    additive_kind: Optional[StimAdditiveKind] = field(
        default=None,
        metadata={
            "name": "AdditiveKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    supplier_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "SupplierCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )


@dataclass
class StimJobDiagnosticSession:
    """
    A pumping diagnostics session.

    :ivar name: The name of the session.
    :ivar number: The number of this pumping diagnostics session.
    :ivar description: A description of the session.
    :ivar choke_size: The size of the choke used during a flow back
        test.
    :ivar dtim_pump_on: The date and time pumping began.
    :ivar dtim_pump_off: The date and time pumping ended.
    :ivar pump_duration: The time between the shutin time and the pump
        on time.
    :ivar dtim_well_shutin: The date and time at which a well ceases
        flowing and the valves are closed.
    :ivar dtim_fracture_close: The date and time when the fluid in the
        fracture is completely leaked off into the formation and the
        fracture closes on its faces.
    :ivar avg_bottomhole_treatment_pres: Average bottomhole treatment
        pressure.
    :ivar avg_bottomhole_treatment_rate: Average bottomhole treatment
        flow rate.
    :ivar base_fluid_vol: Base fluid volume entering equipment.
    :ivar bottomhole_hydrostatic_pres: Bottomhole hydrostatic pressure.
    :ivar bubble_point_pres: The pressure at which gas begins to break
        out of an under saturated oil and form a free gas phase in the
        matrix or a gas cap.
    :ivar fluid_density: The density of the fluid.
    :ivar fracture_close_pres: The pressure when the fracture width
        becomes zero.
    :ivar friction_pres: The pressure loss due to fluid friction with
        the pipe while a fluid is being pumped.
    :ivar initial_shutin_pres: Initial shutin pressure.
    :ivar pore_pres: The pressure of the liquids in the formation pores.
    :ivar wellbore_volume: The volume of fluid in the wellbore.
    :ivar md_surface: The measured depth of the wellbore to its
        injection point.
    :ivar md_bottomhole: The measured depth of the bottom of the hole.
    :ivar md_mid_perforation: The measured depth of the middle
        perforation.
    :ivar tvd_mid_perforation: The true vertical depth of the middle
        perforation.
    :ivar surface_temperature: The constant earth temperature at a given
        depth specific to a region.
    :ivar bottomhole_temperature: Static bottomhole temperature.
    :ivar surface_fluid_temperature: Temperature of the fluid at the
        surface.
    :ivar fluid_compressibility: The volume change of a fluid when
        pressure is applied.
    :ivar reservoir_total_compressibility: The volume change of a
        reservoir material when pressure is applied.
    :ivar fluid_nprime_factor: Power law component. As 'n' decreases
        from 1, the fluid becomes more shear thinning. Reducing 'n'
        produces more non-Newtonian behavior.
    :ivar fluid_kprime_factor: The consistency index K is the shear
        stress or viscosity of the fluid at one sec-1 shear rate. An
        increasing K raises the effective viscosity.
    :ivar fluid_specific_heat: The heat required to raise one unit mass
        of a substance by one degree.
    :ivar fluid_thermal_conductivity: In physics, thermal conductivity
        is the property of a material describing its ability to conduct
        heat. It appears primarily in Fourier's Law for heat conduction.
        Thermal conductivity is measured in watts per kelvin-meter.
        Multiplied by a temperature difference (in kelvins) and an area
        (in square meters), and divided by a thickness (in meters), the
        thermal conductivity predicts the rate of energy loss (in watts)
        through a piece of material.
    :ivar fluid_thermal_expansion_coefficient: Dimensional response to
        temperature change is expressed by its coefficient of thermal
        expansion. When the temperature of a substance changes, the
        energy that is stored in the intermolecular bonds between atoms
        also changes. When the stored energy increases, so does the
        length of the molecular bonds. As a result, solids typically
        expand in response to heating and contract on cooling. The
        degree of expansion divided by the change in temperature is
        called the material's coefficient of thermal expansion and
        generally varies with temperature.
    :ivar fluid_efficiency: A measurement, derived from a data frac, of
        the efficiency of a particular fluid in creating fracture area
        on a particular formation at a set of conditions.
    :ivar foam_quality: Foam quality percentage of foam for the job
        during the stimulation services.
    :ivar percent_pad: The volume of the pad divided by the (volume of
        the pad + the volume of the proppant laden fluid).
    :ivar stage_number: The number of a stage associated with this
        diagnostics session.
    :ivar temperature_correction_applied: Are the calculations corrected
        for temperature? A value of "true" (or "1") indicates that the
        calculations were corrected for temperature. A value of "false"
        (or "0") or not given indicates otherwise.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar fluid_efficiency_test: A diagnostic test determining fluid
        efficiency.
    :ivar step_rate_test: An injection test, plotted pressure against
        injection rate, where a curve deflection and change of slope
        indicates the fracture breakdown pressure.
    :ivar step_down_test: An injection test involving multiple steps of
        injection rate and pressure, where a curve deflection and change
        of slope indicates the fracture breakdown pressure. An injection
        test involving multiple steps of injection rate and pressure,
        where a curve deflection and change of slope indicates the
        fracture breakdown pressure.
    :ivar pump_flow_back_test: A diagnostic test involving flowing a
        well back after treatment.
    :ivar uid: Unique identifier for this instance of
        StimJobDiagnosticSession.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    number: Optional[str] = field(
        default=None,
        metadata={
            "name": "Number",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    choke_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChokeSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_pump_on: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimPumpOn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_pump_off: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimPumpOff",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pump_duration: Optional[str] = field(
        default=None,
        metadata={
            "name": "PumpDuration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_well_shutin: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimWellShutin",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_fracture_close: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimFractureClose",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_bottomhole_treatment_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgBottomholeTreatmentPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_bottomhole_treatment_rate: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgBottomholeTreatmentRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    base_fluid_vol: Optional[str] = field(
        default=None,
        metadata={
            "name": "BaseFluidVol",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bottomhole_hydrostatic_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "BottomholeHydrostaticPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bubble_point_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "BubblePointPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_density: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fracture_close_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureClosePres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    friction_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "FrictionPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    initial_shutin_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "InitialShutinPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pore_pres: Optional[str] = field(
        default=None,
        metadata={
            "name": "PorePres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wellbore_volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellboreVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_surface: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdSurface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_bottomhole: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdBottomhole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_mid_perforation: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdMidPerforation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_mid_perforation: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdMidPerforation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    surface_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "SurfaceTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bottomhole_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "BottomholeTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    surface_fluid_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "SurfaceFluidTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_compressibility: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidCompressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    reservoir_total_compressibility: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReservoirTotalCompressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_nprime_factor: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidNprimeFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_kprime_factor: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidKprimeFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_specific_heat: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidSpecificHeat",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_thermal_conductivity: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidThermalConductivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_thermal_expansion_coefficient: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidThermalExpansionCoefficient",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_efficiency: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidEfficiency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    foam_quality: Optional[str] = field(
        default=None,
        metadata={
            "name": "FoamQuality",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    percent_pad: Optional[str] = field(
        default=None,
        metadata={
            "name": "PercentPad",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    stage_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "StageNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    temperature_correction_applied: Optional[bool] = field(
        default=None,
        metadata={
            "name": "TemperatureCorrectionApplied",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_efficiency_test: List[StimFetTest] = field(
        default_factory=list,
        metadata={
            "name": "FluidEfficiencyTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    step_rate_test: List[StimStepTest] = field(
        default_factory=list,
        metadata={
            "name": "StepRateTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    step_down_test: List[StimStepDownTest] = field(
        default_factory=list,
        metadata={
            "name": "StepDownTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pump_flow_back_test: List[StimPumpFlowBackTest] = field(
        default_factory=list,
        metadata={
            "name": "PumpFlowBackTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimJobStep:
    """
    A step in the treatment of a stage for a stimulation job.

    :ivar step_name: A human readable name for the step.
    :ivar step_number: Step number.
    :ivar kind: The type of step.
    :ivar description: A short description of the step.
    :ivar dtim_start: Date and time the step started.
    :ivar dtim_end: Date and time the step ended.
    :ivar avg_base_fluid_quality: Base quality percentage of foam.
    :ivar avg_co2_base_fluid_quality: Base quality carbon dioxide
        percent of foam.
    :ivar avg_hydraulic_power: Average hydraulic horse power used.
    :ivar avg_internal_phase_fraction: Internal gas phase percentage of
        the foam.
    :ivar avg_material_used_rate: Average material used per minute
        entering the flow stream.
    :ivar avg_material_use_rate_bottomhole: Average material amount used
        (pumped) per minute at bottomhole.
    :ivar avg_n2_base_fluid_quality: Base quality nitrogen percentage of
        foam.
    :ivar avg_pres_bottomhole: Average bottomhole pressure.
    :ivar avg_pres_surface: Average surface pressure.
    :ivar avg_prop_conc: Average proppant concentration at the wellhead.
        ppa: pounds proppant added per volume measure kgpa: kilograms
        proppant added per volume measure
    :ivar avg_proppant_conc_bottomhole: The average proppant
        concentration at bottomhole.
    :ivar avg_proppant_conc_surface: The average proppant concentration
        at the surface.
    :ivar avg_slurry_prop_conc: Average proppant concentration exiting
        the equipment.
    :ivar avg_slurry_rate: Average slurry return rate.
    :ivar avg_temperature: Average fluid temperature.
    :ivar avg_volume_rate_wellhead: Average volume per minute at the
        wellhead.
    :ivar balls_recovered: Balls recovered during execution of the step.
    :ivar balls_used: Balls used during execution of the step.
    :ivar base_fluid_bypass_vol: Base fluid volume recorded after
        equipment set to bypass.
    :ivar base_fluid_vol: Base fluid volume entering the equipment.
    :ivar end_dirty_material_rate: Ending dirty fluid pump volume per
        minute.
    :ivar end_material_used_rate: Ending quantity of material used per
        minute entering the flow stream.
    :ivar end_material_used_rate_bottomhole: Ending quantity of material
        used per minute at bottomhole.
    :ivar end_pres_bottomhole: Final bottomhole pressure.
    :ivar end_pres_surface: Final surface pressure.
    :ivar end_proppant_conc_bottomhole: The final proppant concentration
        at bottomhole.
    :ivar end_proppant_conc_surface: The final proppant concentration at
        the surface.
    :ivar end_rate_surface_co2: Final CO2 pump rate in volume per time
        at the surface.
    :ivar end_std_rate_surface_n2: Final nitrogen pump rate in volume
        per time at the surface.
    :ivar fluid_vol_base: The step volume of the base step.
    :ivar fluid_vol_circulated: Fluid volume circulated.
    :ivar fluid_vol_pumped: Fluid volume pumped.
    :ivar fluid_vol_returned: Fluid volume returned.
    :ivar fluid_vol_slurry: The volume of the slurry (dirty) step.
    :ivar fluid_vol_squeezed: Fluid volume squeezed.
    :ivar fluid_vol_washed: Fluid volume washed.
    :ivar fracture_gradient_final: The fracture gradient when the step
        ends.
    :ivar fracture_gradient_initial: The fracture gradient before
        starting the step.
    :ivar friction_factor: Numeric value used to scale a calculated
        rheological friction.
    :ivar max_hydraulic_power: Maximum hydraulic power used during the
        step.
    :ivar max_pres_surface: Maximum pumping pressure on surface.
    :ivar max_proppant_conc_bottomhole: Maximum proppant concentration
        at bottomhole during the stimulation step.
    :ivar max_proppant_conc_surface: Maximum proppant concentration at
        the wellhead.
    :ivar max_slurry_prop_conc: Maximum proppant concentration exiting
        the equipment.
    :ivar max_volume_rate_wellhead: Maximum volume per minute at the
        wellhead.
    :ivar pipe_friction_pressure: The friction pressure contribution
        from pipes.
    :ivar pump_time: Total pumping time for the step.
    :ivar start_dirty_material_rate: Starting dirty fluid volume per
        minute.
    :ivar start_material_used_rate: Starting quantity of material used
        per minute entering the flow stream.
    :ivar start_material_used_rate_bottom_hole: Starting quantity of
        material used per minute at bottomhole.
    :ivar start_pres_bottomhole: Starting bottomhole pressure.
    :ivar start_pres_surface: Starting surface pressure.
    :ivar start_proppant_conc_bottomhole: The beginning proppant
        concentration at bottomhole.
    :ivar start_proppant_conc_surface: The beginning proppant
        concentration at the surface.
    :ivar wellhead_vol: Slurry volume entering the well.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar material_used: Material used during the step
    :ivar max_material_used_rate:
    :ivar fluid:
    :ivar uid: Unique identifier for this instance of StimJobStep.
    """

    step_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    step_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_base_fluid_quality: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgBaseFluidQuality",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_co2_base_fluid_quality: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgCO2BaseFluidQuality",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_hydraulic_power: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgHydraulicPower",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_internal_phase_fraction: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgInternalPhaseFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_material_used_rate: List[StimMaterialQuantity] = field(
        default_factory=list,
        metadata={
            "name": "AvgMaterialUsedRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_material_use_rate_bottomhole: List[StimMaterialQuantity] = field(
        default_factory=list,
        metadata={
            "name": "AvgMaterialUseRateBottomhole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_n2_base_fluid_quality: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgN2BaseFluidQuality",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_pres_bottomhole: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgPresBottomhole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_pres_surface: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgPresSurface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_prop_conc: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgPropConc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_proppant_conc_bottomhole: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgProppantConcBottomhole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_proppant_conc_surface: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgProppantConcSurface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_slurry_prop_conc: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgSlurryPropConc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_slurry_rate: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgSlurryRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    avg_volume_rate_wellhead: Optional[str] = field(
        default=None,
        metadata={
            "name": "AvgVolumeRateWellhead",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    balls_recovered: Optional[str] = field(
        default=None,
        metadata={
            "name": "BallsRecovered",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    balls_used: Optional[str] = field(
        default=None,
        metadata={
            "name": "BallsUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    base_fluid_bypass_vol: Optional[str] = field(
        default=None,
        metadata={
            "name": "BaseFluidBypassVol",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    base_fluid_vol: Optional[str] = field(
        default=None,
        metadata={
            "name": "BaseFluidVol",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_dirty_material_rate: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndDirtyMaterialRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_material_used_rate: List[StimMaterialQuantity] = field(
        default_factory=list,
        metadata={
            "name": "EndMaterialUsedRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_material_used_rate_bottomhole: List[StimMaterialQuantity] = field(
        default_factory=list,
        metadata={
            "name": "EndMaterialUsedRateBottomhole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_pres_bottomhole: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndPresBottomhole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_pres_surface: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndPresSurface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_proppant_conc_bottomhole: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndProppantConcBottomhole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_proppant_conc_surface: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndProppantConcSurface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_rate_surface_co2: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndRateSurfaceCO2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    end_std_rate_surface_n2: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndStdRateSurfaceN2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_vol_base: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidVolBase",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_vol_circulated: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidVolCirculated",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_vol_pumped: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidVolPumped",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_vol_returned: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidVolReturned",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_vol_slurry: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidVolSlurry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_vol_squeezed: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidVolSqueezed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid_vol_washed: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidVolWashed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fracture_gradient_final: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureGradientFinal",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fracture_gradient_initial: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureGradientInitial",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    friction_factor: Optional[str] = field(
        default=None,
        metadata={
            "name": "FrictionFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_hydraulic_power: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxHydraulicPower",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_pres_surface: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxPresSurface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_proppant_conc_bottomhole: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxProppantConcBottomhole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_proppant_conc_surface: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxProppantConcSurface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_slurry_prop_conc: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxSlurryPropConc",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_volume_rate_wellhead: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxVolumeRateWellhead",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pipe_friction_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "PipeFrictionPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pump_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "PumpTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    start_dirty_material_rate: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartDirtyMaterialRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    start_material_used_rate: List[StimMaterialQuantity] = field(
        default_factory=list,
        metadata={
            "name": "StartMaterialUsedRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    start_material_used_rate_bottom_hole: List[StimMaterialQuantity] = field(
        default_factory=list,
        metadata={
            "name": "StartMaterialUsedRateBottomHole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    start_pres_bottomhole: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartPresBottomhole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    start_pres_surface: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartPresSurface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    start_proppant_conc_bottomhole: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartProppantConcBottomhole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    start_proppant_conc_surface: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartProppantConcSurface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wellhead_vol: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellheadVol",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    material_used: List[StimMaterialQuantity] = field(
        default_factory=list,
        metadata={
            "name": "MaterialUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    max_material_used_rate: List[StimMaterialQuantity] = field(
        default_factory=list,
        metadata={
            "name": "MaxMaterialUsedRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    fluid: Optional[StimFluid] = field(
        default=None,
        metadata={
            "name": "Fluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StimProppantAgent(StimMaterial):
    """
    Captures a description of a proppant used in a stimulation job.

    :ivar friction_coefficient_laminar: Laminar flow friction
        coefficient.
    :ivar friction_coefficient_turbulent: Turbulent flow friction
        coefficient.
    :ivar mass_absorption_coefficient: Characterizes how easily
        radiation passes through a material. This can be used to compute
        the concentration of proppant in a slurry using a densitometer.
    :ivar mesh_size_high: High value of sieve mesh size: for 40/70 sand,
        this value is 70.
    :ivar mesh_size_low: Low value of sieve mesh size: for 40/70 sand,
        this value is 40.
    :ivar unconfined_compressive_strength: The unconfined compressive
        strength of the proppant.
    :ivar proppant_agent_kind: Proppant type or function.
    :ivar iso13503_2_properties:
    :ivar iso13503_5_point:
    """

    friction_coefficient_laminar: Optional[float] = field(
        default=None,
        metadata={
            "name": "FrictionCoefficientLaminar",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    friction_coefficient_turbulent: Optional[float] = field(
        default=None,
        metadata={
            "name": "FrictionCoefficientTurbulent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mass_absorption_coefficient: Optional[str] = field(
        default=None,
        metadata={
            "name": "MassAbsorptionCoefficient",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mesh_size_high: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeshSizeHigh",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mesh_size_low: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeshSizeLow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    unconfined_compressive_strength: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnconfinedCompressiveStrength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    proppant_agent_kind: Optional[ProppantAgentKind] = field(
        default=None,
        metadata={
            "name": "ProppantAgentKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    iso13503_2_properties: List[StimIso135032Properties] = field(
        default_factory=list,
        metadata={
            "name": "ISO13503_2Properties",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    iso13503_5_point: List[StimIso135035Point] = field(
        default_factory=list,
        metadata={
            "name": "ISO13503_5Point",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class CementDesignStage(AbstractCementStage):
    """
    Configuration and other information about the cement stage.
    """


@dataclass
class CementStageDesign(AbstractCementStage):
    """
    Configuration and other information about the cement stage.
    """


@dataclass
class CementStageReport(AbstractCementStage):
    """
    Report of key parameters for a stage of cement job.

    :ivar dtim_mix_start: Date and time when mixing of cement started.
    :ivar dtim_pump_start: Date and time when pumping cement started.
    :ivar dtim_pump_end: Date and time when pumping cement ended.
    :ivar dtim_displace_start: Date and time when displacing of cement
        started.
    :ivar pres_break_down: Breakdown pressure.
    :ivar flowrate_break_down: Breakdown rate.
    :ivar flowrate_displace_av: Average displacement rate.
    :ivar flowrate_displace_mx: Maximum displacement rate.
    :ivar pres_squeeze_av: Squeeze pressure average.
    :ivar pres_squeeze_end: Squeeze pressure final.
    :ivar pres_squeeze_held: Squeeze pressure held.  Values are "true"
        (or "1") and "false" (or "0").
    :ivar etim_mud_circulation: Elapsed time of mud circulation before
        the job/stage.
    :ivar pres_squeeze: Squeeze pressure left on pipe.
    :ivar flowrate_squeeze_av: Squeeze job average rate.
    :ivar flowrate_squeeze_mx: Squeeze job maximum rate.
    :ivar flowrate_end: Final displacement pump rate.
    :ivar flowrate_pump_start: Pump rate at the start of the job.
    :ivar flowrate_pump_end: Pump rate at the end of the job.
    :ivar vis_funnel_mud: Funnel viscosity in seconds (in hole at start
        of job/stage).
    :ivar plug_bumped: Plug bumped? Values are "true" (or "1") and
        "false" (or "0").
    :ivar squeeze_obtained: Squeeze obtained.  Values are "true" (or
        "1") and "false" (or "0").
    :ivar pres_prior_bump: Pressure before bumping plug / pressure at
        the end of  the displacement.
    :ivar float_held: Float held?  Values are "true" (or "1") and
        "false" (or "0").
    :ivar uid: Unique identifier for this instance of CementStageReport
    """

    dtim_mix_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimMixStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_pump_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimPumpStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_pump_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimPumpEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_displace_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimDisplaceStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_break_down: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresBreakDown",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_break_down: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateBreakDown",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_displace_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateDisplaceAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_displace_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateDisplaceMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_squeeze_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresSqueezeAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_squeeze_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresSqueezeEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_squeeze_held: Optional[bool] = field(
        default=None,
        metadata={
            "name": "PresSqueezeHeld",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    etim_mud_circulation: Optional[str] = field(
        default=None,
        metadata={
            "name": "ETimMudCirculation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_squeeze: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresSqueeze",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_squeeze_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateSqueezeAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_squeeze_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateSqueezeMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowrateEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_pump_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowratePumpStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    flowrate_pump_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowratePumpEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vis_funnel_mud: Optional[str] = field(
        default=None,
        metadata={
            "name": "VisFunnelMud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    plug_bumped: Optional[bool] = field(
        default=None,
        metadata={
            "name": "PlugBumped",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    squeeze_obtained: Optional[bool] = field(
        default=None,
        metadata={
            "name": "SqueezeObtained",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_prior_bump: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresPriorBump",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    float_held: Optional[bool] = field(
        default=None,
        metadata={
            "name": "FloatHeld",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ContactIntervalSet:
    """Information on a collection of contact intervals.

    Contains one or more "xxxInterval" objects, each representing the
    details of a single physical connection between well and reservoir,
    e.g., the perforation details, depth, reservoir connected. Meaning:
    this is the physical nature of a connection from reservoir to
    wellbore.
    """

    gravel_pack_interval: List[GravelPackInterval] = field(
        default_factory=list,
        metadata={
            "name": "GravelPackInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    open_hole_interval: List[OpenHoleInterval] = field(
        default_factory=list,
        metadata={
            "name": "OpenHoleInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_set_interval: List[PerforationSetInterval] = field(
        default_factory=list,
        metadata={
            "name": "PerforationSetInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    slots_interval: List[SlotsInterval] = field(
        default_factory=list,
        metadata={
            "name": "SlotsInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class DepthRegTrack:
    """
    Horizontal track layout of the rectified log image that identifies the
    rectangle for a single log track.

    :ivar name: A label associated with the track.
    :ivar type_value: The kind of track.
    :ivar left_edge: The position of the left edge of the track.
    :ivar right_edge: The position of the right edge of the track.
    :ivar track_curve_scale_rect: Coordinates of rectangle representing
        the track.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar associated_curve:
    :ivar uid: Unique identifier for the track.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_value: Optional[LogTrackType] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    left_edge: Optional[str] = field(
        default=None,
        metadata={
            "name": "LeftEdge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    right_edge: Optional[str] = field(
        default=None,
        metadata={
            "name": "RightEdge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    track_curve_scale_rect: List[DepthRegRectangle] = field(
        default_factory=list,
        metadata={
            "name": "TrackCurveScaleRect",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    associated_curve: List[DepthRegTrackCurve] = field(
        default_factory=list,
        metadata={
            "name": "AssociatedCurve",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class GyroToolConfiguration:
    """
    SPE90408 Table 11 &amp; Appendix D.

    :ivar accelerometer_axis_combination: BR VS GyroMode
    :ivar external_reference:
    :ivar continuous_gyro:
    :ivar xy_accelerometer:
    :ivar stationary_gyro:
    """

    accelerometer_axis_combination: Optional[
        AccelerometerAxisCombination
    ] = field(
        default=None,
        metadata={
            "name": "AccelerometerAxisCombination",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    external_reference: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ExternalReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    continuous_gyro: List[ContinuousGyro] = field(
        default_factory=list,
        metadata={
            "name": "ContinuousGyro",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    xy_accelerometer: Optional[XyAccelerometer] = field(
        default=None,
        metadata={
            "name": "XyAccelerometer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    stationary_gyro: List[StationaryGyro] = field(
        default_factory=list,
        metadata={
            "name": "StationaryGyro",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class OperatingConstraints:
    """
    :ivar custom_limits:
    :ivar horizontal_east_west_max_value: Absolute value of the maximum
        value allowed for the product sin(Inclination) * sin(Azimuth).
    :ivar md_range:
    :ivar tvd_range:
    :ivar pressure_limit:
    :ivar thermodynamic_temperature_limit:
    :ivar custom_range: Can be segmented
    :ivar latitude_range: Can be segmented
    :ivar inclination_range: Can be segmented
    :ivar azimuth_range: Can be segmented
    """

    custom_limits: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CustomLimits",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    horizontal_east_west_max_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "HorizontalEastWestMaxValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_range: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MdRange",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_range: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TvdRange",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pressure_limit: Optional[str] = field(
        default=None,
        metadata={
            "name": "PressureLimit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    thermodynamic_temperature_limit: Optional[str] = field(
        default=None,
        metadata={
            "name": "ThermodynamicTemperatureLimit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    custom_range: List[CustomOperatingRange] = field(
        default_factory=list,
        metadata={
            "name": "CustomRange",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    latitude_range: List[PlaneAngleOperatingRange] = field(
        default_factory=list,
        metadata={
            "name": "LatitudeRange",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    inclination_range: List[PlaneAngleOperatingRange] = field(
        default_factory=list,
        metadata={
            "name": "InclinationRange",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    azimuth_range: List[AzimuthRange] = field(
        default_factory=list,
        metadata={
            "name": "AzimuthRange",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class PerforationSets:
    """
    Information on the collection of perforation sets.
    """

    perforation_set: List[PerforationSet] = field(
        default_factory=list,
        metadata={
            "name": "PerforationSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class StimJobMaterialCatalog:
    """A listing of materials for a particular job.

    Any stage of the stim job can reference material(s) in the catalog,
    which eliminates the need to repeat the materials for each stage.

    :ivar additives: List of additives in the catalog.
    :ivar proppant_agents: List of proppant agents in the catalog.
    """

    additives: List[StimAdditive] = field(
        default_factory=list,
        metadata={
            "name": "Additives",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    proppant_agents: List[StimProppantAgent] = field(
        default_factory=list,
        metadata={
            "name": "ProppantAgents",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class StringEquipment:
    """
    Information regarding equipment that composes (makes up) a string.

    :ivar equipment: Reference to a piece of equipment.
    :ivar equipment_type: The type of the equipment. See enumerated
        values.
    :ivar name: The name of the equipment.
    :ivar equipment_event_history: History of events related to this
        equipment.
    :ivar status: The status of the piece of equipment.
    :ivar run_no: The well run number.
    :ivar previous_run_days: The days that the equipment has run.
    :ivar object_condition: Object condition at installation.
    :ivar surface_condition: Object surface condition.
    :ivar count: The count number of the same equipment. The default is
        1.  In some cases, multiple pieces group into one component.
    :ivar length: The total length of the equipment.  This is NOT length
        per unit. This is the length of unit stored at equipmentset's
        equipment information section.
    :ivar md_interval: Measured depth interval in which the equipment is
        installed in the string.
    :ivar tvd_interval: True vertical depth interval in which the
        equipment is installed in the string.
    :ivar outside_string: Flag indicating whether this component is
        inside the string or not .
    :ivar tensile_max: Max tensile strength.
    :ivar pres_rating: Pressure  rating.
    :ivar pres_collapse: Collapse pressure.
    :ivar pres_burst: Burst pressure.
    :ivar heat_rating: Heat rating.
    :ivar is_lineto_surface: Flag indicating the equipment has a line
        connected to the surface.
    :ivar is_centralized: Flag indicating equipment is centralized.
    :ivar has_scratchers: Flag indicating scratchers have been added to
        the equipment.
    :ivar perforation_set: Reference to the perforated hole in the
        equipment after a perforation event.
    :ivar permanent_remarks: Remarks on the equipment stored
        permanently.
    :ivar usage_comment: Remarks on the usage of this equipment.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar order_of_object:
    :ivar inside_component:
    :ivar outside_component:
    :ivar connection_next:
    :ivar assembly:
    :ivar uid: Unique identifier for this instance of StringEquipment.
    """

    equipment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Equipment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    equipment_type: Optional[Union[EquipmentType, str]] = field(
        default=None,
        metadata={
            "name": "EquipmentType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    equipment_event_history: List[EventInfo] = field(
        default_factory=list,
        metadata={
            "name": "EquipmentEventHistory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    status: Optional[str] = field(
        default=None,
        metadata={
            "name": "Status",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    run_no: Optional[str] = field(
        default=None,
        metadata={
            "name": "RunNo",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    previous_run_days: Optional[str] = field(
        default=None,
        metadata={
            "name": "PreviousRunDays",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    object_condition: Optional[str] = field(
        default=None,
        metadata={
            "name": "ObjectCondition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    surface_condition: Optional[str] = field(
        default=None,
        metadata={
            "name": "SurfaceCondition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tvd_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "TvdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    outside_string: Optional[bool] = field(
        default=None,
        metadata={
            "name": "OutsideString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tensile_max: Optional[str] = field(
        default=None,
        metadata={
            "name": "TensileMax",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_rating: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresRating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_collapse: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresCollapse",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_burst: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresBurst",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    heat_rating: Optional[str] = field(
        default=None,
        metadata={
            "name": "HeatRating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_lineto_surface: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsLinetoSurface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    is_centralized: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsCentralized",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    has_scratchers: Optional[bool] = field(
        default=None,
        metadata={
            "name": "HasScratchers",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    perforation_set: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PerforationSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    permanent_remarks: Optional[str] = field(
        default=None,
        metadata={
            "name": "PermanentRemarks",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    usage_comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "UsageComment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    order_of_object: Optional[ObjectSequence] = field(
        default=None,
        metadata={
            "name": "OrderOfObject",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    inside_component: List[ReferenceContainer] = field(
        default_factory=list,
        metadata={
            "name": "InsideComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    outside_component: List[ReferenceContainer] = field(
        default_factory=list,
        metadata={
            "name": "OutsideComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    connection_next: List[EquipmentConnection] = field(
        default_factory=list,
        metadata={
            "name": "ConnectionNext",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    assembly: Optional[Assembly] = field(
        default=None,
        metadata={
            "name": "Assembly",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class TubularComponent:
    """Tubular Component Schema.

    Captures the order of the components in the XML instance,which is
    significant. The components are listed in the order in which they
    enter the hole. That is, the first component is the bit.

    :ivar manufacturer: Pointer to a BusinessAssociate representing the
        manufacturer of this component.
    :ivar nominal_diameter: Nominal size (diameter) of the component,
        e.g., 9.625", 12.25".
    :ivar nominal_weight: Nominal weight of the component
    :ivar supplier: Pointer to a BusinessAssociate representing the
        supplier for this component.
    :ivar tens_strength: Yield stress of steel - worn stress.
    :ivar tubular_component_osduintegration: Information about a
        TubularComponent that is relevant for OSDU integration but does
        not have a natural place in a TubularComponent.
    :ivar type_tubular_component: Type of component.
    :ivar sequence: The sequence within which the components entered the
        hole. That is, a sequence number of 1 entered first, 2 entered
        next, etc.
    :ivar description: Description of item and details.
    :ivar id: Internal diameter of object.
    :ivar od: Outside diameter of the body of the item.
    :ivar od_mx: Maximum outside diameter.
    :ivar len: Length of the item.
    :ivar len_joint_av: Average length of the joint for this string.
    :ivar num_joint_stand: Number of joints per stand of tubulars.
    :ivar wt_per_len: Weight per unit length.
    :ivar count: The count number of the same component.
    :ivar grade: Material grade for the tubular section.
    :ivar od_drift: Minimum pass through diameter.
    :ivar tens_yield: Yield stress of steel - worn stress.
    :ivar tq_yield: Torque at which yield occurs.
    :ivar stress_fatigue: Fatigue endurance limit.
    :ivar len_fishneck: Fish neck length.
    :ivar id_fishneck: Fish neck inside diameter.
    :ivar od_fishneck: Fish neck outside diameter.
    :ivar disp: Closed end displacement.
    :ivar pres_burst: Burst pressure.
    :ivar pres_collapse: Collapse pressure.
    :ivar class_service: Service class.
    :ivar wear_wall: Wall thickness wear (commonly in percent).
    :ivar thick_wall: Wall thickness.
    :ivar config_con: Box/Pin configuration.
    :ivar bend_stiffness: Bending stiffness of tubular.
    :ivar axial_stiffness: Axial stiffness of tubular.
    :ivar torsional_stiffness: Torsional stiffness of tubular.
    :ivar type_material: Type of material.
    :ivar dogleg_mx: Maximum dogleg severity.
    :ivar model: Component name from manufacturer.
    :ivar name_tag: An identification tag for the component tool. A
        serial number is a type of identification tag; however, some
        tags contain many pieces of information. This element only
        identifies the tag; it does not describe the contents.
    :ivar area_nozzle_flow: Total area of nozzles.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar connection:
    :ivar jar:
    :ivar mwd_tool:
    :ivar motor:
    :ivar stabilizer:
    :ivar bend:
    :ivar hole_opener:
    :ivar rotary_steerable_tool:
    :ivar bit_record:
    :ivar nozzle:
    :ivar uid: Unique identifier for this instance of TubularComponent
    """

    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nominal_diameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "NominalDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nominal_weight: Optional[str] = field(
        default=None,
        metadata={
            "name": "NominalWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    supplier: Optional[str] = field(
        default=None,
        metadata={
            "name": "Supplier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tens_strength: Optional[str] = field(
        default=None,
        metadata={
            "name": "TensStrength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tubular_component_osduintegration: Optional[
        TubularComponentOsduintegration
    ] = field(
        default=None,
        metadata={
            "name": "TubularComponentOSDUIntegration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_tubular_component: Optional[Union[TubularComponentType, str]] = field(
        default=None,
        metadata={
            "name": "TypeTubularComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    sequence: Optional[int] = field(
        default=None,
        metadata={
            "name": "Sequence",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    od: Optional[str] = field(
        default=None,
        metadata={
            "name": "Od",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    od_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len: Optional[str] = field(
        default=None,
        metadata={
            "name": "Len",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    len_joint_av: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenJointAv",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    num_joint_stand: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumJointStand",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wt_per_len: Optional[str] = field(
        default=None,
        metadata={
            "name": "WtPerLen",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    grade: Optional[str] = field(
        default=None,
        metadata={
            "name": "Grade",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od_drift: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdDrift",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tens_yield: Optional[str] = field(
        default=None,
        metadata={
            "name": "TensYield",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    tq_yield: Optional[str] = field(
        default=None,
        metadata={
            "name": "TqYield",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    stress_fatigue: Optional[str] = field(
        default=None,
        metadata={
            "name": "StressFatigue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    len_fishneck: Optional[str] = field(
        default=None,
        metadata={
            "name": "LenFishneck",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    id_fishneck: Optional[str] = field(
        default=None,
        metadata={
            "name": "IdFishneck",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    od_fishneck: Optional[str] = field(
        default=None,
        metadata={
            "name": "OdFishneck",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    disp: Optional[str] = field(
        default=None,
        metadata={
            "name": "Disp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_burst: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresBurst",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    pres_collapse: Optional[str] = field(
        default=None,
        metadata={
            "name": "PresCollapse",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    class_service: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClassService",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    wear_wall: Optional[str] = field(
        default=None,
        metadata={
            "name": "WearWall",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    thick_wall: Optional[str] = field(
        default=None,
        metadata={
            "name": "ThickWall",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    config_con: Optional[BoxPinConfig] = field(
        default=None,
        metadata={
            "name": "ConfigCon",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bend_stiffness: Optional[str] = field(
        default=None,
        metadata={
            "name": "BendStiffness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    axial_stiffness: Optional[str] = field(
        default=None,
        metadata={
            "name": "AxialStiffness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    torsional_stiffness: Optional[str] = field(
        default=None,
        metadata={
            "name": "TorsionalStiffness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    type_material: Optional[MaterialType] = field(
        default=None,
        metadata={
            "name": "TypeMaterial",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dogleg_mx: Optional[str] = field(
        default=None,
        metadata={
            "name": "DoglegMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    model: Optional[str] = field(
        default=None,
        metadata={
            "name": "Model",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name_tag: List[NameTag] = field(
        default_factory=list,
        metadata={
            "name": "NameTag",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    area_nozzle_flow: Optional[str] = field(
        default=None,
        metadata={
            "name": "AreaNozzleFlow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    connection: List[Connection] = field(
        default_factory=list,
        metadata={
            "name": "Connection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    jar: Optional[Jar] = field(
        default=None,
        metadata={
            "name": "Jar",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    mwd_tool: Optional[MwdTool] = field(
        default=None,
        metadata={
            "name": "MwdTool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    motor: Optional[Motor] = field(
        default=None,
        metadata={
            "name": "Motor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    stabilizer: List[Stabilizer] = field(
        default_factory=list,
        metadata={
            "name": "Stabilizer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bend: List[Bend] = field(
        default_factory=list,
        metadata={
            "name": "Bend",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    hole_opener: Optional[HoleOpener] = field(
        default=None,
        metadata={
            "name": "HoleOpener",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    rotary_steerable_tool: Optional[RotarySteerableTool] = field(
        default=None,
        metadata={
            "name": "RotarySteerableTool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    bit_record: Optional[BitRecord] = field(
        default=None,
        metadata={
            "name": "BitRecord",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    nozzle: List[Nozzle] = field(
        default_factory=list,
        metadata={
            "name": "Nozzle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Assembly:
    """
    Container element for assemblies, or a collection of all assembly information.
    """

    part: List[StringEquipment] = field(
        default_factory=list,
        metadata={
            "name": "Part",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )


@dataclass
class CementJobDesign(AbstractCementJob):
    """
    Design and other information about the cement job.
    """

    cement_design_stage: List[CementStageDesign] = field(
        default_factory=list,
        metadata={
            "name": "CementDesignStage",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class CementJobReport(AbstractCementJob):
    """
    The as-built report of the job after it has been done.

    :ivar dtim_job_end: Date and time of the end of the cement job.
    :ivar dtim_job_start: Date and time of the start of the cement job.
    :ivar dtim_plug_set: Date and time that cement plug was set.
    :ivar cement_drill_out: Was the cement drilled out? Values are
        "true" (or "1") and "false" (or "0").
    :ivar dtim_cement_drill_out: Date and time that the cement was
        drilled out.
    :ivar dtim_squeeze: Date and time of a squeeze.
    :ivar dtim_pipe_rot_start: Date and time that pipe rotation started.
    :ivar dtim_pipe_rot_end: Date and time that pipe rotation started.
    :ivar dtim_recip_start: Date and time that pipe reciprocation
        started.
    :ivar dtim_recip_end: Date and time that pipe reciprocation ended.
    :ivar dens_meas_by: Method by which density is measured.
    :ivar cement_report_stage:
    """

    dtim_job_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimJobEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_job_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimJobStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_plug_set: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimPlugSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cement_drill_out: Optional[bool] = field(
        default=None,
        metadata={
            "name": "CementDrillOut",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_cement_drill_out: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimCementDrillOut",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_squeeze: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimSqueeze",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_pipe_rot_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimPipeRotStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_pipe_rot_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimPipeRotEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_recip_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimRecipStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dtim_recip_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTimRecipEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    dens_meas_by: Optional[str] = field(
        default=None,
        metadata={
            "name": "DensMeasBy",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    cement_report_stage: List[CementStageReport] = field(
        default_factory=list,
        metadata={
            "name": "CementReportStage",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class DepthRegLogSection:
    """Defines the description and coordinates of a well log section, the curves on
    the log.

    An important XSDelement to note is log:refNameString; it is a
    reference to the actual log/data (in a WITSML server) that this
    raster image represents; this object does not contain the log data.

    :ivar log_section_sequence_number: Zero-based index in the log
        sections, in order of appearance.
    :ivar log_section_type: Type of log section.
    :ivar log_section_name: Name of a log section;  used to distinguish
        log sections of the same type.
    :ivar log_matrix: Log matrix assumed for porosity computations.
    :ivar scale_numerator: The numerator of the index (depth or time)
        scale of the original log, e. g. "5 in".
    :ivar scale_denominator: The denominator of the index (depth or
        time) scale of the original log, e. g. "100 ft".  '@uom' must be
        consistent with '//indexType'.
    :ivar index_kind: Primary index type. For date-time indexes, any
        specified index values should be defined as a time offset (e.g.,
        in seconds) from the creationDate of the well log.
    :ivar index_uom: Index UOM of the original log.
    :ivar index_datum: Pointer to a reference point representing the
        origin for vertical coordinates on the original log. If this is
        not specified, information about the datum should be specified
        in a comment.
    :ivar index_interval: The range of the index values.
    :ivar vertical_label: Vertical log scale label (e.g., "1 IN/100 F").
    :ivar vertical_ratio: Second term of the vertical scale ratio (e.g.,
        "240" for a 5-inch-per-100-foot log section).
    :ivar comment: Comments about the calibration.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar upper_curve_scale_rect: Boundaries of the upper curve scale
        (or horizontal scale) section for this log section.
    :ivar calibration_point: Generally this associates an X, Y value
        pair with a depth value from the log section.
    :ivar white_space: Defines blank space occurring within a log
        section in an image.
    :ivar lower_curve_scale_rect: Boundaries of the lower curve scale
        (or horizontal scale) section for this log section.
    :ivar log_section_rect: The bounding rectangle of this log section.
    :ivar parameter:
    :ivar track:
    :ivar channel_set:
    :ivar uid: Unique identifier for the log section.
    """

    log_section_sequence_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "LogSectionSequenceNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    log_section_type: Optional[LogSectionType] = field(
        default=None,
        metadata={
            "name": "LogSectionType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    log_section_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LogSectionName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    log_matrix: Optional[str] = field(
        default=None,
        metadata={
            "name": "LogMatrix",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    scale_numerator: Optional[str] = field(
        default=None,
        metadata={
            "name": "ScaleNumerator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    scale_denominator: Optional[str] = field(
        default=None,
        metadata={
            "name": "ScaleDenominator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    index_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "IndexKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    index_uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "IndexUom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    index_datum: Optional[str] = field(
        default=None,
        metadata={
            "name": "IndexDatum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    index_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "IndexInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    vertical_label: Optional[str] = field(
        default=None,
        metadata={
            "name": "VerticalLabel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    vertical_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "VerticalRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    upper_curve_scale_rect: List[DepthRegRectangle] = field(
        default_factory=list,
        metadata={
            "name": "UpperCurveScaleRect",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    calibration_point: List[DepthRegCalibrationPoint] = field(
        default_factory=list,
        metadata={
            "name": "CalibrationPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    white_space: List[DepthRegRectangle] = field(
        default_factory=list,
        metadata={
            "name": "WhiteSpace",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    lower_curve_scale_rect: List[DepthRegRectangle] = field(
        default_factory=list,
        metadata={
            "name": "LowerCurveScaleRect",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    log_section_rect: List[DepthRegRectangle] = field(
        default_factory=list,
        metadata={
            "name": "LogSectionRect",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    parameter: List[DepthRegParameter] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    track: List[DepthRegTrack] = field(
        default_factory=list,
        metadata={
            "name": "Track",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    channel_set: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChannelSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StringAccessory:
    """StringAccessories contain the stringequipment's decorative components.

    An accessory is the stringEquipment or Strings’ decorative
    component.  An accessory is NOT directly screwed to the string. This
    part DOES NOT carry the weight of the rest of the String as opposed
    to the stringEquipment, which does. An Accessory is UNLIKE an
    Assembly on which the stringEquipment is built out of.
    """

    accessory: List[StringEquipment] = field(
        default_factory=list,
        metadata={
            "name": "Accessory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class StringEquipmentSet:
    """
    Information on collection of set of equipment included in the string.
    """

    string_equipment: List[StringEquipment] = field(
        default_factory=list,
        metadata={
            "name": "StringEquipment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class BoreholeString:
    """A section of a borehole.

    Used to define the drilled hole that corresponds to the wellbore. A
    collection of contiguous and non-overlapping borehole sections is
    allowed. Each section has depth range, diameter, and kind.

    :ivar name: The name of the borehole string.
    :ivar borehole:
    :ivar geology_feature:
    :ivar accessories:
    :ivar reference_wellbore:
    :ivar uid: Unique identifier for this instance of BoreholeString.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    borehole: List[Borehole] = field(
        default_factory=list,
        metadata={
            "name": "Borehole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    geology_feature: List[GeologyFeature] = field(
        default_factory=list,
        metadata={
            "name": "GeologyFeature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    accessories: Optional[StringAccessory] = field(
        default=None,
        metadata={
            "name": "Accessories",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    reference_wellbore: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReferenceWellbore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DownholeString:
    """A section of the downhole component equipment.

    Strings in the completion including casing, tubing, and rod strings
    .A completion may have multiple sets of strings, which may be nested
    each inside another, or run in parallel as in dual string
    completions; all strings are contained in a parent wellbore. Each
    string is composed of equipment, and may also contain accessories
    and/or assemblies.

    :ivar string_type: The type of string defined in the  enumeration
        DownholeStringType.
    :ivar sub_string_type: The type of substring which can be
        SurfaceCasing, IntermediaCasing or ProductionCasing.
    :ivar name: The name of the downhole string.
    :ivar string_install_date: The install date of the downhole string.
    :ivar string_md_interval: Measured depth interval between the top
        and the base of the downhole string.
    :ivar axis_offset: The distance from a sibling string.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar parent_string:
    :ivar string_equipment_set:
    :ivar accessories:
    :ivar reference_wellbore:
    :ivar uid: Unique identifier for this instance of DownholeString.
    """

    string_type: Optional[DownholeStringType] = field(
        default=None,
        metadata={
            "name": "StringType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    sub_string_type: Optional[SubStringType] = field(
        default=None,
        metadata={
            "name": "SubStringType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    string_install_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "StringInstallDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    string_md_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "StringMdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    axis_offset: Optional[str] = field(
        default=None,
        metadata={
            "name": "AxisOffset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    parent_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "ParentString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    string_equipment_set: Optional[StringEquipmentSet] = field(
        default=None,
        metadata={
            "name": "StringEquipmentSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    accessories: Optional[StringAccessory] = field(
        default=None,
        metadata={
            "name": "Accessories",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
        },
    )
    reference_wellbore: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReferenceWellbore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class BoreholeStringSet:
    """
    Borehole string container element, or a collection of all borehole strings.
    """

    borehole_string: List[BoreholeString] = field(
        default_factory=list,
        metadata={
            "name": "BoreholeString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class DownholeStringSet:
    """
    Information on a collection of downhole strings.
    """

    downhole_string: List[DownholeString] = field(
        default_factory=list,
        metadata={
            "name": "DownholeString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/witsmlv2",
            "min_occurs": 1,
        },
    )
