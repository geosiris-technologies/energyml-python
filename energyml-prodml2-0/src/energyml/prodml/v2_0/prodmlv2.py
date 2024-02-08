from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class AbstractAttenuationMeasure:
    """
    Abstract class of attenuation measure.
    """


@dataclass
class AbstractCable:
    """
    The abstract class of class.
    """


@dataclass
class AbstractDateTimeType:
    """A reporting period that is different from the overall report period.

    For example, a particular day within a monthly report. This period
    must conform to the kind of interval. If one value from a pair are
    given, then both values must be given.

    :ivar date: Date.
    :ivar dtime: DTime.
    :ivar month: Month.
    """

    class Meta:
        name = "AbstractDateTimeClass"

    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtime: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    month: Optional[str] = field(
        default=None,
        metadata={
            "name": "Month",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "pattern": r"([1-9][0-9][0-9][0-9])-(([0][0-9])|([1][0-2]))",
        },
    )


@dataclass
class AbstractDatum:
    """
    The abstract base type of datum.
    """


@dataclass
class AbstractFiberFacility:
    """
    The abstract base type of FiberFacility.
    """


@dataclass
class AbstractFluidComponent:
    """
    The Abstract base type of FluidComponent.

    :ivar mass_fraction: The fluid mass fraction.
    :ivar mole_fraction: The fluid mole fraction.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    mass_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mole_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MoleFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class AbstractGasProducedRatioVolume:
    """
    The abstract class of Gas Produced Ratio Volume.
    """


@dataclass
class AbstractLiquidDropoutPercVolume:
    """
    Provide either the liquid volume, or the liquid dropout percent, which is the
    liquid volume divided by the total volume.
    """


@dataclass
class AbstractLocation:
    """
    The abstract base type of location.
    """


@dataclass
class AbstractMeasureDataType:
    """
    The abstract base type of measure data.
    """


@dataclass
class AbstractOilVolShrinkage:
    """
    The abstract class of oil volume shrinkage.
    """


@dataclass
class AbstractProductQuantity:
    """
    The Abstract base type of product quantity.

    :ivar mass: The amount of product as a mass measure.
    :ivar moles: Moles.
    :ivar volume: The amount of product as a volume measure.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Mass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    moles: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Moles",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Volume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class AbstractRefProductFlow:
    """A reference to a flow within the current product volume report.

    This represents a foreign key from one element to another.
    """


@dataclass
class AbstractRelatedFacilityObject:
    """
    The abstract base type of related facility.
    """

    facility_parent: Optional[FacilityParent] = field(
        default=None,
        metadata={
            "name": "FacilityParent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class AbstractValue:
    """
    The abstract base type of value.
    """


@dataclass
class AbstractWellTest:
    """
    The abstract base type of well test.

    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class AddressKindEnum(Enum):
    """
    Specifies the kinds of company addresses.

    :cvar BOTH:
    :cvar MAILING:
    :cvar PHYSICAL: physical
    """

    BOTH = "both"
    MAILING = "mailing"
    PHYSICAL = "physical"


class AddressQualifier(Enum):
    """
    Specifies qualifiers that can be used for addresses or phone numbers.

    :cvar PERMANENT: permanent
    :cvar PERSONAL: personal
    :cvar WORK:
    """

    PERMANENT = "permanent"
    PERSONAL = "personal"
    WORK = "work"


@dataclass
class ApplicationInfo:
    """
    Information about the application.

    :ivar application_name: The name of the application that is expected
        to use these fluid characterization data.
    :ivar version: The version of the application that is expected to
        use these fluid characterization data.
    """

    application_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ApplicationName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class BalanceDestinationType(Enum):
    """
    Specifies the types of destinations.

    :cvar HARBOR: Defines the name of the destination harbor.
    :cvar TERMINAL: Defines the name of the destination terminal.
    :cvar UNKNOWN: Unknown.
    """

    HARBOR = "harbor"
    TERMINAL = "terminal"
    UNKNOWN = "unknown"


class BalanceEventKind(Enum):
    """
    Specifies the types of events related to a product balance.

    :cvar BILL_OF_LADING: For a cargo, the date of the bill of lading
        for the cargo involved.
    :cvar TRANSACTION_DATE: For a transaction (e.g. gas sales
        transaction), the date for the transaction involved.
    :cvar UNKNOWN: Unknown.
    """

    BILL_OF_LADING = "bill of lading"
    TRANSACTION_DATE = "transaction date"
    UNKNOWN = "unknown"


class BalanceFlowPart(Enum):
    """
    Specifies the kinds of subdivisions of a flow related to the stock balance.

    :cvar ADJUSTED_CLOSING: Volume that remains after the operation of
        transfer.
    :cvar CLOSING_BALANCE: A volume that is the total volume on stock at
        the end of a time period.
    :cvar CLOSING_STORAGE_INVENTORY: A closing storage balance that is
        adjusted according to imbalance at end of period.
    :cvar COMPLETED_LIFTING: A volume that is the total volume of a
        hydrocarbon product  that is exported from a stock within a
        given time period.
    :cvar GAIN_LOSS: A volume that is a lack of proper proportion or
        relation between the corresponding input and lifting
        transactions.
    :cvar INPUT_TO_STORAGE: A volume that is the total volume of
        additions to a stock within a given time period.
    :cvar LIFTED: A volume that is transferred ("lifted").
    :cvar LIFTING_ENTITLEMENT: A volume that is the contracted volume
        which can be transferred.
    :cvar LIFTING_ENTITLEMENT_REMAINING: A volume that is the contracted
        volume which is not transferred but which remains available for
        subsequent transfer.
    :cvar LINEPACK: A gas volume that is the quantity of gas which the
        operator responsible for gas transportation decides must be
        provided by the gas producing fields in order to make deliveries
        as requested by gas shippers and provide operating tolerances.
    :cvar OPENING_BALANCE: A volume that is the total volume on stock at
        the beginning of a time period.
    :cvar OPFLEX: A gas volume that is the unused and available quantity
        of gas within a gas transportation system and/or at one or many
        gas producing fields that is accessible by the operator
        responsible for gas transportation for the purposes of
        alleviating field curtailment.
    :cvar PARTIAL_LIFTING: A volume that is the volume of a hydrocarbon
        product lifting up to a (not completed) determined point in
        time.
    :cvar PIPELINE_LIFTING: A volume that is the volume of a hydrocarbon
        product lifting transferred by pipeline.
    :cvar PRODUCTION_MASS_ADJUSTMENT: A part of a mass adjustment
        process of a given production volume.
    :cvar PRODUCTION_VALUE_ADJUSTMENT: A value that is adjusted due to a
        change in the value of a product.
    :cvar PRODUCTION_IMBALANCE: A gas volume that is the difference
        between gas volume entering and exiting a shipper's nomination
        portfolio. This will take into account all differences whatever
        the time or reason it occurs.
    :cvar SWAP: A swap of a volume in between different parties (often
        used in crude sales),e.g. "I have this volume with this quality
        and value and you can give me this higher volume for it with a
        lower quality."
    :cvar TANKER_LIFTING: A volume that is the volume of a hydrocarbon
        product lifting transferred by tanker.
    :cvar TRANSACTION: Typically used within the cargo shipper
        operations and in this context: is a change in ownership as
        executed between shippers of the cargo.
    :cvar TRANSFER: A volume that is the volume of a hydrocarbon product
        which changes custody in the operation.
    :cvar UNKNOWN: Unknown.
    """

    ADJUSTED_CLOSING = "adjusted closing"
    CLOSING_BALANCE = "closing balance"
    CLOSING_STORAGE_INVENTORY = "closing storage inventory"
    COMPLETED_LIFTING = "completed lifting"
    GAIN_LOSS = "gain/loss"
    INPUT_TO_STORAGE = "input to storage"
    LIFTED = "lifted"
    LIFTING_ENTITLEMENT = "lifting entitlement"
    LIFTING_ENTITLEMENT_REMAINING = "lifting entitlement remaining"
    LINEPACK = "linepack"
    OPENING_BALANCE = "opening balance"
    OPFLEX = "opflex"
    PARTIAL_LIFTING = "partial lifting"
    PIPELINE_LIFTING = "pipeline lifting"
    PRODUCTION_MASS_ADJUSTMENT = "production - mass adjustment"
    PRODUCTION_VALUE_ADJUSTMENT = "production -- value adjustment"
    PRODUCTION_IMBALANCE = "production imbalance"
    SWAP = "swap"
    TANKER_LIFTING = "tanker lifting"
    TRANSACTION = "transaction"
    TRANSFER = "transfer"
    UNKNOWN = "unknown"


@dataclass
class BinaryInteractionCoefficient:
    """
    Binary interaction coefficient.

    :ivar fluid_component1_reference: Reference to the first fluid
        component for this binary interaction coefficient.
    :ivar fluid_component2_reference: Reference to the second fluid
        component for this binary interaction coefficient.
    """

    fluid_component1_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "fluidComponent1Reference",
            "type": "Attribute",
            "required": True,
        },
    )
    fluid_component2_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "fluidComponent2Reference",
            "type": "Attribute",
        },
    )


class BusinessUnitKind(Enum):
    """
    Specifies the types of business units.
    """

    BUSINESSAREA = "businessarea"
    COMPANY = "company"
    FIELD = "field"
    LICENSE = "license"
    PLATFORM = "platform"
    TERMINAL = "terminal"
    UNKNOWN = "unknown"


class CableType(Enum):
    """
    Specifies the types of cable.

    :cvar ELECTRICAL_FIBER_CABLE: electrical-fiber-cable
    :cvar MULTI_FIBER_CABLE: multi-fiber-cable
    :cvar SINGLE_FIBER_CABLE: single-fiber-cable
    """

    ELECTRICAL_FIBER_CABLE = "electrical-fiber-cable"
    MULTI_FIBER_CABLE = "multi-fiber-cable"
    SINGLE_FIBER_CABLE = "single-fiber-cable"


@dataclass
class CalibrationParameter:
    """Parameters are given by name/ value pairs, with optional UOM.

    The parameter name and UOM are attributes, and the value is the
    value of the element.

    :ivar name: The name of the parameter.
    :ivar uom: The unit of measure of the parameter value.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    uom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class CompressibilityKind(Enum):
    """
    Specifies the kinds of compressibility.

    :cvar AVERAGE: The average measure.
    :cvar POINT: A specific point measure.
    """

    AVERAGE = "average"
    POINT = "point"


@dataclass
class ConnectedNode:
    """
    Product Flow Connected Node Schema.

    :ivar comment: A descriptive remark associated with this connection,
        possibly including a reason for termination.
    :ivar dtim_end: The date and time that the connection was
        terminated.
    :ivar dtim_start: The date and time that the connection was
        activated.
    :ivar node: Defines the node to which this port is connected. Only
        two ports should be actively connected to the same node at the
        same point in time. That is, a port should only be connected to
        one other port. There are no semantics for the node except
        common connection. All ports that are connected to a node with
        the same name are inherently connected to each other. The name
        of the node is only required to be unique within the context of
        the current Product Flow Network (that is, not the overall
        model). All ports must be connected to a node and whether or not
        any other port is connected to the same node depends on the
        requirements of the network. Any node that is internally
        connected to only one node is presumably a candidate to be
        connected to an external node. The behavior of ports connected
        at a common node is as follows: a) There is no pressure drop
        across the node. All ports connected to the node have the same
        pressure. That is, there is an assumption of steady state fluid
        flow. b) Conservation of mass exists across the node. The mass
        into the node via all connected ports equals the mass out of the
        node via all connected ports. c) The flow direction of a port
        connected to the node may be transient. That is, flow direction
        may change toward any port if the relative internal pressure of
        the Product Flow Units change and a new steady state is
        achieved.
    :ivar plan_name: The name of a network plan. This indicates a
        planned connection. The connected port must be part of the same
        plan or be an actual. Not specified indicates an actual
        connection.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    node: Optional[str] = field(
        default=None,
        metadata={
            "name": "Node",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    plan_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PlanName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class ControlLineEncapsulationSize(Enum):
    """
    Specifies the control line encapsulation sizes.

    :cvar VALUE_11X11: 11x11
    :cvar VALUE_23X11: 23x11
    """

    VALUE_11X11 = "11x11"
    VALUE_23X11 = "23x11"


class ControlLineEncapsulationType(Enum):
    """
    Specifies the control line encapsulation types.

    :cvar ROUND: round
    :cvar SQUARE: square
    """

    ROUND = "round"
    SQUARE = "square"


class ControlLineMaterial(Enum):
    """
    Specifies the types of control line material.

    :cvar INC_825: inc 825
    :cvar SS_316: ss 316
    """

    INC_825 = "inc 825"
    SS_316 = "ss 316"


class ControlLineSize(Enum):
    """
    Specifies the control line sizes.

    :cvar DIAMETER_0_25_IN_WEIGHT_0_028_LB_FT: diameter 0.25 in weight
        0.028 lb/ft
    :cvar DIAMETER_0_25_IN_WEIGHT_0_035_LB_FT: diameter 0.25 in weight
        0.035 lb/ft
    :cvar DIAMETER_0_375_IN_WEIGHT_0_048_LB_FT: diameter 0.375 in weight
        0.048 lb/ft
    """

    DIAMETER_0_25_IN_WEIGHT_0_028_LB_FT = "diameter 0.25 in weight 0.028 lb/ft"
    DIAMETER_0_25_IN_WEIGHT_0_035_LB_FT = "diameter 0.25 in weight 0.035 lb/ft"
    DIAMETER_0_375_IN_WEIGHT_0_048_LB_FT = (
        "diameter 0.375 in weight 0.048 lb/ft"
    )


class CrewType(Enum):
    """
    Specifies the types of production operations personnel grouping.

    :cvar CATERING_CREW: A count that is the number of persons from the
        catering contractor spending the night at the installation.
    :cvar CONTRACTOR_CREW: A count that is the number of persons from
        other than operator spending the night at the installation.
    :cvar DAY_VISITORS: A count that is the number of persons visiting
        the installation but not  spending the night at the
        installation.
    :cvar DRILLING_CONTRACT_CREW: A count that is the number of persons
        from the drilling contractor spending the night at the
        installation.
    :cvar OTHER_CREW: A count that is the number of persons from an
        unknown source, normally not working on the installation but
        spending the night there.
    :cvar OWN_CREW: A count that is the number of persons from the
        operator, normally working on the installation and spending the
        night there.
    :cvar OWN_OTHER_CREW: A count that is the number of persons from the
        operator, normally not working on the installation but spending
        the night there.
    :cvar PERSONNEL_ON_BOARD: A count of the total personnel on board.
    """

    CATERING_CREW = "catering crew"
    CONTRACTOR_CREW = "contractor crew"
    DAY_VISITORS = "day visitors"
    DRILLING_CONTRACT_CREW = "drilling contract crew"
    OTHER_CREW = "other crew"
    OWN_CREW = "own crew"
    OWN_OTHER_CREW = "own other crew"
    PERSONNEL_ON_BOARD = "personnel on board"


@dataclass
class CurveDefinition:
    """
    The definition of a curve.

    :ivar is_index: True (equal "1" or "true") indicates that this is an
        independent variable in this curve. At least one column column
        should be flagged as independent.
    :ivar measure_class: The measure class of the variable. This defines
        which units of measure are valid for the value.
    :ivar order: The order of the value in the index or data tuple. If
        isIndex is true, this is the order of the (independent) index
        element. If isIndex is false, this is the order of the
        (dependent) value element.
    :ivar parameter: The name of the variable in this curve.
    :ivar unit: The unit of measure of the variable. The unit of measure
        must match a unit allowed by the measure class.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    is_index: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    measure_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeasureClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    order: Optional[str] = field(
        default=None,
        metadata={
            "name": "Order",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class CustomPvtModelParameter:
    """
    Custom PVT model parameter.

    :ivar custom_parameter_value:
    :ivar fluid_component_reference: Reference to a fluid component to
        which this custom model parameter applies.
    """

    custom_parameter_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "CustomParameterValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fluid_component_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "fluidComponentReference",
            "type": "Attribute",
        },
    )


@dataclass
class DasAcquisition:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


class DasCalibrationType(Enum):
    """
    Specifies the types of calibration.

    :cvar LAST_LOCUS_TO_END_OF_FIBER: Calibration point describing the
        fiber distance between the last locus acquired and the end of
        the fiber.
    :cvar LOCUS_CALIBRATION: Calibration point describing the
        relationship between acquired locus number, optical path (fiber)
        distance, and facility length.
    :cvar TAP_TEST: Calibration point describing the location of the
        (well head) tap test as a relationship between estimated locus
        number, optical path (fiber) distance, and facility length. This
        calibration point is often acquired in the field during
        acquisition start to obtain the approximate  position of the
        well head along the fiber.
    """

    LAST_LOCUS_TO_END_OF_FIBER = "last locus to end of fiber"
    LOCUS_CALIBRATION = "locus calibration"
    TAP_TEST = "tap test"


@dataclass
class DasCustom:
    """This object contains service–provider-specific customization parameters.

    Service providers can define the contents of this data element as
    required. This data object has intentionally not been described in
    detail to allow for flexibility. Note that this object is optional
    and if used, the service provider needs to provide a description of
    the data elements to the customer.
    """


class DasDimensions(Enum):
    """Specifies the possible orientations of the data array. For multiple H5
    files:

    - Must specify that the indexes split OVER TIME
    - Even if loci were the index
    - Each divided file still contains the split time array

    :cvar FREQUENCY: Enumeration value to indicate the frequency
        dimension in a multi-dimensional array.
    :cvar LOCUS: Enumeration value to indicate the locus dimension in a
        multi-dimensional array.
    :cvar TIME: Enumeration value to indicate the time dimension in a
        multi-dimensional array.
    """

    FREQUENCY = "frequency"
    LOCUS = "locus"
    TIME = "time"


@dataclass
class DasExternalDatasetPart:
    """Array of integer values provided explicitly by an HDF5 dataset.

    The null value must be  explicitly provided in the NullValue
    attribute of this class.

    :ivar part_end_time: The timestamp in human readable, ISO 8601
        format of the last recorded sample in the sub-record of the raw
        data array stored in the corresponding HDF data file.
    :ivar part_start_time: The timestamp in human readable, ISO 8601
        format of the first recorded sample in the sub-record of the raw
        data array stored in the corresponding HDF data file.
    """

    part_end_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PartEndTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    part_start_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PartStartTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DasInstrumentBox:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class DasTimeArray:
    """The Times arrays contain the ‘scan’ or ‘trace’ times at which the raw, FBE
    and spectrum arrays were acquired or processed:

    - For raw data, these are the times for which all loci in the ‘scanned’ fiber section were interrogated by a single pulse of the DAS measurement system.
    - For the processed data, these are the times of the first sample in the time window used in the frequency filter or transformation function to calculate the FBE or spectrum data.

    :ivar end_time: The timestamp in human readable, ISO 8601 format of
        the last recorded sample in the acquisition. Note that this is
        the end time of the acquistion if a raw data set is stored in
        multiple HDF files. The end time of the sub-record stored in an
        individual HDF file is stored in PartEndTime.
    :ivar start_time: The timestamp in human readable, ISO 8601 format
        of the last recorded sample in the acquistion. Note that this is
        the start time of the acquistion if a raw dataset is stored in
        multiple HDF files. The end time of the sub-record stored in an
        individual HDF file is stored in PartStartTime.
    :ivar time_array:
    """

    end_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EndTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    start_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    time_array: Optional[str] = field(
        default=None,
        metadata={
            "name": "TimeArray",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DatedComment:
    """
    A general time-stamped comment structure.

    :ivar end_time: The date and time where the comment is no longer
        valid.
    :ivar remark: Remarks and comments about this data item.
    :ivar role: The role of the person providing the comment. This is
        the role of the person within the context of comment.
    :ivar start_time: The date and time where the comment begins to be
        valid.
    :ivar who: The name of the person providing the comment.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    end_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "EndTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    role: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Role",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    start_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "StartTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    who: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Who",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class DispositionKind(Enum):
    """
    Specifies the set of categories used to account for how crude oil and petroleum
    products are transferred, distributed, or removed from the supply stream
    (e.g.,stock change, crude oil losses, exports, sales, etc.).

    :cvar FLARED: Burned in a flare.
    :cvar SOLD: Sold and transported to a buyer by pipeline.
    :cvar USED_ON_SITE: Used for entity operations.
    :cvar FUEL: Consumed by processing equipment.
    :cvar VENTED: Released into the atmosphere.
    :cvar DISPOSAL: Disposed of.
    :cvar GAS_LIFT: Injected into a producing well for artificial lift.
    :cvar LOST_OR_STOLEN: Lost or stolen.
    :cvar OTHER: Physically removed from the entity location.
    """

    FLARED = "flared"
    SOLD = "sold"
    USED_ON_SITE = "used on-site"
    FUEL = "fuel"
    VENTED = "vented"
    DISPOSAL = "disposal"
    GAS_LIFT = "gas lift"
    LOST_OR_STOLEN = "lost or stolen"
    OTHER = "other"


@dataclass
class DowntimeReasonCode:
    """Codes to categorize the reason for downtime.

    These codes are company specific so they are not part of PRODML.
    Company's can use this schema to specify their downtime codes.

    :ivar name: Name or explanation of the code specified in the code
        attribute.
    :ivar parent:
    :ivar authority: The authority (usually a company) that defines the
        codes.
    :ivar code: The code value.
    """

    name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    parent: Optional[DowntimeReasonCode] = field(
        default=None,
        metadata={
            "name": "Parent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    authority: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class DtsInstalledSystem:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class DtsInstrumentBox:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class DtsMeasurement:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class DtsPatchCord:
    """
    Information regarding the patch cord used to connect the instrument box to the
    start of the optical fiber path.

    :ivar description: A textual description of the patch cord.
    :ivar fiber_length: Optical distance between the instrument and the
        end of the patch cord that will be attached to the rest of the
        optical path from which a measurement will be taken.
    """

    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fiber_length: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FiberLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


class EndpointQualifier(Enum):
    """
    Specifies values for the endpoint for min/max query parameters on "growing
    objects".

    :cvar EXCLUSIVE: The value is excluded.
    :cvar EXTENSIVE: The endpoint of the range may be extended to the
        first encountered value if an exact value match is not
        found.That is, if a node index value does not match the
        specified range value then the next smaller value (on minimum
        end) or larger value (on maximum end) in the index series should
        be used as the endpoint. Basically, this concept is designed to
        support interpolation across an undefined point.
    :cvar INCLUSIVE: The value is included.
    :cvar OVERLAP_EXTENSIVE: The endpoint of the range may be extended
        to the first encountered value if the interval is overlapped
        with the index interval. That is, if a node index value does not
        match the specified range value then the next smaller value (on
        minimum end) or larger value (on maximum end) in the index
        series should be used as the endpoint. This concept is designed
        to select ALL nodes whose index interval overlap with the query
        range.
    """

    EXCLUSIVE = "exclusive"
    EXTENSIVE = "extensive"
    INCLUSIVE = "inclusive"
    OVERLAP_EXTENSIVE = "overlap extensive"


class EndpointQualifierInterval(Enum):
    """
    Specifies the meaning of the endpoint for a simple interval.

    :cvar EXCLUSIVE: The value is excluded.
    :cvar INCLUSIVE: The value is included.
    :cvar UNKNOWN: The value is unknown.
    """

    EXCLUSIVE = "exclusive"
    INCLUSIVE = "inclusive"
    UNKNOWN = "unknown"


class EstimationMethod(Enum):
    """
    Specifies the methods for estimating deferred production.

    :cvar ANALYTICS_MODEL: analytics model
    :cvar DECLINE_CURVE: decline curve
    :cvar EXPERT_RECOMMENDATION: recommendation text
    :cvar FLOWING_MATERIAL_BALANCE: flowing material balance
    :cvar FROM_LAST_ALLOCATED_VOLUME: from last allocated volume
    :cvar NUMERICAL_RESERVOIR_SIMULATION: numerical reservoir simulation
    :cvar PRODUCTION_PROFILE: production profile
    :cvar RATE_TRANSIENT_ANALYSIS: rate transient analysis
    :cvar RATIO_ANALYSIS: ration analysis
    :cvar RESERVOIR_MODEL: reservoir model
    :cvar WELL_MODEL: well model
    """

    ANALYTICS_MODEL = "analytics model"
    DECLINE_CURVE = "decline curve"
    EXPERT_RECOMMENDATION = "expert recommendation"
    FLOWING_MATERIAL_BALANCE = "flowing material balance"
    FROM_LAST_ALLOCATED_VOLUME = "from last allocated volume"
    NUMERICAL_RESERVOIR_SIMULATION = "numerical reservoir simulation"
    PRODUCTION_PROFILE = "production profile"
    RATE_TRANSIENT_ANALYSIS = "rate transient analysis"
    RATIO_ANALYSIS = "ratio analysis"
    RESERVOIR_MODEL = "reservoir model"
    WELL_MODEL = "well model"


@dataclass
class ExpectedFlowQualifier:
    pass


class FacilityKind(Enum):
    """
    Specifies the types of facility kinds.

    :cvar GENERIC: The calibration affects the acquisition which runs
        neither inside a well or a pipeline.
    :cvar PIPELINE: The calibration affects the acquisition which runs
        inside a pipeline.
    :cvar WELL: The calibration affects the acquisition which runs
        inside a well.
    """

    GENERIC = "generic"
    PIPELINE = "pipeline"
    WELL = "well"


class FacilityParameter(Enum):
    """
    Specifies the kinds of facility parameters.

    :cvar ABSORBED_DOSE_CLASS: The amount of energy absorbed per mass.
    :cvar ACCELERATION_LINEAR_CLASS: Acceleration linear class.
    :cvar ACTIVITY_OF_RADIOACTIVITY_CLASS: A measure of the radiation
        being emitted.
    :cvar ALARM_ABSOLUTE_PRESSURE: Absolute minimum pressure of the flow
        stream before the system gives an alarm. Equivalent to element
        absoluteMinPres in the ProductVolume data schema.
    :cvar AMOUNT_OF_SUBSTANCE_CLASS: Molar amount of a substance.
    :cvar ANGLE_PER_LENGTH: Angle per length.
    :cvar ANGLE_PER_TIME: The angular velocity. The rate of change of an
        angle.
    :cvar ANGLE_PER_VOLUME: Angle per volume.
    :cvar ANGULAR_ACCELERATION_CLASS: Angular acceleration class.
    :cvar ANNULUS_INNER_DIAMETER: Annulus inner diameter.
    :cvar ANNULUS_OUTER_DIAMETER: Annulus outer diameter.
    :cvar AREA_CLASS: Area class.
    :cvar AREA_PER_AREA: A dimensionless quantity where the basis of the
        ratio is area.
    :cvar AREA_PER_VOLUME: Area per volume.
    :cvar ATMOSPHERIC_PRESSURE: The average atmospheric pressure during
        the reporting period. Equivalent to element atmosphere in the
        ProductVolume data schema.
    :cvar ATTENUATION_CLASS: A logarithmic, fractional change of some
        measure, generally power or amplitude, over a standard range.
        This is generally used for frequency attenuation over an octave.
    :cvar ATTENUATION_PER_LENGTH: Attenuation per length.
    :cvar AVAILABLE: Indicates the availability of the facility. This
        should be implemented as a string value. A value of "true"
        indicates that it is available for use. That is, it may be
        currently shut-down but it can be restarted. A value of "false"
        indicates that the facility is not available to be used. That
        is, it cannot be restarted at this time.
    :cvar AVAILABLE_ROOM: Defines the unoccupied volume of a tank. Zero
        indicates that the tank is full.
    :cvar BLOCK_VALVE_STATUS: Indicates the status of a block valve.
        This should be implemented as a string value. A value of "open"
        indicates that it is open. A value of "closed" indicates that it
        is closed.
    :cvar CAPACITANCE_CLASS: Capacitance class.
    :cvar CATEGORICAL: The abstract supertype of all enumerated string
        properties.
    :cvar CATHODIC_PROTECTION_OUTPUT_CURRENT: Rectifier DC output
        current.
    :cvar CATHODIC_PROTECTION_OUTPUT_VOLTAGE: Rectifier DC output
        voltage.
    :cvar CHARGE_DENSITY_CLASS: Charge density class.
    :cvar CHEMICAL_POTENTIAL_CLASS: Chemical potential class.
    :cvar CHOKE_POSITION: A coded value describing the position of the
        choke (open, close, traveling).
    :cvar CHOKE_SETTING: A fraction value (percentage) of the choke
        opening.
    :cvar CODE: A property whose values are constrained to specific
        string values
    :cvar COMPRESSIBILITY_CLASS: Compressibility class.
    :cvar CONCENTRATION_OF_B_CLASS: Concentration of B class.
    :cvar CONDUCTIVITY_CLASS: Conductivity class.
    :cvar CONTINUOUS: Continuous.
    :cvar CROSS_SECTION_ABSORPTION_CLASS: Cross section absorption
        class.
    :cvar CURRENT_DENSITY_CLASS: Current density class.
    :cvar DARCY_FLOW_COEFFICIENT_CLASS: Darcy flow coefficient class.
    :cvar DATA_TRANSMISSION_SPEED_CLASS: Data transmission speed class.
    :cvar DELTA_TEMPERATURE_CLASS: Delta temperature class.
    :cvar DENSITY: Density.
    :cvar DENSITY_CLASS: Density class.
    :cvar DENSITY_FLOW_RATE: Density flow rate.
    :cvar DENSITY_STANDARD: Density standard.
    :cvar DEWPOINT_TEMPERATURE: Dewpoint temperature.
    :cvar DIFFERENTIAL_PRESSURE: Differential pressure.
    :cvar DIFFERENTIAL_TEMPERATURE: differential temperature
    :cvar DIFFUSION_COEFFICIENT_CLASS: diffusion coefficient class
    :cvar DIGITAL_STORAGE_CLASS: digital storage class
    :cvar DIMENSIONLESS_CLASS: dimensionless class
    :cvar DISCRETE: discrete
    :cvar DOSE_EQUIVALENT_CLASS: dose equivalent class
    :cvar DOSE_EQUIVALENT_RATE_CLASS: dose equivalent rate class
    :cvar DYNAMIC_VISCOSITY_CLASS: dynamic viscosity class
    :cvar ELECTRIC_CHARGE_CLASS: electric charge class
    :cvar ELECTRIC_CONDUCTANCE_CLASS: electric conductance class
    :cvar ELECTRIC_CURRENT_CLASS: electric current class
    :cvar ELECTRIC_DIPOLE_MOMENT_CLASS: electric dipole moment class
    :cvar ELECTRIC_FIELD_STRENGTH_CLASS: electric field strength class
    :cvar ELECTRIC_POLARIZATION_CLASS: electric polarization class
    :cvar ELECTRIC_POTENTIAL_CLASS: electric potential class
    :cvar ELECTRICAL_RESISTIVITY_CLASS: electrical resistivity class
    :cvar ELECTROCHEMICAL_EQUIVALENT_CLASS: electrochemical equivalent
        class
    :cvar ELECTROMAGNETIC_MOMENT_CLASS: electromagnetic moment class
    :cvar ENERGY_LENGTH_PER_AREA: energy length per area
    :cvar ENERGY_LENGTH_PER_TIME_AREA_TEMPERATURE: energy length per
        time area temperature
    :cvar ENERGY_PER_AREA: energy per area
    :cvar ENERGY_PER_LENGTH: energy per length
    :cvar EQUIVALENT_PER_MASS: equivalent per mass
    :cvar EQUIVALENT_PER_VOLUME: equivalent per volume
    :cvar EXPOSURE_RADIOACTIVITY_CLASS: exposure (radioactivity) class
    :cvar FACILITY_UPTIME: facility uptime
    :cvar FLOW_RATE: flow rate
    :cvar FLOW_RATE_STANDARD: flow rate standard
    :cvar FORCE_AREA_CLASS: force area class
    :cvar FORCE_CLASS: force class
    :cvar FORCE_LENGTH_PER_LENGTH: force length per length
    :cvar FORCE_PER_FORCE: force per force
    :cvar FORCE_PER_LENGTH: force per length
    :cvar FORCE_PER_VOLUME: force per volume
    :cvar FREQUENCY_CLASS: frequency class
    :cvar FREQUENCY_INTERVAL_CLASS: frequency interval class
    :cvar GAMMA_RAY_API_UNIT_CLASS: gamma ray API unit class
    :cvar GAS_LIQUID_RATIO: gas liquid ratio
    :cvar GAS_OIL_RATIO: gas oil ratio
    :cvar GROSS_CALORIFIC_VALUE_STANDARD: gross calorific value standard
    :cvar HEAT_CAPACITY_CLASS: heat capacity class
    :cvar HEAT_FLOW_RATE_CLASS: heat flow rate class
    :cvar HEAT_TRANSFER_COEFFICIENT_CLASS: heat transfer coefficient
        class
    :cvar ILLUMINANCE_CLASS: illuminance class
    :cvar INTERNAL_CONTROL_VALVE_STATUS: internal control valve status
    :cvar IRRADIANCE_CLASS: irradiance class
    :cvar ISOTHERMAL_COMPRESSIBILITY_CLASS: isothermal compressibility
        class
    :cvar KINEMATIC_VISCOSITY_CLASS: kinematic viscosity class
    :cvar LENGTH_CLASS: length class
    :cvar LENGTH_PER_LENGTH: length per length
    :cvar LENGTH_PER_TEMPERATURE: length per temperature
    :cvar LENGTH_PER_VOLUME: length per volume
    :cvar LEVEL_OF_POWER_INTENSITY_CLASS: level of power intensity class
    :cvar LIGHT_EXPOSURE_CLASS: light exposure class
    :cvar LINEAR_THERMAL_EXPANSION_CLASS: linear thermal expansion class
    :cvar LUMINANCE_CLASS: luminance class
    :cvar LUMINOUS_EFFICACY_CLASS: luminous efficacy class
    :cvar LUMINOUS_FLUX_CLASS: luminous flux class
    :cvar LUMINOUS_INTENSITY_CLASS: luminous intensity class
    :cvar MAGNETIC_DIPOLE_MOMENT_CLASS: magnetic dipole moment class
    :cvar MAGNETIC_FIELD_STRENGTH_CLASS: magnetic field strength class
    :cvar MAGNETIC_FLUX_CLASS: magnetic flux class
    :cvar MAGNETIC_INDUCTION_CLASS: magnetic induction class
    :cvar MAGNETIC_PERMEABILITY_CLASS: magnetic permeability class
    :cvar MAGNETIC_VECTOR_POTENTIAL_CLASS: magnetic vector potential
        class
    :cvar MASS: mass
    :cvar MASS_ATTENUATION_COEFFICIENT_CLASS: mass attenuation
        coefficient class
    :cvar MASS_CLASS: mass class
    :cvar MASS_CONCENTRATION: mass concentration
    :cvar MASS_CONCENTRATION_CLASS: mass concentration class
    :cvar MASS_FLOW_RATE_CLASS: mass flow rate class
    :cvar MASS_LENGTH_CLASS: mass length class
    :cvar MASS_PER_ENERGY: mass per energy
    :cvar MASS_PER_LENGTH: mass per length
    :cvar MASS_PER_TIME_PER_AREA: mass per time per area
    :cvar MASS_PER_TIME_PER_LENGTH: mass per time per length
    :cvar MASS_PER_VOLUME_PER_LENGTH: mass per volume per length
    :cvar MEASURED_DEPTH: measured depth
    :cvar MOBILITY_CLASS: mobility class
    :cvar MODULUS_OF_COMPRESSION_CLASS: modulus of compression class
    :cvar MOLAR_CONCENTRATION: molar concentration
    :cvar MOLAR_FRACTION: molar fraction
    :cvar MOLAR_HEAT_CAPACITY_CLASS: molar heat capacity class
    :cvar MOLAR_VOLUME_CLASS: molar volume class
    :cvar MOLE_PER_AREA: mole per area
    :cvar MOLE_PER_TIME: mole per time
    :cvar MOLE_PER_TIME_PER_AREA: mole per time per area
    :cvar MOLECULAR_WEIGHT: molecular weight
    :cvar MOMENT_OF_FORCE_CLASS: moment of force class
    :cvar MOMENT_OF_INERTIA_CLASS: moment of inertia class
    :cvar MOMENT_OF_SECTION_CLASS: moment of section class
    :cvar MOMENTUM_CLASS: momentum class
    :cvar MOTOR_CURRENT: motor current
    :cvar MOTOR_CURRENT_LEAKAGE: motor current leakage
    :cvar MOTOR_SPEED: motor speed
    :cvar MOTOR_TEMPERATURE: motor temperature
    :cvar MOTOR_VIBRATION: motor vibration
    :cvar MOTOR_VOLTAGE: motor voltage
    :cvar NEUTRON_API_UNIT_CLASS: neutron API unit class
    :cvar NON_DARCY_FLOW_COEFFICIENT_CLASS: nonDarcy flow coefficient
        class
    :cvar OPENING_SIZE: opening size
    :cvar OPERATIONS_PER_TIME: operations per time
    :cvar PARACHOR_CLASS: parachor class
    :cvar PER_AREA: per area
    :cvar PER_ELECTRIC_POTENTIAL: per electric potential
    :cvar PER_FORCE: per force
    :cvar PER_LENGTH: per length
    :cvar PER_MASS: per mass
    :cvar PER_VOLUME: per volume
    :cvar PERMEABILITY_LENGTH_CLASS: permeability length class
    :cvar PERMEABILITY_ROCK_CLASS: permeability rock class
    :cvar PERMEANCE_CLASS: permeance class
    :cvar PERMITTIVITY_CLASS: permittivity class
    :cvar P_H_CLASS: pH class
    :cvar PLANE_ANGLE_CLASS: plane angle class
    :cvar POTENTIAL_DIFFERENCE_PER_POWER_DROP: potential difference per
        power drop
    :cvar POWER_CLASS: power class
    :cvar POWER_PER_VOLUME: power per volume
    :cvar PRESSURE: pressure
    :cvar PRESSURE_CLASS: pressure class
    :cvar PRESSURE_PER_TIME: pressure per time
    :cvar PRESSURE_SQUARED_CLASS: pressure squared class
    :cvar PRESSURE_SQUARED_PER_FORCE_TIME_PER_AREA: pressure squared per
        force time per area
    :cvar PRESSURE_TIME_PER_VOLUME: pressure time per volume
    :cvar PRODUCTIVITY_INDEX_CLASS: productivity index class
    :cvar PUMP_COUNT_ONLINE: pump count online
    :cvar PUMP_STATUS: pump status
    :cvar QUANTITY: quantity
    :cvar QUANTITY_OF_LIGHT_CLASS: quantity of light class
    :cvar RADIANCE_CLASS: radiance class
    :cvar RADIANT_INTENSITY_CLASS: radiant intensity class
    :cvar RECIPROCATING_SPEED: reciprocating speed
    :cvar RECTIFIER_STRUCTURE_POTENTIAL: rectifier structure potential
    :cvar REID_VAPOR_PRESSURE: reid vapor pressure
    :cvar RELATIVE_OPENING_SIZE: relative opening size
    :cvar RELATIVE_POWER_CLASS: relative power class
    :cvar RELATIVE_TANK_LEVEL: relative tank level
    :cvar RELATIVE_TIME_CLASS: relative time class
    :cvar RELATIVE_VALVE_OPENING: relative valve opening
    :cvar RELUCTANCE_CLASS: reluctance class
    :cvar RESISTANCE_CLASS: resistance class
    :cvar RESISTIVITY_PER_LENGTH: resistivity per length
    :cvar ROOT_PROPERTY: root property
    :cvar SCHEDULED_DOWNTIME: scheduled downtime
    :cvar SECOND_MOMENT_OF_AREA_CLASS: second moment of area class
    :cvar SHUTDOWN_ORDER: shutdown order
    :cvar SHUTIN_PRESSURE: shutin pressure
    :cvar SHUTIN_TEMPERATURE: shutin temperature
    :cvar SOLID_ANGLE_CLASS: solid angle class
    :cvar SPECIFIC_ACTIVITY_OF_RADIOACTIVITY: specific activity (of
        radioactivity)
    :cvar SPECIFIC_ENERGY_CLASS: specific energy class
    :cvar SPECIFIC_GRAVITY: specific gravity
    :cvar SPECIFIC_HEAT_CAPACITY_CLASS: specific heat capacity class
    :cvar SPECIFIC_PRODUCTIVITY_INDEX_CLASS: specific productivity index
        class
    :cvar SPECIFIC_VOLUME_CLASS: specific volume class
    :cvar SUB_SURFACE_SAFETY_VALVE_STATUS: sub surface safety valve
        status
    :cvar SURFACE_DENSITY_CLASS: surface density class
    :cvar SURFACE_SAFETY_VALVE_STATUS: surface safety valve status
    :cvar TANK_FLUID_LEVEL: tank fluid level
    :cvar TANK_PRODUCT_STANDARD_VOLUME: tank product standard volume
    :cvar TANK_PRODUCT_VOLUME: tank product volume
    :cvar TEMPERATURE: temperature
    :cvar TEMPERATURE_PER_LENGTH: temperature per length
    :cvar TEMPERATURE_PER_TIME: temperature per time
    :cvar THERMAL_CONDUCTANCE_CLASS: thermal conductance class
    :cvar THERMAL_CONDUCTIVITY_CLASS: thermal conductivity class
    :cvar THERMAL_DIFFUSIVITY_CLASS: thermal diffusivity class
    :cvar THERMAL_INSULANCE_CLASS: thermal insulance class
    :cvar THERMAL_RESISTANCE_CLASS: thermal resistance class
    :cvar THERMODYNAMIC_TEMPERATURE_CLASS: thermodynamic temperature
        class
    :cvar TIME_CLASS: time class
    :cvar TIME_PER_LENGTH: time per length
    :cvar TIME_PER_VOLUME: time per volume
    :cvar TRUE_VAPOR_PRESSURE: true vapor pressure
    :cvar UNIT_PRODUCTIVITY_INDEX_CLASS: unit productivity index class
    :cvar UNITLESS: unitless
    :cvar UNKNOWN: unknown
    :cvar VALVE_OPENING: valve opening
    :cvar VALVE_STATUS: valve status
    :cvar VELOCITY_CLASS: velocity class
    :cvar VOLUME: volume
    :cvar VOLUME_CLASS: volume class
    :cvar VOLUME_CONCENTRATION: volume concentration
    :cvar VOLUME_FLOW_RATE_CLASS: volume flow rate class
    :cvar VOLUME_LENGTH_PER_TIME: volume length per time
    :cvar VOLUME_PER_AREA: volume per area
    :cvar VOLUME_PER_LENGTH: volume per length
    :cvar VOLUME_PER_TIME_PER_AREA: volume per time per area
    :cvar VOLUME_PER_TIME_PER_LENGTH: volume per time per length
    :cvar VOLUME_PER_TIME_PER_TIME: volume per time per time
    :cvar VOLUME_PER_TIME_PER_VOLUME: volume per time per volume
    :cvar VOLUME_PER_VOLUME: volume per volume
    :cvar VOLUME_STANDARD: volume standard
    :cvar VOLUMETRIC_EFFICIENCY: volumetric efficiency
    :cvar VOLUMETRIC_HEAT_TRANSFER_COEFFICIENT: volumetric heat transfer
        coefficient
    :cvar VOLUMETRIC_THERMAL_EXPANSION_CLASS: volumetric thermal
        expansion class
    :cvar WELL_OPERATING_STATUS: well operating status
    :cvar WELL_OPERATION_TYPE: well operation type
    :cvar WOBBE_INDEX: wobbe index
    :cvar WORK: work
    :cvar WORK_CLASS: work class
    """

    ABSORBED_DOSE_CLASS = "absorbed dose class"
    ACCELERATION_LINEAR_CLASS = "acceleration linear class"
    ACTIVITY_OF_RADIOACTIVITY_CLASS = "activity (of radioactivity) class"
    ALARM_ABSOLUTE_PRESSURE = "alarm absolute pressure"
    AMOUNT_OF_SUBSTANCE_CLASS = "amount of substance class"
    ANGLE_PER_LENGTH = "angle per length"
    ANGLE_PER_TIME = "angle per time"
    ANGLE_PER_VOLUME = "angle per volume"
    ANGULAR_ACCELERATION_CLASS = "angular acceleration class"
    ANNULUS_INNER_DIAMETER = "annulus inner diameter"
    ANNULUS_OUTER_DIAMETER = "annulus outer diameter"
    AREA_CLASS = "area class"
    AREA_PER_AREA = "area per area"
    AREA_PER_VOLUME = "area per volume"
    ATMOSPHERIC_PRESSURE = "atmospheric pressure"
    ATTENUATION_CLASS = "attenuation class"
    ATTENUATION_PER_LENGTH = "attenuation per length"
    AVAILABLE = "available"
    AVAILABLE_ROOM = "available room"
    BLOCK_VALVE_STATUS = "block valve status"
    CAPACITANCE_CLASS = "capacitance class"
    CATEGORICAL = "categorical"
    CATHODIC_PROTECTION_OUTPUT_CURRENT = "cathodic protection output current"
    CATHODIC_PROTECTION_OUTPUT_VOLTAGE = "cathodic protection output voltage"
    CHARGE_DENSITY_CLASS = "charge density class"
    CHEMICAL_POTENTIAL_CLASS = "chemical potential class"
    CHOKE_POSITION = "choke position"
    CHOKE_SETTING = "choke setting"
    CODE = "code"
    COMPRESSIBILITY_CLASS = "compressibility class"
    CONCENTRATION_OF_B_CLASS = "concentration of B class"
    CONDUCTIVITY_CLASS = "conductivity class"
    CONTINUOUS = "continuous"
    CROSS_SECTION_ABSORPTION_CLASS = "cross section absorption class"
    CURRENT_DENSITY_CLASS = "current density class"
    DARCY_FLOW_COEFFICIENT_CLASS = "darcy flow coefficient class"
    DATA_TRANSMISSION_SPEED_CLASS = "data transmission speed class"
    DELTA_TEMPERATURE_CLASS = "delta temperature class"
    DENSITY = "density"
    DENSITY_CLASS = "density class"
    DENSITY_FLOW_RATE = "density flow rate"
    DENSITY_STANDARD = "density standard"
    DEWPOINT_TEMPERATURE = "dewpoint temperature"
    DIFFERENTIAL_PRESSURE = "differential pressure"
    DIFFERENTIAL_TEMPERATURE = "differential temperature"
    DIFFUSION_COEFFICIENT_CLASS = "diffusion coefficient class"
    DIGITAL_STORAGE_CLASS = "digital storage class"
    DIMENSIONLESS_CLASS = "dimensionless class"
    DISCRETE = "discrete"
    DOSE_EQUIVALENT_CLASS = "dose equivalent class"
    DOSE_EQUIVALENT_RATE_CLASS = "dose equivalent rate class"
    DYNAMIC_VISCOSITY_CLASS = "dynamic viscosity class"
    ELECTRIC_CHARGE_CLASS = "electric charge class"
    ELECTRIC_CONDUCTANCE_CLASS = "electric conductance class"
    ELECTRIC_CURRENT_CLASS = "electric current class"
    ELECTRIC_DIPOLE_MOMENT_CLASS = "electric dipole moment class"
    ELECTRIC_FIELD_STRENGTH_CLASS = "electric field strength class"
    ELECTRIC_POLARIZATION_CLASS = "electric polarization class"
    ELECTRIC_POTENTIAL_CLASS = "electric potential class"
    ELECTRICAL_RESISTIVITY_CLASS = "electrical resistivity class"
    ELECTROCHEMICAL_EQUIVALENT_CLASS = "electrochemical equivalent class"
    ELECTROMAGNETIC_MOMENT_CLASS = "electromagnetic moment class"
    ENERGY_LENGTH_PER_AREA = "energy length per area"
    ENERGY_LENGTH_PER_TIME_AREA_TEMPERATURE = (
        "energy length per time area temperature"
    )
    ENERGY_PER_AREA = "energy per area"
    ENERGY_PER_LENGTH = "energy per length"
    EQUIVALENT_PER_MASS = "equivalent per mass"
    EQUIVALENT_PER_VOLUME = "equivalent per volume"
    EXPOSURE_RADIOACTIVITY_CLASS = "exposure (radioactivity) class"
    FACILITY_UPTIME = "facility uptime"
    FLOW_RATE = "flow rate"
    FLOW_RATE_STANDARD = "flow rate standard"
    FORCE_AREA_CLASS = "force area class"
    FORCE_CLASS = "force class"
    FORCE_LENGTH_PER_LENGTH = "force length per length"
    FORCE_PER_FORCE = "force per force"
    FORCE_PER_LENGTH = "force per length"
    FORCE_PER_VOLUME = "force per volume"
    FREQUENCY_CLASS = "frequency class"
    FREQUENCY_INTERVAL_CLASS = "frequency interval class"
    GAMMA_RAY_API_UNIT_CLASS = "gamma ray API unit class"
    GAS_LIQUID_RATIO = "gas liquid ratio"
    GAS_OIL_RATIO = "gas oil ratio"
    GROSS_CALORIFIC_VALUE_STANDARD = "gross calorific value standard"
    HEAT_CAPACITY_CLASS = "heat capacity class"
    HEAT_FLOW_RATE_CLASS = "heat flow rate class"
    HEAT_TRANSFER_COEFFICIENT_CLASS = "heat transfer coefficient class"
    ILLUMINANCE_CLASS = "illuminance class"
    INTERNAL_CONTROL_VALVE_STATUS = "internal control valve status"
    IRRADIANCE_CLASS = "irradiance class"
    ISOTHERMAL_COMPRESSIBILITY_CLASS = "isothermal compressibility class"
    KINEMATIC_VISCOSITY_CLASS = "kinematic viscosity class"
    LENGTH_CLASS = "length class"
    LENGTH_PER_LENGTH = "length per length"
    LENGTH_PER_TEMPERATURE = "length per temperature"
    LENGTH_PER_VOLUME = "length per volume"
    LEVEL_OF_POWER_INTENSITY_CLASS = "level of power intensity class"
    LIGHT_EXPOSURE_CLASS = "light exposure class"
    LINEAR_THERMAL_EXPANSION_CLASS = "linear thermal expansion class"
    LUMINANCE_CLASS = "luminance class"
    LUMINOUS_EFFICACY_CLASS = "luminous efficacy class"
    LUMINOUS_FLUX_CLASS = "luminous flux class"
    LUMINOUS_INTENSITY_CLASS = "luminous intensity class"
    MAGNETIC_DIPOLE_MOMENT_CLASS = "magnetic dipole moment class"
    MAGNETIC_FIELD_STRENGTH_CLASS = "magnetic field strength class"
    MAGNETIC_FLUX_CLASS = "magnetic flux class"
    MAGNETIC_INDUCTION_CLASS = "magnetic induction class"
    MAGNETIC_PERMEABILITY_CLASS = "magnetic permeability class"
    MAGNETIC_VECTOR_POTENTIAL_CLASS = "magnetic vector potential class"
    MASS = "mass"
    MASS_ATTENUATION_COEFFICIENT_CLASS = "mass attenuation coefficient class"
    MASS_CLASS = "mass class"
    MASS_CONCENTRATION = "mass concentration"
    MASS_CONCENTRATION_CLASS = "mass concentration class"
    MASS_FLOW_RATE_CLASS = "mass flow rate class"
    MASS_LENGTH_CLASS = "mass length class"
    MASS_PER_ENERGY = "mass per energy"
    MASS_PER_LENGTH = "mass per length"
    MASS_PER_TIME_PER_AREA = "mass per time per area"
    MASS_PER_TIME_PER_LENGTH = "mass per time per length"
    MASS_PER_VOLUME_PER_LENGTH = "mass per volume per length"
    MEASURED_DEPTH = "measured depth"
    MOBILITY_CLASS = "mobility class"
    MODULUS_OF_COMPRESSION_CLASS = "modulus of compression class"
    MOLAR_CONCENTRATION = "molar concentration"
    MOLAR_FRACTION = "molar fraction"
    MOLAR_HEAT_CAPACITY_CLASS = "molar heat capacity class"
    MOLAR_VOLUME_CLASS = "molar volume class"
    MOLE_PER_AREA = "mole per area"
    MOLE_PER_TIME = "mole per time"
    MOLE_PER_TIME_PER_AREA = "mole per time per area"
    MOLECULAR_WEIGHT = "molecular weight"
    MOMENT_OF_FORCE_CLASS = "moment of force class"
    MOMENT_OF_INERTIA_CLASS = "moment of inertia class"
    MOMENT_OF_SECTION_CLASS = "moment of section class"
    MOMENTUM_CLASS = "momentum class"
    MOTOR_CURRENT = "motor current"
    MOTOR_CURRENT_LEAKAGE = "motor current leakage"
    MOTOR_SPEED = "motor speed"
    MOTOR_TEMPERATURE = "motor temperature"
    MOTOR_VIBRATION = "motor vibration"
    MOTOR_VOLTAGE = "motor voltage"
    NEUTRON_API_UNIT_CLASS = "neutron API unit class"
    NON_DARCY_FLOW_COEFFICIENT_CLASS = "nonDarcy flow coefficient class"
    OPENING_SIZE = "opening size"
    OPERATIONS_PER_TIME = "operations per time"
    PARACHOR_CLASS = "parachor class"
    PER_AREA = "per area"
    PER_ELECTRIC_POTENTIAL = "per electric potential"
    PER_FORCE = "per force"
    PER_LENGTH = "per length"
    PER_MASS = "per mass"
    PER_VOLUME = "per volume"
    PERMEABILITY_LENGTH_CLASS = "permeability length class"
    PERMEABILITY_ROCK_CLASS = "permeability rock class"
    PERMEANCE_CLASS = "permeance class"
    PERMITTIVITY_CLASS = "permittivity class"
    P_H_CLASS = "pH class"
    PLANE_ANGLE_CLASS = "plane angle class"
    POTENTIAL_DIFFERENCE_PER_POWER_DROP = "potential difference per power drop"
    POWER_CLASS = "power class"
    POWER_PER_VOLUME = "power per volume"
    PRESSURE = "pressure"
    PRESSURE_CLASS = "pressure class"
    PRESSURE_PER_TIME = "pressure per time"
    PRESSURE_SQUARED_CLASS = "pressure squared class"
    PRESSURE_SQUARED_PER_FORCE_TIME_PER_AREA = (
        "pressure squared per force time per area"
    )
    PRESSURE_TIME_PER_VOLUME = "pressure time per volume"
    PRODUCTIVITY_INDEX_CLASS = "productivity index class"
    PUMP_COUNT_ONLINE = "pump count online"
    PUMP_STATUS = "pump status"
    QUANTITY = "quantity"
    QUANTITY_OF_LIGHT_CLASS = "quantity of light class"
    RADIANCE_CLASS = "radiance class"
    RADIANT_INTENSITY_CLASS = "radiant intensity class"
    RECIPROCATING_SPEED = "reciprocating speed"
    RECTIFIER_STRUCTURE_POTENTIAL = "rectifier structure potential"
    REID_VAPOR_PRESSURE = "reid vapor pressure"
    RELATIVE_OPENING_SIZE = "relative opening size"
    RELATIVE_POWER_CLASS = "relative power class"
    RELATIVE_TANK_LEVEL = "relative tank level"
    RELATIVE_TIME_CLASS = "relative time class"
    RELATIVE_VALVE_OPENING = "relative valve opening"
    RELUCTANCE_CLASS = "reluctance class"
    RESISTANCE_CLASS = "resistance class"
    RESISTIVITY_PER_LENGTH = "resistivity per length"
    ROOT_PROPERTY = "root property"
    SCHEDULED_DOWNTIME = "scheduled downtime"
    SECOND_MOMENT_OF_AREA_CLASS = "second moment of area class"
    SHUTDOWN_ORDER = "shutdown order"
    SHUTIN_PRESSURE = "shutin pressure"
    SHUTIN_TEMPERATURE = "shutin temperature"
    SOLID_ANGLE_CLASS = "solid angle class"
    SPECIFIC_ACTIVITY_OF_RADIOACTIVITY = "specific activity (of radioactivity)"
    SPECIFIC_ENERGY_CLASS = "specific energy class"
    SPECIFIC_GRAVITY = "specific gravity"
    SPECIFIC_HEAT_CAPACITY_CLASS = "specific heat capacity class"
    SPECIFIC_PRODUCTIVITY_INDEX_CLASS = "specific productivity index class"
    SPECIFIC_VOLUME_CLASS = "specific volume class"
    SUB_SURFACE_SAFETY_VALVE_STATUS = "sub surface safety valve status"
    SURFACE_DENSITY_CLASS = "surface density class"
    SURFACE_SAFETY_VALVE_STATUS = "surface safety valve status"
    TANK_FLUID_LEVEL = "tank fluid level"
    TANK_PRODUCT_STANDARD_VOLUME = "tank product standard volume"
    TANK_PRODUCT_VOLUME = "tank product volume"
    TEMPERATURE = "temperature"
    TEMPERATURE_PER_LENGTH = "temperature per length"
    TEMPERATURE_PER_TIME = "temperature per time"
    THERMAL_CONDUCTANCE_CLASS = "thermal conductance class"
    THERMAL_CONDUCTIVITY_CLASS = "thermal conductivity class"
    THERMAL_DIFFUSIVITY_CLASS = "thermal diffusivity class"
    THERMAL_INSULANCE_CLASS = "thermal insulance class"
    THERMAL_RESISTANCE_CLASS = "thermal resistance class"
    THERMODYNAMIC_TEMPERATURE_CLASS = "thermodynamic temperature class"
    TIME_CLASS = "time class"
    TIME_PER_LENGTH = "time per length"
    TIME_PER_VOLUME = "time per volume"
    TRUE_VAPOR_PRESSURE = "true vapor pressure"
    UNIT_PRODUCTIVITY_INDEX_CLASS = "unit productivity index class"
    UNITLESS = "unitless"
    UNKNOWN = "unknown"
    VALVE_OPENING = "valve opening"
    VALVE_STATUS = "valve status"
    VELOCITY_CLASS = "velocity class"
    VOLUME = "volume"
    VOLUME_CLASS = "volume class"
    VOLUME_CONCENTRATION = "volume concentration"
    VOLUME_FLOW_RATE_CLASS = "volume flow rate class"
    VOLUME_LENGTH_PER_TIME = "volume length per time"
    VOLUME_PER_AREA = "volume per area"
    VOLUME_PER_LENGTH = "volume per length"
    VOLUME_PER_TIME_PER_AREA = "volume per time per area"
    VOLUME_PER_TIME_PER_LENGTH = "volume per time per length"
    VOLUME_PER_TIME_PER_TIME = "volume per time per time"
    VOLUME_PER_TIME_PER_VOLUME = "volume per time per volume"
    VOLUME_PER_VOLUME = "volume per volume"
    VOLUME_STANDARD = "volume standard"
    VOLUMETRIC_EFFICIENCY = "volumetric efficiency"
    VOLUMETRIC_HEAT_TRANSFER_COEFFICIENT = (
        "volumetric heat transfer coefficient"
    )
    VOLUMETRIC_THERMAL_EXPANSION_CLASS = "volumetric thermal expansion class"
    WELL_OPERATING_STATUS = "well operating status"
    WELL_OPERATION_TYPE = "well operation type"
    WOBBE_INDEX = "wobbe index"
    WORK = "work"
    WORK_CLASS = "work class"


class FiberConnectorTypes(Enum):
    """
    Specifies the types of fiber connector.

    :cvar DRY_MATE: dry mate
    :cvar WET_MATE: wet mate
    """

    DRY_MATE = "dry mate"
    WET_MATE = "wet mate"


class FiberEndType(Enum):
    """
    Specifies the types of fiber end.

    :cvar ANGLE_POLISHED: angle polished
    :cvar FLAT_POLISHED: flat polished
    """

    ANGLE_POLISHED = "angle polished"
    FLAT_POLISHED = "flat polished"


class FiberMode(Enum):
    """
    Specifies the modes of a distributed temperature survey (DTS) fiber.
    """

    MULTIMODE = "multimode"
    OTHER = "other"
    SINGLEMODE = "singlemode"


@dataclass
class FiberOpticalPath:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class FiberPumpActivity:
    """
    The activity of pumping the fiber downhole into a control line (small diameter
    tube).

    :ivar cable_meter_calibration_date: The date the cable meter was
        calibrated.
    :ivar cable_meter_serial_number: The serial number of the cable
        meter.
    :ivar cable_meter_type: The type of cable meter.
    :ivar comment: Comment about the pump activity.
    :ivar control_line_fluid: The type of fluid used in the control
        line.
    :ivar engineer_name: The person in charge of the pumping activity.
    :ivar excess_fiber_recovered: The length of the excess fiber that
        was removed.
    :ivar fiber_end_seal: The type of end seal on the fiber.
    :ivar installed_fiber: The name of the InstalledFiberInstance that
        this activity relates to.
    :ivar name: A name that can be used to reference the pumping
        activity. In general, a pumping activity does not have a natural
        name, so this element is often not used.
    :ivar pump_direction: The direction of the pumping.
    :ivar pump_fluid_type: The type of fluid used in the pump.
    :ivar pumping_date: The date of the pumping activity.
    :ivar service_company: The company that performed the pumping
        activity.
    :ivar uid: Unique identifier of this object.
    """

    cable_meter_calibration_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "CableMeterCalibrationDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cable_meter_serial_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CableMeterSerialNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cable_meter_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CableMeterType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    control_line_fluid: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ControlLineFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    engineer_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EngineerName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    excess_fiber_recovered: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExcessFiberRecovered",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fiber_end_seal: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FiberEndSeal",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    installed_fiber: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InstalledFiber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pump_direction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PumpDirection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pump_fluid_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PumpFluidType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pumping_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "PumpingDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    service_company: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ServiceCompany",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FiberRefractiveIndex:
    """The refractive index of a material depends on the frequency (or wavelength)
    of the light.

    Hence, it is necessary to include both the value (a unitless number)
    and the frequency (or wavelength) it was measured at. The frequency
    will be a quantity type with a frequency unit such as Hz.

    :ivar frequency: The frequency (and UOM) for which the refractive
        index is measured.
    :ivar value: The value of the refractive index.
    :ivar wavelength: The wavelength (and UOM) for which the refractive
        index is measured. The reported wavelength should be the
        wavelength of the light in a vacuum.
    :ivar uid: Unique identifier of this object.
    """

    frequency: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Frequency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    wavelength: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Wavelength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class FiberSpliceTypes(Enum):
    """
    Specifies the type of fiber splice.
    """

    CABLE_SPLICE = "cable splice"
    H_SPLICE = "h splice"
    USER_CUSTOM = "user-custom"


class FlowQualifier(Enum):
    """
    Specifies qualifiers for the type of flow.
    """

    ALLOCATED = "allocated"
    BUDGET = "budget"
    CONSTRAINT = "constraint"
    DERIVED = "derived"
    DIFFERENCE = "difference"
    ESTIMATE = "estimate"
    FORECAST = "forecast"
    MASS_ADJUSTED = "mass adjusted"
    MEASURED = "measured"
    METERED = "metered"
    METERED_FISCAL = "metered - fiscal"
    NOMINATED = "nominated"
    POTENTIAL = "potential"
    PROCESSED = "processed"
    QUOTA = "quota"
    RECOMMENDED = "recommended"
    SIMULATED = "simulated"
    TARGET = "target"
    TARIFF_BASIS = "tariff basis"
    VALUE_ADJUSTED = "value adjusted"


class FlowSubQualifier(Enum):
    """
    Specifies specializations of a flow qualifier.
    """

    DECLINE_CURVE = "decline curve"
    DIFFERENCE = "difference"
    FISCAL = "fiscal"
    FIXED = "fixed"
    MAXIMUM = "maximum"
    MINIMUM = "minimum"
    RAW = "raw"
    RECALIBRATED = "recalibrated"
    STANDARD = "standard"


@dataclass
class FluidAnalysis:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


class FluidAnalysisStepCondition(Enum):
    """
    Specifies the conditions of a fluid analysis step.

    :cvar CURRENT_RESERVOIR_CONDITIONS: The fluid analysis step is at
        current reservoir conditions.
    :cvar INITIAL_RESERVOIR_CONDITIONS: The fluid analysis step is at
        initial reservoir conditions.
    :cvar INITIAL_SATURATION_CONDITIONS: The fluid analysis step is at
        initial saturation conditions.
    :cvar STOCK_TANK_CONDITIONS: The fluid analysis step is at stock
        tank conditions.
    """

    CURRENT_RESERVOIR_CONDITIONS = "current reservoir conditions"
    INITIAL_RESERVOIR_CONDITIONS = "initial reservoir conditions"
    INITIAL_SATURATION_CONDITIONS = "initial saturation conditions"
    STOCK_TANK_CONDITIONS = "stock tank conditions"


@dataclass
class FluidCharacterization:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class FluidCharacterizationSource:
    """
    Fluid characterization source.

    :ivar fluid_analysis_reference:
    :ivar fluid_analysis_test_reference: A reference to a fluid analysis
        test which was used as source data for this fluid
        characterization.
    """

    fluid_analysis_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FluidAnalysisReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_analysis_test_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FluidAnalysisTestReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FluidComponent:
    """
    Fluid component.

    :ivar kvalue: K value.
    :ivar mass_fraction: The mass fraction for the fluid component.
    :ivar mole_fraction: The mole fraction for the fluid component.
    :ivar fluid_component_reference: Fluid component reference.
    """

    kvalue: List[str] = field(
        default_factory=list,
        metadata={
            "name": "KValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mass_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mole_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MoleFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_component_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "fluidComponentReference",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class FluidComponentProperty:
    """
    The properties of a fluid component.

    :ivar acentric_factor: The acentric factor for this fluid component.
    :ivar compact_volume: The compact volume for this fluid component.
    :ivar critical_pressure: The critical pressure for this fluid
        component.
    :ivar critical_temperature: The critical temperature for this fluid
        component.
    :ivar critical_viscosity: The critical viscosity for this fluid
        component.
    :ivar critical_volume: The critical volume for this fluid component.
    :ivar mass_density: The mass density for this fluid component.
    :ivar omega_a: The omega A for this fluid component.
    :ivar omega_b: The omega B for this fluid component.
    :ivar parachor: The parachor for this fluid component.
    :ivar partial_molar_density: The partial molar density for this
        fluid component.
    :ivar partial_molar_volume: The partial molar volume for this fluid
        component.
    :ivar reference_density_zj: The reference density for this fluid
        component.
    :ivar reference_gravity_zj: The reference gravity for this fluid
        component.
    :ivar reference_temperature_zj: The reference temperature for this
        fluid component.
    :ivar remark: Remarks and comments about this data item.
    :ivar viscous_compressibility: The viscous compressibility for this
        fluid component.
    :ivar volume_shift_parameter: The volume shift parameter for this
        fluid component.
    :ivar fluid_component_reference: The reference to the fluid
        component to which these properties apply.
    """

    acentric_factor: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "AcentricFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    compact_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CompactVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    critical_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CriticalPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    critical_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CriticalTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    critical_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CriticalViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    critical_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CriticalVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mass_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    omega_a: Optional[float] = field(
        default=None,
        metadata={
            "name": "OmegaA",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    omega_b: Optional[float] = field(
        default=None,
        metadata={
            "name": "OmegaB",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    parachor: Optional[float] = field(
        default=None,
        metadata={
            "name": "Parachor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    partial_molar_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PartialMolarDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    partial_molar_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PartialMolarVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reference_density_zj: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReferenceDensityZJ",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reference_gravity_zj: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReferenceGravityZJ",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reference_temperature_zj: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReferenceTemperatureZJ",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    viscous_compressibility: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ViscousCompressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    volume_shift_parameter: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "VolumeShiftParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_component_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "fluidComponentReference",
            "type": "Attribute",
            "required": True,
        },
    )


class FluidContaminant(Enum):
    """
    Specifies the kinds of contaminating fluid present in a fluid sample.

    :cvar CEMENT_FLUIDS: The fluid contaminant is cement fluids.
    :cvar COMPLETION_FLUID: The fluid contaminant is completion fluid.
    :cvar DRILLING_MUD: The fluid contaminant is drilling mud.
    :cvar EXTRANEOUS_GAS: The fluid contaminant is extraneous gas.
    :cvar EXTRANEOUS_OIL: The fluid contaminant is extraneous oil.
    :cvar EXTRANEOUS_WATER: The fluid contaminant is extraneous water.
    :cvar FORMATION_WATER: The fluid contaminant is formation water.
    :cvar TREATMENT_CHEMICALS: The fluid contaminant is treatment
        chemicals.
    :cvar SOLID: The fluid contaminant is solid.
    :cvar UNKNOWN: The fluid contaminant is unknown.
    """

    CEMENT_FLUIDS = "cement fluids"
    COMPLETION_FLUID = "completion fluid"
    DRILLING_MUD = "drilling mud"
    EXTRANEOUS_GAS = "extraneous gas"
    EXTRANEOUS_OIL = "extraneous oil"
    EXTRANEOUS_WATER = "extraneous water"
    FORMATION_WATER = "formation water"
    TREATMENT_CHEMICALS = "treatment chemicals"
    SOLID = "solid"
    UNKNOWN = "unknown"


@dataclass
class FluidSample:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class FluidSampleAcquisitionJob:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class FluidSampleAcquisitionJobSource:
    """
    :ivar fluid_sample_acquisition_job_reference:
    :ivar fluid_sample_acquisition_reference: Reference to the fluid
        sample acquisition (by uid) within a fluid sample acquisition
        job (which is referred to as a top-level object) which acquired
        this fluid sample.
    """

    fluid_sample_acquisition_job_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidSampleAcquisitionJobReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fluid_sample_acquisition_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidSampleAcquisitionReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FluidSampleComposition:
    """
    Fluid sample points to a mixture from other samples.

    :ivar fluid_sample:
    :ivar mass_fraction: The mass fraction of this parent sample within
        this combined sample.
    :ivar mole_fraction: The mole fraction of this parent sample within
        this combined sample.
    :ivar remark: Remarks and comments about this data item.
    :ivar volume_fraction: The volume fraction of this parent sample
        within this combined sample.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    fluid_sample: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FluidSample",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mass_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mole_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MoleFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    volume_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VolumeFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FluidSampleContainer:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class FluidSystem:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class GeneralMeasureType:
    """
    General measure type.

    :ivar uom: The unit of measure.
    """

    uom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class GeologyType(Enum):
    """Specifies the types of geology: water and reservoir.

    :cvar AQUIFER: aquifer
    :cvar RESERVOIR: reservoir
    """

    AQUIFER = "aquifer"
    RESERVOIR = "reservoir"


@dataclass
class IndexedObject:
    """
    Indexed object.

    :ivar description: Description.
    :ivar index: Index.
    :ivar name: Name.
    :ivar uom: Unit of measure.
    """

    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    index: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    uom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class InjectionFluid(Enum):
    """
    Specifies the types of fluids which are injected into a well.

    :cvar AIR: air
    :cvar BRINE: brine
    :cvar CO2: co2
    :cvar CONDENSATE: condensate
    :cvar DRY: dry
    :cvar FRESH_WATER: fresh water
    :cvar GAS: gas
    :cvar GAS_WATER: gas-water
    :cvar NON_HC_GAS: non HC gas
    :cvar OIL: oil
    :cvar OIL_GAS: oil-gas
    :cvar OIL_WATER: oil-water
    :cvar OTHER: other
    :cvar STEAM: steam
    :cvar WATER: water
    """

    AIR = "air"
    BRINE = "brine"
    CO2 = "co2"
    CONDENSATE = "condensate"
    DRY = "dry"
    FRESH_WATER = "fresh water"
    GAS = "gas"
    GAS_WATER = "gas-water"
    NON_HC_GAS = "non HC gas"
    OIL = "oil"
    OIL_GAS = "oil-gas"
    OIL_WATER = "oil-water"
    OTHER = "other"
    STEAM = "steam"
    WATER = "water"


@dataclass
class InterfacialTensionTestStep:
    """
    The interfacial tension test step.

    :ivar interfacial_tension: The interfacial tension for this test
        step.
    :ivar remark: Remarks and comments about this data item.
    :ivar step_number: The step number is the index of a (P,T) step in
        the overall test.
    :ivar step_pressure: The pressure for this test step.
    :ivar step_temperature: The temperature for this test step.
    :ivar surfactant_concentration: The surfactant concentration for
        this test step.
    :ivar wetting_phase_saturation: The wetting phase saturation for
        this test step.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    interfacial_tension: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InterfacialTension",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    step_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StepPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StepTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    surfactant_concentration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SurfactantConcentration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wetting_phase_saturation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WettingPhaseSaturation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class InterpretationProcessingType(Enum):
    """
    Specifies the types of mnemonics.

    :cvar AVERAGED: averaged
    :cvar DENORMALIZED: denormalized
    :cvar DEPTH_CORRECTED: depth-corrected
    :cvar MANUFACTURER_GENERATED: manufacturer-generated
    :cvar TEMPERATURE_SHIFTED: temperature-shifted
    :cvar USER_CUSTOM: user-custom
    """

    AVERAGED = "averaged"
    DENORMALIZED = "denormalized"
    DEPTH_CORRECTED = "depth-corrected"
    MANUFACTURER_GENERATED = "manufacturer-generated"
    TEMPERATURE_SHIFTED = "temperature-shifted"
    USER_CUSTOM = "user-custom"


class InterventionConveyanceType(Enum):
    """
    Specifies the types of intervention conveyance.
    """

    COILED_TUBING = "coiled tubing"
    ROD = "rod"
    SLICKLINE = "slickline"
    WIRELINE = "wireline"


@dataclass
class MassIn:
    """
    The mass of fluid in the connecting lines.

    :ivar mass_fluid_connecting_lines: The mass of fluid in the
        connecting lines for this slim tube test volume step mass
        balance.
    :ivar mass_fluid_slimtube: The mass of fluid in the slim tube for
        this slim tube test volume step mass balance.
    :ivar mass_injected_gas_solvent: The mass of injected gas solvent
        for this slim tube test volume step mass balance.
    :ivar total_mass_in: The total mass in for this slim tube test
        volume step mass balance.
    """

    mass_fluid_connecting_lines: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassFluidConnectingLines",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mass_fluid_slimtube: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassFluidSlimtube",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mass_injected_gas_solvent: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassInjectedGasSolvent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_mass_in: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalMassIn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class MassOut:
    """
    The  mass out for this slim tube.

    :ivar mass_effluent_stock_tank_oil: The mass of effluent stock tank
        oil for this slim tube test volume step mass balance.
    :ivar mass_produced_effluent_gas: The mass of produced effluent gas
        for this slim tube test volume step mass balance.
    :ivar mass_produced_effluent_gas_flow_down: The mass of produced
        effluent gas flow down for this slim tube test volume step mass
        balance.
    :ivar mass_residual_oil: The mass of residual oil for this slim tube
        test volume step mass balance.
    :ivar total_mass_out: The total mass out for this slim tube test
        volume step mass balance.
    """

    mass_effluent_stock_tank_oil: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassEffluentStockTankOil",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mass_produced_effluent_gas: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassProducedEffluentGas",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mass_produced_effluent_gas_flow_down: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassProducedEffluentGasFlowDown",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mass_residual_oil: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassResidualOil",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_mass_out: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalMassOut",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class MeasureOrQuantity:
    """A measure with a UOM or a quantity (without a UOM).

    Use this only where the underlying class of data is captured
    elsewhere. For example, using a measure class.

    :ivar uom: The unit of measure for the quantity. This value must
        conform to the values allowed by a measure class. If the value
        is a measure, then the UOM must be specified.
    """

    uom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class MeasuredDepthCoord:
    """A measured depth coordinate in a wellbore.

    Positive moving from the reference datum toward the bottomhole. All
    coordinates with the same datum (and same UOM) can be considered to
    be in the same coordinate reference system (CRS) and are thus
    directly comparable.

    :ivar uom: The unit of measure of the measured depth coordinate.
    """

    uom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class MixingRule(Enum):
    """
    Specifies the kinds of mixing rules.

    :cvar ASYMMETRIC: The mixing rule kind is asymmetric.
    :cvar CLASSICAL: The mixing rule kind is classical.
    """

    ASYMMETRIC = "asymmetric"
    CLASSICAL = "classical"


@dataclass
class MultipleContactMiscibilityTest:
    """
    Multiple contact miscibility test.

    :ivar gas_solvent_composition_reference: The reference to the
        composition of the gas solvent that is a fluid composition.
    :ivar mix_ratio: The mix ratio for the multiple contact miscibility
        test.
    :ivar test_number: A unique identifier for this data element. It is
        not globally unique (not a uuid) and only need be unique within
        the context of the parent top-level object.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    gas_solvent_composition_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasSolventCompositionReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mix_ratio: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MixRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class NameStruct:
    """
    The name of something within a naming system.

    :ivar authority: The authority for the naming system, e.g., a
        company.
    """

    authority: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class NorthSeaOffshore:
    """
    A type of offshore location that captures the North Sea offshore terminology.

    :ivar area_name: An optional, uncontrolled value, which may be used
        to describe the general area of offshore North Sea in which the
        point is located.
    :ivar block_suffix: A lower case letter assigned if a block is
        subdivided.
    :ivar quadrant: The number or letter of the quadrant in the North
        Sea.
    """

    area_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AreaName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    block_suffix: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BlockSuffix",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    quadrant: Optional[str] = field(
        default=None,
        metadata={
            "name": "Quadrant",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


class Otdrdirection(Enum):
    """
    Specifies the OTDR directions.

    :cvar BACKWARD: backward
    :cvar FORWARD: forward
    """

    BACKWARD = "backward"
    FORWARD = "forward"


class Otdrreason(Enum):
    """
    Specifies the reasons an OTDR test was run within a distributed temperature
    survey (DTS).

    :cvar DTS: dts
    :cvar OTHER: other
    :cvar POST_INSTALLATION: post-installation
    :cvar PRE_INSTALLATION: pre-installation
    :cvar RUN: run
    """

    DTS = "dts"
    OTHER = "other"
    POST_INSTALLATION = "post-installation"
    PRE_INSTALLATION = "pre-installation"
    RUN = "run"


class OperationKind(Enum):
    """
    Specifies the types of production operations for which general comments can be
    defined.

    :cvar AIR_TRAFFIC: air traffic
    :cvar CONSTRUCTION: construction
    :cvar DEVIATIONS: deviations
    :cvar MAINTENANCE: maintenance
    :cvar OTHER: other
    :cvar POWER_STATION_FAILURE: power station failure
    :cvar PRODUCTION: production
    :cvar WELL: well
    """

    AIR_TRAFFIC = "air traffic"
    CONSTRUCTION = "construction"
    DEVIATIONS = "deviations"
    MAINTENANCE = "maintenance"
    OTHER = "other"
    POWER_STATION_FAILURE = "power station failure"
    PRODUCTION = "production"
    WELL = "well"


class OutputFluidProperty(Enum):
    """
    Specifies the output fluid properties.

    :cvar COMPRESSIBILITY: Compressibility (expected to be defined for a
        phase). UoM: 1/pressure.
    :cvar DENSITY: Density (expected to be defined for a phase). UoM:
        mass/volume.
    :cvar DERIVATIVE_OF_DENSITY_W_R_T_PRESSURE: Derivative of density
        w.r.t pressure (expected to be defined for a phase). UoM:
        density/pressure.
    :cvar DERIVATIVE_OF_DENSITY_W_R_T_TEMPERATURE: Derivative of density
        w.r.t temperature (expected to be defined for a phase). UoM:
        density/temperature.
    :cvar ENTHALPY: Enthalpy (expected to be defined for a phase). UoM:
        energy/mass.
    :cvar ENTROPY: Entropy (expected to be defined for a phase). UoM:
        energy/temperature.
    :cvar EXPANSION_FACTOR: Expansion factor - volume expanded/volume in
        reservoir (expected to be defined for a phase). UoM:
        volume/volume.
    :cvar FORMATION_VOLUME_FACTOR: Formation volume factor - volume in
        reservoir/volume expanded (expected to be defined for a phase).
        UoM: volume/volume.
    :cvar GAS_OIL_INTERFACIAL_TENSION: Gas-oil interfacial tension. UoM:
        force/length.
    :cvar GAS_WATER_INTERFACIAL_TENSION: Gas-water interfacial tension.
        UoM: force/length.
    :cvar INDEX: Index number (which will be the index of a row in the
        table). UoM: integer.
    :cvar K_VALUE: The ratio of vapor concentration to liquid
        concentration at equilibrium (expected to be defined for a
        phase). UoM: dimensionless.
    :cvar MISC_BANK_CRITICAL_SOLVENT_SATURATION: The critical solvent
        saturation of a miscible bank . UoM: volume/volume.
    :cvar MISC_BANK_PHASE_DENSITY: The density of a phase within a
        miscible bank  (expected to be defined for a phase). UoM:
        density.
    :cvar MISC_BANK_PHASE_VISCOSITY: The viscosity of a phase within a
        miscible bank  (expected to be defined for a phase). UoM:
        viscosity.
    :cvar MISCIBILITY_PARAMETER_ALPHA: The critical solvent saturation
        of a miscible bank.
    :cvar MIXING_PARAMETER_OIL_GAS: Mixing parameter for oil and gas.
    :cvar OIL_GAS_RATIO: The oil-gas ratio in a vapour-liquid system.
        UoM: volume/volume.
    :cvar OIL_WATER_INTERFACIAL_TENSION: Oil-water interfacial tension.
    :cvar PARACHOR: Parachor is the quantity defined according to the
        formula: P = γ1/4 M / D. Where γ1/4 is the fourth root of
        surface tension.
    :cvar PRESSURE: Pressure. UoM: pressure.
    :cvar P_T_CROSS_TERM: This is a specific parameter unique to CMG
        software.
    :cvar SATURATION_PRESSURE: The saturation pressure of a mixture.
        UoM: pressure.
    :cvar SOLUTION_GOR: The gas-oil ratio in a liquid-vapour system.
        UoM: volume/volume.
    :cvar SOLVENT_DENSITY: The density of a solvent phase. UoM: density.
    :cvar SPECIFIC_HEAT: The amount of heat per unit mass required to
        raise the temperature by one unit temperature (expected to be
        defined for a phase). UoM: energy/mass/temperature.
    :cvar TEMPERATURE: Temperature. UoM: temperature.
    :cvar THERMAL_CONDUCTIVITY: Thermal conductivity (expected to be
        defined for a phase). UoM: power/length.temperature.
    :cvar VISCOSITY: Viscosity (expected to be defined for a phase).
        UoM: viscosity.
    :cvar VISCOSITY_COMPRESSIBILITY: Slope of viscosity change with
        pressure in a semi-log plot (1/psi) (expected to be defined for
        a phase). UoM: viscosity/pressure.
    :cvar WATER_VAPOR_MASS_FRACTION_IN_GAS_PHASE: The mass fraction of
        water in a gas phase. UoM: mass/mass.
    :cvar Z_FACTOR: The compressibility factor (z).
    """

    COMPRESSIBILITY = "Compressibility"
    DENSITY = "Density"
    DERIVATIVE_OF_DENSITY_W_R_T_PRESSURE = (
        "Derivative of Density w.r.t Pressure"
    )
    DERIVATIVE_OF_DENSITY_W_R_T_TEMPERATURE = (
        "Derivative of Density w.r.t Temperature"
    )
    ENTHALPY = "Enthalpy"
    ENTROPY = "Entropy"
    EXPANSION_FACTOR = "Expansion Factor"
    FORMATION_VOLUME_FACTOR = "Formation Volume Factor"
    GAS_OIL_INTERFACIAL_TENSION = "Gas-Oil Interfacial Tension"
    GAS_WATER_INTERFACIAL_TENSION = "Gas-Water Interfacial Tension"
    INDEX = "Index"
    K_VALUE = "K value"
    MISC_BANK_CRITICAL_SOLVENT_SATURATION = (
        "Misc Bank Critical Solvent Saturation"
    )
    MISC_BANK_PHASE_DENSITY = "Misc Bank Phase Density"
    MISC_BANK_PHASE_VISCOSITY = "Misc Bank Phase Viscosity"
    MISCIBILITY_PARAMETER_ALPHA = "Miscibility Parameter (Alpha)"
    MIXING_PARAMETER_OIL_GAS = "Mixing Parameter Oil-Gas"
    OIL_GAS_RATIO = "Oil-Gas Ratio"
    OIL_WATER_INTERFACIAL_TENSION = "Oil-Water Interfacial Tension"
    PARACHOR = "Parachor"
    PRESSURE = "Pressure"
    P_T_CROSS_TERM = "P-T Cross Term"
    SATURATION_PRESSURE = "Saturation Pressure"
    SOLUTION_GOR = "Solution GOR"
    SOLVENT_DENSITY = "Solvent Density"
    SPECIFIC_HEAT = "Specific Heat"
    TEMPERATURE = "Temperature"
    THERMAL_CONDUCTIVITY = "Thermal Conductivity"
    VISCOSITY = "Viscosity"
    VISCOSITY_COMPRESSIBILITY = "Viscosity Compressibility"
    WATER_VAPOR_MASS_FRACTION_IN_GAS_PHASE = (
        "Water vapor mass fraction in gas phase"
    )
    Z_FACTOR = "Z Factor"


@dataclass
class OwnershipBusinessAcct:
    pass


class PathDefectTypes(Enum):
    """
    Specifies the types of fiber zone that can be reported on.

    :cvar DARKENED_FIBER: darkened fiber
    :cvar OTHER: other
    """

    DARKENED_FIBER = "darkened fiber"
    OTHER = "other"


class PermanentCableInstallationType(Enum):
    """
    Specifies the types of permanent cable installations.
    """

    BURIED_PARALLEL_TO_TUBULAR = "buried parallel to tubular"
    CLAMPED_TO_TUBULAR = "clamped to tubular"
    WRAPPED_AROUND_TUBULAR = "wrapped around tubular"


@dataclass
class PersonName:
    """
    The components of a person's name.

    :ivar first: The person's first name, sometimes called their "given
        name".
    :ivar last: The person's last or family name.
    :ivar middle: The person's middle name or initial.
    :ivar prefix: A name prefix. Such as, Dr, Ms, Miss, Mr, etc.
    :ivar suffix: A name suffix such as Esq, Phd, etc.
    """

    first: Optional[str] = field(
        default=None,
        metadata={
            "name": "First",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    last: Optional[str] = field(
        default=None,
        metadata={
            "name": "Last",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    middle: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Middle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    prefix: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Prefix",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    suffix: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Suffix",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class PhaseDensity:
    """
    Phase density.

    :ivar density: The phase density.
    :ivar pressure: The pressure corresponding to this phase density.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Density",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Pressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class PhaseViscosity:
    """
    Phase viscosity.

    :ivar pressure: The pressure corresponding to this phase viscosity.
    :ivar viscosity: The phase viscosity.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Pressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Viscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class PhoneType(Enum):
    """
    Specifies the types phone number (e.g., fax, mobile, etc.)
    """

    FAX = "fax"
    MOBILE = "mobile"
    PAGER = "pager"
    UNKNOWN = "unknown"
    VOICE = "voice"
    VOICE_FAX = "voice/fax"
    VOICEMAIL = "voicemail"


class PlusComponentEnum(Enum):
    """
    Specifies the types of plus components.
    """

    C10 = "c10+"
    C11 = "c11+"
    C12 = "c12+"
    C20 = "c20+"
    C25 = "c25+"
    C30 = "c30+"
    C36 = "c36+"
    C5 = "c5+"
    C6 = "c6+"
    C7 = "c7+"
    C8 = "c8+"
    C9 = "c9+"


@dataclass
class ProducedOilProperties:
    """
    Properties of produced oil.

    :ivar asphaltene_content: The asphaltene content of this produced
        oil.
    :ivar stoapi_gravity: The stock tank oil API gravity of this
        produced oil.
    :ivar stodensity: The stock tank oil density of this produced oil.
    :ivar stomw: The stock tank oil molecular weight of this produced
        oil.
    :ivar stowater_content: The stock tank oil water content of this
        produced oil.
    """

    asphaltene_content: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AsphalteneContent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    stoapi_gravity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "STOApiGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    stodensity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "STODensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    stomw: List[str] = field(
        default_factory=list,
        metadata={
            "name": "STOMW",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    stowater_content: List[str] = field(
        default_factory=list,
        metadata={
            "name": "STOWaterContent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class ProductFlowChangeLog:
    """
    Documents the point in time where changes were made.

    :ivar dtim: The timestamp associated with the change. All changes
        must use this timestamp.
    :ivar name: A name assigned to the change.
    :ivar reason: A textual reason for the change.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    dtim: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    reason: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Reason",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductFlowModel:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class ProductFlowNetwork:
    """
    The non-contextual content of a product flow network object.

    :ivar change_log: Documents that a change occurred at a particular
        time.
    :ivar comment: A descriptive remark about the network.
    :ivar name: The name of the product flow network. This must be
        unique within the context of the overall product flow model.
    :ivar parent_network_reference: A pointer to the network containing
        the unit that this network represents. That is, the unit must
        exist in a different network. If a parent network is not
        specified then the network represents the model. A model should
        only be represented by one network. The model network represents
        the overall installation. All other networks represent internal
        detail and should not be referenced from outside the model. The
        external ports on the model network represent the external ports
        to the overall product flow model. A pointer to an external port
        on the product flow model does not require the name of the model
        network because it is redundant to knowledge of the model name
        (i.e., there is a one-to-one correspondence).
    :ivar plan: Defines the existance of a planned network which is a
        variant of this network beginning at a specified point in time.
        Any changes to the actual network after that time do not affect
        the plan.
    :ivar plan_name: The name of a network plan. This indicates a
        planned network. All child network components must all be
        planned and be part of the same plan. The parent network must
        either contain the plan (i.e., be an actual) or be part of the
        same plan. Not specified indicates an actual network.
    :ivar port: An external port. This exposes an internal node for the
        purpose of allowing connections to the internal behavior of the
        network. Networks that represent a Flow Unit should always have
        external ports. If this network represents a Unit then the name
        of the external port must match the name of a port on the Unit
        (i.e., they are logically the same port).
    :ivar unit: A flow behavior for one unit. Within this context, a
        unit represents a usage of equipment for some purpose. The unit
        is generally identified by its function rather than the actual
        equipment used to realize the function. A unit might represent
        something complex like a field or separator or something simple
        like a valve or pump.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    change_log: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ChangeLog",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    parent_network_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ParentNetworkReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    plan: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Plan",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    plan_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PlanName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    port: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Port",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    unit: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class ProductFlowPortType(Enum):
    """
    Specifies the types of product flow ports.
    """

    INLET = "inlet"
    OUTLET = "outlet"
    UNKNOWN = "unknown"


class ProductFluidKind(Enum):
    """
    Specifies the kinds of product in a fluid system.
    """

    CONDENSATE = "condensate"
    CONDENSATE_GROSS = "condensate - gross"
    CONDENSATE_NET = "condensate - net"
    CRUDE_STABILIZED = "crude - stabilized"
    GAS_COMPONENT_IN_OIL = "gas - component in oil"
    GAS_DRY = "gas - dry"
    GAS_RICH = "gas - rich"
    GAS_WET = "gas - wet"
    LIQUEFIED_NATURAL_GAS = "liquefied natural gas"
    LIQUEFIED_PETROLEUM_GAS = "liquefied petroleum gas"
    LIQUID = "liquid"
    NAPHTHA = "naphtha"
    NATURAL_GAS_LIQUID = "natural gas liquid"
    NGL_COMPONENT_IN_GAS = "NGL - component in gas"
    OIL_COMPONENT_IN_WATER = "oil - component in water"
    OIL_GROSS = "oil - gross"
    OIL_NET = "oil - net"
    OIL_AND_GAS = "oil and gas"
    PETROLEUM_GAS_LIQUID = "petroleum gas liquid"
    VAPOR = "vapor"
    SAND = "sand"
    WATER_DISCHARGE = "water - discharge"
    WATER_PROCESSED = "water - processed"


@dataclass
class ProductVolume:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class ProductVolumeAlert:
    """
    Alert Schema.

    :ivar description: A textual description of the alert.
    :ivar level: The level of the alert.
    :ivar target: An XPATH to the target value within the message
        containing this XPATH value.
    :ivar type_value: The type of alert. For example "off
        specification".
    """

    description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    level: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Level",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    target: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Target",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    type_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class ProductVolumePortDifference:
    """
    Product Volume port differential characteristics.

    :ivar choke_relative: The relative size of the choke restriction.
        This characterizes the overall unit with respect to the flow
        restriction between the ports. The restriction might be
        implemented using a valve or an actual choke.
    :ivar choke_size: The size of the choke. This characterizes the
        overall unit with respect to the flow restriction between the
        ports. The restriction might be implemented using a valve or an
        actual choke.
    :ivar port_reference: A port on the other end of an internal
        connection. This should always be specified if a product flow
        network is being referenced by this report. If this is not
        specified then there is an assumption that there is only one
        other port for the unit. For example, if this end of the
        connection represents an inlet port then the implied other end
        is the outlet port for the unit.
    :ivar pres_diff: The differential pressure between the ports.
    :ivar temp_diff: The differential temperature between the ports.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    choke_relative: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ChokeRelative",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    choke_size: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ChokeSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    port_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PortReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pres_diff: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PresDiff",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    temp_diff: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TempDiff",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionOperation:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class ProductionOperationAlarm:
    """
    A structure to record information about a single alarm.

    :ivar area: The area where the alarm sounded.
    :ivar comment: A general comment about the alarm.
    :ivar dtim: The date and time when the alarms sounded.
    :ivar reason: The reason the alarm sounded.
    :ivar type_value: The type of alarm that sounded.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    area: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Area",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reason: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Reason",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    type_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionOperationWeather:
    """
    Operations Weather Schema.

    :ivar agency: Name of company that supplied the data.
    :ivar amt_precip: Amount of precipitation.
    :ivar azi_current_sea: Azimuth of current.
    :ivar azi_wave: The direction from which the waves are coming,
        measured from true north.
    :ivar azi_wind: The direction from which the wind is blowing,
        measured from true north.
    :ivar barometric_pressure: Atmospheric pressure.
    :ivar ceiling_cloud: Height of cloud cover.
    :ivar comments: Comments and remarks.
    :ivar cover_cloud: Description of cloud cover.
    :ivar current_sea: Current speed.
    :ivar dtim: Date and time the information is related to.
    :ivar ht_wave: Average height of the waves.
    :ivar max_wave: The maximum wave height.
    :ivar period_wave: The elapsed time between the passing of two wave
        tops.
    :ivar significant_wave: An average of the higher 1/3 of the wave
        heights passing during a sample period (typically 20 to 30
        minutes).
    :ivar tempsea: Sea temperature.
    :ivar temp_surface: Average temperature above ground for the period.
        Temperature of the atmosphere.
    :ivar temp_surface_mn: Minimum temperature above ground. Temperature
        of the atmosphere.
    :ivar temp_surface_mx: Maximum temperature above ground.
    :ivar temp_wind_chill: A measure of the combined chilling effect of
        wind and low temperature on living things, also named chill
        factor, e.g., according to US Weather Service table, an air
        temperature of 30 degF with a 10 mph wind corresponds to a wind
        chill of 22 degF.
    :ivar type_precip: Type of precipitation.
    :ivar vel_wind: Wind speed.
    :ivar visibility: Horizontal visibility.
    :ivar beaufort_scale_number: The Beaufort wind scale is a system
        used to estimate and report wind speeds when no measuring
        apparatus is available. It was invented in the early 19th
        Century by Admiral Sir Francis Beaufort of the British Navy as a
        way to interpret winds from conditions.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    agency: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Agency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    amt_precip: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AmtPrecip",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    azi_current_sea: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AziCurrentSea",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    azi_wave: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AziWave",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    azi_wind: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AziWind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    barometric_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BarometricPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    ceiling_cloud: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CeilingCloud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    comments: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cover_cloud: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CoverCloud",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    current_sea: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CurrentSea",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    ht_wave: List[str] = field(
        default_factory=list,
        metadata={
            "name": "HtWave",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    max_wave: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MaxWave",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    period_wave: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PeriodWave",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    significant_wave: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SignificantWave",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tempsea: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Tempsea",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    temp_surface: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TempSurface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    temp_surface_mn: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TempSurfaceMn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    temp_surface_mx: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TempSurfaceMx",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    temp_wind_chill: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TempWindChill",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    type_precip: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TypePrecip",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vel_wind: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VelWind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    visibility: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Visibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    beaufort_scale_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "BeaufortScaleNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_inclusive": 0,
            "max_exclusive": 12,
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
class PrsvParameter:
    """
    PRSV parameter.

    :ivar a1: The parameter a1.
    :ivar a2: The parameter a2.
    :ivar b1: The parameter b1.
    :ivar b2: The parameter b2.
    :ivar c2: The parameter c2.
    :ivar fluid_component_reference: The fluid component to which this
        PRSV parameter set applies.
    """

    a1: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    a2: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    b1: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    b2: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    c2: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fluid_component_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "fluidComponentReference",
            "type": "Attribute",
            "required": True,
        },
    )


class PseudoComponentEnum(Enum):
    """
    Specifies the kinds of pseudo-components.

    :cvar C10: c10
    :cvar C11:
    :cvar C12:
    :cvar C13:
    :cvar C14:
    :cvar C15:
    :cvar C16:
    :cvar C17:
    :cvar C18:
    :cvar C19:
    :cvar C20:
    :cvar C21:
    :cvar C22:
    :cvar C23:
    :cvar C24:
    :cvar C25:
    :cvar C26:
    :cvar C27:
    :cvar C28:
    :cvar C29:
    :cvar C2_C4_N2:
    :cvar C30:
    :cvar C31:
    :cvar C32:
    :cvar C33:
    :cvar C34:
    :cvar C35:
    :cvar C4:
    :cvar C5:
    :cvar C6:
    :cvar C7:
    :cvar C8:
    :cvar C9:
    """

    C10 = "c10"
    C11 = "c11"
    C12 = "c12"
    C13 = "c13"
    C14 = "c14"
    C15 = "c15"
    C16 = "c16"
    C17 = "c17"
    C18 = "c18"
    C19 = "c19"
    C20 = "c20"
    C21 = "c21"
    C22 = "c22"
    C23 = "c23"
    C24 = "c24"
    C25 = "c25"
    C26 = "c26"
    C27 = "c27"
    C28 = "c28"
    C29 = "c29"
    C2_C4_N2 = "c2-c4+n2"
    C30 = "c30"
    C31 = "c31"
    C32 = "c32"
    C33 = "c33"
    C34 = "c34"
    C35 = "c35"
    C4 = "c4"
    C5 = "c5"
    C6 = "c6"
    C7 = "c7"
    C8 = "c8"
    C9 = "c9"


class PureComponentEnum(Enum):
    """
    Specifies the kinds of pure components.

    :cvar VALUE_1_2_4_TRIMETHYLBENZENE:
    :cvar VALUE_2_DIMETHYLBUTANE:
    :cvar VALUE_3_DIMETHYLBUTANE:
    :cvar AR:
    :cvar C1:
    :cvar C2:
    :cvar C3:
    :cvar CO2:
    :cvar H2:
    :cvar H2O:
    :cvar H2S:
    :cvar HE:
    :cvar HG:
    :cvar I_C4:
    :cvar I_C5:
    :cvar N2:
    :cvar N_C10:
    :cvar N_C4:
    :cvar N_C5:
    :cvar N_C6:
    :cvar N_C7:
    :cvar N_C8:
    :cvar N_C9:
    :cvar NEO_C5:
    :cvar BENZENE: benzene
    :cvar VALUE_2_METHYLPENTANE:
    :cvar VALUE_3_METHYLPENTANE:
    :cvar VALUE_2_METHYLHEXANE:
    :cvar VALUE_3_METHYLHEXANE:
    :cvar VALUE_2_METHYLHEPTANE:
    :cvar VALUE_3_METHYLHEPTANE:
    :cvar CYCLOHEXANE:
    :cvar ETHYLBENZENE:
    :cvar ETHYLCYCLOHEXANE:
    :cvar METHYLCYCLOHEXANE:
    :cvar METHYLCYCLOPENTANE:
    :cvar TOLUENE:
    :cvar M_XYLENE:
    :cvar O_XYLENE:
    :cvar P_XYLENE:
    """

    VALUE_1_2_4_TRIMETHYLBENZENE = "1-2-4-trimethylbenzene"
    VALUE_2_DIMETHYLBUTANE = "2-dimethylbutane"
    VALUE_3_DIMETHYLBUTANE = "3-dimethylbutane"
    AR = "ar"
    C1 = "c1"
    C2 = "c2"
    C3 = "c3"
    CO2 = "co2"
    H2 = "h2"
    H2O = "h2o"
    H2S = "h2s"
    HE = "he"
    HG = "hg"
    I_C4 = "i-c4"
    I_C5 = "i-c5"
    N2 = "n2"
    N_C10 = "n-c10"
    N_C4 = "n-c4"
    N_C5 = "n-c5"
    N_C6 = "n-c6"
    N_C7 = "n-c7"
    N_C8 = "n-c8"
    N_C9 = "n-c9"
    NEO_C5 = "neo-c5"
    BENZENE = "benzene"
    VALUE_2_METHYLPENTANE = "2-methylpentane"
    VALUE_3_METHYLPENTANE = "3-methylpentane"
    VALUE_2_METHYLHEXANE = "2-methylhexane"
    VALUE_3_METHYLHEXANE = "3-methylhexane"
    VALUE_2_METHYLHEPTANE = "2-methylheptane"
    VALUE_3_METHYLHEPTANE = "3-methylheptane"
    CYCLOHEXANE = "cyclohexane"
    ETHYLBENZENE = "ethylbenzene"
    ETHYLCYCLOHEXANE = "ethylcyclohexane"
    METHYLCYCLOHEXANE = "methylcyclohexane"
    METHYLCYCLOPENTANE = "methylcyclopentane"
    TOLUENE = "toluene"
    M_XYLENE = "m-xylene"
    O_XYLENE = "o-xylene"
    P_XYLENE = "p-xylene"


class PvtModelParameterKind(Enum):
    """
    Specifies the kinds of PVT model parameters.

    :cvar B0: The value represents the parameter b0.
    :cvar B1: The value represents the parameter b1.
    :cvar B2: The value represents the parameter b2.
    :cvar C1: The value represents the parameter c1.
    :cvar C2: The value represents the parameter c2.
    :cvar D1: The value represents the parameter d1.
    :cvar D2: The value represents the parameter d2.
    :cvar E1: The value represents the parameter e1.
    :cvar E2: The value represents the parameter e2.
    :cvar F1: The value represents the parameter f1.
    :cvar F2: The value represents the parameter f2.
    :cvar G1: The value represents the parameter g1.
    :cvar G2: The value represents the parameter g2.
    :cvar H1: The value represents the parameter h1.
    :cvar H2: The value represents the parameter h2.
    :cvar A0: The value represents the parameter a0.
    :cvar A1: The value represents the parameter a1.
    :cvar A2: The value represents the parameter a2.
    :cvar A3: The value represents the parameter a3.
    :cvar A4: The value represents the parameter a4.
    :cvar A5: The value represents the parameter a5.
    :cvar A6: The value represents the parameter a6.
    :cvar A7: The value represents the parameter a7.
    :cvar A8: The value represents the parameter a8.
    :cvar A9: The value represents the parameter a9.
    :cvar A10: The value represents the parameter a10.
    :cvar C0: The value represents the parameter c0.
    :cvar D0: The value represents the parameter d0.
    :cvar E0: The value represents the parameter e0.
    :cvar F0: The value represents the parameter f0.
    :cvar G0: The value represents the parameter g0.
    :cvar H0: The value represents the parameter h0.
    """

    B0 = "b0"
    B1 = "b1"
    B2 = "b2"
    C1 = "c1"
    C2 = "c2"
    D1 = "d1"
    D2 = "d2"
    E1 = "e1"
    E2 = "e2"
    F1 = "f1"
    F2 = "f2"
    G1 = "g1"
    G2 = "g2"
    H1 = "h1"
    H2 = "h2"
    A0 = "a0"
    A1 = "a1"
    A2 = "a2"
    A3 = "a3"
    A4 = "a4"
    A5 = "a5"
    A6 = "a6"
    A7 = "a7"
    A8 = "a8"
    A9 = "a9"
    A10 = "a10"
    C0 = "c0"
    D0 = "d0"
    E0 = "e0"
    F0 = "f0"
    G0 = "g0"
    H0 = "h0"


class QuantityMethod(Enum):
    """
    Specifies the available methods for deriving a quantity or volume.

    :cvar ALLOCATED: allocated
    :cvar ALLOWED: allowed
    :cvar ESTIMATED: estimated
    :cvar TARGET: target
    :cvar MEASURED: measured
    :cvar BUDGET: budget
    :cvar CONSTRAINT: constraint
    :cvar FORECAST: forecast
    """

    ALLOCATED = "allocated"
    ALLOWED = "allowed"
    ESTIMATED = "estimated"
    TARGET = "target"
    MEASURED = "measured"
    BUDGET = "budget"
    CONSTRAINT = "constraint"
    FORECAST = "forecast"


class ReasonLost(Enum):
    """
    Specifies the reasons for lost production.

    :cvar VALUE_3RD_PARTY_PROCESSING: 3rd party processing
    :cvar DAILY_TOTAL_LOSS_OF_PROD: daily total loss of prod
    :cvar EXTENDED_MAINT_TURNAROUND: extended maint turnaround
    :cvar EXTENDED_MAINT_TURNAROUND_EXPORT: extended maint turnaround
        export
    :cvar HSE: hse
    :cvar MARKED_GAS: marked gas
    :cvar MARKED_OIL: marked oil
    :cvar MODIFICATION_PROJECT: modification project
    :cvar OPERATION_MISTAKES: operation mistakes
    :cvar OTHER: other
    :cvar PLANNED_MAINT_TURNAROUND: planned maint turnaround
    :cvar PREVENTIVE_MAINT_TOPSIDE: preventive maint topside
    :cvar PROCESS_AND_OPERATION_PROBLEM: process and operation problem
    :cvar PRODUCTION: production
    :cvar REGULATORY_REFERENCE: regulatory reference
    :cvar RESERVOIR: reservoir
    :cvar STRIKE_LOCK_OUT: strike/lock-out
    :cvar TESTING_AND_LOGGING: testing and logging
    :cvar TOPSIDE_EQUIPMENT_FAILURE_MAINT: topside equipment failure-
        maint
    :cvar UNAVAILABLE_TANKER_STORAGE: unavailable tanker storage
    :cvar UNKNOWN: unknown
    :cvar WEATHER_PROBLEM: weather problem
    :cvar WELL_EQUIPMENT_FAILURE_MAINT: well equipment failure-maint
    :cvar WELL_PLANNED_OPERATIONS: well planned operations
    :cvar WELL_PREVENTIVE_MAINT: well preventive maint
    :cvar WELL_PROBLEMS: well problems
    """

    VALUE_3RD_PARTY_PROCESSING = "3rd party processing"
    DAILY_TOTAL_LOSS_OF_PROD = "daily total loss of prod"
    EXTENDED_MAINT_TURNAROUND = "extended maint turnaround"
    EXTENDED_MAINT_TURNAROUND_EXPORT = "extended maint turnaround export"
    HSE = "hse"
    MARKED_GAS = "marked gas"
    MARKED_OIL = "marked oil"
    MODIFICATION_PROJECT = "modification project"
    OPERATION_MISTAKES = "operation mistakes"
    OTHER = "other"
    PLANNED_MAINT_TURNAROUND = "planned maint turnaround"
    PREVENTIVE_MAINT_TOPSIDE = "preventive maint topside"
    PROCESS_AND_OPERATION_PROBLEM = "process and operation problem"
    PRODUCTION = "production"
    REGULATORY_REFERENCE = "regulatory reference"
    RESERVOIR = "reservoir"
    STRIKE_LOCK_OUT = "strike/lock-out"
    TESTING_AND_LOGGING = "testing and logging"
    TOPSIDE_EQUIPMENT_FAILURE_MAINT = "topside equipment failure-maint"
    UNAVAILABLE_TANKER_STORAGE = "unavailable tanker storage"
    UNKNOWN = "unknown"
    WEATHER_PROBLEM = "weather problem"
    WELL_EQUIPMENT_FAILURE_MAINT = "well equipment failure-maint"
    WELL_PLANNED_OPERATIONS = "well planned operations"
    WELL_PREVENTIVE_MAINT = "well preventive maint"
    WELL_PROBLEMS = "well problems"


@dataclass
class RefInjectedGasAdded:
    """
    Reference to injected gas added.

    :ivar injection_gas_reference: Reference to the injection gas
        composition.
    """

    injection_gas_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "injectionGasReference",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ReferenceSeparatorStage:
    """
    Reference to the separator stage.

    :ivar separator_number: The separator number for a separator stage
        used to define the separation train, which is used as the basis
        of this fluid characterization.
    :ivar separator_pressure: The separator pressure for a separator
        stage used to define the separation train, which is used as the
        basis of this fluid characterization.
    :ivar separator_temperature: The separator temperature for a
        separator stage used to define the separation train, which is
        used as the basis of this fluid characterization.
    """

    separator_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SeparatorNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    separator_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SeparatorPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    separator_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SeparatorTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class RelativeCoordinate:
    """
    :ivar x: Defines the relative from-left-to-right location on a
        display screen. The display origin (0,0) is the upper left-hand
        corner of the display as viewed by the user.
    :ivar y: Defines the relative from-top-to-bottom location on a
        display screen. The display origin (0,0) is the upper left-hand
        corner of the display as viewed by the user.
    :ivar z: Defines the relative from-front-to-back location in a 3D
        system. The unrotated display origin (0,0) is the upper left-
        hand corner of the display as viewed by the user. The "3D
        picture" may be rotated on the 2D display.
    """

    x: List[str] = field(
        default_factory=list,
        metadata={
            "name": "X",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    y: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Y",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    z: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Z",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class RelativeVolumeRatio:
    """
    Reference to the fluid volume ratio.

    :ivar fluid_volume_reference: Reference to a fluid volume.
    """

    fluid_volume_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "fluidVolumeReference",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Report:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class ReportLocation:
    """Report location.

    Informaiton about a network location (e.g., URL) where the report is
    stored.

    :ivar location: The location of the report, e.g., a path or URL.
    :ivar location_date: The date when this report was stored in this
        location.
    :ivar location_type: The type of location in which the report is to
        be located.
    :ivar remark: Remarks and comments about this data item.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    location: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    location_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "LocationDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    location_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LocationType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class ReportingDurationKind(Enum):
    """
    Specifies the time periods for a report.
    """

    DAY = "day"
    LIFE_TO_DATE = "life to date"
    MONTH = "month"
    MONTH_TO_DATE = "month to date"
    TOTAL_CUMULATIVE = "total cumulative"
    WEEK = "week"
    YEAR = "year"
    YEAR_TO_DATE = "year to date"


@dataclass
class ReportingEntity:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


class ReportingFacility(Enum):
    """
    Specifies the kinds of facilities (usage of equipment or material) that can be
    reported on.

    :cvar BLOCK_VALVE: block valve
    :cvar BOTTOMHOLE: bottomhole
    :cvar CASING: casing
    :cvar CHOKE: choke
    :cvar CLUSTER: cluster
    :cvar COMMERCIAL_ENTITY: commercial entity
    :cvar COMPANY: company
    :cvar COMPLETION: completion
    :cvar COMPRESSOR: compressor
    :cvar CONTROLLER: controller
    :cvar CONTROLLER_LIFT: controller -- lift
    :cvar COUNTRY: country
    :cvar COUNTY: county
    :cvar DOWNHOLE_MONITORING_SYSTEM: downhole monitoring system
    :cvar ELECTRIC_SUBMERSIBLE_PUMP: electric submersible pump
    :cvar FIELD: field
    :cvar FIELD_AREA: field - area
    :cvar FIELD_GROUP: field - group
    :cvar FIELD_PART: field - part
    :cvar FLOW_METER: flow meter
    :cvar FLOWLINE: flowline
    :cvar FORMATION: formation
    :cvar GAS_LIFT_VALVE_MANDREL: gas lift valve mandrel
    :cvar GENERATOR: generator
    :cvar INSTALLATION: installation
    :cvar LEASE: lease
    :cvar LICENSE: license
    :cvar MANIFOLD: manifold
    :cvar ORGANIZATIONAL_UNIT: organizational unit
    :cvar PACKER: packer
    :cvar PERFORATED_INTERVAL: perforated interval
    :cvar PIPELINE: pipeline
    :cvar PLANT_PROCESSING: plant - processing
    :cvar PLATFORM: platform
    :cvar PRESSURE_METER: pressure meter
    :cvar PROCESSING_FACILITY: processing facility
    :cvar PRODUCTION_TUBING: production tubing
    :cvar PUMP: pump
    :cvar RECTIFIER: rectifier
    :cvar REGULATING_VALVE: regulating valve
    :cvar REMOTE_TERMINAL_UNIT: remote terminal unit
    :cvar RESERVOIR: reservoir
    :cvar SEPARATOR: separator
    :cvar SLEEVE_VALVE: sleeve valve
    :cvar STATE: state
    :cvar STORAGE: storage
    :cvar TANK: tank
    :cvar TEMPERATURE_METER: temperature meter
    :cvar TEMPLATE: template
    :cvar TERMINAL: terminal
    :cvar TRAP: trap
    :cvar TRUNKLINE: trunkline
    :cvar TUBING_HEAD: tubing head
    :cvar TURBINE: turbine
    :cvar UNKNOWN: unknown
    :cvar WELL: well
    :cvar WELL_GROUP: well group
    :cvar WELLBORE: wellbore
    :cvar WELLHEAD: wellhead
    :cvar ZONE: zone
    """

    BLOCK_VALVE = "block valve"
    BOTTOMHOLE = "bottomhole"
    CASING = "casing"
    CHOKE = "choke"
    CLUSTER = "cluster"
    COMMERCIAL_ENTITY = "commercial entity"
    COMPANY = "company"
    COMPLETION = "completion"
    COMPRESSOR = "compressor"
    CONTROLLER = "controller"
    CONTROLLER_LIFT = "controller -- lift"
    COUNTRY = "country"
    COUNTY = "county"
    DOWNHOLE_MONITORING_SYSTEM = "downhole monitoring system"
    ELECTRIC_SUBMERSIBLE_PUMP = "electric submersible pump"
    FIELD = "field"
    FIELD_AREA = "field - area"
    FIELD_GROUP = "field - group"
    FIELD_PART = "field - part"
    FLOW_METER = "flow meter"
    FLOWLINE = "flowline"
    FORMATION = "formation"
    GAS_LIFT_VALVE_MANDREL = "gas lift valve mandrel"
    GENERATOR = "generator"
    INSTALLATION = "installation"
    LEASE = "lease"
    LICENSE = "license"
    MANIFOLD = "manifold"
    ORGANIZATIONAL_UNIT = "organizational unit"
    PACKER = "packer"
    PERFORATED_INTERVAL = "perforated interval"
    PIPELINE = "pipeline"
    PLANT_PROCESSING = "plant - processing"
    PLATFORM = "platform"
    PRESSURE_METER = "pressure meter"
    PROCESSING_FACILITY = "processing facility"
    PRODUCTION_TUBING = "production tubing"
    PUMP = "pump"
    RECTIFIER = "rectifier"
    REGULATING_VALVE = "regulating valve"
    REMOTE_TERMINAL_UNIT = "remote terminal unit"
    RESERVOIR = "reservoir"
    SEPARATOR = "separator"
    SLEEVE_VALVE = "sleeve valve"
    STATE = "state"
    STORAGE = "storage"
    TANK = "tank"
    TEMPERATURE_METER = "temperature meter"
    TEMPLATE = "template"
    TERMINAL = "terminal"
    TRAP = "trap"
    TRUNKLINE = "trunkline"
    TUBING_HEAD = "tubing head"
    TURBINE = "turbine"
    UNKNOWN = "unknown"
    WELL = "well"
    WELL_GROUP = "well group"
    WELLBORE = "wellbore"
    WELLHEAD = "wellhead"
    ZONE = "zone"


class ReportingFlow(Enum):
    """
    Specifies the types of flow for volume reports.

    :cvar CONSUME: consume
    :cvar CONSUME_BLACK_START: consume - black start
    :cvar CONSUME_COMPRESSOR: consume - compressor
    :cvar CONSUME_EMITTED: consume - emitted
    :cvar CONSUME_FLARE: consume - flare
    :cvar CONSUME_FUEL: consume - fuel
    :cvar CONSUME_HP_FLARE: consume - HP flare
    :cvar CONSUME_LP_FLARE: consume - LP flare
    :cvar CONSUME_NON_COMPRESSOR: consume - non compressor
    :cvar CONSUME_VENTING: consume - venting
    :cvar DISPOSAL: disposal
    :cvar EXPORT: export
    :cvar EXPORT_NOMINATED: export - nominated
    :cvar EXPORT_REQUESTED: export - requested
    :cvar EXPORT_SHORTFALL: export - shortfall
    :cvar GAS_LIFT: gas lift
    :cvar HYDROCARBON_ACCOUNTING: hydrocarbon accounting
    :cvar IMPORT: import
    :cvar INJECTION: injection
    :cvar INVENTORY: inventory
    :cvar OVERBOARD: overboard
    :cvar PRODUCTION: production
    :cvar SALE: sale
    :cvar STORAGE: storage
    :cvar UNKNOWN: unknown
    """

    CONSUME = "consume"
    CONSUME_BLACK_START = "consume - black start"
    CONSUME_COMPRESSOR = "consume - compressor"
    CONSUME_EMITTED = "consume - emitted"
    CONSUME_FLARE = "consume - flare"
    CONSUME_FUEL = "consume - fuel"
    CONSUME_HP_FLARE = "consume - HP flare"
    CONSUME_LP_FLARE = "consume - LP flare"
    CONSUME_NON_COMPRESSOR = "consume - non compressor"
    CONSUME_VENTING = "consume - venting"
    DISPOSAL = "disposal"
    EXPORT = "export"
    EXPORT_NOMINATED = "export - nominated"
    EXPORT_REQUESTED = "export - requested"
    EXPORT_SHORTFALL = "export - shortfall"
    GAS_LIFT = "gas lift"
    HYDROCARBON_ACCOUNTING = "hydrocarbon accounting"
    IMPORT = "import"
    INJECTION = "injection"
    INVENTORY = "inventory"
    OVERBOARD = "overboard"
    PRODUCTION = "production"
    SALE = "sale"
    STORAGE = "storage"
    UNKNOWN = "unknown"


@dataclass
class ReportingHierarchy:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class ReportingHierarchyNode:
    """
    Association that contains the parent and child of this node.

    :ivar reporting_enitity_reference:
    :ivar child_node:
    :ivar id: The identification of node.
    :ivar name: The entity name.
    """

    reporting_enitity_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReportingEnitityReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    child_node: List[ReportingHierarchyNode] = field(
        default_factory=list,
        metadata={
            "name": "ChildNode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class ReportingProduct(Enum):
    """
    Specifies the kinds of product in a fluid system.

    :cvar AQUEOUS: aqueous
    :cvar C10: c10
    :cvar C10_1: c10-
    :cvar C10_2: c10+
    :cvar C2: c2-
    :cvar C2_1: c2+
    :cvar C3: c3-
    :cvar C3_1: c3+
    :cvar C4: c4-
    :cvar C4_1: c4+
    :cvar C5: c5-
    :cvar C5_1: c5+
    :cvar C6: c6-
    :cvar C6_1: c6+
    :cvar C7: c7
    :cvar C7_1: c7-
    :cvar C7_2: c7+
    :cvar C8: c8
    :cvar C8_1: c8-
    :cvar C8_2: c8+
    :cvar C9: c9
    :cvar C9_1: c9-
    :cvar C9_2: c9+
    :cvar CARBON_DIOXIDE_GAS: carbon dioxide gas
    :cvar CARBON_MONOXIDE_GAS: carbon monoxide gas
    :cvar CHEMICAL: chemical
    :cvar CONDENSATE: condensate
    :cvar CONDENSATE_GROSS: condensate - gross
    :cvar CONDENSATE_NET: condensate - net
    :cvar CRUDE_STABILIZED: crude - stabilized
    :cvar CUTTINGS: cuttings
    :cvar DIESEL: diesel
    :cvar DIETHYLENE_GLYCOL: diethylene glycol
    :cvar DIOXYGEN: dioxygen
    :cvar ELECTRIC_POWER: electric power
    :cvar ETHANE: ethane
    :cvar ETHANE_COMPONENT: ethane - component
    :cvar GAS: gas
    :cvar GAS_COMPONENT_IN_OIL: gas - component in oil
    :cvar GAS_DRY: gas - dry
    :cvar GAS_RICH: gas - rich
    :cvar GAS_WET: gas - wet
    :cvar HELIUM_GAS: helium gas
    :cvar HEPTANE: heptane
    :cvar HYDRAULIC_CONTROL_FLUID: hydraulic control fluid
    :cvar HYDROGEN_GAS: hydrogen gas
    :cvar HYDROGEN_SULFIDE: hydrogen sulfide
    :cvar I_BUTANE_COMPONENT: i-butane - component
    :cvar ISOBUTANE: isobutane
    :cvar ISOPENTANE: isopentane
    :cvar LIQUEFIED_NATURAL_GAS: liquefied natural gas
    :cvar LIQUEFIED_PETROLEUM_GAS: liquefied petroleum gas
    :cvar LIQUID: liquid
    :cvar METHANE: methane
    :cvar METHANE_COMPONENT: methane - component
    :cvar METHANOL: methanol
    :cvar MIXED_BUTANE: mixed butane
    :cvar MONOETHYLENE_GLYCOL: monoethylene glycol
    :cvar NAPHTHA: naphta
    :cvar NATURAL_GAS_LIQUID: natural gas liquid
    :cvar N_BUTANE_COMPONENT: n-butane - component
    :cvar NEOPENTANE: neopentane
    :cvar NGL_COMPONENT_IN_GAS: NGL - component in gas
    :cvar NITROGEN_GAS: nitrogen gas
    :cvar NITROGEN_OXIDE_GAS: nitrogen oxide gas
    :cvar NORMAL_BUTANE: normal butane
    :cvar NORMAL_PENTANE: normal pentane
    :cvar OIL: oil
    :cvar OIL_COMPONENT_IN_WATER: oil - component in water
    :cvar OIL_GROSS: oil - gross
    :cvar OIL_NET: oil - net
    :cvar OIL_AND_GAS: oil and gas
    :cvar OLEIC: oleic
    :cvar PENTANE_COMPONENT: pentane - component
    :cvar PETROLEUM_GAS_LIQUID: petroleum gas liquid
    :cvar PROPANE: propane
    :cvar PROPANE_COMPONENT: propane - component
    :cvar SALT: salt
    :cvar SAND_COMPONENT: sand - component
    :cvar TRIETHYLENE_GLYCOL: triethylene glycol
    :cvar UNKNOWN: unknown
    :cvar VAPOR: vapor
    :cvar WATER: water
    :cvar WATER_DISCHARGE: water - discharge
    :cvar WATER_PROCESSED: water - processed
    """

    AQUEOUS = "aqueous"
    C10 = "c10"
    C10_1 = "c10-"
    C10_2 = "c10+"
    C2 = "c2-"
    C2_1 = "c2+"
    C3 = "c3-"
    C3_1 = "c3+"
    C4 = "c4-"
    C4_1 = "c4+"
    C5 = "c5-"
    C5_1 = "c5+"
    C6 = "c6-"
    C6_1 = "c6+"
    C7 = "c7"
    C7_1 = "c7-"
    C7_2 = "c7+"
    C8 = "c8"
    C8_1 = "c8-"
    C8_2 = "c8+"
    C9 = "c9"
    C9_1 = "c9-"
    C9_2 = "c9+"
    CARBON_DIOXIDE_GAS = "carbon dioxide gas"
    CARBON_MONOXIDE_GAS = "carbon monoxide gas"
    CHEMICAL = "chemical"
    CONDENSATE = "condensate"
    CONDENSATE_GROSS = "condensate - gross"
    CONDENSATE_NET = "condensate - net"
    CRUDE_STABILIZED = "crude - stabilized"
    CUTTINGS = "cuttings"
    DIESEL = "diesel"
    DIETHYLENE_GLYCOL = "diethylene glycol"
    DIOXYGEN = "dioxygen"
    ELECTRIC_POWER = "electric power"
    ETHANE = "ethane"
    ETHANE_COMPONENT = "ethane - component"
    GAS = "gas"
    GAS_COMPONENT_IN_OIL = "gas - component in oil"
    GAS_DRY = "gas - dry"
    GAS_RICH = "gas - rich"
    GAS_WET = "gas - wet"
    HELIUM_GAS = "helium gas"
    HEPTANE = "heptane"
    HYDRAULIC_CONTROL_FLUID = "hydraulic control fluid"
    HYDROGEN_GAS = "hydrogen gas"
    HYDROGEN_SULFIDE = "hydrogen sulfide"
    I_BUTANE_COMPONENT = "i-butane - component"
    ISOBUTANE = "isobutane"
    ISOPENTANE = "isopentane"
    LIQUEFIED_NATURAL_GAS = "liquefied natural gas"
    LIQUEFIED_PETROLEUM_GAS = "liquefied petroleum gas"
    LIQUID = "liquid"
    METHANE = "methane"
    METHANE_COMPONENT = "methane - component"
    METHANOL = "methanol"
    MIXED_BUTANE = "mixed butane"
    MONOETHYLENE_GLYCOL = "monoethylene glycol"
    NAPHTHA = "naphtha"
    NATURAL_GAS_LIQUID = "natural gas liquid"
    N_BUTANE_COMPONENT = "n-butane - component"
    NEOPENTANE = "neopentane"
    NGL_COMPONENT_IN_GAS = "NGL - component in gas"
    NITROGEN_GAS = "nitrogen gas"
    NITROGEN_OXIDE_GAS = "nitrogen oxide gas"
    NORMAL_BUTANE = "normal butane"
    NORMAL_PENTANE = "normal pentane"
    OIL = "oil"
    OIL_COMPONENT_IN_WATER = "oil - component in water"
    OIL_GROSS = "oil - gross"
    OIL_NET = "oil - net"
    OIL_AND_GAS = "oil and gas"
    OLEIC = "oleic"
    PENTANE_COMPONENT = "pentane - component"
    PETROLEUM_GAS_LIQUID = "petroleum gas liquid"
    PROPANE = "propane"
    PROPANE_COMPONENT = "propane - component"
    SALT = "salt"
    SAND_COMPONENT = "sand - component"
    TRIETHYLENE_GLYCOL = "triethylene glycol"
    UNKNOWN = "unknown"
    VAPOR = "vapor"
    WATER = "water"
    WATER_DISCHARGE = "water - discharge"
    WATER_PROCESSED = "water - processed"


class SafetyType(Enum):
    """
    Specifies the types of safety issues for which a count can be defined.

    :cvar DRILL_OR_EXERCISE: drill or exercise
    :cvar FIRE: fire
    :cvar FIRST_AID: first aid
    :cvar HAZARD_REPORT_CARD: hazard report card
    :cvar JOB_OBSERVATION: job observation
    :cvar LOST_TIME_ACCIDENT: lost time accident
    :cvar LOST_TIME_INCIDENT: lost time incident
    :cvar MISCELLANEOUS: miscellaneous
    :cvar NEAR_MISS: near miss
    :cvar PERMIT_WITH_SJA: permit with SJA
    :cvar RELEASED_TO_AIR: released to air
    :cvar RELEASED_TO_WATER: released to water
    :cvar RESTRICTED_WORK: restricted work
    :cvar SAFETY_MEETING: safety meeting
    :cvar SENT_ASHORE: sent ashore
    :cvar SEVERE_ACCIDENT: severe accident
    :cvar SICK_ON_BOARD: sick on board
    :cvar SPILL_OR_LEAK: spill or leak
    :cvar TOTAL_PERMITS: total permits
    :cvar TRAFFIC_ACCIDENT: traffic accident
    :cvar YEAR_TO_DATE_INCIDENTS: year-to-date incidents
    """

    DRILL_OR_EXERCISE = "drill or exercise"
    FIRE = "fire"
    FIRST_AID = "first aid"
    HAZARD_REPORT_CARD = "hazard report card"
    JOB_OBSERVATION = "job observation"
    LOST_TIME_ACCIDENT = "lost time accident"
    LOST_TIME_INCIDENT = "lost time incident"
    MISCELLANEOUS = "miscellaneous"
    NEAR_MISS = "near miss"
    PERMIT_WITH_SJA = "permit with SJA"
    RELEASED_TO_AIR = "released to air"
    RELEASED_TO_WATER = "released to water"
    RESTRICTED_WORK = "restricted work"
    SAFETY_MEETING = "safety meeting"
    SENT_ASHORE = "sent ashore"
    SEVERE_ACCIDENT = "severe accident"
    SICK_ON_BOARD = "sick on board"
    SPILL_OR_LEAK = "spill or leak"
    TOTAL_PERMITS = "total permits"
    TRAFFIC_ACCIDENT = "traffic accident"
    YEAR_TO_DATE_INCIDENTS = "year-to-date incidents"


class SampleAction(Enum):
    """
    Specifies the actions that may be performed to a fluid sample.

    :cvar CUSTODY_TRANSFER: The action on the sample for this event was
        custody transfer to new custodian.
    :cvar DESTROYED: The action on the sample for this event was
        destruction.
    :cvar SAMPLE_TRANSFER: The action on the sample for this event was
        sample transfer.
    :cvar STORED: The action on the sample for this event was movement
        to storage.
    :cvar SUB_SAMPLE_DEAD: The action on the sample for this event was
        sub-sampling under dead conditions.
    :cvar SUB_SAMPLE_LIVE: The action on the sample for this event was
        sub-sampling under live conditions.
    """

    CUSTODY_TRANSFER = "custodyTransfer"
    DESTROYED = "destroyed"
    SAMPLE_TRANSFER = "sampleTransfer"
    STORED = "stored"
    SUB_SAMPLE_DEAD = "subSample Dead"
    SUB_SAMPLE_LIVE = "subSample Live"


class SampleQuality(Enum):
    """
    Specifies the values for the quality of data.

    :cvar INVALID: The sample quality is invalid.
    :cvar UNKNOWN: The sample quality is unknown.
    :cvar VALID: The sample quality is valid.
    """

    INVALID = "invalid"
    UNKNOWN = "unknown"
    VALID = "valid"


@dataclass
class SampleRestoration:
    """
    Sample restoration.

    :ivar date: The date when this test was performed.
    :ivar mixing_mechanism: The mixing mechanism when the sample is
        restored in preparation for analysis.
    :ivar remark: Remarks and comments about this data item.
    :ivar restoration_duration: The restoration duration when the sample
        is restored in preparation for analysis.
    :ivar restoration_pressure: The restoration pressure when the sample
        is restored in preparation for analysis.
    :ivar restoration_temperature: The restoration temperature when the
        sample is restored in preparation for analysis.
    """

    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mixing_mechanism: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MixingMechanism",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    restoration_duration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RestorationDuration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    restoration_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RestorationPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    restoration_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RestorationTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class Sara:
    """SARA analysis results.

    SARA stands for saturates, asphaltenes, resins and aromatics.

    :ivar aromatics_weight_fraction: The aromatics weight fraction in
        the sample.
    :ivar asphaltenes_weight_fraction: The asphaltenes weight fraction
        in the sample.
    :ivar napthenes_weight_fraction: The napthenes weight fraction in
        the sample.
    :ivar paraffins_weight_fraction: The paraffins weight fraction in
        the sample.
    :ivar remark: Remarks and comments about this data item.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    aromatics_weight_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AromaticsWeightFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    asphaltenes_weight_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AsphaltenesWeightFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    napthenes_weight_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "NapthenesWeightFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    paraffins_weight_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ParaffinsWeightFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class SaturationPointKind(Enum):
    """
    Specifies the kinds of saturation points.

    :cvar BUBBLE_POINT: bubble point
    :cvar DEW_POINT: dew point
    :cvar RETROGRADE_DEW_POINT: retrograde dew point
    :cvar CRITICAL_POINT: critical point
    """

    BUBBLE_POINT = "bubble point"
    DEW_POINT = "dew point"
    RETROGRADE_DEW_POINT = "retrograde dew point"
    CRITICAL_POINT = "critical point"


@dataclass
class SeparatorConditions:
    """
    Separator conditions.

    :ivar separator_test_reference: Reference to a separator test
        element, which contains the separator conditions (stages) which
        apply to this test.
    """

    separator_test_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "separatorTestReference",
            "type": "Attribute",
        },
    )


class ServiceFluidKind(Enum):
    """
    Specifies the kinds of product in a fluid system.

    :cvar ALKALINE_SOLUTIONS: alkaline solutions
    :cvar BIOCIDE: biocide
    :cvar CARBON_DIOXIDE: carbon dioxide
    :cvar CARBON_MONOXIDE: carbon monoxide
    :cvar CORROSION_INHIBITOR: corrosion inhibitor
    :cvar DEMULSIFIER: demulsifier
    :cvar DIESEL: diesel
    :cvar DIETHYLENE_GLYCOL: diethylene glycol
    :cvar DISPERSANT: dispersant
    :cvar DRAG_REDUCING_AGENT: drag reducing agent
    :cvar EMULSIFIER: emulsifier
    :cvar FLOCCULANT: flocculant
    :cvar HYDRAULIC_CONTROL_FLUID: hydraulic control fluid
    :cvar ISOPROPANOL: isopropanol
    :cvar LUBRICANT: lubricant
    :cvar METHANOL: methanol
    :cvar MONOETHYLENE_GLYCOL: monoethylene glycol
    :cvar OIL: oil
    :cvar OTHER_CHEMICAL: other chemical
    :cvar OTHER_HYDRATE_INHIBITOR: other hydrate inhibitor
    :cvar POLYMER: polymer
    :cvar SCALE_INHIBITOR: scale inhibitor
    :cvar SOLVENT: solvent
    :cvar STABILIZING_AGENT: stabilizing agent
    :cvar SURFACTANT: surfactant
    :cvar THINNER: thinner
    :cvar TRIETHYLENE_GLYCOL: triethylene glycol
    """

    ALKALINE_SOLUTIONS = "alkaline solutions"
    BIOCIDE = "biocide"
    CARBON_DIOXIDE = "carbon dioxide"
    CARBON_MONOXIDE = "carbon monoxide"
    CORROSION_INHIBITOR = "corrosion inhibitor"
    DEMULSIFIER = "demulsifier"
    DIESEL = "diesel"
    DIETHYLENE_GLYCOL = "diethylene glycol"
    DISPERSANT = "dispersant"
    DRAG_REDUCING_AGENT = "drag reducing agent"
    EMULSIFIER = "emulsifier"
    FLOCCULANT = "flocculant"
    HYDRAULIC_CONTROL_FLUID = "hydraulic control fluid"
    ISOPROPANOL = "isopropanol"
    LUBRICANT = "lubricant"
    METHANOL = "methanol"
    MONOETHYLENE_GLYCOL = "monoethylene glycol"
    OIL = "oil"
    OTHER_CHEMICAL = "other chemical"
    OTHER_HYDRATE_INHIBITOR = "other hydrate inhibitor"
    POLYMER = "polymer"
    SCALE_INHIBITOR = "scale inhibitor"
    SOLVENT = "solvent"
    STABILIZING_AGENT = "stabilizing agent"
    SURFACTANT = "surfactant"
    THINNER = "thinner"
    TRIETHYLENE_GLYCOL = "triethylene glycol"


@dataclass
class TableDelimiter:
    """
    Delimiter definition for a table.

    :ivar ascii_characters: The ascii character which represents a
        column delimiter in each row of a table using this table format.
    """

    ascii_characters: Optional[str] = field(
        default=None,
        metadata={
            "name": "asciiCharacters",
            "type": "Attribute",
            "required": True,
        },
    )


class TerminationType(Enum):
    """
    Specifies the types of fiber terminations.
    """

    LOOPED_BACK_TO_INSTRUMENT_BOX = "looped back to instrument box"
    TERMINATION_AT_CABLE = "termination at cable"


class ThermodynamicPhase(Enum):
    """
    Specifies the thermodynamic phases.

    :cvar AQUEOUS: A water-rich liquid phase.
    :cvar OLEIC: An oil-rich liquid phase.
    :cvar VAPOR: A gaseous phase at the conditions present.
    :cvar TOTAL_HYDROCARBON: A phase comprised of the total hydrocarbons
        (e.g., above the critical pressure for a gas condensate).
    """

    AQUEOUS = "aqueous"
    OLEIC = "oleic"
    VAPOR = "vapor"
    TOTAL_HYDROCARBON = "total hydrocarbon"


@dataclass
class TimeSeriesData:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


class TimeSeriesKeyword(Enum):
    """
    Specifies the keywords used for defining keyword-value pairs in a time series.

    :cvar ASSET_IDENTIFIER: asset identifier
    :cvar FLOW: flow
    :cvar PRODUCT: product
    :cvar QUALIFIER: qualifier
    :cvar SUBQUALIFIER: subqualifier
    :cvar UNKNOWN: unknown
    """

    ASSET_IDENTIFIER = "asset identifier"
    FLOW = "flow"
    PRODUCT = "product"
    QUALIFIER = "qualifier"
    SUBQUALIFIER = "subqualifier"
    UNKNOWN = "unknown"


@dataclass
class TimeSeriesStatistic:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class TimeSeriesStringSample:
    """
    A single string value in a time series.

    :ivar d_tim: The date and time at which the value applies. If no
        time is specified then the value is static and only one sample
        can be defined. Either dTim or value or both must be specified.
        If the status attribute is absent and the value is not "NaN",
        the data value can be assumed to be good with no restrictions.
    """

    d_tim: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "dTim",
            "type": "Attribute",
        },
    )


class TraceProcessingType(Enum):
    """
    Specifies the types of facility that can be mapped to for a given length of
    fiber measurement.

    :cvar AS_ACQUIRED: as acquired
    :cvar RECALIBRATED: recalibrated
    """

    AS_ACQUIRED = "as acquired"
    RECALIBRATED = "recalibrated"


class TransferKind(Enum):
    """
    Specifies if the transfer is input or output.

    :cvar INPUT: Transfer into an asset.
    :cvar OUTPUT: Transfer out of an asset.
    """

    INPUT = "input"
    OUTPUT = "output"


class ValidationOperation(Enum):
    """
    Specifies the well test validation operations.

    :cvar ACQUISITION_VALIDATION: acquisition validation
    :cvar ALLOCATION_VALIDATION: allocation validation
    :cvar EXTERNAL_QUALITY_ASSURANCE: external quality assurance
    :cvar SITE_VALIDATION: site validation
    :cvar UNKNOWN: unknown
    :cvar VALIDATION_RESULT: validation result
    :cvar WELL_MODEL_VALIDATION: well model validation
    """

    ACQUISITION_VALIDATION = "acquisition validation"
    ALLOCATION_VALIDATION = "allocation validation"
    EXTERNAL_QUALITY_ASSURANCE = "external quality assurance"
    SITE_VALIDATION = "site validation"
    UNKNOWN = "unknown"
    VALIDATION_RESULT = "validation result"
    WELL_MODEL_VALIDATION = "well model validation"


class ValidationResult(Enum):
    """
    Specifies well test validation results.

    :cvar FAILED: failed
    :cvar PASSED: passed
    :cvar PASSED_WITH_CHANGES: passed with changes
    :cvar UNKNOWN: unknown
    """

    FAILED = "failed"
    PASSED = "passed"
    PASSED_WITH_CHANGES = "passed with changes"
    UNKNOWN = "unknown"


class ValueStatus(Enum):
    """Specifies the indicators of the quality of a value.

    This is designed for a SCADA or OPC style of value status.

    :cvar ACCESS_DENIED: access denied
    :cvar BAD: bad
    :cvar BAD_CALIBRATION: bad calibration
    :cvar CALCULATION_FAILURE: calculation failure
    :cvar COMM_FAILURE: comm failure
    :cvar DEVICE_FAILURE: device failure
    :cvar FROZEN: frozen
    :cvar NOT_AVAILABLE: not available
    :cvar OVERFLOW: overflow
    :cvar QUESTIONABLE: questionable
    :cvar RANGE_LIMIT: range limit
    :cvar SENSOR_FAILURE: sensor failure
    :cvar SUBSTITUTED: substituted
    :cvar TIMEOUT: timeout
    """

    ACCESS_DENIED = "access denied"
    BAD = "bad"
    BAD_CALIBRATION = "bad calibration"
    CALCULATION_FAILURE = "calculation failure"
    COMM_FAILURE = "comm failure"
    DEVICE_FAILURE = "device failure"
    FROZEN = "frozen"
    NOT_AVAILABLE = "not available"
    OVERFLOW = "overflow"
    QUESTIONABLE = "questionable"
    RANGE_LIMIT = "range limit"
    SENSOR_FAILURE = "sensor failure"
    SUBSTITUTED = "substituted"
    TIMEOUT = "timeout"


@dataclass
class ViscosityAtTemperature:
    """
    Viscosity measurement at a specific temperature.

    :ivar viscosity: Viscosity measurement at the associated
        temperature.
    :ivar viscosity_temperature: Temperature at which the viscosity was
        measured.
    """

    viscosity: Optional[str] = field(
        default=None,
        metadata={
            "name": "Viscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    viscosity_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "ViscosityTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


class VolumeReferenceKind(Enum):
    """
    Specifies the conditions at which the volume was measured.

    :cvar INITIAL_RESERVOIR: The reference volume is measured at initial
        reservoir conditions.
    :cvar SATURATION_CALCULATED: The reference volume is measured at
        saturation-calculated conditions.
    :cvar SATURATION_MEASURED: The reference volume is measured at
        saturation-measured conditions.
    :cvar SEPARATOR_STAGE_1: The reference volume is measured at
        separator stage 1 conditions.
    :cvar SEPARATOR_STAGE_10: The reference volume is measured at
        separator stage 10 conditions.
    :cvar SEPARATOR_STAGE_2: The reference volume is measured at
        separator stage 2 conditions.
    :cvar SEPARATOR_STAGE_3: The reference volume is measured at
        separator stage 3 conditions.
    :cvar SEPARATOR_STAGE_4: The reference volume is measured at
        separator stage 4 conditions.
    :cvar SEPARATOR_STAGE_5: The reference volume is at measured
        separator stage 5 conditions.
    :cvar SEPARATOR_STAGE_6: The reference volume is measured  at
        separator stage 6 conditions.
    :cvar SEPARATOR_STAGE_7: The reference volume is measured at
        separator stage 7 conditions.
    :cvar SEPARATOR_STAGE_8: The reference volume is measured at
        separator stage 8 conditions.
    :cvar SEPARATOR_STAGE_9: The reference volume is measured at
        separator stage 9 conditions.
    :cvar STOCK_TANK: The reference volume is measured at stock tank
        conditions.
    :cvar UNKNOWN: The reference volume was measured at unknown
        conditions.
    """

    INITIAL_RESERVOIR = "initial reservoir"
    SATURATION_CALCULATED = "saturation-calculated"
    SATURATION_MEASURED = "saturation-measured"
    SEPARATOR_STAGE_1 = "separator stage 1"
    SEPARATOR_STAGE_10 = "separator stage 10"
    SEPARATOR_STAGE_2 = "separator stage 2"
    SEPARATOR_STAGE_3 = "separator stage 3"
    SEPARATOR_STAGE_4 = "separator stage 4"
    SEPARATOR_STAGE_5 = "separator stage 5"
    SEPARATOR_STAGE_6 = "separator stage 6"
    SEPARATOR_STAGE_7 = "separator stage 7"
    SEPARATOR_STAGE_8 = "separator stage 8"
    SEPARATOR_STAGE_9 = "separator stage 9"
    STOCK_TANK = "stock tank"
    UNKNOWN = "unknown"


@dataclass
class WaterAnalysisTestStep:
    """
    Water analysis test step.

    :ivar remark: Remarks and comments about this data item.
    :ivar solution_gas_water_ratio: The solution gas-water ratio for the
        water analysis test step.
    :ivar step_number: The step number is the index of a (P,T) step in
        the overall test.
    :ivar step_pressure: The pressure for this test step.
    :ivar step_temperature: The temperature for this test step.
    :ivar water_density: The water density for the water analysis test
        step.
    :ivar water_density_change_with_pressure: The water density change
        with pressure for the water analysis test step.
    :ivar water_density_change_with_temperature: The water density
        change with temperature for the water analysis test step.
    :ivar water_enthalpy: The water enthalpy for the water analysis test
        step.
    :ivar water_entropy: The water entropy for the water analysis test
        step.
    :ivar water_formation_volume_factor: The water formation volume
        factor for the water analysis test step.
    :ivar water_heat_capacity: The water heat capacity for the water
        analysis test step.
    :ivar water_isothermal_compressibility: The water isothermal
        compressibility for the water analysis test step.
    :ivar water_specific_heat: The water specific heat for the water
        analysis test step.
    :ivar water_specific_volume: The water specific volume for the water
        analysis test step.
    :ivar water_thermal_conductivity: The water thermal conductivity for
        the water analysis test step.
    :ivar water_thermal_expansion: The water thermal expansion for the
        water analysis test step.
    :ivar water_viscosity: The water viscosity for the water analysis
        test step.
    :ivar water_viscous_compressibility: The water viscous
        compressibility for the water analysis test step.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    solution_gas_water_ratio: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SolutionGasWaterRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    step_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    step_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    water_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_density_change_with_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterDensityChangeWithPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_density_change_with_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterDensityChangeWithTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_enthalpy: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterEnthalpy",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_entropy: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterEntropy",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_formation_volume_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterFormationVolumeFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_heat_capacity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterHeatCapacity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_isothermal_compressibility: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterIsothermalCompressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_specific_heat: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterSpecificHeat",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_specific_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterSpecificVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_thermal_conductivity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterThermalConductivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_thermal_expansion: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterThermalExpansion",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_viscous_compressibility: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterViscousCompressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class WaterSampleComponent:
    """
    Water sample component.

    :ivar equivalent_concentration: The equivalent concentration of the
        water sample component.
    :ivar ion: The ion of the water sample component.
    :ivar mass_concentration: The mass concentration of the water sample
        component.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    equivalent_concentration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EquivalentConcentration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    ion: Optional[str] = field(
        default=None,
        metadata={
            "name": "Ion",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    mass_concentration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassConcentration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class WellDirection(Enum):
    """
    Specifies the directions of flow of the fluids in a well facility (generally,
    injected or produced, or some combination).

    :cvar HUFF_N_PUFF: The well facility alternately injects (usually a
        steam or hot fluid) and produces.
    :cvar INJECTOR: The well facility is injecting fluids into the
        subsurface.
    :cvar PRODUCER: The well facility is producing fluids from the
        subsurface.
    :cvar UNCERTAIN: The flow direction of the fluids is variable, but
        not on a regular basis as is the case with the huff-n-puff flow.
    """

    HUFF_N_PUFF = "huff-n-puff"
    INJECTOR = "injector"
    PRODUCER = "producer"
    UNCERTAIN = "uncertain"


@dataclass
class WellElevationCoord:
    """A vertical (gravity-based) elevation coordinate within the context of a
    well.

    Positive moving upward from the reference datum. All coordinates
    with the same datum (and same UOM) can be considered to be in the
    same coordinate reference system (CRS) and are thus directly
    comparable.

    :ivar uom: The unit of measure of the quantity value. If not given
        then the default unit of measure of the explicitly or implicitly
        given datum must be assumed.
    """

    uom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class WellFlowingCondition:
    """
    Describes key conditions of the flowing well during a production well test.

    :ivar bottom_hole_flowing_pressure: The pressure at the bottom of
        the hole.
    :ivar bottom_hole_flowing_temperature: The temperature at the bottom
        of the hole when the well is flowing.
    :ivar bottom_hole_gauge_depth_md: The measure depth of the
        bottomhole gauge.
    :ivar bottom_hole_shut_in_pressure: The shut-in pressure of at the
        bottom of the hole.
    :ivar bottom_hole_static_pressure: The static pressure of the bottom
        of the hole.
    :ivar casing_head_pressure: The pressure at the casing head.
    :ivar choke_orifice_size: The choke diameter.
    :ivar flowing_pressure: The flowing pressure.
    :ivar tubing_head_flowing_pressure: The pressure at the tubing head.
    :ivar tubing_head_flowing_temperature: The temperature at the tubing
        head when the well is flowing.
    :ivar tubing_head_shut_in_pressure: The pressure at the tubing head
        when the well is shut in.
    """

    bottom_hole_flowing_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BottomHoleFlowingPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bottom_hole_flowing_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BottomHoleFlowingTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bottom_hole_gauge_depth_md: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BottomHoleGaugeDepthMD",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bottom_hole_shut_in_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BottomHoleShutInPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bottom_hole_static_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BottomHoleStaticPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    casing_head_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CasingHeadPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    choke_orifice_size: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ChokeOrificeSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flowing_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlowingPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tubing_head_flowing_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TubingHeadFlowingPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tubing_head_flowing_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TubingHeadFlowingTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tubing_head_shut_in_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TubingHeadShutInPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


class WellFluid(Enum):
    """
    Specifies the types of fluid being produced from or injected into a well
    facility.

    :cvar AIR: This is generally an injected fluid.
    :cvar CONDENSATE: Liquid hydrocarbons produced with natural gas that
        are separated from the gas by cooling and various other means.
        Condensate generally has an API gravity of 50 degrees to 120
        degrees and is water white, straw, or bluish in color. It is the
        liquid recovery from a well classified as a gas well. It is
        generally dissolved in the gaseous state under reservoir
        conditions but separates as a liquid either in passing up the
        hole or at the surface. These hydrocarbons, from associated and
        non-associated gas well gas, normally are recovered from lease
        separators or field facilities by mechanical separation.
    :cvar DRY: The well facility is classified as a dry well. It has not
        been nor will it be used to produce or inject any fluids.
    :cvar GAS: The well is classified as a gas well, producing or
        injecting a hydrocarbon gas. The gas is generally methane, but
        may have a mixture of other gases also.
    :cvar GAS_WATER: The well facility is classified as producing both
        gas and water. This classification is to be used when the
        produced stream flow is a mixture of gas and water. When a
        facility produces gas and water in separate streams, it should
        be classified twice as gas and as water.
    :cvar NON_HC_GAS: The well produces or injects non-hydrocarbon
        gases. Typical other gases would be helium and carbon dioxide.
    :cvar NON_HC_GAS_CO2: Carbon dioxide gas.
    :cvar OIL: The liquid hydrocarbon, generally referred to as crude
        oil.
    :cvar OIL_GAS: The well facility is classified as producing both gas
        and oil. This classification is to be used when the produced
        stream flow is a mixture of oil and gas. When a facility
        produces oil and gas in separate streams, it should be
        classified twice as oil and as gas.
    :cvar OIL_WATER: The well facility is classified as producing both
        oil and water. This classification is to be used when the
        produced stream flow is a mixture of oil and water. When a
        facility produces oil and water in separate streams, it should
        be classified twice as oil and as water.
    :cvar STEAM: The gaseous state of water. This is generally an
        injected fluid, but it is possible that some hydrothermal wells
        produce steam.
    :cvar WATER: The well is classified as a water well without
        distinguishing between brine or fresh water.
    :cvar WATER_BRINE: The well facility is classified as producing or
        injecting salt water.
    :cvar WATER_FRESH_WATER: The well facility is classified as
        producing fresh water that is capable of use for drinking or
        crop irrigation.
    """

    AIR = "air"
    CONDENSATE = "condensate"
    DRY = "dry"
    GAS = "gas"
    GAS_WATER = "gas-water"
    NON_HC_GAS = "non HC gas"
    NON_HC_GAS_CO2 = "non HC gas -- CO2"
    OIL = "oil"
    OIL_GAS = "oil-gas"
    OIL_WATER = "oil-water"
    STEAM = "steam"
    WATER = "water"
    WATER_BRINE = "water -- brine"
    WATER_FRESH_WATER = "water -- fresh water"


@dataclass
class WellKnownNameStruct:
    """
    The name of something within a mandatory naming system with an optional code.

    :ivar authority: The naming system within the name is unique.
    :ivar code: A unique (short) code associated with the name.
    """

    authority: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class WellOperationMethod(Enum):
    """
    Specifies the lift methods for producing a well.

    :cvar CONTINUOUS_GAS_LIFT: continuous gas lift
    :cvar ELECTRIC_SUBMERSIBLE_PUMP_LIFT: electric submersible pump lift
    :cvar FOAM_LIFT: foam lift
    :cvar HYDRAULIC_PUMP_LIFT: hydraulic pump lift
    :cvar INTERMITTENT_GAS_LIFT: intermittent gas lift
    :cvar JET_PUMP_LIFT: jet pump lift
    :cvar NATURAL_FLOW: natural flow
    :cvar PLUNGER_GAS_LIFT: plunger gas lift
    :cvar PROGRESSIVE_CAVITY_PUMP_LIFT: progressive cavity pump lift
    :cvar SUCKER_ROD_PUMP_LIFT: sucker rod pump lift
    :cvar UNKNOWN: unknown
    """

    CONTINUOUS_GAS_LIFT = "continuous gas lift"
    ELECTRIC_SUBMERSIBLE_PUMP_LIFT = "electric submersible pump lift"
    FOAM_LIFT = "foam lift"
    HYDRAULIC_PUMP_LIFT = "hydraulic pump lift"
    INTERMITTENT_GAS_LIFT = "intermittent gas lift"
    JET_PUMP_LIFT = "jet pump lift"
    NATURAL_FLOW = "natural flow"
    PLUNGER_GAS_LIFT = "plunger gas lift"
    PROGRESSIVE_CAVITY_PUMP_LIFT = "progressive cavity pump lift"
    SUCKER_ROD_PUMP_LIFT = "sucker rod pump lift"
    UNKNOWN = "unknown"


@dataclass
class WellTest:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class WellTestCumulative:
    """The cumulative amounts of the fluids at the time of the well test.

    The fluids are oil, gas, and water.

    :ivar cumulative_gas: The cumulative amount of gas.
    :ivar cumulative_oil: The cumulative amount of oil.
    :ivar cumulative_water: The cumulative amount of water.
    """

    cumulative_gas: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CumulativeGas",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cumulative_oil: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CumulativeOil",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cumulative_water: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CumulativeWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WellTestElectricSubmersiblePumpData:
    """
    Information about an electric submersible pump (ESP).

    :ivar electric_current: The average electric current of the ESP
        during the test. The presumption is that only one pump per well
        is operational during each test.
    :ivar frequency: The average frequency of the ESP during the test.
        The presumption is that only one pump per well is operational
        during each test.
    """

    electric_current: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ElectricCurrent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    frequency: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Frequency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WellTestFluidRate:
    """
    Information about fluid rate during a well test.

    :ivar fluid_rate: The fluid flow rate.
    :ivar fluid_rate_std_temp_pres: The fluid flow rate that has been
        corrected to standard temperature and pressure.
    :ivar gas_class: Class for natural gas. This is not valid for oil or
        water.
    """

    fluid_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FluidRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_rate_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FluidRateStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_class: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WellTestSeparatorData:
    """
    Well test data gathered at the separator.

    :ivar separator_pressure: The pressure measured at the separator
        during the well test.
    :ivar separator_temperature: The temperature measured at the
        separator during the well test.
    """

    separator_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SeparatorPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    separator_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SeparatorTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WellTestTestVolume:
    """
    The following sequence of four elements can be used for reporting of most
    production fluids.

    :ivar density: The density of the fluid, uncorrected.
    :ivar density_std_temp_pres: The density of the fluid, corrected to
        standard conditions of temperature and pressure.
    :ivar gas_class: Class for natural gas. This is not valid for oil or
        water.
    :ivar volume: The volume, uncorrected. This volume is generally
        reported at reservoir conditions.
    :ivar volume_std_temp_pres: The volume is the fluid, corrected to
        standard conditions of temperature and pressure.
    """

    density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Density",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    density_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DensityStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_class: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Volume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    volume_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VolumeStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WellVerticalDepthCoord:
    """A vertical (gravity-based) depth coordinate within the context of a well.

    Positive moving downward from the reference datum. All coordinates
    with the same datum (and same UOM) can be considered to be in the
    same coordinate reference system (CRS) and are thus directly
    comparable.

    :ivar uom: The unit of measure of the quantity value.
    """

    uom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class WftCurveSection:
    """
    Points to an interval on a curve in a log (or wellLog).

    :ivar channel_reference: A pointer to a specific channel that
        contains the curve.
    :ivar dtim_end: The date and time of the end of the relevant
        interval. If not specified then the end of the curve is assumed.
    :ivar dtim_start: The date and time of the start of the relevant
        interval. If not specified then the beginning of the curve is
        assumed.
    :ivar mnemonic: The curve mnemonic name.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    channel_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChannelReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    dtim_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mnemonic: Optional[str] = field(
        default=None,
        metadata={
            "name": "Mnemonic",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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


class WftEventKind(Enum):
    """
    Specifies the kinds of events that occur while operating a wireline formation
    tester (WFT) in a wellbore.

    :cvar TOOL_RETRACT: When the tool is being lowered into or raised
        out the of the hole the tool is in a retracted position. After a
        measurement is taken, the tool is retracted.
    :cvar TOOL_SET: When the tool reaches the location (depth) in the
        wellbore where a measurement is to be taken, the tool must be
        hydraulically set to take the measurement.
    :cvar UNKNOWN: unknown
    """

    TOOL_RETRACT = "tool retract"
    TOOL_SET = "tool set"
    UNKNOWN = "unknown"


class WftFlowingIntervalKind(Enum):
    """Specifies the kinds of connection between the WFT tool and the formation via
    a section of wellbore.

    Because WFTs can have probes or pairs of packers, which have
    different geometries (respectively a point connection or a section
    of wellbore like a welltest), it is necessary to state which kind if
    flowing for this station.

    :cvar PACKED_INTERVAL: packed interval
    :cvar PROBE: probe
    :cvar UNKNOWN: unknown
    """

    PACKED_INTERVAL = "packed interval"
    PROBE = "probe"
    UNKNOWN = "unknown"


@dataclass
class WftResultReference:
    """Defines a set of pointers which collectively identify a particular
    outputParameter beginning at a point in the hierarchy.

    The combination of pointers needed depends on the starting point.

    :ivar output_parameter_reference: A pointer to the desired
        outputParameter.
    :ivar result_reference: A pointer to the desired result containing
        the outputParameter.
    :ivar sample_acquisition:
    :ivar station_reference: A pointer to the station node containing
        the specified nodes.
    :ivar test: A pointer to the test node containing the specified
        nodes.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    output_parameter_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "OutputParameterReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    result_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResultReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    sample_acquisition: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SampleAcquisition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    station_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StationReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Test",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class WftRun:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


class WftStationKind(Enum):
    """
    Specifies the kinds of station.

    :cvar CONVENTIONAL: The flow is occurring and being measured.
    :cvar OBSERVATION: There is no flow;  you are observing the effect
        of pressure at this station of flow that is occurring at a
        different station.
    :cvar UNKNOWN: unknown
    """

    CONVENTIONAL = "conventional"
    OBSERVATION = "observation"
    UNKNOWN = "unknown"


class WftTestDataRole(Enum):
    """
    Specifies the role of test data being described.

    :cvar FLOW_HISTORY: flow history
    :cvar PRESSURE_STREAM: pressure stream
    :cvar UNKNOWN: unknown
    """

    FLOW_HISTORY = "flow history"
    PRESSURE_STREAM = "pressure stream"
    UNKNOWN = "unknown"


class WftTestKind(Enum):
    """
    Specifies the kinds of WFT tests at a given time, at a given station.

    :cvar BUILDUP: buildup
    :cvar DRAWDOWN: drawdown
    :cvar UNKNOWN: unknown
    """

    BUILDUP = "buildup"
    DRAWDOWN = "drawdown"
    UNKNOWN = "unknown"


class WftTestResultKind(Enum):
    """
    Specifies the kinds of test results.

    :cvar BUILDUP_RESULT: buildup result
    :cvar DRAWDOWN_RESULT: drawdown result
    :cvar UNKNOWN: unknown
    """

    BUILDUP_RESULT = "buildup result"
    DRAWDOWN_RESULT = "drawdown result"
    UNKNOWN = "unknown"


class SaturationKind(Enum):
    """
    Specifies the kinds of saturation.

    :cvar SATURATED: The fluid is saturated.
    :cvar UNDERSATURATED: The fluid is under-saturated.
    """

    SATURATED = "saturated"
    UNDERSATURATED = "undersaturated"


@dataclass
class AbstractDisposition:
    """
    The Abstract base type of disposition.

    :ivar product_disposition_code: A unique disposition code associated
        within a given naming system. This may be a code specified by a
        regulatory agency.
    :ivar remark: A descriptive remark relating to this disposition.
    :ivar disposition_quantity: The amount of product to which this
        disposition applies.
    :ivar quantity_method: Quantity method.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    product_disposition_code: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProductDispositionCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    disposition_quantity: List[AbstractProductQuantity] = field(
        default_factory=list,
        metadata={
            "name": "DispositionQuantity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    quantity_method: Optional[Union[QuantityMethod, str]] = field(
        default=None,
        metadata={
            "name": "QuantityMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class BinaryInteractionCoefficientSet:
    """
    Binary interaction coefficient set.
    """

    binary_interaction_coefficient: List[BinaryInteractionCoefficient] = field(
        default_factory=list,
        metadata={
            "name": "BinaryInteractionCoefficient",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class CommonPropertiesProductVolume:
    """
    Properties that are common to multiple structures in the product volume schema.

    :ivar absolute_min_pres: Absolute minimum pressure before the system
        will give an alarm.
    :ivar atmosphere: The average atmospheric pressure during the
        reporting period.
    :ivar bsw: Basic sediment and water is measured from a liquid sample
        of the production stream. It includes free water, sediment and
        emulsion and is measured as a volume percentage of the
        production stream.
    :ivar bsw_previous: The basic sediment and water as measured on the
        previous reporting period (e.g., day).
    :ivar bsw_stabilized_crude: Basic sediment and water content in
        stabilized crude.
    :ivar concentration: The concentration of the product as a volume
        percentage of the product stream.
    :ivar density_flow_rate: The mass basis flow rate of the product.
        This is used for things like a sand component.
    :ivar density_stabilized_crude: The density of stabilized crude.
    :ivar density_value:
    :ivar efficiency: The actual volume divided by the potential volume.
    :ivar flow_rate_value:
    :ivar gas_liquid_ratio: The volumetric ratio of gas to liquid for
        all products in the whole flow.
    :ivar gor: Gas oil ratio. The ratio between the total produced gas
        volume and the total produced oil volume including oil and gas
        volumes used on the installation.
    :ivar gor_mtd: Gas oil ratio month to date. The gas oil ratio from
        the beginning of the month to the end of the reporting period.
    :ivar gross_calorific_value_std: The amount of heat that would be
        released by the complete combustion in air of a specific
        quantity of product at standard temperature and pressure.
    :ivar hc_dewpoint: The temperature at which the heavier hydrocarbons
        come out of solution.
    :ivar mass: The mass of the product.
    :ivar mole_amt: The molar amount.
    :ivar molecular_weight: The molecular weight of the product.
    :ivar mole_percent: The mole fraction of the product.
    :ivar pres: Pressure of the port. Specifying the pressure here (as
        opposed to in Period) implies that the pressure is constant for
        all periods of the flow.
    :ivar rvp: Reid vapor pressure of the product. The absolute vapor
        pressure of volatile crude oil and volatile petroleum liquids,
        except liquefied petroleum gases, as determined in accordance
        with American Society for Testing and Materials under the
        designation ASTM D323-56.
    :ivar rvp_stabilized_crude: Reid vapor pressure of stabilized crude.
    :ivar sg: The specific gravity of the product.
    :ivar temp: Temperature of the port. Specifying the temperature here
        (as opposed to in Period) implies that the temperature is
        constant for all periods of the flow.
    :ivar tvp: True vapor pressure of the product. The equilibrium
        partial pressure exerted by a petroleum liquid as determined in
        accordance with standard methods.
    :ivar volume_value:
    :ivar water_conc_mass: Water concentration mass basis. The ratio of
        water produced compared to the mass of total liquids produced.
    :ivar water_conc_vol: Water concentration volume basis. The ratio of
        water produced compared to the mass of total liquids produced.
    :ivar water_dewpoint: The temperature at which the first water comes
        out of solution.
    :ivar weight_percent: The weight fraction of the product.
    :ivar wobbe_index: Indicator value of the interchangeability of fuel
        gases.
    :ivar work: The electrical energy represented by the product.
    :ivar port_diff: The internal differences between this port and one
        other port on this unit.
    """

    absolute_min_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AbsoluteMinPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    atmosphere: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Atmosphere",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bsw: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Bsw",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bsw_previous: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BswPrevious",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bsw_stabilized_crude: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BswStabilizedCrude",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    concentration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Concentration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    density_flow_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DensityFlowRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    density_stabilized_crude: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DensityStabilizedCrude",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    density_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DensityValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    efficiency: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Efficiency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flow_rate_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlowRateValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_liquid_ratio: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasLiquidRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Gor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gor_mtd: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GorMTD",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gross_calorific_value_std: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GrossCalorificValueStd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    hc_dewpoint: List[str] = field(
        default_factory=list,
        metadata={
            "name": "HcDewpoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Mass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mole_amt: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MoleAmt",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mole_percent: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MolePercent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Pres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    rvp: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Rvp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    rvp_stabilized_crude: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RvpStabilizedCrude",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sg: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Sg",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    temp: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Temp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tvp: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Tvp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    volume_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VolumeValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_conc_mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterConcMass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_conc_vol: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterConcVol",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_dewpoint: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterDewpoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    weight_percent: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WeightPercent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wobbe_index: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WobbeIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    work: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Work",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    port_diff: List[ProductVolumePortDifference] = field(
        default_factory=list,
        metadata={
            "name": "PortDiff",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class ComponentPropertySet:
    """
    Component property set.
    """

    fluid_component_property: List[FluidComponentProperty] = field(
        default_factory=list,
        metadata={
            "name": "FluidComponentProperty",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class CrewCount:
    """
    A one-based count of personnel on a type of crew.

    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    :ivar type_value: The type of crew for which a count is being
        defined.
    """

    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    type_value: Optional[CrewType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass
class CumulativeGasProducedRatioStd(AbstractGasProducedRatioVolume):
    """
    The standard condition of cumulative gas produced ratio.

    :ivar cumulative_gas_produced_ratio_std: The standard condition of
        cumulative gas produced ratio.
    """

    cumulative_gas_produced_ratio_std: Optional[str] = field(
        default=None,
        metadata={
            "name": "CumulativeGasProducedRatioStd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class CumulativeGasProducedVol(AbstractGasProducedRatioVolume):
    """
    The cumulative gas produced volume.

    :ivar cumulative_gas_produced_volume: The cumulative gas oil
        produced ratio at standard conditions.
    """

    cumulative_gas_produced_volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "CumulativeGasProducedVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class CurveData(AbstractMeasureDataType):
    """
    The data of a curve.

    :ivar index: The value of an independent (index) variable in a row
        of the curve table. The units of measure are specified in the
        curve definition. The first value corresponds to order=1 for
        columns where isIndex is true. The second to order=2. And so on.
        The number of index and data values must match the number of
        columns in the table.
    :ivar value: The value of a dependent (data) variable in a row of
        the curve table. The units of measure are specified in the curve
        definition. The first value corresponds to order=1 for columns
        where isIndex is false. The second to order=2. And so on. The
        number of index and data values must match the number of columns
        in the table.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    index: Optional[str] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    value: List[float] = field(
        default_factory=list,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
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
class CustomPvtModelExtension:
    """
    Custom PVT model extension.

    :ivar description: A description of the custom model.
    :ivar custom_pvt_model_parameter:
    """

    description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    custom_pvt_model_parameter: List[CustomPvtModelParameter] = field(
        default_factory=list,
        metadata={
            "name": "CustomPvtModelParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DasCalibrationPoint:
    """
    This object contains calibration points in the array.

    :ivar calibration_facility_length: The ‘facility length’
        corresponding to the CalibrationOpticPathDistance. The ‘facility
        length’ is the length along the ‘optical path’ and is corrected
        for overstuffing, additional fiber in turnaround-subs or
        H-splices that increase the optical path length on the OTDR, but
        not the actual facility length.
    :ivar calibration_locus_index: The locus index for the calibration
        point. Where ‘Locus Index 0’ is the acoustic sample point at the
        connector of the measurement instrument.
    :ivar calibration_optical_path_distance: The ‘fiber distance’
        corresponding with the locus index of the calibration point.
        This is similar to the OpticalPathDistance used in DTS. This
        ‘fiber distance’ is the distance from the connector of the
        measurement instrument to the acoustic sample point along the
        fiber that is the furthest from the measurement instrument for
        that particular test.
    :ivar calibration_type: A brief meaningful description of the type
        of calibration point. This is an extensible enumeration type.
        Current reserved keywords are ‘locus calibration’, ‘tap test’
        and ‘last locus to end of fiber’ for commonly used calibration
        points.
    """

    calibration_facility_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "CalibrationFacilityLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    calibration_locus_index: Optional[str] = field(
        default=None,
        metadata={
            "name": "CalibrationLocusIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    calibration_optical_path_distance: Optional[str] = field(
        default=None,
        metadata={
            "name": "CalibrationOpticalPathDistance",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    calibration_type: Optional[Union[DasCalibrationType, str]] = field(
        default=None,
        metadata={
            "name": "CalibrationType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DasFbeData:
    """Two dimensional (loci &amp; time) array containing processed frequency band
    extracted data samples.

    This processed data type is obtained by applying a frequency band
    filter to the raw data acquired by the DAS acquisition system. For
    each frequency band provided, a separate DASFbeData array object is
    created.

    :ivar end_frequency: End of an individual frequency band in a DAS
        FBE data set. This typically corresponds to the frequency of the
        3dB point of the filter.
    :ivar fbe_data_array:
    :ivar fbe_data_index: The nth count of this DasFbeData in the
        DasFbe.  Recommended if there is more than 1 dataset in this
        Fbe.  This index corresponds to the FbeData array number in the
        H5 file.
    :ivar start_frequency: Start of an individual frequency band in a
        DAS FBE data set. This typically corresponds to the frequency of
        the 3dB point of the filter.
    :ivar dimensions: An array of two elements describing the ordering
        of the FBE data array. The fastest running index is stored in
        the second element. For example the {‘time’, ‘locus’} indicates
        that ‘locus’ is the fastest running index. Note that vendors may
        deliver data with different orderings.
    """

    end_frequency: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndFrequency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fbe_data_array: Optional[str] = field(
        default=None,
        metadata={
            "name": "FbeDataArray",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fbe_data_index: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FbeDataIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    start_frequency: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartFrequency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    dimensions: List[DasDimensions] = field(
        default_factory=list,
        metadata={
            "name": "Dimensions",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 2,
            "max_occurs": 2,
        },
    )


@dataclass
class DasRawData:
    """
    Two- dimensional array containing raw data samples acquired by the DAS
    acquisition system.

    :ivar raw_data_array:
    :ivar dimensions: An array of two elements describing the ordering
        of the raw data array. The fastest running index is stored in
        the second element. For the DAS measurement instrument, the
        ordering is typically {‘time’, ‘locus’} indicating that the
        locus is the fastest running index, but in some cases the order
        may be reversed.
    """

    raw_data_array: Optional[str] = field(
        default=None,
        metadata={
            "name": "RawDataArray",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    dimensions: List[DasDimensions] = field(
        default_factory=list,
        metadata={
            "name": "Dimensions",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 2,
            "max_occurs": 2,
        },
    )


@dataclass
class DasSpectraData:
    """Three-dimensional array (loci, time, transform) containing spectrum data
    samples.

    Spectrum data is processed data obtained by applying a mathematical
    transformation function to the DAS raw data acquired by the
    acquisition system. The array is 3D and contains TransformSize
    points for each locus and time for which the data is provided. For
    example, many service providers will provide Fourier transformed
    versions of the raw data to customers, but other transformation
    functions are also allowed.

    :ivar end_frequency: End frequency in a DAS spectra data set. This
        value is typically set to the maximum frequency present in the
        spectra data set.
    :ivar spectra_data_array:
    :ivar start_frequency: Start frequency in a DAS spectra data set.
        This value typically is set to the minimum frequency present in
        the spectra data set.
    :ivar dimensions: An array of three elements describing the ordering
        of the raw data array. The fastest running index is stored in
        the last element. For example {‘time’, ‘locus’, ‘frequency’}
        indicates that the frequency is the fastest running index. Note
        that vendors may deliver data with different orderings.
    """

    end_frequency: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndFrequency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    spectra_data_array: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpectraDataArray",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    start_frequency: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartFrequency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    dimensions: List[DasDimensions] = field(
        default_factory=list,
        metadata={
            "name": "Dimensions",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 3,
            "max_occurs": 3,
        },
    )


@dataclass
class DatumCrs(AbstractDatum):
    """
    DatumCRS.

    :ivar datum_crs: A reference to the coordinateReferenceSystem object
        representing the vertical reference datum (i.e., this
        wellDatum). This should only be specified if the above 'code'
        represents some variation of sea level.
    """

    class Meta:
        name = "DatumCRS"

    datum_crs: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DatumCRS",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DatumName(AbstractDatum):
    """
    DatumName.
    """

    datum_name: Optional[WellKnownNameStruct] = field(
        default=None,
        metadata={
            "name": "DatumName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DeferredProduction:
    """
    The production volume deferred for the reporting period.

    :ivar remark: Remarks and comments about this data item.
    :ivar deferred_product_quantity:
    :ivar estimation_method: The method used to estimate deferred
        production. See enum EstimationMethod.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    deferred_product_quantity: List[AbstractProductQuantity] = field(
        default_factory=list,
        metadata={
            "name": "DeferredProductQuantity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    estimation_method: Optional[Union[EstimationMethod, str]] = field(
        default=None,
        metadata={
            "name": "EstimationMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DtsCalibration:
    """Calibration parameters vary from vendor to vendor, depending on the
    calibration method being used.

    This is a general type that allows a calibration date, business
    associate, and many name/value pairs.

    :ivar calibrated_by: The business associate that performed the
        calibration.
    :ivar calibration_protocol: This may be a standard protocol or a
        software application.
    :ivar dtim_calibration: The date of the calibration.
    :ivar extension_name_value:
    :ivar parameter: Attribute name is the name of the parameter.
        Optional attribute uom is the unit of measure of the parameter.
        The value of the element is the value of the parameter. Note
        that a string value may appear as a parameter.
    :ivar remark: Any remarks that may be useful regarding the
        calibration information.
    :ivar uid: A  unique identifier (UID) of an instance of
        DtsCalibration.
    """

    calibrated_by: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CalibratedBy",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    calibration_protocol: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CalibrationProtocol",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_calibration: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "DTimCalibration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    parameter: List[CalibrationParameter] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class DtsInterpretationData:
    """
    Header data for a particular collection of interpretation data.

    :ivar bad_flag: Indicates whether or not the interpretation log
        contains bad data. This flag allows you to keep bad data  (so at
        least you know that something was generated/acquired) and filter
        it out when doing relevant data operations.
    :ivar channel_set_reference: Pointer to a ChannelSet containing the
        comma-delimited list of mnemonics and units, and channel data
        representing the interpretation data. BUSINESS RULE: The
        mnemonics and the units must follow a strict order. The mnemonic
        list must be in this order: facilityDistance,
        adjustedTemperature The unit list must be one of the following:
        - m,degC - ft,degF
    :ivar comment: A descriptive remark about the interpretation log.
    :ivar creation_start_time: Time when the interpretation log data was
        generated.
    :ivar facility_mapping: A reference to the facilityMapping to which
        this InterpretationData relates. The facility mapping relates a
        length of fiber to a corresponding length of a facility
        (probably a wellbore or pipeline). The facilityMapping also
        contains the datum from which the InterpretedData is indexed.
    :ivar index_mnemonic: The mnemonic of the channel in the
        InterpretedData that represents the index to the data (expected
        to be a length along the facility (e.g., wellbore, pipeline)
        being measured.
    :ivar point_count: The number of rows in this interpreted data
        object. Each row or "point" represents a measurement along the
        fiber.
    :ivar sampling_interval: The difference in fiber distance between
        consecutive temperature sample points in a single temperature
        trace.
    :ivar interpretation_processing_type: Indicates what type of post-
        processing technique was used to generate this interpretation
        log. Enum list. The meaning is that this process was applied to
        the InterpretedData referenced by the parentInterpretationID.
    :ivar measurement_reference: Mandatory element indicating that the
        referenced MeasuredTraceSet object is the raw trace data from
        which this InterpretedData is derived. This is needed so that
        any InterpretedData can be related to the raw measurement from
        which it is derived.
    :ivar parent_interpretation_reference: Optional element indicating
        that the referenced InterpretedData object is the parent from
        which this InterpretedData is derived. Example, this instance
        may be derived from a parent by the data having been
        temperature-shifted to match an external data source. The
        element InterpretationProcessingType is provided to record which
        type of operation was performed on the parent data to obtain
        this instance of data.
    :ivar uid: Unique identifier of this object.
    """

    bad_flag: Optional[bool] = field(
        default=None,
        metadata={
            "name": "BadFlag",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    channel_set_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChannelSetReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    creation_start_time: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "CreationStartTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    facility_mapping: Optional[str] = field(
        default=None,
        metadata={
            "name": "FacilityMapping",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    index_mnemonic: Optional[str] = field(
        default=None,
        metadata={
            "name": "IndexMnemonic",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    point_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "PointCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    sampling_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "SamplingInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    interpretation_processing_type: Optional[
        InterpretationProcessingType
    ] = field(
        default=None,
        metadata={
            "name": "InterpretationProcessingType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    measurement_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "measurementReference",
            "type": "Attribute",
            "required": True,
        },
    )
    parent_interpretation_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "parentInterpretationReference",
            "type": "Attribute",
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
class DtsMeasurementTrace:
    """
    Header data for raw (measured) traces collections.

    :ivar channel_set_reference: Pointer to a ChannelSet containing the
        comma-delimited list of mnemonics and units, and channel data
        representing the measurement trace. BUSINESS RULE: The mnemonics
        and the units must follow a strict order. The mnemonic list must
        be in this order: fiberDistance, antistokes, stokes,
        reverseAntiStokes, reverseStokes, rayleigh1, rayleigh2,
        brillouinfrequency, loss, lossRatio, cumulativeExcessLoss,
        frequencyQualityMeasure, measurementUncertainty,
        brillouinAmplitude, opticalPathTemperature,
        uncalibratedTemperature1, uncalibratedTemperature2 The unit list
        must be one of the following: - m, mW, mW, mW, mW, mW, mW, GHz,
        dB/Km, dB/Km, dB, dimensionless, degC, mW, degC, DegC, degC -
        ft, mW, mW, mW, mW,mW, mW, GHz, dB/Km, dB/Km,dB, dimensionless,
        degF, mW, degF, degF, degF
    :ivar comment: A descriptive remark about the measured trace set.
    :ivar frequency_rayleigh1: Frequency reference for Rayleigh 1
        measurement.
    :ivar frequency_rayleigh2: Frequency reference for Rayleigh 2
        measurement.
    :ivar index_mnemonic: The mnemonic of the channel in the
        MeasuredTraceSet that represents the index to the data (expected
        to be a length along the facility (e.g., wellbore, pipeline)
        being measured.
    :ivar point_count: The number of rows in this interpreted data
        object. Each row or "point" represents a measurement along the
        fiber.
    :ivar sampling_interval: The difference in fiber distance between
        consecutive temperature sample points in a single temperature
        trace.
    :ivar trace_processing_type: Denotes whether the trace was stored as
        acquired by the measurement device or recalibrated in any way.
    :ivar parent_measurement_reference: Where this dtsMeasuredTraceSet
        was derived from a parent dtsMeasuredTraceSet (having been
        recalibrated for example), the parent dtsMeasuredTraceSet can be
        indicated by referencing its UID with this element.
    :ivar uid: Unique identifier of this object.
    """

    channel_set_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChannelSetReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    frequency_rayleigh1: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FrequencyRayleigh1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    frequency_rayleigh2: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FrequencyRayleigh2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    index_mnemonic: Optional[str] = field(
        default=None,
        metadata={
            "name": "IndexMnemonic",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    point_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "PointCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    sampling_interval: Optional[str] = field(
        default=None,
        metadata={
            "name": "SamplingInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    trace_processing_type: Optional[TraceProcessingType] = field(
        default=None,
        metadata={
            "name": "TraceProcessingType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    parent_measurement_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "parentMeasurementReference",
            "type": "Attribute",
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
class EmailQualifierStruct:
    """
    An email address with an attribute, used to "qualify" an email as personal,
    work, or permanent.
    """

    qualifier: Optional[AddressQualifier] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class EndpointDateTime:
    """A value used for the endpoint of a date-time interval.

    The meaning of the endpoint of an interval must be defined by the
    endpoint attribute.

    :ivar endpoint: Defines the semantics (inclusive or exclusive) of
        the endpoint within the context of the interval.
    """

    endpoint: Optional[EndpointQualifierInterval] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EndpointQualifiedDate:
    """A date value used for min/max query parameters related to "growing objects".

    The meaning of the endpoint of an interval can be modified by the
    endpoint attribute.

    :ivar endpoint: The default is "inclusive".
    """

    endpoint: Optional[EndpointQualifier] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class EndpointQualifiedDateTime:
    """A timestamp value used for min/max query parameters related to "growing
    objects".

    The meaning of the endpoint of an interval can be modified by the
    endpoint attribute.

    :ivar endpoint: The default is "inclusive".
    """

    endpoint: Optional[EndpointQualifier] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class EndpointQuantity:
    """A value used for the endpoint of an interval.

    If the value represents a measure then the unit must be specified
    elsewhere. The meaning of the endpoint of an interval must be
    defined by the endpoint attribute.

    :ivar endpoint: Defines the semantics (inclusive or exclusive) of
        the endpoint within the context of the interval.
    """

    endpoint: Optional[EndpointQualifierInterval] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class FacilityIdentifierStruct:
    """
    Identifies a facility.

    :ivar naming_system: The naming system within which the name is
        unique. For example, API or NPD.
    :ivar site_kind: A custom sub-categorization of facility kind. This
        attribute is free-form text and allows implementers to provide a
        more specific or specialized description of the facility kind.
    :ivar uid_ref: The referencing uid.
    :ivar kind: The kind of facility.
    :ivar content:
    """

    naming_system: Optional[str] = field(
        default=None,
        metadata={
            "name": "namingSystem",
            "type": "Attribute",
        },
    )
    site_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "siteKind",
            "type": "Attribute",
        },
    )
    uid_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "uidRef",
            "type": "Attribute",
        },
    )
    kind: Optional[ReportingFacility] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class FacilityUnitPort(AbstractRelatedFacilityObject):
    """
    Facility unit port.

    :ivar network_reference: The product flow network representing the
        facility. This is only required if the network is not the same
        as the primary network that represents the Product Flow Model.
        This must be unique within the context of the product flow model
        represented by this report.
    :ivar port_reference: The product flow port associated with the
        product flow unit.
    :ivar unit_reference: The product flow unit representing the
        facility.
    """

    network_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "NetworkReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    port_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "PortReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    unit_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FiberControlLine(AbstractCable):
    """
    Information regarding the control line into which a fiber cable may be pumped
    to measure a facility.

    :ivar comment: A descriptive remark about the fiber control line.
    :ivar encapsulation_size: Enum of the size of encapsulation of a
        fiber within a control line.
    :ivar encapsulation_type: Enum of square or round encapsulation for
        a control line. A fiber may be installed inside the control
        line.
    :ivar material: Enum of the common materials from which a control
        line may be made. A fiber may be installed inside the control
        line.
    :ivar size: Enum of the common sizes of control line. The enum list
        gives diameters and weight per length values. A fiber may be
        installed inside the control line.
    :ivar pump_activity: The activity of pumping the fiber downhole into
        a control line (small diameter tube).
    :ivar downhole_control_line_reference: A reference to the control
        line string in a completion data object that represents this
        control line containing a fiber.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    encapsulation_size: Optional[ControlLineEncapsulationSize] = field(
        default=None,
        metadata={
            "name": "EncapsulationSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    encapsulation_type: Optional[ControlLineEncapsulationType] = field(
        default=None,
        metadata={
            "name": "EncapsulationType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    material: Optional[ControlLineMaterial] = field(
        default=None,
        metadata={
            "name": "Material",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    size: Optional[ControlLineSize] = field(
        default=None,
        metadata={
            "name": "Size",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    pump_activity: List[FiberPumpActivity] = field(
        default_factory=list,
        metadata={
            "name": "PumpActivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    downhole_control_line_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "downholeControlLineReference",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class FiberConveyance:
    """The means by which this fiber segment is conveyed into the well.

    Choices: permanent, intervention, or control line conveyance method.
    """

    cable: Optional[AbstractCable] = field(
        default=None,
        metadata={
            "name": "Cable",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FiberFacilityGeneric(AbstractFiberFacility):
    """
    If a facility mapping is not explicitly to a well or pipeline, use this element
    to show what optical path distances map to lengths in a generic facility.

    :ivar facility_kind: A comment to describe this facility.
    :ivar facility_name: The name or description of the facility.
    """

    facility_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "FacilityKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    facility_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FacilityName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FiberFacilityMappingPart:
    """
    Relates distances measured along the optical path to specific lengths along
    facilities (wellbores or pipelines).

    :ivar comment: A descriptive remark about the facility mapping.
    :ivar facility_length_end: Distance between the facility datum and
        the distance where the mapping with the optical path ends.
    :ivar facility_length_start: Distance between the facility datum and
        the distance where the mapping with the optical path takes
        place.
    :ivar optical_path_distance_end: Distance between the beginning of
        the optical path to the distance where the mapping with the
        facility ends.
    :ivar optical_path_distance_start: Distance between the beginning of
        the optical path to the distance where the mapping with the
        facility takes place.
    :ivar fiber_facility:
    :ivar uid: Unique identifier or this object.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility_length_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "FacilityLengthEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    facility_length_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "FacilityLengthStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    optical_path_distance_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "OpticalPathDistanceEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    optical_path_distance_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "OpticalPathDistanceStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fiber_facility: Optional[AbstractFiberFacility] = field(
        default=None,
        metadata={
            "name": "FiberFacility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FiberFacilityWell(AbstractFiberFacility):
    """
    If facility mapping is to a wellbore, this element shows what optical path
    distances map to wellbore measured depths.

    :ivar name: The name of this facilityMapping instance.
    :ivar wellbore_reference:
    :ivar well_datum: A reference to the wellDatum from which the
        facilityLength (i.e., in this case, depth of a wellbore being
        mapped) is measured from.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    wellbore_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellboreReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    well_datum: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellDatum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FiberOneWayAttenuation:
    """The power loss for one-way travel of a beam of light, usually measured in
    decibels per unit length.

    It is necessary to include both the value (and its unit) and the
    wavelength at which this attenuation was measured.

    :ivar value: The value of the one-way loss per unit of length. The
        usual UOM is decibels per kilometer (dB/km) although this might
        vary depending on the calibration method used.
    :ivar attenuation_measure:
    :ivar uid: Unique identifier of this object.
    """

    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    attenuation_measure: Optional[AbstractAttenuationMeasure] = field(
        default=None,
        metadata={
            "name": "AttenuationMeasure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FiberPathDefect:
    """
    A zone of the fiber that has defective optical properties (e.g., darkening).

    :ivar comment: A descriptive remark about the defect found on this
        location.
    :ivar optical_path_distance_end: Ending point of the detected defect
        as distance in the optical path from the lightbox. if the defect
        is found at a specific location rather than a segment, then it
        can have the same value as the opticalPathDistanceStart.
    :ivar optical_path_distance_start: Starting point of the detected
        defect as distance in the optical path from the lightbox.
    :ivar time_end: Date when the defect was no longer detected (or was
        corrected).
    :ivar time_start: Date when the defect was detected.
    :ivar defect_type: Enum. The type of defect on the optical path.
    :ivar defect_id: The unique identifier of this object.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "sequence": 1,
        },
    )
    optical_path_distance_end: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OpticalPathDistanceEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "sequence": 1,
        },
    )
    optical_path_distance_start: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OpticalPathDistanceStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "sequence": 1,
        },
    )
    time_end: List[XmlDateTime] = field(
        default_factory=list,
        metadata={
            "name": "TimeEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "sequence": 1,
        },
    )
    time_start: List[XmlDateTime] = field(
        default_factory=list,
        metadata={
            "name": "TimeStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "sequence": 1,
        },
    )
    defect_type: List[PathDefectTypes] = field(
        default_factory=list,
        metadata={
            "name": "DefectType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "sequence": 1,
        },
    )
    defect_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "defectID",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class FluidAnalysisReport:
    """
    Fluid analysis report.

    :ivar analysis_laboratory: The laboratory that provided this fluid
        analysis report.
    :ivar author: The author of this fluid analysis report.
    :ivar report_date: The date of this report.
    :ivar report_document_reference: A reference to the report document,
        which will use the Energistics Attachment Object.
    :ivar report_identifier: The identifier of this fluid analysis
        report.
    :ivar report_location:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    analysis_laboratory: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AnalysisLaboratory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    author: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Author",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    report_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "ReportDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    report_document_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReportDocumentReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    report_identifier: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReportIdentifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    report_location: List[ReportLocation] = field(
        default_factory=list,
        metadata={
            "name": "ReportLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FluidCharacterizationTableColumn:
    """
    Column of a table.

    :ivar keyword_alias:
    :ivar phase:
    :ivar property: The property that this column contains. Enum. See
        output fluid property ext.
    :ivar fluid_component_reference: The  reference to a fluid component
        for this column in this fluid characterization table.
    :ivar name: The name for this column in this fluid characterization
        table.
    :ivar sequence: Index number for this column for consumption by an
        external system.
    :ivar uom: The UOM for this column in this fluid characterization
        table.
    """

    keyword_alias: List[str] = field(
        default_factory=list,
        metadata={
            "name": "KeywordAlias",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    phase: Optional[ThermodynamicPhase] = field(
        default=None,
        metadata={
            "name": "Phase",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    property: Optional[Union[OutputFluidProperty, str]] = field(
        default=None,
        metadata={
            "name": "Property",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fluid_component_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "fluidComponentReference",
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    sequence: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    uom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class FluidCharacterizationTableConstant:
    """
    The constant definition used in the table.

    :ivar keyword_alias:
    :ivar phase:
    :ivar property: The property that this table constant contains.
        Enum. See output fluid property ext.
    :ivar fluid_component_reference: Reference to the fluid component to
        which this value relates.
    :ivar name: User-defined name for this attribute.
    :ivar uom: The UOM for this constant for this fluid characterization
        table.
    :ivar value: The value for this table constant.
    """

    keyword_alias: List[str] = field(
        default_factory=list,
        metadata={
            "name": "KeywordAlias",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    phase: Optional[ThermodynamicPhase] = field(
        default=None,
        metadata={
            "name": "Phase",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    property: Optional[Union[OutputFluidProperty, str]] = field(
        default=None,
        metadata={
            "name": "Property",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fluid_component_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "fluidComponentReference",
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    uom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class FluidCharacterizationTableRow:
    """
    The row of a table.

    :ivar row: The string containing the contents of a row in the table.
    :ivar kind: This type characteristic describes the row of data as
        either saturated or under-saturated at the conditions defined
        for the row.
    """

    row: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    kind: Optional[SaturationKind] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class FluidSampleChainofCustodyEvent:
    """
    Fluid sample custody history event.

    :ivar container_location: The container location for this chain of
        custody event.
    :ivar current_container:
    :ivar custodian: The custodian for this chain of custody event.
    :ivar custody_date: The date for this chain of custody event.
    :ivar lost_volume: The lost volume of sample for this chain of
        custody event.
    :ivar prev_container:
    :ivar remaining_volume: The remaining volume of sample for this
        chain of custody event.
    :ivar remark: Remarks and comments about this data item.
    :ivar sample_integrity: The sample integrity for this chain of
        custody event. Enum. See sample quality.
    :ivar transfer_pressure: The transfer pressure for this chain of
        custody event.
    :ivar transfer_temperature: The transfer temperature for this chain
        of custody event.
    :ivar transfer_volume: The transfer volume for this chain of custody
        event.
    :ivar custody_action: The action for this chain of custody event.
        Enum. See sample action.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    container_location: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ContainerLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    current_container: Optional[str] = field(
        default=None,
        metadata={
            "name": "CurrentContainer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    custodian: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Custodian",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    custody_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "CustodyDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    lost_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LostVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    prev_container: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PrevContainer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remaining_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RemainingVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sample_integrity: Optional[SampleQuality] = field(
        default=None,
        metadata={
            "name": "SampleIntegrity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    transfer_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TransferPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    transfer_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TransferTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    transfer_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TransferVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    custody_action: Optional[SampleAction] = field(
        default=None,
        metadata={
            "name": "CustodyAction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FluidVolumeReference:
    """
    The reference uid to the fluid volume.

    :ivar reference_volume: The reference volume for this analysis.
    :ivar remark: Remarks and comments about this data item.
    :ivar kind: The kind of fluid volume references. Enum, see volume
        reference kind.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    reference_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReferenceVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: Optional[VolumeReferenceKind] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FormationWater(AbstractFluidComponent):
    """
    The water in the formation.

    :ivar remark: Remarks and comments about this data item.
    :ivar salinity: Salinity level.
    :ivar specific_gravity: Specific gravity.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    salinity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Salinity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    specific_gravity: Optional[float] = field(
        default=None,
        metadata={
            "name": "SpecificGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class Frequency(AbstractAttenuationMeasure):
    """
    Frequency.

    :ivar frequency: Frequency.
    """

    frequency: Optional[str] = field(
        default=None,
        metadata={
            "name": "Frequency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class GeneralAddress:
    """An general address structure.

    This form is appropriate for most countries.

    :ivar city: The city for the business associate's address.
    :ivar country: The country may be included. Although this is
        optional, it is probably required for most uses.
    :ivar county: The county, if applicable or necessary.
    :ivar name: The name line of an address. If missing, use the name of
        the business associate.
    :ivar postal_code: A postal code, if appropriate for the country. In
        the USA, this would be the five or nine digit zip code.
    :ivar province: Province.
    :ivar state: State.
    :ivar street: A generic term for the middle lines of an address.
        They may be a street address, PO box, suite number, or any lines
        that come between the "name" and "city" lines. This may be
        repeated for up to four, ordered lines.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    :ivar kind: The type of address: mailing, physical, or both. See
        AddressKindEnum.
    """

    city: Optional[str] = field(
        default=None,
        metadata={
            "name": "City",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    country: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Country",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    county: Optional[str] = field(
        default=None,
        metadata={
            "name": "County",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    postal_code: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PostalCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    province: Optional[str] = field(
        default=None,
        metadata={
            "name": "Province",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    state: Optional[str] = field(
        default=None,
        metadata={
            "name": "State",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    street: Optional[str] = field(
        default=None,
        metadata={
            "name": "Street",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
    kind: Optional[AddressKindEnum] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class GeneralQualifiedMeasure:
    """A measure which may have a quality status.

    The measure class (e.g., length) must be defined within the context
    of the usage of this type (e.g., in another element). This should
    not be used if the measure class will always be the same thing. If
    the 'status' attribute is absent and the value is not "NaN", the
    data value can be assumed to be good with no restrictions.

    :ivar component_reference: The kind of the value component. For
        example, "X" in a tuple of X and Y.
    :ivar uom: The unit of measure for the value. This value must
        conform to the values allowed by the measure class.
    :ivar status: An indicator of the quality of the value.
    """

    component_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "componentReference",
            "type": "Attribute",
        },
    )
    uom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    status: Optional[ValueStatus] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class GeologyFeature:
    """
    Geology features found in the location of the borehole string.

    :ivar name: Name of the feature.
    :ivar geology_type: Aquifer or reservoir.
    :ivar md_top: Measured depth at the top of the interval.
    :ivar md_bottom: Measured depth at the base of the interval.
    :ivar tvd_top:
    :ivar tvd_bottom:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    geology_type: Optional[GeologyType] = field(
        default=None,
        metadata={
            "name": "GeologyType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    md_top: Optional[MeasuredDepthCoord] = field(
        default=None,
        metadata={
            "name": "MdTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    md_bottom: Optional[MeasuredDepthCoord] = field(
        default=None,
        metadata={
            "name": "MdBottom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tvd_top: Optional[WellVerticalDepthCoord] = field(
        default=None,
        metadata={
            "name": "TvdTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tvd_bottom: Optional[WellVerticalDepthCoord] = field(
        default=None,
        metadata={
            "name": "TvdBottom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class Injection:
    """
    Volume injected per reporting entity.

    :ivar remark: A descriptive remark relating to any significant
        events.
    :ivar injection_quantity:
    :ivar quantity_method: The method in which the quantity/volume was
        determined. See enum QuantityMethod.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    injection_quantity: List[AbstractProductQuantity] = field(
        default_factory=list,
        metadata={
            "name": "InjectionQuantity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    quantity_method: Optional[Union[QuantityMethod, str]] = field(
        default=None,
        metadata={
            "name": "QuantityMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class IntegerQualifiedCount:
    """An integer which may have a quality status.

    If the 'status' attribute is absent and the value is not "NaN", the
    data value can be assumed to be good with no restrictions.

    :ivar status: An indicator of the quality of the value.
    """

    status: Optional[ValueStatus] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class InterfacialTensionTest:
    """
    The interfacial tension test.

    :ivar remark: Remarks and comments about this data item.
    :ivar surfactant: The surfactant for this interfacial tension test.
    :ivar test_number: An integer number to identify this test in a
        sequence of tests.
    :ivar interfacial_tension_test_step:
    :ivar wetting_phase: The wetting phase for this interfacial tension
        test.
    :ivar non_wetting_phase: The non-wetting phase for this interfacial
        tension test.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    surfactant: Optional[AbstractFluidComponent] = field(
        default=None,
        metadata={
            "name": "Surfactant",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    interfacial_tension_test_step: List[InterfacialTensionTestStep] = field(
        default_factory=list,
        metadata={
            "name": "InterfacialTensionTestStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wetting_phase: Optional[ThermodynamicPhase] = field(
        default=None,
        metadata={
            "name": "WettingPhase",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    non_wetting_phase: Optional[ThermodynamicPhase] = field(
        default=None,
        metadata={
            "name": "nonWettingPhase",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class InterventionConveyance(AbstractCable):
    """
    Information on type of intervention conveyance used by the optical path.

    :ivar comment: Comment about the intervention conveyance.
    :ivar intervention_conveyance_type: The type from the enumeration
        list of InterventionConveyanceType.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    intervention_conveyance_type: Optional[InterventionConveyanceType] = field(
        default=None,
        metadata={
            "name": "InterventionConveyanceType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class KeywordValueStruct:
    """A value for the specified keyword.

    That is, a keyword-value pair. The allowed length of the value is
    constrained by the keyword.

    :ivar keyword: The keyword within which the value is unique. The
        concept of a keyword is very close to the concept of a
        classification system.
    """

    keyword: Optional[TimeSeriesKeyword] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class KindQualifiedString:
    """A kind which may have a quality status.

    If the 'status' attribute is absent and the value is not "NaN", the
    data value can be assumed to be good with no restrictions.

    :ivar status: An indicator of the quality of the value.
    """

    status: Optional[ValueStatus] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class LiquidComposition:
    """
    The composition of liquid.

    :ivar remark: Remarks and comments about this data item.
    :ivar liquid_component:
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_component: List[FluidComponent] = field(
        default_factory=list,
        metadata={
            "name": "LiquidComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class LiquidDropoutFraction(AbstractLiquidDropoutPercVolume):
    """
    The fraction of liquid by volume.

    :ivar liquid_dropout_percent: The fraction of liquid by volume for
        this test step.
    """

    liquid_dropout_percent: Optional[str] = field(
        default=None,
        metadata={
            "name": "LiquidDropoutPercent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class LiquidVolume(AbstractLiquidDropoutPercVolume):
    """
    The amount of liquid by volume.

    :ivar liquid_volume: The amount of liquid by volume for this test
        step.
    """

    liquid_volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "LiquidVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class Location:
    """Location Component Schema.

    This is a location that is expressed in terms of 2D coordinates. In
    order that the location be understood, the coordinate reference
    system (CRS) must be known. The survey location is given by a pair
    of tagged values. The pairs may be: (1) latitude/longitude, (2)
    easting/northing, (3) westing/southing, (4) projectedX/projectedY,
    or (5) localX/localY. The appropriate pair must be chosen for the
    data.

    :ivar description: A comment, generally given to help the reader
        interpret the coordinates if the CRS and the chosen pair do not
        make them clear.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar original: Flag indicating (if "true" or "1") that this pair of
        values was the original data given for the location. If the pair
        of values was calculated from an original pair of values, this
        flag should be "false" (or "0"), or not present.
    :ivar well_crs: A pointer to the wellCRS that defines the CRS for
        the coordinates. While optional, it is strongly recommended that
        this be specified.
    :ivar abstract_location:
    """

    description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    original: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Original",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_crs: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellCRS",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    abstract_location: Optional[AbstractLocation] = field(
        default=None,
        metadata={
            "name": "AbstractLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class LostVolumeAndReason:
    """
    A volume corrected to standard temperature and pressure.

    :ivar reason_lost: Defines why the volume was lost.
    """

    reason_lost: Optional[ReasonLost] = field(
        default=None,
        metadata={
            "name": "reasonLost",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MassBalance:
    """
    The balance sheet of mass.

    :ivar mass_balance_fraction: The mass balance fraction for this slim
        tube test volume step.
    :ivar remark: Remarks and comments about this data item.
    :ivar mass_in:
    :ivar mass_out:
    """

    mass_balance_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassBalanceFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mass_in: Optional[MassIn] = field(
        default=None,
        metadata={
            "name": "MassIn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mass_out: Optional[MassOut] = field(
        default=None,
        metadata={
            "name": "MassOut",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class NaturalGas(AbstractFluidComponent):
    """
    Natural gas.

    :ivar gas_gravity: Gas gravity.
    :ivar gross_energy_content_per_unit_mass: The amount of heat
        released during the combustion of a specified amount of gas. It
        is also known as higher heating value (HHV), gross energy, upper
        heating value, gross calorific value (GCV) or higher calorific
        Value (HCV). This value takes into account the latent heat of
        vaporization of water in the combustion products, and is useful
        in calculating heating values for fuels where condensation of
        the reaction products is practical.
    :ivar gross_energy_content_per_unit_volume: The amount of heat
        released during the combustion of a specified amount of gas. It
        is also known as higher heating value (HHV), gross energy, upper
        heating value, gross calorific value (GCV) or higher calorific
        value (HCV). This value takes into account the latent heat of
        vaporization of water in the combustion products, and is useful
        in calculating heating values for fuels where condensation of
        the reaction products is practical.
    :ivar molecular_weight: Molecular weight.
    :ivar net_energy_content_per_unit_mass: The amount of heat released
        during the combustion of a specified amount of gas. It is also
        known as lower heating value (LHV), net energy, net calorific
        value (NCV) or lower calorific value (LCV). This value ignores
        the latent heat of vaporization of water in the combustion
        products, and is useful in calculating heating values for fuels
        where condensation of the reaction products is not possible and
        is ignored.
    :ivar net_energy_content_per_unit_volume: The amount of heat
        released during the combustion of a specified amount of gas. It
        is also known as lower heating value (LHV), net energy, net
        calorific value (NCV) or lower calorific value (LCV). This value
        ignores the latent heat of vaporization of water in the
        combustion products, and is useful in calculating heating values
        for fuels where condensation of the reaction products is not
        possible and is ignored.
    :ivar remark: Remarks and comments about this data item.
    """

    gas_gravity: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gross_energy_content_per_unit_mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GrossEnergyContentPerUnitMass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gross_energy_content_per_unit_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GrossEnergyContentPerUnitVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    net_energy_content_per_unit_mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "NetEnergyContentPerUnitMass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    net_energy_content_per_unit_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "NetEnergyContentPerUnitVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class OffshoreLocation:
    """A generic type of offshore location.

    This allows an offshore location to be given by an area name, and up
    to four block names. A comment is also allowed.

    :ivar area_name: A general meaning of area. It may be as general as
        'UK North Sea' or 'Viosca Knoll'. The user community must agree
        on the meaning of this element.
    :ivar block_id: A block ID that can more tightly locate the object.
        The BlockID should be an identifying name or code. The user
        community for an area must agree on the exact meaning of this
        element. An aggregate of increasingly specialized block IDs are
        sometimes necessary to define the location.
    :ivar comment: An general comment that further explains the offshore
        location.
    :ivar north_sea_offshore:
    """

    area_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AreaName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    block_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "BlockID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    north_sea_offshore: Optional[NorthSeaOffshore] = field(
        default=None,
        metadata={
            "name": "NorthSeaOffshore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class OilCompressibility:
    """
    Oil compressibility.

    :ivar kind: The kind of measurement for oil compressibility.
    """

    kind: Optional[CompressibilityKind] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class OilShrinkageFactor(AbstractOilVolShrinkage):
    """
    Oil shrinkage factor.

    :ivar oil_shrinkage_factor: The oil shrinkage factor.
    """

    oil_shrinkage_factor: Optional[str] = field(
        default=None,
        metadata={
            "name": "OilShrinkageFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class OilVolume(AbstractOilVolShrinkage):
    """
    Oil volume.

    :ivar oil_volume: The volume of oil.
    """

    oil_volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "OilVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class OtherMeasurementTestStep:
    """
    Other measurement test step.

    :ivar gas_gravity: The gas gravity at this test step.
    :ivar gas_mass_density: The gas density at this test step.
    :ivar gas_viscosity: The viscosity of the gas phase at this test
        step.
    :ivar gas_zfactor: The gas Z factor value at this test step.
    :ivar oil_mass_density: The oil mass density for this test step.
    :ivar oil_viscosity: The viscosity of the oil phase at this test
        step.
    :ivar remark: Remarks and comments about this data item.
    :ivar rsw: The rsw for this test step.
    :ivar salinity: The salinity for this test step.
    :ivar shear: The shear for this test step.
    :ivar step_number: The step number is the index of a (P,T) step in
        the overall test.
    :ivar step_pressure: The pressure for this test step.
    :ivar step_temperature: The temperature for this test step.
    :ivar water_content: The water content for this test step.
    :ivar water_viscosity: The water viscosity for this test step.
    :ivar fluid_condition: The fluid condition at this test step. Enum,
        see fluid analysis step condition.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    gas_gravity: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_mass_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasMassDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_zfactor: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasZFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_mass_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilMassDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    rsw: Optional[float] = field(
        default=None,
        metadata={
            "name": "Rsw",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    salinity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Salinity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    shear: Optional[float] = field(
        default=None,
        metadata={
            "name": "Shear",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    step_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StepPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StepTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_content: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterContent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_condition: Optional[FluidAnalysisStepCondition] = field(
        default=None,
        metadata={
            "name": "FluidCondition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class OverallComposition:
    """
    Overall composition.

    :ivar remark: Remarks and comments about this data item.
    :ivar fluid_component:
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_component: List[FluidComponent] = field(
        default_factory=list,
        metadata={
            "name": "FluidComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class Parentfacility(AbstractRefProductFlow):
    """
    Parent facility.

    :ivar parentfacility_reference: A reference to a flow within the
        current product volume report. This represents a foreign key
        from one element to another.
    """

    parentfacility_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "ParentfacilityReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class PermanentCable(AbstractCable):
    """
    Information on the type of permanent conveyance used by the optical path.

    :ivar comment: Comment about the intervention conveyance.
    :ivar permanent_cable_installation_type: Enum. For permanent
        conveyance option, the type of conveyance. Example: clamped to
        tubular.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    permanent_cable_installation_type: Optional[
        PermanentCableInstallationType
    ] = field(
        default=None,
        metadata={
            "name": "PermanentCableInstallationType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class PhoneNumberStruct:
    """A phone number with two attributes, used to "type" and "qualify" a phone
    number.

    The type would carry information such as fax, modem, voice, and the
    qualifier would carry information such as home or office.

    :ivar extension: The phone number extension.
    :ivar type_value: The kind of phone such as voice or fax.
    :ivar qualifier: Indicates whether the number is personal, business
        or both.
    :ivar content:
    """

    extension: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: Optional[PhoneType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    qualifier: Optional[AddressQualifier] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class PlusFluidComponent(AbstractFluidComponent):
    """
    Plus fluid component.

    :ivar avg_density: The average density of the fluid.
    :ivar avg_molecular_weight: The average molecular weight of the
        fluid.
    :ivar remark: Remarks and comments about this data item.
    :ivar specific_gravity: The fluid specific gravity.
    :ivar starting_boiling_point: The starting boiling temperature
        measure.
    :ivar starting_carbon_number: The start/min carbon number.
    :ivar kind: The kind from plus fluid component. See
        PlusComponentEnum.
    """

    avg_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AvgDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    avg_molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AvgMolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    specific_gravity: Optional[float] = field(
        default=None,
        metadata={
            "name": "SpecificGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    starting_boiling_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StartingBoilingPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    starting_carbon_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StartingCarbonNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: Optional[Union[PlusComponentEnum, str]] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class ProductFlowExternalPort:
    """
    Product Flow Network External Port Schema.

    :ivar comment: A descriptive remark about the port.
    :ivar connected_node: Defines the internal node to which this
        external port is connected. All ports (whether internal or
        external) that are connected to a node with the same name are
        connected to each other. Node names are unique to each network.
        The purpose of the external port is to provide input to or
        output from the internal network except when the port is an
        "exposed" port. The purpose of an exposed port is to allow the
        properties of the port to be seen external to the network. For
        an exposed port, the connection points to the associated port.
    :ivar direction: Defines whether this port is an inlet or outlet.
        Note that this is a nominal intended direction.
    :ivar exposed: True ("true" or "1") indicates that the port is an
        exposed internal port and cannot be used in a connection
        external to the network. False ("false" or "0") or not given
        indicates a normal port.
    :ivar name: The name of the external port within the context of the
        current product flow network.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    connected_node: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConnectedNode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    direction: Optional[ProductFlowPortType] = field(
        default=None,
        metadata={
            "name": "Direction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    exposed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Exposed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductFlowNetworkPlan:
    """
    A plan to extend an actual network.

    :ivar dtim_start: The date and time of the start of the plan. This
        point coincides with the end of the actual configuration. The
        configuration of the actual at this point in time represents the
        configuration of the plan at this starting point. All changes to
        this plan must be in the future from this point in time.
    :ivar name: The name assigned to the plan.
    :ivar purpose: A textual description of the purpose of the plan.
    :ivar change_log: Documents that a change occurred at a particular
        time.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    dtim_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    purpose: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Purpose",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    change_log: List[ProductFlowChangeLog] = field(
        default_factory=list,
        metadata={
            "name": "ChangeLog",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductFlowQualifierExpected(ExpectedFlowQualifier):
    """
    Defines an expected combination of kinds.

    :ivar flow: The expected kind of flow.
    :ivar product: The expected kind of product within the flow.
    :ivar qualifier: The expected kind of qualifier of the flow.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    flow: Optional[ReportingFlow] = field(
        default=None,
        metadata={
            "name": "Flow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    product: Optional[ReportingProduct] = field(
        default=None,
        metadata={
            "name": "Product",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    qualifier: List[FlowQualifier] = field(
        default_factory=list,
        metadata={
            "name": "Qualifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductRate:
    """
    The production rate of the product.

    :ivar mass_flow_rate: Mass flow rate.
    :ivar product_fluid_reference: String UID pointer to the
        productFluid in the fluidComponentSet.
    :ivar remark: Remarks and comments about this data item.
    :ivar volume_flow_rate: Volume flow rate.
    :ivar product_fluid_kind: Information about the product that the
        product quantity represents. See enum ProductFluidKind (in the
        ProdmlCommon package).
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    mass_flow_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassFlowRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    product_fluid_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProductFluidReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    volume_flow_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VolumeFlowRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    product_fluid_kind: Optional[Union[ProductFluidKind, str]] = field(
        default=None,
        metadata={
            "name": "ProductFluidKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductVolumeBalanceEvent:
    """
    Captures information about an event related to a product balance.

    :ivar date: The date of the event.
    :ivar kind: The kind of event.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    kind: Optional[BalanceEventKind] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductVolumeBusinessSubUnit:
    """
    Product volume schema for defining ownership shares of business units.

    :ivar kind: Points to business unit which is part of another
        business unit.
    :ivar ownership_business_acct:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    ownership_business_acct: Optional[OwnershipBusinessAcct] = field(
        default=None,
        metadata={
            "name": "OwnershipBusinessAcct",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductVolumeDestination:
    """
    Product Flow Sales Destination Schema.

    :ivar country: The country of the destination.
    :ivar name: The name of the destination.
    :ivar type_value: The type of destination.
    """

    country: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Country",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    type_value: Optional[BalanceDestinationType] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class ProductVolumeParameterValue:
    """
    Parameter Value Schema.

    :ivar dtim: The date and time at which the parameter applies. If no
        time is specified then the value is static.
    :ivar dtim_end: The date and time at which the parameter no longer
        applies. The "active" time interval is inclusive of this point.
        If dTimEnd is given then dTim shall also be given.
    :ivar port: A port related to the parameter. If a port is given then
        the corresponding unit usually must be given. For example, an
        "offset along network" parameter must specify a port from which
        the offset was measured.
    :ivar unit: A unit related to the parameter. For example, an "offset
        along network" parameter must specify a port (on a unit) from
        which the offset was measured.
    :ivar measure_data_type:
    :ivar alert: An indication of some sort of abnormal condition
        relative this parameter.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    dtim: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    port: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Port",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    unit: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    measure_data_type: List[AbstractMeasureDataType] = field(
        default_factory=list,
        metadata={
            "name": "MeasureDataType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )
    alert: Optional[ProductVolumeAlert] = field(
        default=None,
        metadata={
            "name": "Alert",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductVolumeRelatedFacility:
    """A second facility related to this flow.

    For a production flow, this would represent a role of 'produced
    for'. For an import flow, this would represent a role of 'import
    from'. For an export flow, this would represent a role of 'export
    to'.

    :ivar kind: A kind of facility where the specific name is not
        relevant.
    :ivar related_facility_object:
    """

    kind: Optional[ReportingFacility] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    related_facility_object: Optional[AbstractRelatedFacilityObject] = field(
        default=None,
        metadata={
            "name": "RelatedFacilityObject",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class Production:
    """
    Product volume that is produce from a reporting entity.

    :ivar remark: Remarks and comments about this data item.
    :ivar production_quantity:
    :ivar quantity_method: The method in which the quantity/volume was
        determined. See enum QuantityMethod.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    production_quantity: List[AbstractProductQuantity] = field(
        default_factory=list,
        metadata={
            "name": "ProductionQuantity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    quantity_method: Optional[Union[QuantityMethod, str]] = field(
        default=None,
        metadata={
            "name": "QuantityMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class ProductionOperationCargoShipOperation:
    """
    Information about an operation involving a cargo ship.

    :ivar bsw: Basic sediment and water is measured from a liquid sample
        the production stream. It includes free water, sediment and
        emulsion and is measured as a volume percentage of the liquid.
    :ivar captain: Name of the captain of the vessel.
    :ivar cargo: Description of cargo on the vessel.
    :ivar cargo_batch_number: The cargo batch number. Used if the vessel
        needs to temporarily disconnect for some reason (e.g., weather).
    :ivar cargo_number: The cargo identifier.
    :ivar comment: A commnet about the operation.
    :ivar density: Density of the liquid loaded to the tanker.
    :ivar density_std_temp_pres: Density of the liquid loaded to the
        tanker. This density has been corrected to standard conditions
        of temperature and pressure.
    :ivar dtim_end: The date and time that the vessel left.
    :ivar dtim_start: The date and time that the vessel arrived.
    :ivar oil_gross_std_temp_pres: Gross oil loaded to the ship during
        the report period. Gross oil includes BS and W. This volume has
        been corrected to standard conditions of temperature and
        pressure.
    :ivar oil_gross_total_std_temp_pres: Gross oil loaded to the ship in
        total during the operation. Gross oil includes BS and W. This
        volume has been corrected to standard conditions of temperature
        and pressure.
    :ivar oil_net_month_to_date_std_temp_pres: Net oil loaded to the
        ship from the beginning of the month to the end of the reporting
        period. Net oil excludes BS and W, fuel, spills, and leaks. This
        volume has been corrected to standard conditions of temperature
        and pressure.
    :ivar oil_net_std_temp_pres: Net oil loaded to the ship during the
        report period. Net oil excludes BS and W, fuel, spills, and
        leaks. This volume has been corrected to standard conditions of
        temperature and pressure.
    :ivar rvp: Reid vapor pressure of the liquid.
    :ivar salt: Salt content. The product formed by neutralization of an
        acid and a base. The term is more specifically applied to sodium
        chloride.
    :ivar vessel_name: Name of the cargo vessel.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    bsw: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Bsw",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    captain: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Captain",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cargo: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Cargo",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cargo_batch_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "CargoBatchNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cargo_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CargoNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    comment: List[DatedComment] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Density",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    density_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DensityStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_gross_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilGrossStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_gross_total_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilGrossTotalStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_net_month_to_date_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilNetMonthToDateStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_net_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilNetStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    rvp: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Rvp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    salt: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Salt",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vessel_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VesselName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionOperationMarineOperation:
    """
    Information about a marine operation.

    :ivar activity: A comment on a special event in the marine area.
    :ivar basket_movement: Report of any basket movement to and from the
        installation.
    :ivar dtim_end: The ending date and time that the comment
        represents.
    :ivar dtim_start: The beginning date and time that the comment
        represents.
    :ivar general_comment: A general comment on marine activity in the
        area.
    :ivar standby_vessel: Name of the standby vessel for the
        installation.
    :ivar standby_vessel_comment: Comment regarding the standby vessel.
    :ivar supply_ship: Name of the supply vessel for the installation.
    :ivar supply_ship_comment: Comment regarding the supply ship.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    activity: List[DatedComment] = field(
        default_factory=list,
        metadata={
            "name": "Activity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    basket_movement: List[DatedComment] = field(
        default_factory=list,
        metadata={
            "name": "BasketMovement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    general_comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GeneralComment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    standby_vessel: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StandbyVessel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    standby_vessel_comment: List[DatedComment] = field(
        default_factory=list,
        metadata={
            "name": "StandbyVesselComment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    supply_ship: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SupplyShip",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    supply_ship_comment: List[DatedComment] = field(
        default_factory=list,
        metadata={
            "name": "SupplyShipComment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionOperationOperationalComment:
    """
    Operational Comments Schema.

    :ivar comment: A comment about the operation and/or the activities
        within the operation.
    :ivar dtim_end: The ending date and time that the comment
        represents.
    :ivar dtim_start: The beginning date and time that the comment
        represents.
    :ivar type_value: The kind of operation.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    type_value: Optional[OperationKind] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionOperationWaterCleaningQuality:
    """Information about the contaminants in water, and the general water quality.

    The values are measured from a sample, which is described below.
    Values measured from other samples should be given in different
    instances of the type.

    :ivar ammonium: The amount of ammonium found in the water sample.
    :ivar amount_of_oil: Total measured oil in the water after the water
        cleaning process, but before it is discharged from the
        installation
    :ivar comment: Any comment that may be useful in describing the
        water quality. There can be multiple comments.
    :ivar coulter_counter: A measure of the number of particles in water
        as measured by a coulter counter.
    :ivar glycol: The amount of glycol found in the water sample.
    :ivar oil_in_water_produced: Total measured oil in the water after
        the water cleaning process, but before it is discharged from the
        installation.
    :ivar oxygen: Total measured oxygen in the water after the water
        cleaning process, but before it is discharged from the
        installation.
    :ivar phenol: The amount of phenol found in the water sample.
    :ivar ph_value: The pH value of the treated water. The pH value is
        best given as a value, with no unit of measure, since there are
        no variations from the pH.
    :ivar residual_chloride: Total measured residual chlorides in the
        water after the water cleaning process, but before it is
        discharged from the installation.
    :ivar sample_point: An identifier of the point from which the sample
        was taken. This is an uncontrolled string value, which should be
        as descriptive as possible.
    :ivar total_organic_carbon: The amount of total organic carbon found
        in the water. The water is under high temperature and the carbon
        left is measured.
    :ivar turbidity: A measure of the cloudiness of water caused by
        suspended particles.
    :ivar water_temperature: The temperature of the water before it is
        discharged.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    ammonium: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Ammonium",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    amount_of_oil: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AmountOfOil",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    comment: List[DatedComment] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    coulter_counter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CoulterCounter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    glycol: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Glycol",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_in_water_produced: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilInWaterProduced",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oxygen: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Oxygen",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    phenol: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Phenol",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    ph_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PhValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    residual_chloride: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ResidualChloride",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sample_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SamplePoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_organic_carbon: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalOrganicCarbon",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    turbidity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Turbidity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class PseudoFluidComponent(AbstractFluidComponent):
    """
    Pseudo fluid component.

    :ivar avg_boiling_point: The average boiling point measure.
    :ivar avg_density: The average fluid density.
    :ivar avg_molecular_weight: Average molecular weight.
    :ivar ending_boiling_point: The ending boiling point measure.
    :ivar ending_carbon_number: The ending / largest carbon number.
    :ivar remark: Remarks and comments about this data item.
    :ivar specific_gravity: The fluid specific gravity.
    :ivar starting_boiling_point: The starting boiling point measure.
    :ivar starting_carbon_number: The starting / smalestl carbon number.
    :ivar kind: The type from pseudo component enumeration.
    """

    avg_boiling_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AvgBoilingPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    avg_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AvgDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    avg_molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AvgMolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    ending_boiling_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EndingBoilingPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    ending_carbon_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EndingCarbonNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    specific_gravity: Optional[float] = field(
        default=None,
        metadata={
            "name": "SpecificGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    starting_boiling_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StartingBoilingPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    starting_carbon_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StartingCarbonNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: Optional[Union[PseudoComponentEnum, str]] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class PureFluidComponent(AbstractFluidComponent):
    """
    Pure fluid component.

    :ivar hydrocarbon_flag: Yes/no  flag indicates if hydrocarbon or
        not.
    :ivar molecular_weight: The molecular weight of the pure component.
    :ivar remark: Remarks and comments about this data item.
    :ivar kind: The type of component.
    """

    hydrocarbon_flag: Optional[bool] = field(
        default=None,
        metadata={
            "name": "HydrocarbonFlag",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: Optional[Union[PureComponentEnum, str]] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class PvtModelParameter:
    """
    PVT model parameter.

    :ivar name: The  user-defined name of a parameter, which can be
        added to any model.
    :ivar kind: The kind of model parameter. Extensible enum.  See PVT
        model parameter kind ext.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    kind: Optional[Union[PvtModelParameterKind, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Qualifier(ExpectedFlowQualifier):
    """
    :ivar qualifier: The expected kind of qualifier of the property.
        This element should only be specified for properties that do not
        represent the fluid stream (e.g., a valve status).
    """

    qualifier: List[FlowQualifier] = field(
        default_factory=list,
        metadata={
            "name": "Qualifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class ReferenceFlow(AbstractRefProductFlow):
    """
    Reference flow.

    :ivar flow_reference: A pointer to the flow within the facility.
    """

    flow_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class StoflashedLiquid:
    """
    Stock tank oil flashed liquid properties and composition.

    :ivar asphaltene_content: The asphaltene content of the liquid phase
        of the stock tank analysis.
    :ivar astmflash_point: The ASTM flash point of the liquid phase of
        the stock tank analysis.
    :ivar cloud_point: The cloud point of the liquid phase of the stock
        tank analysis.
    :ivar elemental_sulfur: The elemental sulfur content of the liquid
        phase of the stock tank analysis.
    :ivar iron: The iron content of the liquid phase of the stock tank
        analysis.
    :ivar lead: The lead content of the liquid phase of the stock tank
        analysis.
    :ivar nickel: The nickel content of the liquid phase of the stock
        tank analysis.
    :ivar nitrogen: The nitrogen content of the liquid phase of the
        stock tank analysis.
    :ivar oil_apigravity: Oil API gravity.
    :ivar paraffin_content: The paraffin content of the liquid phase of
        the stock tank analysis.
    :ivar pour_point: The pour point of the liquid phase of the stock
        tank analysis.
    :ivar reid_vapor_pressure: The reid vapor pressure of the liquid
        phase of the stock tank analysis.
    :ivar total_acid_number: The total acid number of the liquid phase
        of the stock tank analysis.
    :ivar total_sulfur: The total sulfur content of the liquid phase of
        the stock tank analysis.
    :ivar vanadium: The vanadium content of the liquid phase of the
        stock tank analysis.
    :ivar water_content: The water content of the liquid phase of the
        stock tank analysis.
    :ivar watson_kfactor: The Watson K factor of the liquid phase of the
        stock tank analysis.
    :ivar wax_appearance_temperature: The wax appearance temperature of
        the liquid phase of the stock tank analysis.
    :ivar sara:
    :ivar viscosity_at_temperature: The viscosity at test temperature of
        the liquid phase of the stock tank analysis.
    """

    class Meta:
        name = "STOFlashedLiquid"

    asphaltene_content: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AsphalteneContent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    astmflash_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ASTMFlashPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cloud_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CloudPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    elemental_sulfur: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ElementalSulfur",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    iron: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Iron",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    lead: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Lead",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    nickel: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Nickel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    nitrogen: Optional[str] = field(
        default=None,
        metadata={
            "name": "Nitrogen",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    oil_apigravity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilAPIGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    paraffin_content: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ParaffinContent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pour_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PourPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reid_vapor_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReidVaporPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_acid_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalAcidNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_sulfur: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalSulfur",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vanadium: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Vanadium",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_content: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterContent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    watson_kfactor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WatsonKFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wax_appearance_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaxAppearanceTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sara: List[Sara] = field(
        default_factory=list,
        metadata={
            "name": "Sara",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    viscosity_at_temperature: List[ViscosityAtTemperature] = field(
        default_factory=list,
        metadata={
            "name": "ViscosityAtTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class SafetyCount:
    """
    A zero-based count of a type of safety item.

    :ivar period: The type of period being reported by this count.
    :ivar type_value: The type of safety issue for which a count is
        being defined.
    """

    period: Optional[ReportingDurationKind] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: Optional[SafetyType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass
class SaturationPressure:
    """
    Saturation pressure.

    :ivar kind: The kind of saturation point whose pressure is being
        measured. Enum. See saturationpointkind.
    """

    kind: Optional[SaturationPointKind] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class SaturationTemperature:
    """
    Saturation temperature.

    :ivar kind: The kind of saturation point whose temperature is being
        measured. Enum. See saturationpointkind.
    """

    kind: Optional[SaturationPointKind] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ServiceFluid(AbstractProductQuantity):
    """
    Service fluid (e.g., biocides, lubricants, etc.) being reported on.

    :ivar service_fluid_kind: Indicates the kind of service fluid. See
        enum ServiceFluidKind (in ProdmlCommon).
    :ivar service_fluid_reference: String ID that points to a service
        fluid in the FluidComponentSet.
    """

    service_fluid_kind: Optional[Union[ServiceFluidKind, str]] = field(
        default=None,
        metadata={
            "name": "ServiceFluidKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    service_fluid_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "serviceFluidReference",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StartEndDate(AbstractDateTimeType):
    """
    The start and end date for a reporting period.

    :ivar date_end: The ending date that the period represents.
    :ivar date_start: The beginning date that the period represents.
    """

    date_end: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "DateEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    date_start: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "DateStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class StartEndTime(AbstractDateTimeType):
    """
    Start and end time of a reporting period.

    :ivar dtim_end: The ending date and time that the period represents.
    :ivar dtim_start: The beginning date and time that the period
        represents.
    """

    dtim_end: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_start: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class StockTankOil(AbstractFluidComponent):
    """
    Stock tank oil (STO).

    :ivar apigravity: API gravity.
    :ivar gross_energy_content_per_unit_mass: The amount of heat
        released during the combustion of a specified amount of STO. It
        is also known as higher heating value (HHV), gross energy, upper
        heating value, gross calorific value (GCV) or higher calorific
        value (HCV). This value takes into account the latent heat of
        vaporization of water in the combustion products, and is useful
        in calculating heating values for fuels where condensation of
        the reaction products is practical.
    :ivar gross_energy_content_per_unit_volume: The amount of heat
        released during the combustion of a specified amount of STO. It
        is also known as higher heating value (HHV), gross energy, upper
        heating value,  gross calorific value (GCV) or higher calorific
        value (HCV). This value takes into account the latent heat of
        vaporization of water in the combustion products, and is useful
        in calculating heating values for fuels where condensation of
        the reaction products is practical.
    :ivar molecular_weight: Molecular weight.
    :ivar net_energy_content_per_unit_mass: The amount of heat released
        during the combustion of a specified amount of STO. It is also
        known as lower heating value (LHV), net energy, lower heating
        value, net calorific value  (NCV) or lower calorific value
        (LCV). This value ignores the latent heat of vaporization of
        water in the combustion products, and is useful in calculating
        heating values for fuels where condensation of the reaction
        products is not possible and is ignored.
    :ivar net_energy_content_per_unit_volume: The amount of heat
        released during the combustion of a specified amount of STO. It
        is also known as lower heating value  (LHV), net energy, net
        calorific value (NCV) or lower calorific value (LCV). This value
        ignores the latent heat of vaporization of water in the
        combustion products, and is useful in calculating heating values
        for fuels where condensation of the reaction products is not
        possible and is ignored.
    :ivar remark: Remarks and comments about this data item.
    """

    apigravity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "APIGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gross_energy_content_per_unit_mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GrossEnergyContentPerUnitMass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gross_energy_content_per_unit_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GrossEnergyContentPerUnitVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    net_energy_content_per_unit_mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "NetEnergyContentPerUnitMass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    net_energy_content_per_unit_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "NetEnergyContentPerUnitVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class StringValue(AbstractValue):
    """
    A single string value in the time series.

    :ivar string_value: A single string value in the time series.
    """

    string_value: Optional[TimeSeriesStringSample] = field(
        default=None,
        metadata={
            "name": "StringValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class TimeSeriesDoubleSample:
    """
    A single double value in a time series.

    :ivar d_tim: The date and time at which the value applies. If no
        time is specified then the value is static and only one sample
        can be defined. Either dTim or value or both must be specified.
        If the status attribute is absent and the value is not "NaN",
        the data value can be assumed to be good with no restrictions.
    :ivar status: An indicator of the quality of the value.
    """

    d_tim: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "dTim",
            "type": "Attribute",
        },
    )
    status: Optional[ValueStatus] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class VaporComposition:
    """
    Vapor composition.

    :ivar remark: Remarks and comments about this data item.
    :ivar vapor_component:
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_component: List[FluidComponent] = field(
        default_factory=list,
        metadata={
            "name": "VaporComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class VolumeQualifiedMeasure:
    """A volume flow rate which may have a quality status.

    If the 'status' attribute is absent and the value is not "NaN", the
    data value can be assumed to be good with no restrictions.

    :ivar status: An indicator of the quality of the value.
    """

    status: Optional[ValueStatus] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class WaterAnalysisTest:
    """
    Water analysis test.

    :ivar liquid_gravity: The liquid gravity for the water analysis
        test.
    :ivar ph: The ph for the water analysis test.
    :ivar remark: Remarks and comments about this data item.
    :ivar resistivity: The resistivity for the water analysis test.
    :ivar salinity: The salinity for the water analysis test.
    :ivar test_number: An integer number to identify this test in a
        sequence of tests.
    :ivar total_dissolved_solids: The total dissolved solids for the
        water analysis test.
    :ivar total_hardness: The total water hardness for the water
        analysis test.
    :ivar total_suspended_solids: The total suspended solids for the
        water analysis test.
    :ivar water_analysis_test_step: The name of the Fluid Analysis
        Result.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    liquid_gravity: Optional[float] = field(
        default=None,
        metadata={
            "name": "LiquidGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    ph: Optional[float] = field(
        default=None,
        metadata={
            "name": "PH",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    resistivity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Resistivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    salinity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Salinity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    total_dissolved_solids: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalDissolvedSolids",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_hardness: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalHardness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_suspended_solids: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalSuspendedSolids",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_analysis_test_step: List[WaterAnalysisTestStep] = field(
        default_factory=list,
        metadata={
            "name": "WaterAnalysisTestStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class WaveLength(AbstractAttenuationMeasure):
    """
    Wave length.

    :ivar wave_length: Wave length.
    """

    wave_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "WaveLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class WellTestBottomholeData:
    """
    Well test data gathered at the bottomhole.

    :ivar bottomhole_md: The measured depth of the bottomhole.
    :ivar bottomhole_pover_z: The P/Z value at the bottomhole. This is
        P/Z, pressure over gas compressibility factor (z), at the
        bottomhole of the well. Note that the UOM is units of pressure,
        because Z is dimensionless.
    :ivar bottomhole_pres: The pressure at the bottomhole of the well.
    :ivar bottomhole_temp: The temperature at the bottomhole of the
        well.
    :ivar wellbore_reference: Defines the wellbore (sidetract)
        represented by the measured depth. This must be given when the
        well has multiple wellbores and the measured depth value is
        deeper than the first kickoff point. It is recommended that it
        always be given.
    """

    bottomhole_md: Optional[MeasuredDepthCoord] = field(
        default=None,
        metadata={
            "name": "BottomholeMD",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bottomhole_pover_z: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BottomholePOverZ",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bottomhole_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BottomholePres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bottomhole_temp: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BottomholeTemp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellbore_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellboreReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WellTestFluidLevelTest(AbstractWellTest):
    """
    Information about fluid levels achieved/observed during a test.

    :ivar base_usable_water: The lowest usable water depth as measured
        from the surface. See TxRRC H-15.
    :ivar fluid_level: The fluid level achieved in the well. The value
        is given as length units from the top of the well.
    :ivar tested_by: The business associate that conducted the test.
        This is generally a person.
    """

    base_usable_water: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BaseUsableWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_level: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidLevel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    tested_by: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestedBy",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WellTestInterval:
    """
    Information about the interval in the wellbore where the well test was
    conducted.

    :ivar md_base: The measured depth to the bottom of the interval.
    :ivar md_top: The measured depth to the top of the interval.
    :ivar tested_formation: The formation that was tested.
    :ivar valve_position: The relative opening of the downhole control
        valve for the tested zone. This is for surface controllable
        valves.
    :ivar wellbore_reference: Defines the wellbore (sidetract)
        represented by the measured depth. This must be given when the
        well has multiple wellbores and the measured depth value is
        deeper than the first kickoff point. It is recommended that it
        always be given.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    md_base: Optional[MeasuredDepthCoord] = field(
        default=None,
        metadata={
            "name": "MdBase",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    md_top: Optional[MeasuredDepthCoord] = field(
        default=None,
        metadata={
            "name": "MdTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    tested_formation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestedFormation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    valve_position: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ValvePosition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellbore_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellboreReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class WellTestPointData:
    """
    Well test data gathered at a point in the wellbore.

    :ivar bottomhole: A value of true (1 or "true") indicates that the
        point is at the bottomhole. A value of false (0 or "false") or
        not given indicates otherwise.
    :ivar md: The measured depth of the point being tested.
    :ivar pover_z: The P/Z value at the point. This is P/Z, pressure
        over gas compressibility factor (z). Note that the UOM is units
        of pressure., because Z is dimensionless.
    :ivar pres: The pressure at the point.
    :ivar static: A value of true (1 or "true") indicates a static (non-
        flowing) pressure. A value of false (0 or "false") or not given
        indicates otherwise. The pressure may be measured (e.g., shut-in
        well) or calculated.
    :ivar temp: The temperature at the point.
    :ivar wellbore_reference: Defines the wellbore (sidetract)
        represented by the measured depth. This must be given when the
        well has multiple wellbores and the measured depth value is
        deeper than the first kickoff point. It is recommended that it
        always be given.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    bottomhole: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Bottomhole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    md: Optional[MeasuredDepthCoord] = field(
        default=None,
        metadata={
            "name": "Md",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pover_z: List[str] = field(
        default_factory=list,
        metadata={
            "name": "POverZ",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Pres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    static: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Static",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    temp: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Temp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellbore_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellboreReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class WellTestProductionTestResults:
    """Oil, gas, and water volumes and rates measured during the well test.

    The volumes allow either actual volumes or standard (corrected)
    volumes. The densities are also recorded with the volumes.

    :ivar allocated_split: True ("true" or "1") indicates that the split
        factors are allocated as opposed to measured. False ("false" or
        "0") or not given indicates otherwise.
    :ivar basic_sediment_and_water: This is the measured of impurities
        present in crude oil as it comes from the well. BSandW content
        is commonly used as a measure for treating performance of
        hydrocarbon liquids
    :ivar condensate_split_factor: The split factor for condensate
        relative to the overall volume of the test.
    :ivar condensate_yield: This is the condensate yield, which
        describes the amount of condensate per unit of natural gas
        produced
    :ivar density: The density of the fluid mixture.
    :ivar fluid_velocity: The velocity of the overall fluid mixture.
    :ivar gas_oil_ratio: The ratio of the volume of gas and the volume
        of oil that was produced.
    :ivar gas_potential: This is the potential of the well to produce
        natural gas. This represents the flow rate that could be
        achieved under maximum drawdown.
    :ivar gas_split_factor: The split factor for gas relative to the
        overall volume of the test.
    :ivar oil_potential: This is the potential of the well to produce
        crude oil. This represents the flow rate that could be achieved
        under maximum drawdown.
    :ivar oil_split_factor: The split factor for oil relative to the
        overall volume of the test.
    :ivar productivity_index: Productivity index (PI) is an expression
        which defines the pressure drop in the reservoir to produce a
        unit of oil per day. That is, the energy to produce a unit of
        oil. The value was defined at ambient temperature and pressure.
    :ivar productivity_index_std_temp_pres: Productivity index (PI) is
        an expression which defines the pressure drop in the reservoir
        to produce a unit of oil per day. That is, the energy to produce
        a unit of oil. The value has been converted to the declared
        conditions of standard temperature and pressure.
    :ivar sand_volume: The volume of sand that was produced.
    :ivar water_cut: The ratio of water produced compared to the volume
        of total liquids produced.
    :ivar water_split_factor: The split factor for water relative to the
        overall volume of the test.
    :ivar oil_rate: Oil rates measured during the well test.
    :ivar water_rate: Water rates measured during the well test.
    :ivar gas_rate: Gas rates measured during the well test.
    :ivar condensate_rate: Condensate rates measured during the well
        test.
    :ivar water_volume: Water volumes measured during the well test.
    :ivar condensate_volume: condensate volumes measured during the well
        test.
    :ivar oil_volume: Oil volumes measured during the well test.
    :ivar gas_volume: Gas volumes measured during the well test.
    """

    allocated_split: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AllocatedSplit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    basic_sediment_and_water: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BasicSedimentAndWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    condensate_split_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CondensateSplitFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    condensate_yield: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CondensateYield",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Density",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_velocity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FluidVelocity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_oil_ratio: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasOilRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_potential: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasPotential",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_split_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasSplitFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_potential: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilPotential",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_split_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilSplitFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    productivity_index: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProductivityIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    productivity_index_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProductivityIndexStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sand_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SandVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_cut: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterCut",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_split_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterSplitFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_rate: Optional[WellTestFluidRate] = field(
        default=None,
        metadata={
            "name": "OilRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_rate: Optional[WellTestFluidRate] = field(
        default=None,
        metadata={
            "name": "WaterRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_rate: Optional[WellTestFluidRate] = field(
        default=None,
        metadata={
            "name": "GasRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    condensate_rate: Optional[WellTestFluidRate] = field(
        default=None,
        metadata={
            "name": "CondensateRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_volume: Optional[WellTestTestVolume] = field(
        default=None,
        metadata={
            "name": "WaterVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    condensate_volume: Optional[WellTestTestVolume] = field(
        default=None,
        metadata={
            "name": "CondensateVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_volume: Optional[WellTestTestVolume] = field(
        default=None,
        metadata={
            "name": "OilVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_volume: Optional[WellTestTestVolume] = field(
        default=None,
        metadata={
            "name": "GasVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WellTestValidationOperation:
    """
    The validation operation of a well test.

    :ivar date: The date of the validation operation.
    :ivar method: The method used for the validation operation..
    :ivar remark: A comment about the operation.
    :ivar tool: The tool used for the validation operation.
    :ivar kind: The kind of validation operation. See enum
        ValidationOperation.
    :ivar result: The result of the validation operation. See enum
        ValidationResult.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    method: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Method",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tool: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Tool",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: Optional[ValidationOperation] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    result: Optional[ValidationResult] = field(
        default=None,
        metadata={
            "name": "Result",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class WellTestWellheadData:
    """
    Basic measurements at the wellhead, during the well test.

    :ivar choke_orifice_size: The size of the choke opening at the
        wellhead.
    :ivar flowing_pressure: The flowing pressure measured at the
        wellhead during the well test.
    :ivar flow_line_pressure: The pressure measured at the flow line
        connected to the wellhead during this well test.
    :ivar gas_liftchoke_orifice_size: The size of the gas lift choke
        opening.
    :ivar gas_lift_pres: The pressure of the lift gas at the wellhead.
    :ivar gas_lift_temp: The temperature of the lift gas at the
        wellhead.
    :ivar shut_in_pressure: The shut-in pressure measured at the
        wellhead during the well test.
    :ivar temperature: The temperature measured at the wellhead during
        the well test.
    :ivar gas_lift_rate: Lift gas rates injected during the well test at
        the wellhead.
    :ivar gas_lift_volume: Lift gas volumes injected during the well
        test at the wellhead.
    """

    choke_orifice_size: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ChokeOrificeSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flowing_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlowingPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flow_line_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlowLinePressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_liftchoke_orifice_size: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasLiftchokeOrificeSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_lift_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasLiftPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_lift_temp: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasLiftTemp",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    shut_in_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ShutInPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Temperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_lift_rate: Optional[WellTestFluidRate] = field(
        default=None,
        metadata={
            "name": "GasLiftRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_lift_volume: Optional[WellTestTestVolume] = field(
        default=None,
        metadata={
            "name": "GasLiftVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WftEvent:
    """
    Captures information about an event that occurred.

    :ivar dtim: Date and time of the start of the event.
    :ivar duration: The time duration of the event.
    :ivar remark: A comment about the event.
    :ivar kind: The kind of event. See enum WftEventKind.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    dtim: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    duration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: Optional[WftEventKind] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class WftInOutParameter:
    """
    Defines a parameter which may have been used for input or output depending on
    the parent node.

    :ivar measure_class: The kind of the measure. For example, "length".
        If the value requires a unit of measure, this must be specified.
    :ivar name: The name of the parameter.
    :ivar value: The value of the parameter. If the value represents a
        measure, then the UOM attribute and the corresponding
        measureClass must be specified.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    measure_class: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MeasureClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    value: Optional[MeasureOrQuantity] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class BusinessAssociate:
    """Describes any company, person, group, consultant, etc., which is associated
    within a context (e.g., a well).

    The information contained in this module is: (1) contact information, such as address, phone numbers, email, (2) alternate name, or aliases, and (3) associations, such as the business associate that this one is associated with, or a contact who is associated with this business associate.

    :ivar associated_with: A pointer to another business associate that
        this business associate is associated with. The most common
        situation is that of an employee being associated with a
        company. But it may also be, for example, a work group
        associated with a university.
    :ivar contact: A pointer to a business associate (generally a
        person) who serves as a contact for this business associate.
    :ivar name: Name of the business associate.
    :ivar personnel_count: The count of personnel in a group.
    :ivar email: The email address may be home, office, or permanent.
        More than one may be given.
    :ivar address: The business address.
    :ivar role: The role of the business associate within the context.
        For example, "driller" or "operator", "lead agency - CEQA
        compliance" "regulatory contact", "safety contact". A business
        associate generally has one role but the role may be called
        different things in different naming systems.
    :ivar alias: An alternate name of a business associate. It is
        generally associated with a naming system. An alias is not
        necessarily unique within the naming system.
    :ivar person_name:
    :ivar phone_number: Various types of phone numbers may be given.
        They may be office or home, they may be a number for a cell
        phone, or for a fax, etc. Attributes of PhoneNumber declare the
        type of phone number that is being given.
    """

    associated_with: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AssociatedWith",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    contact: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Contact",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    personnel_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "PersonnelCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    email: List[EmailQualifierStruct] = field(
        default_factory=list,
        metadata={
            "name": "Email",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    address: Optional[GeneralAddress] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    role: List[NameStruct] = field(
        default_factory=list,
        metadata={
            "name": "Role",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    alias: List[NameStruct] = field(
        default_factory=list,
        metadata={
            "name": "Alias",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    person_name: Optional[PersonName] = field(
        default=None,
        metadata={
            "name": "PersonName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    phone_number: List[PhoneNumberStruct] = field(
        default_factory=list,
        metadata={
            "name": "PhoneNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class ConstantCompositionExpansionTestStep:
    """
    The CCE test steps.

    :ivar gas_compressibility: The gas compressibility at this test
        step.
    :ivar gas_density: The gas density at the conditions for this
        viscosity correlation to be used.
    :ivar gas_viscosity: The viscosity of the gas phase at this test
        step.
    :ivar gas_zfactor: The gas Z factor value at this test step.
    :ivar liquid_composition: The liquid composition at this test step.
    :ivar oil_density: The density of the oil phase at this test step.
    :ivar oil_viscosity: The viscosity of the oil phase at this test
        step.
    :ivar overall_composition: The overall composition at this test
        step.
    :ivar phases_present: The phases present at this test step (oil,
        water, gas etc.). Enum, see phases present.
    :ivar remark: Remarks and comments about this data item.
    :ivar step_number: The step number is the index of a (P,T) step in
        the overall test.
    :ivar step_pressure: The pressure for this test step.
    :ivar total_volume: The total volume of the expanded mixture at this
        test step.
    :ivar vapor_composition: The vapor composition at this test step.
    :ivar yfunction: The Y function at this test step. See  Standing,
        M.B.: Volumetric And Phase Behavior Of Oil Field Hydrocarbon
        Systems, Eighth Edition, SPE Richardson, Texas (1977).
    :ivar fluid_condition: The fluid condition at this test step. Enum,
        see fluid analysis step condition.
    :ivar oil_compressibility: The oil compressibility at this test
        step.
    :ivar liquid_fraction: The fraction of liquid by volume for this
        test step.
    :ivar relative_volume_ratio: Measured relative volume ratio =
        measured volume/volume at Psat.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    gas_compressibility: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasCompressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_zfactor: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasZFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_composition: Optional[LiquidComposition] = field(
        default=None,
        metadata={
            "name": "LiquidComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    overall_composition: Optional[OverallComposition] = field(
        default=None,
        metadata={
            "name": "OverallComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    phases_present: Optional[str] = field(
        default=None,
        metadata={
            "name": "PhasesPresent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    step_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    total_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_composition: Optional[VaporComposition] = field(
        default=None,
        metadata={
            "name": "VaporComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    yfunction: Optional[float] = field(
        default=None,
        metadata={
            "name": "YFunction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_condition: Optional[FluidAnalysisStepCondition] = field(
        default=None,
        metadata={
            "name": "FluidCondition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_compressibility: Optional[OilCompressibility] = field(
        default=None,
        metadata={
            "name": "OilCompressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_fraction: Optional[RelativeVolumeRatio] = field(
        default=None,
        metadata={
            "name": "LiquidFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    relative_volume_ratio: Optional[RelativeVolumeRatio] = field(
        default=None,
        metadata={
            "name": "RelativeVolumeRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class DasCalibration:
    """This object contains a mapping of loci-to-fiber distance along the optical
    path for the DAS acquisition.

    The actual calibration points are provided in an array of DasCalibrationPoint structures consisting of three elements: a locus index, the corresponding fiber distance, and a description of the calibration type. Provide as many calibration points as necessary.

    :ivar calibration_datum: Datum used as basis for measurement of
        calibration point distance and length.
    :ivar calibration_description: Free format description of the DAS
        calibration provided for an instance of a DAS acquisition.
    :ivar calibration_facility_length_unit: Unit of measurement of
        FacilityLength value CalibrationPoints
    :ivar calibration_index: The nth count of this Calibration in the
        Acquisition.  Recommended if there is more than 1 Calibration in
        this Acquisition.  This index corresponds to the Calibration
        array number in the H5 file.
    :ivar calibration_optical_path_distance_unit: Unit of measurement of
        OpticalPathDistance value CalibrationPoints
    :ivar facility_name: Indicates which facility is being calibrated.
    :ivar number_of_calibration_points: The total number of calibration
        points in the array.
    :ivar calibration_data_points:
    :ivar facility_kind: Enumeration to indicate the type of facility
        (well or pipeline) for this acquisition.
    """

    calibration_datum: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CalibrationDatum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    calibration_description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CalibrationDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    calibration_facility_length_unit: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CalibrationFacilityLengthUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    calibration_index: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CalibrationIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    calibration_optical_path_distance_unit: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CalibrationOpticalPathDistanceUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FacilityName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    number_of_calibration_points: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumberOfCalibrationPoints",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    calibration_data_points: List[DasCalibrationPoint] = field(
        default_factory=list,
        metadata={
            "name": "CalibrationDataPoints",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )
    facility_kind: Optional[FacilityKind] = field(
        default=None,
        metadata={
            "name": "FacilityKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DasFbe:
    """This object contains the attributes of FBE processed data.

    This includes the FBE data unit, location of the FBE data along the
    fiber optical path, information about times, (optional) filter
    related parameters, and UUIDs of the original raw and/or spectra
    files from which the files were processed. Note that the actual FBE
    data samples and times arrays are not present in the XML files but
    only in the HDF5 files because of their size. The XML files only
    contain references to locate the corresponding HDF files containing
    the actual FBE samples and times.

    :ivar fbe_data_unit: Data unit for the FBE data.
    :ivar fbe_description: Description of the FBE data.
    :ivar fbe_index: The nth count of this Fbe instance in the
        Acquisition.  Recommended if there is more than 1 Fbe instance
        in this Acquisition.  This index corresponds to the Fbe array
        number in the H5 file.
    :ivar filter_type: A string describing the type of filter applied by
        the vendor. Important frequency type filter classes are:
        frequency response filters (low-pass, high-pass, band-pass,
        notch filters) and butterworth, chebyshev and bessel filters.
        The filter type and characteristics applied to the acquired or
        processed data is important information for end-user
        applications.
    :ivar number_of_loci: The total number of ‘loci’ (acoustic sample
        points) acquired by the measurement instrument in a single
        ‘scan’ of the fiber.
    :ivar output_data_rate: The rate at which the FBE data is provided
        for all ‘loci’ (spatial samples). This is typically equal to the
        interrogation rate/pulse rate of the DAS measurement system or
        an integer fraction thereof. Note this attribute is mandatory
        for FBE and spectrum data. For raw data this attribute is
        optional.
    :ivar raw_reference: A universally unique identifier (UUID) for the
        HDF file containing the raw data.
    :ivar spatial_sampling_interval: The separation between two
        consecutive ‘spatial sample’ points on the fiber at which the
        signal is measured. It should not be confused with ‘spatial
        resolution’. If this data element is present in the DASFbe
        object, then it overwrites the SpatialSamplingInterval value
        described in DASAcquistion.
    :ivar spatial_sampling_interval_unit: Only required in Hdf5 file to
        record the unit of measure of the sampling interval of the Fbe.
    :ivar spectra_reference: A universally unique identifier (UUID) for
        the HDF file containing the spectra data.
    :ivar start_locus_index: The first ‘locus’ acquired by the
        interrogator unit, where ‘Locus Index 0’ is the acoustic sample
        point at the connector of the measurement instrument.
    :ivar transform_size: The number of samples used in the
        TransformType.
    :ivar transform_type: A string describing the type of mathematical
        transformation applied by the vendor. Typically this is some
        type of discrete fast Fourier transform (often abbreviated as
        DFT, DFFT or FFT).
    :ivar window_function: The window function applied to the sample
        window used to calculate the frequency band. Example 'HANNING',
        'HAMMING', 'BESSEL' window.
    :ivar window_overlap: The number of sample overlaps between
        consecutive filter windows applied.
    :ivar window_size: The number of samples in the filter window
        applied.
    :ivar custom:
    :ivar fbe_data: A DAS array object containing the FBE DAS data.
    :ivar fbe_data_time: A DAS array object containing the sample times
        corresponding to a single ‘scan’ of the fiber. In a single
        ‘scan’, the DAS measurement system acquires raw data samples for
        all the loci specified by StartLocusIndex and NumberOfLoci. The
        ‘scan’ frequency is equal to the DAS acquisition pulse rate.
    :ivar uuid: A universally unique identifier (UUID) of an instance of
        FBE DAS data.
    """

    fbe_data_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "FbeDataUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fbe_description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FbeDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fbe_index: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FbeIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    filter_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FilterType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    number_of_loci: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumberOfLoci",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    output_data_rate: Optional[str] = field(
        default=None,
        metadata={
            "name": "OutputDataRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    raw_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RawReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    spatial_sampling_interval: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SpatialSamplingInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    spatial_sampling_interval_unit: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SpatialSamplingIntervalUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    spectra_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SpectraReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    start_locus_index: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartLocusIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    transform_size: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TransformSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    transform_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TransformType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    window_function: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WindowFunction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    window_overlap: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WindowOverlap",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    window_size: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WindowSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    custom: Optional[DasCustom] = field(
        default=None,
        metadata={
            "name": "Custom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fbe_data: List[DasFbeData] = field(
        default_factory=list,
        metadata={
            "name": "FbeData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )
    fbe_data_time: Optional[DasTimeArray] = field(
        default=None,
        metadata={
            "name": "FbeDataTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DasRaw:
    """This object contains the attributes of raw data acquired by the DAS
    measurement instrument.

    This includes the raw data unit, the location of the raw data
    acquired along the fiber optical path, and information about times
    and (optional) triggers. Note that the actual raw data samples,
    times and trigger times arrays are not present in the XML files but
    only in the HDF5 files because of their size. The XML files only
    contain references to locate the corresponding HDF files, which
    contain the actual raw samples, times, and (optional) trigger times.

    :ivar number_of_loci: The total number of ‘loci’ (acoustic sample
        points) acquired by the measurement instrument in a single
        ‘scan’ of the fiber.
    :ivar output_data_rate: The rate at which the spectra data is
        provided for all ‘loci’ (spatial samples). This is typically
        equal to the interrogation rate/pulse rate of the DAS
        measurement system or an integer fraction thereof. This
        attribute is optional in the Raw Data object. If present, it
        overrides the Acquisition PulseRate. If not present, then
        OutputDataRate is assumed equal to the PulseRate.
    :ivar raw_data_unit: Data unit for the DAS measurement instrument.
    :ivar raw_description: Free format description of the raw DAS data
        acquired.
    :ivar raw_index: The nth count of this Raw instance in the
        Acquisition.  Recommended if there is more than 1 Raw instance
        in this Acquisition.  This index corresponds to the Raw array
        number in the H5 file.
    :ivar start_locus_index: The first ‘locus’ acquired by the
        interrogator unit. Where ‘Locus Index 0’ is the acoustic sample
        point at the connector of the measurement instrument.
    :ivar custom:
    :ivar raw_data: A DAS array object containing the raw DAS data.
    :ivar raw_data_time: A DAS array object containing the sample times
        corresponding to a single ‘scan’ of the fiber. In a single
        ‘scan’, the DAS measurement system acquires raw data samples for
        all the loci specified by StartLocusIndex . The ‘scan’ frequency
        is equal to the DAS Acquisition Pulse Rate.
    :ivar raw_data_trigger_time: A DAS array object containing the times
        of the triggers in a triggered measurement. Multiple times may
        be stored to indicate multiple triggers within a single DAS raw
        data recording. This array contains only valid data if
        TriggeredMeasurement is set to ‘true’ in DAS Acquisition.
    :ivar uuid: A universally unique identifier (UUID) for an instance
        of raw DAS data.
    """

    number_of_loci: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumberOfLoci",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    output_data_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OutputDataRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    raw_data_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "RawDataUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    raw_description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RawDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    raw_index: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RawIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    start_locus_index: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartLocusIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    custom: Optional[DasCustom] = field(
        default=None,
        metadata={
            "name": "Custom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    raw_data: Optional[DasRawData] = field(
        default=None,
        metadata={
            "name": "RawData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    raw_data_time: Optional[DasTimeArray] = field(
        default=None,
        metadata={
            "name": "RawDataTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    raw_data_trigger_time: Optional[DasTimeArray] = field(
        default=None,
        metadata={
            "name": "RawDataTriggerTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DasSpectra:
    """This object contains the attributes of spectra processed data.

    This includes the spectra data unit, location of the spectra data
    along the fiber optical path, information about times, (optional)
    filter related parameters, and UUIDs of the original raw from which
    the spectra file was processed and/or the UUID of the FBE files that
    were processed from the spectra files. Note that the actual spectrum
    data samples and times arrays are not present in the XML files but
    only in the HDF5 files because of their size. The XML files only
    contain references to locate the corresponding HDF files containing
    the actual spectrum samples and times.

    :ivar fbe_reference: A universally unique identifier (UUID) of an
        instance of DAS FBE data.
    :ivar filter_type: A string describing the type of filter applied by
        the vendor. Important frequency type filter classes are:
        frequency response filters (low-pass, high-pass, band-pass,
        notch filters) and butterworth, chebyshev and bessel filters.
        The filter type and characteristics applied to the acquired or
        processed data is important information for end-user
        applications.
    :ivar number_of_loci: The total number of ‘loci’ (acoustic sample
        points) acquired by the measurement instrument in a single
        ‘scan’ of the fiber.
    :ivar output_data_rate: The rate at which the spectra data is
        provided for all ‘loci’ (spatial samples). This is typically
        equal to the interrogation rate/pulse rate of the DAS
        measurement system or an integer fraction thereof. Note this
        attribute is mandatory for FBE and spectrum data. For raw data
        this attribute is optional.
    :ivar raw_reference: Unique identifier for the HDF5 file containing
        the raw data.
    :ivar spatial_sampling_interval: The separation between two
        consecutive ‘spatial sample’ points on the fiber at which the
        signal is measured. It should not be confused with ‘spatial
        resolution’. If this data element is present in the DasSpectrum
        object, then it overwrites the SpatialSamplingInterval value
        described in DasAcquistion.
    :ivar spatial_sampling_interval_unit: Only required in an HDF5 file
        to record the unit of measure of the sampling interval of the
        spectra.
    :ivar spectra_data_unit: Data unit for the spectra data.
    :ivar spectra_description: Description of the spectra data.
    :ivar spectra_index: The nth count of this Spectra instance in the
        acquisition. Recommended if there is more than 1 Spectra
        instance in this acquisition.  This index corresponds to the
        Spectra array number in the H5 file.
    :ivar start_locus_index: The first ‘locus’ acquired by the
        interrogator unit, where ‘Locus Index 0’ is the acoustic sample
        point at the connector of the measurement instrument.
    :ivar transform_size: The number of samples used in the
        TransformType.
    :ivar transform_type: A string describing the type of mathematical
        transformation applied by the vendor. Typically this is some
        type of discrete fast Fourier transform (often abbreviated as
        DFT, DFFT or FFT).
    :ivar window_function: A string describing the window function
        applied by the vendor. Examples are "Hamming" or "Hanning".
    :ivar window_overlap: The number of sample overlaps between
        consecutive filter windows applied.
    :ivar window_size: The number of samples in the filter window
        applied.
    :ivar custom:
    :ivar spectra_data: A DAS array object containing the spectra DAS
        data.
    :ivar spectra_data_time: A DAS array object containing the sample
        times corresponding to a single ‘scan’ of the fiber. In a single
        ‘scan’, the DAS measurement system acquires raw data samples for
        all the loci specified by StartLocusIndex and NumberOfLoci. The
        ‘scan’ frequency is equal to the DAS acquisition pulse rate.
    :ivar uuid: A universally unique identifier (UUID) for an instance
        of spectra DAS data.
    """

    fbe_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FbeReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    filter_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FilterType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    number_of_loci: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumberOfLoci",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    output_data_rate: Optional[str] = field(
        default=None,
        metadata={
            "name": "OutputDataRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    raw_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RawReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    spatial_sampling_interval: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SpatialSamplingInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    spatial_sampling_interval_unit: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SpatialSamplingIntervalUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    spectra_data_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpectraDataUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    spectra_description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SpectraDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    spectra_index: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SpectraIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    start_locus_index: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartLocusIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    transform_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransformSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    transform_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransformType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    window_function: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WindowFunction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    window_overlap: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WindowOverlap",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    window_size: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WindowSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    custom: Optional[DasCustom] = field(
        default=None,
        metadata={
            "name": "Custom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    spectra_data: Optional[DasSpectraData] = field(
        default=None,
        metadata={
            "name": "SpectraData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    spectra_data_time: Optional[DasTimeArray] = field(
        default=None,
        metadata={
            "name": "SpectraDataTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DeferredProductionEvent:
    """
    Information about the event or incident that caused production to be deferred.

    :ivar duration: The duration of the event.
    :ivar end_date: The end date of the event.
    :ivar start_date: The start date of the event.
    :ivar deferred_production:
    :ivar downtime_reason_code: The reason code for the downtime event.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    duration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    end_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "EndDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    start_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "StartDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    deferred_production: List[DeferredProduction] = field(
        default_factory=list,
        metadata={
            "name": "DeferredProduction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    downtime_reason_code: Optional[DowntimeReasonCode] = field(
        default=None,
        metadata={
            "name": "DowntimeReasonCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class DoubleValue(AbstractValue):
    """
    A single double value in the time series.

    :ivar double_value: A single double value in the time series.
    """

    double_value: Optional[TimeSeriesDoubleSample] = field(
        default=None,
        metadata={
            "name": "DoubleValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DtsInterpretationLogSet:
    """
    Container of interpreted data which also specifies by reference the measured
    data on which the interpretation is based.

    :ivar preferred_interpretation_reference: For a set of
        dtsInterpretedData logs that are generated from the same
        measurement (each log having gone through a different post-
        processing type, for example), if there is one log that is
        ‘preferred’ for additional business decisions (while the other
        ones were merely what-if scenarios), then this preferred log in
        the collection of child dtsInterpretedData can be flagged by
        referencing its UID with this element.
    :ivar interpretation_data:
    """

    preferred_interpretation_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PreferredInterpretationReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    interpretation_data: List[DtsInterpretationData] = field(
        default_factory=list,
        metadata={
            "name": "InterpretationData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class FacilityParent(AbstractRelatedFacilityObject):
    """
    Facility parent.

    :ivar facility_parent1: For facilities whose name is unique within
        the context of another facility, the name of the parent
        facility. The name can be qualified by a naming system. This
        also defines the kind of facility.
    :ivar facility_parent2: For facilities whose name is unique within
        the context of another facility, the name of the parent facility
        of parent1. The name can be qualified by a naming system. This
        also defines the kind of facility.
    :ivar name: The name of the facility. The name can be qualified by a
        naming system. This can also define the kind of facility.
    """

    facility_parent1: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "FacilityParent1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility_parent2: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "FacilityParent2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FiberFacilityMapping:
    """Relates lengths of fiber to corresponding lengths of facilities (probably
    wellbores or pipelines).

    The facilityMapping also contains the datum from which the
    InterpretedData is indexed.

    :ivar comment: A descriptive remark about the facility mapping.
    :ivar time_end: Date when the mapping between the facility and the
        optical path is no longer valid.
    :ivar time_start: Date when the mapping between the facility and the
        optical path becomes effective.
    :ivar fiber_facility_mapping_part: Relates distances measured along
        the optical path to specific lengths along facilities (wellbores
        or pipelines).
    :ivar uid: Unique identifier of this object.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    time_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "TimeEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    time_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "TimeStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fiber_facility_mapping_part: List[FiberFacilityMappingPart] = field(
        default_factory=list,
        metadata={
            "name": "FiberFacilityMappingPart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
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
class FiberFacilityPipeline(AbstractFiberFacility):
    """
    If facility mapping is to a pipeline, this element shows what optical path
    distances map to pipeline lengths.

    :ivar context_facility: The name and type of a facility whose
        context is relevant to the represented installation.
    :ivar datum_port_reference: A description of which "port" (i.e.,
        connection/end or defined point on a pipeline) the
        facilityLength is indexed from.
    :ivar installation: The name of the facility that is represented by
        this facilityMapping.
    :ivar kind: The kind of facility mapped to the optical path.
        Expected to be a pipeline, but this element can be used to show
        other facilities being mapped to fiber length in future.
    :ivar name: The name of this facilityMapping instance.
    """

    context_facility: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "ContextFacility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    datum_port_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DatumPortReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    installation: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "Installation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: Optional[NameStruct] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FlashedGas:
    """
    Flashed gas.

    :ivar gas_gravity: The gas gravity of the flashed gas in this
        atmospheric flash test.
    :ivar gas_heating_value: The gas molecular weight of the flashed gas
        in this atmospheric flash test.
    :ivar gas_molecular_weight: The molecular weight of the gas phase at
        this test step.
    :ivar gas_zfactor: The gas Z factor value at this test step.
    :ivar vapor_composition: The vapor composition of the flashed gas in
        this atmospheric flash test.
    """

    gas_gravity: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_heating_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasHeatingValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasMolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_zfactor: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasZFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_composition: Optional[VaporComposition] = field(
        default=None,
        metadata={
            "name": "VaporComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FlashedLiquid:
    """
    Flashed liquid.

    :ivar liquid_composition: The oil API gravity of the flashed liquid
        in this atmospheric flash test.
    :ivar oil_apigravity: The oil molecular weight of the flashed liquid
        in this atmospheric flash test.
    :ivar oil_molecular_weight: The liquid composition of the flashed
        liquid in this atmospheric flash test.
    """

    liquid_composition: Optional[LiquidComposition] = field(
        default=None,
        metadata={
            "name": "LiquidComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_apigravity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilAPIGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilMolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FluidCharacterizationTable:
    """
    Fluid characterization table.

    :ivar remark: Remarks and comments about this data item.
    :ivar table_constant: A constant associated with this fluid
        characterization table.
    :ivar table_row:
    :ivar name: The name of this table.
    :ivar table_format: The uid reference of the table format for this
        table.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    table_constant: List[FluidCharacterizationTableConstant] = field(
        default_factory=list,
        metadata={
            "name": "TableConstant",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    table_row: List[FluidCharacterizationTableRow] = field(
        default_factory=list,
        metadata={
            "name": "TableRow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    table_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "tableFormat",
            "type": "Attribute",
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
class FluidCharacterizationTableFormat:
    """
    Fluid characterization table format.

    :ivar null_value: The null value for this fluid characterization
        table format.
    :ivar table_column:
    :ivar delimiter: The delimiter for this fluid characterization table
        format.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    null_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "NullValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    table_column: List[FluidCharacterizationTableColumn] = field(
        default_factory=list,
        metadata={
            "name": "TableColumn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )
    delimiter: Optional[TableDelimiter] = field(
        default=None,
        metadata={
            "name": "Delimiter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FluidComponentCatalog:
    """
    Fluid component catalog.

    :ivar formation_water: Formation water.
    :ivar natural_gas: Natural gas.
    :ivar plus_fluid_component: Plus-fluid component.
    :ivar pseudo_fluid_component: Pseudo-fluid component.
    :ivar pure_fluid_component: Pure fluid component.
    :ivar stock_tank_oil: Stock tank oil.
    """

    formation_water: List[FormationWater] = field(
        default_factory=list,
        metadata={
            "name": "FormationWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    natural_gas: List[NaturalGas] = field(
        default_factory=list,
        metadata={
            "name": "NaturalGas",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    plus_fluid_component: List[PlusFluidComponent] = field(
        default_factory=list,
        metadata={
            "name": "PlusFluidComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pseudo_fluid_component: List[PseudoFluidComponent] = field(
        default_factory=list,
        metadata={
            "name": "PseudoFluidComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pure_fluid_component: List[PureFluidComponent] = field(
        default_factory=list,
        metadata={
            "name": "PureFluidComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    stock_tank_oil: List[StockTankOil] = field(
        default_factory=list,
        metadata={
            "name": "StockTankOil",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FluidCvdTestStep:
    """
    The CVD test steps.

    :ivar cumulative_fluid_produced_fraction: The cumulative fluid
        produced (molar) fraction at this test step.
    :ivar gas_formation_volume_factor: The gas formation volume factor
        at this test step.
    :ivar gas_gravity: The gas gravity at this test step.
    :ivar gas_molecular_weight: The molecular weight of the gas phase at
        this test step.
    :ivar gas_viscosity: The viscosity of the gas phase at this test
        step.
    :ivar gas_zfactor: The gas Z factor value at this test step.
    :ivar liquid_composition: The liquid composition at this test step.
    :ivar oil_density: The density of the oil phase at this test step.
    :ivar oil_viscosity: The viscosity of the oil phase at this test
        step.
    :ivar overall_composition: The overall composition at this test
        step.
    :ivar phase2_zfactor: The standard Z = PV/RT, but here for a two-
        phase Z-factor, use total molar volume for both phases.
    :ivar phases_present: The phases present at this test step.
    :ivar remark: Remarks and comments about this data item.
    :ivar step_number: The step number is the index of a (P,T) step in
        the overall test.
    :ivar step_pressure: The pressure for this test step.
    :ivar vapor_composition: The vapor composition at this test step.
    :ivar fluid_condition: The fluid condition at this test step. Enum,
        see fluid analysis step condition.
    :ivar liquid_fraction: The fraction of liquid by volume for this
        test step.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    cumulative_fluid_produced_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CumulativeFluidProducedFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_formation_volume_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasFormationVolumeFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_gravity: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasMolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_zfactor: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasZFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_composition: Optional[LiquidComposition] = field(
        default=None,
        metadata={
            "name": "LiquidComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    overall_composition: Optional[OverallComposition] = field(
        default=None,
        metadata={
            "name": "OverallComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    phase2_zfactor: Optional[float] = field(
        default=None,
        metadata={
            "name": "Phase2ZFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    phases_present: Optional[str] = field(
        default=None,
        metadata={
            "name": "PhasesPresent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    step_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    vapor_composition: Optional[VaporComposition] = field(
        default=None,
        metadata={
            "name": "VaporComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_condition: Optional[FluidAnalysisStepCondition] = field(
        default=None,
        metadata={
            "name": "FluidCondition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_fraction: Optional[RelativeVolumeRatio] = field(
        default=None,
        metadata={
            "name": "LiquidFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FluidDifferentialLiberationTestStep:
    """
    The DLT test steps.

    :ivar cumulative_stock_tank_gor: The cumulative stock tank GOR at
        this test step.
    :ivar gas_density: The density of gas at this test step.
    :ivar gas_formation_volume_factor: The gas formation volume factor
        at this test step.
    :ivar gas_gravity: The gas gravity at this test step.
    :ivar gas_molecular_weight: The molecular weight of the gas phase at
        this test step.
    :ivar gas_viscosity: The viscosity of the gas phase at this test
        step.
    :ivar gas_zfactor: The gas Z factor value at this test step.
    :ivar liquid_composition: The liquid composition at this test step.
    :ivar oil_density: The density of the oil phase at this test step.
    :ivar oil_formation_volume_factor: The formation volume factor for
        the oil (liquid) phase at the conditions of this test--volume at
        test conditions/volume st standard conditions.
    :ivar oil_formation_volume_factor_corrected: The oil formation
        volume factor (corrected) at this test step.
    :ivar oil_viscosity: The viscosity of the oil phase at this test
        step.
    :ivar overall_composition: The overall composition at this test
        step.
    :ivar phases_present: The phases present at this test step.
    :ivar remark: Remarks and comments about this data item.
    :ivar residual_apigravity: The residual API gravity at this test
        step.
    :ivar solution_gorcorrect: The solution GOR (corrected) at this test
        step.
    :ivar solution_gormeasured: The solution GOR measured at this test
        step.
    :ivar step_number: The step number is the index of a (P,T) step in
        the overall test.
    :ivar step_pressure: The pressure for this test step.
    :ivar step_temperature: The temperature for this test step.
    :ivar total_formation_volume_factor: The total formation volume
        factor at this test step.
    :ivar vapor_composition: The vapor composition at this test step.
    :ivar fluid_condition: The fluid condition at this test step. Enum,
        see fluid analysis step condition.
    :ivar oil_compressibility: The oil compressibility at this test
        step.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    cumulative_stock_tank_gor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CumulativeStockTankGOR",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_formation_volume_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasFormationVolumeFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_gravity: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasMolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_zfactor: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasZFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_composition: Optional[LiquidComposition] = field(
        default=None,
        metadata={
            "name": "LiquidComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_formation_volume_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilFormationVolumeFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_formation_volume_factor_corrected: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilFormationVolumeFactorCorrected",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    overall_composition: Optional[OverallComposition] = field(
        default=None,
        metadata={
            "name": "OverallComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    phases_present: Optional[str] = field(
        default=None,
        metadata={
            "name": "PhasesPresent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    residual_apigravity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ResidualAPIGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    solution_gorcorrect: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SolutionGORCorrect",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    solution_gormeasured: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SolutionGORMeasured",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    step_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    step_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StepTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_formation_volume_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalFormationVolumeFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_composition: Optional[VaporComposition] = field(
        default=None,
        metadata={
            "name": "VaporComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_condition: Optional[FluidAnalysisStepCondition] = field(
        default=None,
        metadata={
            "name": "FluidCondition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_compressibility: Optional[OilCompressibility] = field(
        default=None,
        metadata={
            "name": "OilCompressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FluidSeparatorTestStep:
    """
    Fluid separator test step.

    :ivar bubble_point_pressure: The bubble point pressure for this test
        step.
    :ivar gas_density: The density of gas at this test step.
    :ivar gas_gravity: The gas gravity at this test step.
    :ivar gas_molecular_weight: The molecular weight of the gas phase at
        this test step.
    :ivar gas_viscosity: The viscosity of the gas phase at this test
        step.
    :ivar gas_volume: The gas volume for this test step.
    :ivar gas_zfactor: The gas Z factor value at this test step.
    :ivar liquid_composition: The liquid composition for this test step.
    :ivar oil_density: The density of the oil phase at this test step.
    :ivar oil_formation_volume_factor_corrected: The oil formation
        volume factor (corrected) for this test step.
    :ivar oil_formation_volume_factor_std: The oil formation volume
        factor at standard conditions for this test step.
    :ivar oil_shrinkage_factor: The oil shrinkage factor for this test
        step.
    :ivar oil_specific_gravity: The oil specific gravity for this test
        step.
    :ivar oil_viscosity: The viscosity of the oil phase at this test
        step.
    :ivar overall_composition: The overall composition for this test
        step.
    :ivar phases_present: The phases present for this test step. Enum,
        see phases present.
    :ivar remark: Remarks and comments about this data item.
    :ivar residual_apigravity: The residual API gravity for this test
        step.
    :ivar stage_separator_gorcorrected: The stage separator GOR
        (corrected) for this test step.
    :ivar stage_separator_gorstd: The stage separator GOR at standard
        conditions for this test step.
    :ivar step_number: The step number is the index of a (P,T) step in
        the overall test.
    :ivar step_pressure: The pressure for this test step.
    :ivar step_temperature: The temperature for this test step.
    :ivar vapor_composition: The vapor composition for this test step.
    :ivar fluid_condition: The fluid condition at this test step. Enum,
        see fluid analysis step condition.
    :ivar saturation_pressure: The saturation (or bubble point) pressure
        measured in this test.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    bubble_point_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BubblePointPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_gravity: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasMolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_zfactor: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasZFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_composition: Optional[LiquidComposition] = field(
        default=None,
        metadata={
            "name": "LiquidComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_formation_volume_factor_corrected: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilFormationVolumeFactorCorrected",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_formation_volume_factor_std: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilFormationVolumeFactorStd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_shrinkage_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilShrinkageFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_specific_gravity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilSpecificGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    overall_composition: Optional[OverallComposition] = field(
        default=None,
        metadata={
            "name": "OverallComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    phases_present: Optional[str] = field(
        default=None,
        metadata={
            "name": "PhasesPresent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    residual_apigravity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ResidualAPIGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    stage_separator_gorcorrected: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StageSeparatorGORCorrected",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    stage_separator_gorstd: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StageSeparatorGORStd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    step_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    step_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    vapor_composition: Optional[VaporComposition] = field(
        default=None,
        metadata={
            "name": "VaporComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_condition: Optional[FluidAnalysisStepCondition] = field(
        default=None,
        metadata={
            "name": "FluidCondition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    saturation_pressure: Optional[SaturationPressure] = field(
        default=None,
        metadata={
            "name": "SaturationPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class GeographicContext:
    """
    A geographic context of a report.

    :ivar comment: A general comment that further explains the offshore
        location.
    :ivar country: The name of the country.
    :ivar county: The name of county.
    :ivar state: The state or province within the country.
    :ivar field_value: The name of the field within whose context the
        report exists.
    :ivar offshore_location:
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    country: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Country",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    county: List[str] = field(
        default_factory=list,
        metadata={
            "name": "County",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    state: List[str] = field(
        default_factory=list,
        metadata={
            "name": "State",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    field_value: Optional[NameStruct] = field(
        default=None,
        metadata={
            "name": "Field",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    offshore_location: Optional[OffshoreLocation] = field(
        default=None,
        metadata={
            "name": "OffshoreLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class InjectedGas:
    """
    The injected gas volume.

    :ivar vapor_composition: The composition of injected gas (vapor) for
        this test.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    vapor_composition: List[VaporComposition] = field(
        default_factory=list,
        metadata={
            "name": "VaporComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
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
class IntegerData(AbstractMeasureDataType):
    """
    Integer data.

    :ivar integer_value: The value of a dependent (data) variable in a
        row of the curve table. The units of measure are specified in
        the curve definition. The first value corresponds to order=1 for
        columns where isIndex is false. The second to order=2. And so
        on. The number of index and data values must match the number of
        columns in the table.
    """

    integer_value: Optional[IntegerQualifiedCount] = field(
        default=None,
        metadata={
            "name": "IntegerValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class OtherMeasurementTest:
    """
    Other measurement test.

    :ivar fluid_characterization_table:
    :ivar fluid_characterization_table_format_set:
    :ivar remark: Remarks and comments about this data item.
    :ivar test_number: An integer number to identify this test in a
        sequence of tests.
    :ivar other_measurement_test_step:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    fluid_characterization_table: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidCharacterizationTable",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_characterization_table_format_set: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidCharacterizationTableFormatSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    other_measurement_test_step: List[OtherMeasurementTestStep] = field(
        default_factory=list,
        metadata={
            "name": "OtherMeasurementTestStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProducedGasProperties:
    """
    The properties of produced gas.

    :ivar produced_gas_gravity: The produced gas gravity of this
        produced gas.
    :ivar vapor_composition: The vapor composition of this produced gas.
    """

    produced_gas_gravity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProducedGasGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_composition: List[VaporComposition] = field(
        default_factory=list,
        metadata={
            "name": "VaporComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ProductDisposition(AbstractDisposition):
    """
    Volumes that "left" the reporting entity by one of the disposition methods
    defined in Kind (e.g., flaring, sold, used on site, etc.)

    :ivar kind: The method of disposition. See enum DispositionKind.
    """

    kind: Optional[Union[DispositionKind, str]] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class ProductFlowExpectedUnitProperty:
    """
    Defines expected properties of a facility represented by a unit.

    :ivar child_facility_identifier: The PRODML Relative Identifier (or
        URI) of a child of the parent facility. The identifier path is
        presumed to begin with the identity of the parent facility. This
        identifies a sub-facility which is identified within the context
        of the parent facilityParent2/facilityParent1/name
        identification hierarchy. The property is only expected to be
        defined for this child and not for the parent. For more
        information about URIs, see the Energistics Identifier
        Specification, which is available in the zip file when download
        PRODML.
    :ivar comment: A descriptive remark associated with this property.
    :ivar deadband: Difference between two consecutive readings, which
        must exceed deadband value to be accepted.
    :ivar maximum_frequency: The maximum time difference from the last
        sent event before the next event is sent.
    :ivar property: The expected kind of facility property. Each
        property is documented to have values of a particular type.
    :ivar tag_alias: An alternative name for the sensor that  measures
        the property.
    :ivar expected_flow_qualifier:
    :ivar expected_flow_product: Defines the expected flow and product
        pairs to be assigned to this port by a Product Volume report. A
        set of expected qualifiers can be defined for each pair. The
        aggregate of expectations on all properties should be a subset
        of the aggregate of expectations on the port. If no expectations
        are defined on the port then the port aggregate will be defined
        by the properties.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    child_facility_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChildFacilityIdentifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    deadband: Optional[GeneralMeasureType] = field(
        default=None,
        metadata={
            "name": "Deadband",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    maximum_frequency: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MaximumFrequency",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    property: Optional[FacilityParameter] = field(
        default=None,
        metadata={
            "name": "Property",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    tag_alias: List[NameStruct] = field(
        default_factory=list,
        metadata={
            "name": "TagAlias",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    expected_flow_qualifier: Optional[ExpectedFlowQualifier] = field(
        default=None,
        metadata={
            "name": "ExpectedFlowQualifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    expected_flow_product: List[ProductFlowQualifierExpected] = field(
        default_factory=list,
        metadata={
            "name": "ExpectedFlowProduct",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductFlowExternalReference:
    """
    A reference to an external port in a different product flow model.This value
    represents a foreign key from one element to another.

    :ivar connected_model_reference: Reference to the connected model.
    :ivar connected_port_reference: Reference to the connected port.
    :ivar port_reference: Reference to a type of port.
    :ivar connected_installation:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top level object.
    """

    connected_model_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConnectedModelReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    connected_port_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConnectedPortReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    port_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "PortReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    connected_installation: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "ConnectedInstallation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductFluid(AbstractProductQuantity):
    """Contains the physical properties of the product fluid.

    Every volume has a product fluid reference.

    :ivar gross_energy_content: The amount of heat released during the
        combustion of the reported amount of this product. This value
        takes into account the latent heat of vaporization of water in
        the combustion products, and is useful in calculating heating
        values for fuels where condensation of the reaction products is
        practical.
    :ivar net_energy_content: The amount of heat released during the
        combustion of the reported amount of this product. This value
        ignores the latent heat of vaporization of water in the
        combustion products, and is useful in calculating heating values
        for fuels where condensation of the reaction products is not
        possible and is ignored.
    :ivar overall_composition:
    :ivar product_fluid_kind: A simple enumeration to provide
        information about the product that the production quantity
        represents.
    :ivar product_fluid_reference: String UID that points to the
        productFluid in the fluidComponentSet.
    """

    gross_energy_content: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GrossEnergyContent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    net_energy_content: List[str] = field(
        default_factory=list,
        metadata={
            "name": "NetEnergyContent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    overall_composition: Optional[OverallComposition] = field(
        default=None,
        metadata={
            "name": "OverallComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    product_fluid_kind: Optional[Union[ProductFluidKind, str]] = field(
        default=None,
        metadata={
            "name": "ProductFluidKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    product_fluid_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "productFluidReference",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ProductVolumeBusinessUnit:
    """
    Product volume schema for defining business units.

    :ivar description: A textual description of the business unit.
    :ivar kind: The type of business unit.
    :ivar name: The human contextual name of the business unit.
    :ivar sub_unit: A component part of the unit. The composition of a
        unit may vary with time. This defines the ownership share or
        account information for a sub unit within the context of the
        whole unit. For ownership shares, at any one point in time the
        sum of the shares should be 100%.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: Optional[BusinessUnitKind] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sub_unit: List[ProductVolumeBusinessSubUnit] = field(
        default_factory=list,
        metadata={
            "name": "SubUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductVolumeComponentContent:
    """
    Product Volume Component Content Schema.

    :ivar kind: The type of product whose relative content is being
        described. This should be a specific component (e.g., water)
        rather than a phase (e.g., aqueous).
    :ivar reference_kind: The type of product to which the product is
        being compared. If not given then the product is being compared
        against the overall flow stream.
    :ivar properties:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    kind: Optional[ReportingProduct] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    reference_kind: Optional[ReportingProduct] = field(
        default=None,
        metadata={
            "name": "ReferenceKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    properties: Optional[CommonPropertiesProductVolume] = field(
        default=None,
        metadata={
            "name": "Properties",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductVolumeParameterSet:
    """
    Product Volume Facility Parameter Set Schema.

    :ivar child_facility_identifier: The PRODML Relative Identifier (or
        URI) of a child of the parent facility. The identifier path is
        presumed to begin with the identity of the parent facility. This
        identifies a sub-facility which is identified within the context
        of the parent facilityParent2/facilityParent1/name
        identification hierarchy. The property is only expected to be
        defined for this child and not for the parent. For more
        information about URIs, see the Energistics Identifier
        Specification, which is available in the zip file when download
        PRODML.
    :ivar comment: A comment about the parameter.
    :ivar coordinate_reference_system: The pointer to the coordinate
        reference system (CRS). This is needed for coordinates such as
        measured depth to specify the reference datum.
    :ivar measure_class: If the value is a measure (value with unit of
        measure), this defines the measurement class of the value. The
        units of measure for the value must conform to the list allowed
        by the measurement class in the unit dictionary file. Mutually
        exclusive with curveDefinition.
    :ivar name: The name of the facility parameter. This should reflect
        the business semantics of all values in the set and not the
        underlying kind. For example, specify "diameter" rather than
        "length" or "distance".
    :ivar period_kind: The type of period that is being reported.
    :ivar port: The port to which this parameter is assigned. This must
        be a port on the unit representing the parent facility of this
        parameter. If not specified then the parameter represents the
        unit.
    :ivar product: The type of product that is being reported. This
        would be useful for something like specifying a tank product
        volume or level.
    :ivar qualifier: Qualifies the type of parameter that is being
        reported.
    :ivar sub_qualifier: Defines a specialization of the qualifier
        value. This should only be given if a qualifier is given.
    :ivar version: A timestamp representing the version of this data. A
        parameter set with a more recent timestamp will represent the
        "current" version.
    :ivar version_source: Identifies the source of the version. This
        will commonly be the name of the software which created the
        version.
    :ivar curve_definition: If the value is a curve, this defines the
        meaning of the one column in the table representing the curve.
        Mutually exclusive with measureClass.
    :ivar parameter: A parameter value, possibly at a time. If a time is
        not given then only one parameter should be given. If a time is
        specified with one value then time should be specified for all
        values. Each value in a time series should be of the same
        underling kind of value (for example, a length measure).
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    child_facility_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChildFacilityIdentifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    coordinate_reference_system: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CoordinateReferenceSystem",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    measure_class: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MeasureClass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: Optional[FacilityParameter] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    period_kind: Optional[ReportingDurationKind] = field(
        default=None,
        metadata={
            "name": "PeriodKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    port: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Port",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    product: Optional[ReportingProduct] = field(
        default=None,
        metadata={
            "name": "Product",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    qualifier: Optional[FlowQualifier] = field(
        default=None,
        metadata={
            "name": "Qualifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sub_qualifier: Optional[FlowSubQualifier] = field(
        default=None,
        metadata={
            "name": "SubQualifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    version: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Version",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    version_source: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VersionSource",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    curve_definition: List[CurveDefinition] = field(
        default_factory=list,
        metadata={
            "name": "CurveDefinition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    parameter: List[ProductVolumeParameterValue] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
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
class ProductionOperationSafety:
    """
    Safety Information Schema.

    :ivar comment: Safety related comment.
    :ivar meantime_incident: The mean time between safety incidents.
    :ivar safety_count:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    comment: List[DatedComment] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    meantime_incident: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MeantimeIncident",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    safety_count: List[SafetyCount] = field(
        default_factory=list,
        metadata={
            "name": "SafetyCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionOperationShutdown:
    """
    Information about a shutdown event.

    :ivar activity: A description of main activities from time to time
        during the shutdown period.
    :ivar description: A general description of the shutdown with reason
        and other relevant information.
    :ivar dtim_end: The time the shutdown ended.
    :ivar dtim_start: The time the shutdown started.
    :ivar installation: The name of the installation which was shut
        down. The name can be qualified by a naming system. This also
        defines the kind of facility.
    :ivar loss_gas_std_temp_pres: Estimated loss of gas deliveries
        because of the shutdown. This volume has been corrected to
        standard conditions of temperature and pressure.
    :ivar loss_oil_std_temp_pres: Estimated loss of oil deliveries
        because of the shutdown. This volume has been corrected to
        standard conditions of temperature and pressure.
    :ivar volumetric_down_time: Downtime when the installation is unable
        to produce 100% of its capability.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    activity: List[DatedComment] = field(
        default_factory=list,
        metadata={
            "name": "Activity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    installation: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "Installation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    loss_gas_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LossGasStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    loss_oil_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LossOilStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    volumetric_down_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VolumetricDownTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionOperationThirdPartyProcessing:
    """
    Production losses due to third-party processing.

    :ivar gas_std_temp_pres: The estimated amount of gas lost. This
        volume has been corrected to standard conditions of temperature
        and pressure
    :ivar installation: The name of the installation which performed the
        processing. The name can be qualified by a naming system. This
        also defines the kind of facility.
    :ivar oil_std_temp_pres: The estimated amount of oil lost. This
        volume has been corrected to standard conditions of temperature
        and pressure
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    gas_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    installation: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "Installation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_std_temp_pres: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilStdTempPres",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionWellPeriod:
    """
    Period during which the well choke did not vary.

    :ivar duration: The duration at the given choke setting.
    :ivar remark: A descriptive remark relating to any significant
        events during this period.
    :ivar start_time: The start time at a given choke setting.
    :ivar well_status: The status of the well.
    :ivar product_rate:
    :ivar well_flowing_condition:
    """

    duration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    start_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "StartTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    well_status: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellStatus",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    product_rate: List[ProductRate] = field(
        default_factory=list,
        metadata={
            "name": "ProductRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_flowing_condition: Optional[WellFlowingCondition] = field(
        default=None,
        metadata={
            "name": "WellFlowingCondition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class PvtModelParameterSet:
    """
    A collection of parameters.
    """

    coefficient: List[PvtModelParameter] = field(
        default_factory=list,
        metadata={
            "name": "Coefficient",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class Stoanalysis:
    """
    Stock tank oil analysis.

    :ivar date: The date when this test was performed.
    :ivar flash_from_pressure: The pressure from which the sample was
        flashed for the stock tank oil analysis.
    :ivar flash_from_temperature: The temperature from which the sample
        was flashed for the stock tank oil analysis.
    :ivar liquid_composition: The liquid composition for the stock tank
        oil analysis.
    :ivar molecular_weight: The molecular weight for the stock tank oil
        analysis.
    :ivar overall_composition: The overall composition for the stock
        tank oil analysis.
    :ivar phases_present: The phases present for the stock tank oil
        analysis.
    :ivar remark: Remarks and comments about this data item.
    :ivar vapor_composition: The vapor composition for the stock tank
        oil analysis.
    :ivar fluid_condition: The fluid condition at this test step. Enum,
        see fluid analysis step condition.
    :ivar stoflashed_liquid:
    """

    class Meta:
        name = "STOAnalysis"

    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    flash_from_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlashFromPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flash_from_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlashFromTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_composition: Optional[LiquidComposition] = field(
        default=None,
        metadata={
            "name": "LiquidComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    overall_composition: Optional[OverallComposition] = field(
        default=None,
        metadata={
            "name": "OverallComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    phases_present: Optional[str] = field(
        default=None,
        metadata={
            "name": "PhasesPresent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_composition: Optional[VaporComposition] = field(
        default=None,
        metadata={
            "name": "VaporComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_condition: Optional[FluidAnalysisStepCondition] = field(
        default=None,
        metadata={
            "name": "FluidCondition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    stoflashed_liquid: Optional[StoflashedLiquid] = field(
        default=None,
        metadata={
            "name": "STOFlashedLiquid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class SampleContaminant:
    """
    Sample contaminant information.

    :ivar contaminant_composition: The composition of contaminant in the
        fluid sample.
    :ivar density: The density of contaminant in the fluid sample.
    :ivar description: Description of the contaminant.
    :ivar molecular_weight: The molecular weight of contaminant in the
        fluid sample.
    :ivar remark: Remarks and comments about this data item.
    :ivar sample_of_contaminant_reference:
    :ivar volume_fraction_live_sample: The volume fraction of
        contaminant in the fluid sample.
    :ivar volume_fraction_stock_tank: The contaminant volume percent in
        stock tank oil.
    :ivar weight_fraction_live_sample: The weight fraction of
        contaminant in the fluid sample.
    :ivar weight_fraction_stock_tank: The contaminant weight percent in
        stock tank oil.
    :ivar contaminant_kind: The kind of contaminant.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    contaminant_composition: Optional[LiquidComposition] = field(
        default=None,
        metadata={
            "name": "ContaminantComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Density",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sample_of_contaminant_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SampleOfContaminantReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    volume_fraction_live_sample: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VolumeFractionLiveSample",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    volume_fraction_stock_tank: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VolumeFractionStockTank",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    weight_fraction_live_sample: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WeightFractionLiveSample",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    weight_fraction_stock_tank: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WeightFractionStockTank",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    contaminant_kind: Optional[FluidContaminant] = field(
        default=None,
        metadata={
            "name": "ContaminantKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class SampleIntegrityAndPreparation:
    """
    Sample integrity And preparation information.

    :ivar basic_sediment_and_water: The basic sediment and water of the
        sample when prepared for analysis.
    :ivar free_water_volume: The free water volume of the sample when
        prepared for analysis.
    :ivar initial_volume: The initial volume of the sample when prepared
        for analysis.
    :ivar opening_date: The date when this fluid sample was opened.
    :ivar opening_pressure: The opening pressure of the sample when
        prepared for analysis.
    :ivar opening_remark: Remarks and comments about the opening of the
        sample.
    :ivar opening_temperature: The opening temperature of the sample
        when prepared for analysis.
    :ivar water_content_in_hydrocarbon: The water content in hydrocarbon
        of the sample when prepared for analysis.
    :ivar sample_restoration:
    :ivar saturation_pressure: The saturation (or bubble point) pressure
        measured in this test.
    :ivar saturation_temperature: The saturation temperature of the
        sample when prepared for analysis.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    basic_sediment_and_water: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BasicSedimentAndWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    free_water_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FreeWaterVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    initial_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InitialVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    opening_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "OpeningDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    opening_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OpeningPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    opening_remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OpeningRemark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    opening_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OpeningTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_content_in_hydrocarbon: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterContentInHydrocarbon",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sample_restoration: List[SampleRestoration] = field(
        default_factory=list,
        metadata={
            "name": "SampleRestoration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    saturation_pressure: Optional[SaturationPressure] = field(
        default=None,
        metadata={
            "name": "SaturationPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    saturation_temperature: Optional[SaturationTemperature] = field(
        default=None,
        metadata={
            "name": "SaturationTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class SampleRecombinationRequirement:
    """
    A sample recombination.

    :ivar liquid_composition: The fluid sampling recombination started
        with this liquid composition.
    :ivar liquid_sample: Reference to the liquid sample used in this
        sample recombination.
    :ivar overall_composition: The aim of the fluid sampling
        recombination was this overall composition.
    :ivar recombination_gor: The recombination gas-oil ratio for this
        sample recombination.
    :ivar recombination_pressure: The recombination pressure for this
        sample recombination.
    :ivar recombination_saturation_pressure: The recombination
        saturation pressure for this sample recombination.
    :ivar recombination_temperature: The recombination temperature for
        this sample recombination.
    :ivar remark: Remarks and comments about this data item.
    :ivar vapor_composition: The fluid sampling recombination started
        with this vapor composition.
    :ivar vapor_sample: Reference to the vapor sample used in this
        sample recombination.
    """

    liquid_composition: Optional[LiquidComposition] = field(
        default=None,
        metadata={
            "name": "LiquidComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_sample: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LiquidSample",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    overall_composition: Optional[OverallComposition] = field(
        default=None,
        metadata={
            "name": "OverallComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    recombination_gor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RecombinationGOR",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    recombination_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RecombinationPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    recombination_saturation_pressure: Optional[SaturationPressure] = field(
        default=None,
        metadata={
            "name": "RecombinationSaturationPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    recombination_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RecombinationTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_composition: Optional[VaporComposition] = field(
        default=None,
        metadata={
            "name": "VaporComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_sample: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VaporSample",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class SaturationTest:
    """
    Saturation test.

    :ivar remark: Remarks and comments about this data item.
    :ivar test_number: A number for this test for purposes of, e.g.,
        tracking lab sequence.
    :ivar test_temperature: The temperature of this test.
    :ivar saturation_pressure: The saturation (or bubble point) pressure
        measured in this test.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    test_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    saturation_pressure: Optional[SaturationPressure] = field(
        default=None,
        metadata={
            "name": "SaturationPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class StringData(AbstractMeasureDataType):
    """
    String data.

    :ivar string_value: The value of a dependent (data) variable in a
        row of the curve table. The units of measure are specified in
        the curve definition. The first value corresponds to order=1 for
        columns where isIndex is false. The second to order=2. And so
        on. The number of index and data values must match the number of
        columns in the table.
    """

    string_value: Optional[KindQualifiedString] = field(
        default=None,
        metadata={
            "name": "StringValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class SwellingTestStep:
    """
    Swelling test step.

    :ivar constant_composition_expansion_test: A reference to a constant
        composition expansion test associated with this swelling test.
    :ivar density_at_saturation_point: The density at saturation point
        for this swelling test step.
    :ivar gor: The gas-oil ratio for this swelling test step.
    :ivar remark: Remarks and comments about this data item.
    :ivar step_number: The step number is the index of a (P,T) step in
        the overall test.
    :ivar swelling_factor: The swelling factor for this swelling test
        step.
    :ivar transport_property_test_reference: A reference to a transport
        property test associated with this swelling test.
    :ivar incremental_gas_added: The incremental gas added for this
        swelling test step.
    :ivar cumulative_gas_added: The cumulative gas added for this
        swelling test step.
    :ivar swollen_volume: The swollen volume for this swelling test
        step, relative to a reference volume.
    :ivar saturation_pressure: The saturation (or bubble point) pressure
        measured in this test.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    constant_composition_expansion_test: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ConstantCompositionExpansionTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    density_at_saturation_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DensityAtSaturationPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Gor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    swelling_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SwellingFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    transport_property_test_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TransportPropertyTestReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    incremental_gas_added: List[RefInjectedGasAdded] = field(
        default_factory=list,
        metadata={
            "name": "IncrementalGasAdded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cumulative_gas_added: List[RefInjectedGasAdded] = field(
        default_factory=list,
        metadata={
            "name": "CumulativeGasAdded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    swollen_volume: Optional[RelativeVolumeRatio] = field(
        default=None,
        metadata={
            "name": "SwollenVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    saturation_pressure: Optional[SaturationPressure] = field(
        default=None,
        metadata={
            "name": "SaturationPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class TestCondition:
    """
    Test conditions for a production well test.

    :ivar remark: Remarks and comments about this data item.
    :ivar start_time: The date and time when the test  began.
    :ivar test_duration: The duration of the test.
    :ivar product_rate:
    :ivar service_fluid:
    :ivar parameters:
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    start_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "StartTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    test_duration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestDuration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    product_rate: List[ProductRate] = field(
        default_factory=list,
        metadata={
            "name": "ProductRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    service_fluid: List[ServiceFluid] = field(
        default_factory=list,
        metadata={
            "name": "ServiceFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    parameters: Optional[WellFlowingCondition] = field(
        default=None,
        metadata={
            "name": "Parameters",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class TimeSeriesThreshold:
    """
    Defines a value threshold window and the cumulative time duration that the data
    was within that window.

    :ivar duration: The sum of the time intervals over the range of
        dTimMin to dTimMax during which the values were within the
        specified threshold range.
    :ivar threshold_minimum: The lower bound of the threshold for
        testing whether values are within a specific range.The element
        "unit" defines the unit of measure of this value. At least one
        of minimumValue and maximumValue must be specified. The
        thresholdMinimum must be less than thresholdMaximum. If
        thresholdMinimum is not specified then the minimum shall be
        assumed to be minus infinity.
    :ivar threshold_maximum: The upper bound of the threshold for
        testing whether values are within a specific range. Element
        "unit" defines the unit of measure of this value. At least one
        of minimumValue and maximumValue must be specified. The
        thresholdMaximum must be greater than thresholdMinimum. If
        thresholdMaximum is not specified then the maximum shall be
        assumed to be plus infinity.
    """

    duration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    threshold_minimum: Optional[EndpointQuantity] = field(
        default=None,
        metadata={
            "name": "ThresholdMinimum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    threshold_maximum: Optional[EndpointQuantity] = field(
        default=None,
        metadata={
            "name": "ThresholdMaximum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WellDatum:
    """
    Defines the vertical datums associated with elevation, vertical depth and
    measured depth coordinates within the context of a well.

    :ivar code: The code value that represents the type of reference
        datum. This may represent a point on a device (e.g., kelly
        bushing) or it may represent a vertical reference datum (e.g.,
        mean sea level).
    :ivar elevation:
    :ivar kind: Since various activities may use different points as
        measurement datums, it is useful to characterize the point based
        on its usage. A well reference datum may have more than one such
        characterization. For example, it may be the datum used by the
        driller and logger for measuring their depths. Example usage
        values would be 'permanent','driller', 'logger' 'WRP' (well
        reference point) and 'SRP' (site reference point).
    :ivar measured_depth: The measured depth coordinate of this
        reference datum as measured from another datum. The measured
        depth datum should either be the same as the elevation datum or
        it should be relatable to the elevation datum through other
        datums. Positive moving toward the bottomhole from the measured
        depth datum. This should be given when a local reference is
        "downhole", such as a kickoff point or ocean bottom template,
        and the borehole may not be vertical. If a Depth is given then
        an Elevation should also be given.
    :ivar name: The human understandable contextual name of the
        reference datum.
    :ivar remark: A contextual description of the well reference datum.
    :ivar wellbore:
    :ivar abstract_datum:
    :ivar horizontal_location:
    :ivar default_elevation: True indicates that this is the default
        reference datum for elevation coordinates. False or not given
        indicates that this is not the default reference datum.
        Elevation coordinates that do not specify a datum reference
        should be assumed to be measured relative to the default
        reference datum. Only one reference datum may be designated as
        the default elevation datum for each well. Values are "true" (or
        "1") and "false" ( or "0").
    :ivar default_measured_depth: True indicates that this is the
        default reference datum for measured depth coordinates. False or
        not given indicates that this is not the default reference
        datum. Measured depth coordinates that do not specify a datum
        reference should be assumed to be measured relative to this
        default reference datum. Only one reference datum may be
        designated as the default measured depth datum for each well.
        Values are "true" (or "1") and "false" ( or "0").
    :ivar default_vertical_depth: True indicates that this is the
        default reference datum for vertical depth coordinates. False or
        not given indicates that this is not the default reference
        datum. Vertical depth coordinates that do not specify a datum
        reference should be assumed to be measured relative to the
        default reference datum. Only one reference datum may be
        designated as the default vertical depth datum for each well.
        Values are "true" (or "1") and "false" ( or "0").
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    code: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    elevation: Optional[WellElevationCoord] = field(
        default=None,
        metadata={
            "name": "Elevation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    measured_depth: Optional[MeasuredDepthCoord] = field(
        default=None,
        metadata={
            "name": "MeasuredDepth",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellbore: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Wellbore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    abstract_datum: Optional[AbstractDatum] = field(
        default=None,
        metadata={
            "name": "AbstractDatum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    horizontal_location: Optional[Location] = field(
        default=None,
        metadata={
            "name": "HorizontalLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    default_elevation: Optional[bool] = field(
        default=None,
        metadata={
            "name": "DefaultElevation",
            "type": "Attribute",
            "required": True,
        },
    )
    default_measured_depth: Optional[bool] = field(
        default=None,
        metadata={
            "name": "DefaultMeasuredDepth",
            "type": "Attribute",
            "required": True,
        },
    )
    default_vertical_depth: Optional[bool] = field(
        default=None,
        metadata={
            "name": "DefaultVerticalDepth",
            "type": "Attribute",
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
class WellTestInjectionTestData(AbstractWellTest):
    """
    Information related to fluid injection during a well test.

    :ivar choke_orifice_size: The size of the opening in the flow choke
        at the wellhead.
    :ivar maximum_annular_pressure: The maximum pressure measured at the
        annulus.
    :ivar minimum_annular_pressure: The minimum pressure measured at the
        annulus.
    :ivar test_duration: The time length (with UOM) of the well test.
    :ivar wellhead_flowing_pressure: The flowing pressure measured at
        the wellhead during the test.
    :ivar wellhead_maximum_pressure: The maximum pressure measured at
        the wellhead during the well test.
    :ivar injected_fluid: The fluid that is being injected.
    :ivar well_test_cumulative: The cumulative volumes of fluids at the
        time of the well test. The fluids are oil, gas, and water.
    :ivar test_interval: The interval tested. This element includes a
        top and base depth, and the formation tested.
    """

    choke_orifice_size: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ChokeOrificeSize",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    maximum_annular_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MaximumAnnularPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    minimum_annular_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MinimumAnnularPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_duration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestDuration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellhead_flowing_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellheadFlowingPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellhead_maximum_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellheadMaximumPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    injected_fluid: Optional[InjectionFluid] = field(
        default=None,
        metadata={
            "name": "InjectedFluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_test_cumulative: Optional[WellTestCumulative] = field(
        default=None,
        metadata={
            "name": "WellTestCumulative",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_interval: Optional[WellTestInterval] = field(
        default=None,
        metadata={
            "name": "TestInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WellTestProductionTestData(AbstractWellTest):
    """
    Information about a production well test.

    :ivar operating_method: The method being used to operate the well.
        Examples are 'flowing', 'pumping', 'gas lifted'.
    :ivar test_duration: The length of time (with UOM) of the well test.
    :ivar bottomhole_data: DEPRECATED - Use pointData instead. This
        element records measurements made at the bottomhole.
    :ivar well_test_cumulative: The cumulative volumes of fluids at the
        time of the well test. The fluids are oil, gas, and water.
    :ivar esp_data: Frequency and electric current measured during the
        well test for electric submersible pump (ESP) wells. The
        presumption is that only one pump per well is operational during
        each test.
    :ivar test_interval: The interval tested. This element includes a
        top and base depth, and the formation(s) tested. It also
        includes control data for the tested interval.
    :ivar point_data: This element records temperature and pressure at
        points in the wellbore.
    :ivar production_test_results: The production results of the test.
    :ivar separator_data: This element records the measurements
        (pressure and temperature) at the separator.
    :ivar wellhead_data: This element records measurements made and
        settings made at the wellhead.
    """

    operating_method: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OperatingMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_duration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestDuration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bottomhole_data: Optional[WellTestBottomholeData] = field(
        default=None,
        metadata={
            "name": "BottomholeData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_test_cumulative: Optional[WellTestCumulative] = field(
        default=None,
        metadata={
            "name": "WellTestCumulative",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    esp_data: Optional[WellTestElectricSubmersiblePumpData] = field(
        default=None,
        metadata={
            "name": "EspData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_interval: List[WellTestInterval] = field(
        default_factory=list,
        metadata={
            "name": "TestInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    point_data: List[WellTestPointData] = field(
        default_factory=list,
        metadata={
            "name": "PointData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    production_test_results: Optional[WellTestProductionTestResults] = field(
        default=None,
        metadata={
            "name": "ProductionTestResults",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    separator_data: Optional[WellTestSeparatorData] = field(
        default=None,
        metadata={
            "name": "SeparatorData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellhead_data: Optional[WellTestWellheadData] = field(
        default=None,
        metadata={
            "name": "WellheadData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WftTestData:
    """
    A reference to a set of formation tester data that was recorded.

    :ivar curve_section: A reference to a specific interval of a
        specific curve in a specific log.
    :ivar parameter: Test parameters used here are either control
        parameters used to govern the test or are single value
        parameters measured by the test (and not by subsequent
        analysis).
    :ivar role: The role of the test data. The role applies either to a
        curve or to a point parameter. See enum WftTestRoleData.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    curve_section: List[WftCurveSection] = field(
        default_factory=list,
        metadata={
            "name": "CurveSection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    parameter: List[WftInOutParameter] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    role: Optional[WftTestDataRole] = field(
        default=None,
        metadata={
            "name": "Role",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class AbstractDtsEquipment:
    """
    The abstract class of equipment in the optical path from which all components
    in the optical path inherit.

    :ivar comment: A descriptive remark about the equipment (e.g.,
        optical fiber).
    :ivar manufacturer: The manufacturer for this item of equipment.
    :ivar manufacturing_date: Date when the equipment (e.g., instrument
        box) was manufactured.
    :ivar name: The DTS instrument equipment name.
    :ivar software_version: Latest known version of the
        software/firmware that is running in the equipment
    :ivar supplier: Contact details for the company/person supplying the
        equipment.
    :ivar supplier_model_number: The model number (alphanumeric) that is
        used by the supplier to reference the type of fiber that is
        supplied to the user.
    :ivar supply_date: The date on which this fiber segment was
        supplied.
    :ivar type_value: The type of equipment. This might include the
        model type.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    manufacturer: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    manufacturing_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "ManufacturingDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    software_version: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SoftwareVersion",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    supplier: Optional[BusinessAssociate] = field(
        default=None,
        metadata={
            "name": "Supplier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    supplier_model_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SupplierModelNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    supply_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "SupplyDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    type_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class AbstractPvtModel:
    """
    Abstract class of  PVT model.
    """

    custom_pvt_model_extension: Optional[CustomPvtModelExtension] = field(
        default=None,
        metadata={
            "name": "CustomPvtModelExtension",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pvt_model_parameter_set: Optional[PvtModelParameterSet] = field(
        default=None,
        metadata={
            "name": "PvtModelParameterSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class AbstractSimpleProductVolume:
    """The parent abstract class for any object that will be included in a
    regulatory report.

    Those objects must inherit from this abstract object.

    :ivar approval_date: The date on which the report was approved.
    :ivar fluid_component_catalog:
    :ivar geographic_context: Geographic context for reporting entities.
    :ivar operator:
    :ivar standard_conditions: The condition-dependant measurements
        (e.g.,  volumes) in this transfer are taken to be measured at
        standard conditions. The element is mandatory in all the SPVR
        objects.  A choice is available – either to supply the
        temperature and pressure for all the volumes that follow, or to
        choose from a list of standards organizations’ reference
        conditions. Note that the enum list of standard conditions is
        extensible, allowing for local measurement condition standards
        to be used
    """

    approval_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "ApprovalDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_component_catalog: Optional[FluidComponentCatalog] = field(
        default=None,
        metadata={
            "name": "FluidComponentCatalog",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    geographic_context: Optional[GeographicContext] = field(
        default=None,
        metadata={
            "name": "GeographicContext",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    operator: Optional[BusinessAssociate] = field(
        default=None,
        metadata={
            "name": "Operator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    standard_conditions: Optional[str] = field(
        default=None,
        metadata={
            "name": "StandardConditions",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class AtmosphericFlashTestAndCompositionalAnalysis:
    """
    The flash test and compositional analysis.

    :ivar atmospheric_pressure: The atmospheric pressure at the time of
        this analysis.
    :ivar atmospheric_temperature: The atmospheric temperature at the
        time of this analysis.
    :ivar avg_molecular_weight: The average molecular weight of the
        sample for this test.
    :ivar date: The date when this test was performed.
    :ivar density_at_sample_pressureand_temperature: The density of the
        sample at the pressure and temperature conditions of this test.
    :ivar flash_gor: The gas-oil ratio of the flash in this analysis.
    :ivar flash_to_pressure: The pressure to which the sample is flashed
        in this analysis.
    :ivar flash_to_temperature: The temperature to which the sample is
        flashed in this analysis.
    :ivar oil_formation_volume_factor: The formation volume factor for
        the oil (liquid) phase at the conditions of this test--volume at
        test conditions/volume at standard conditions.
    :ivar overall_composition:
    :ivar remark: Remarks and comments about this data item.
    :ivar test_number: An integer number to identify this test in a
        sequence of tests.
    :ivar flashed_gas:
    :ivar flashed_liquid:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    atmospheric_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AtmosphericPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    atmospheric_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AtmosphericTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    avg_molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AvgMolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    density_at_sample_pressureand_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DensityAtSamplePressureandTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flash_gor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlashGOR",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flash_to_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlashToPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flash_to_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlashToTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_formation_volume_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilFormationVolumeFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    overall_composition: Optional[OverallComposition] = field(
        default=None,
        metadata={
            "name": "OverallComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    flashed_gas: Optional[FlashedGas] = field(
        default=None,
        metadata={
            "name": "FlashedGas",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flashed_liquid: Optional[FlashedLiquid] = field(
        default=None,
        metadata={
            "name": "FlashedLiquid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ConstantCompositionExpansionTest:
    """
    The CCE test.

    :ivar remark: Expected to be a yes or no value to indicate if
        differential liberation/vaporization data are corrected to
        separator conditions/flash data or not.
    :ivar test_number: A number for this test for purposes of e.g.,
        tracking lab sequence.
    :ivar test_temperature: The temperature of this test.
    :ivar constant_composition_expansion_test_step: Measured relative
        volume ratio = measured volume/volume at Psat.
    :ivar liquid_fraction_reference: Volume reference for the measured
        liquid fraction in a constant composition expansion
        test. Referenced to liquid volume at saturation pressure
        (generally).
    :ivar relative_volume_reference: Volume reference for the relative
        volume ratio in a constant composition expansion
        test. Referenced to liquid volume at saturation pressure
        (generally).
    :ivar saturation_pressure: The saturation (or bubble point) pressure
        measured in this test.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    test_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    constant_composition_expansion_test_step: List[
        ConstantCompositionExpansionTestStep
    ] = field(
        default_factory=list,
        metadata={
            "name": "ConstantCompositionExpansionTestStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_fraction_reference: List[FluidVolumeReference] = field(
        default_factory=list,
        metadata={
            "name": "LiquidFractionReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    relative_volume_reference: List[FluidVolumeReference] = field(
        default_factory=list,
        metadata={
            "name": "RelativeVolumeReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    saturation_pressure: Optional[SaturationPressure] = field(
        default=None,
        metadata={
            "name": "SaturationPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ConstantVolumeDepletionTest:
    """
    The CVT test.

    :ivar cumulative_gas_produced_reference_std: The volume is corrected
        to standard conditions of temperature and pressure.
    :ivar remark: Remarks and comments about this data item.
    :ivar test_number: A number for this test for purposes of, e.g.,
        tracking lab sequence.
    :ivar test_temperature: The temperature of this test.
    :ivar cvd_test_step:
    :ivar liquid_dropout_reference:
    :ivar satuation_pressure:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    cumulative_gas_produced_reference_std: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CumulativeGasProducedReferenceStd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    test_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    cvd_test_step: List[FluidCvdTestStep] = field(
        default_factory=list,
        metadata={
            "name": "CvdTestStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_dropout_reference: List[FluidVolumeReference] = field(
        default_factory=list,
        metadata={
            "name": "LiquidDropoutReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    satuation_pressure: Optional[SaturationPressure] = field(
        default=None,
        metadata={
            "name": "SatuationPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class DasProcessed:
    """This object contains data objects for processed data types and has no data
    attributes.

    Currently only two processed data types have been defined: the frequency band extracted (FBE) and spectra. In the future other processed data types may be added.
    Note that a DasProcessed object is optional and only present if DAS FBE or DAS spectra data is exchanged.
    """

    fbe: List[DasFbe] = field(
        default_factory=list,
        metadata={
            "name": "Fbe",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    spectra: List[DasSpectra] = field(
        default_factory=list,
        metadata={
            "name": "Spectra",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DifferentialLiberationTest:
    """
    The differential liberation test.

    :ivar correction_method: A flag to indicate if differential
        liberation/vaporization data are corrected to separator
        conditions/flash data or not.
    :ivar remark: Remarks and comments about this data item.
    :ivar test_number: A number for this test for purposes of, e.g.,
        tracking lab sequence.
    :ivar test_temperature: The temperature of this test.
    :ivar dl_test_step:
    :ivar shrinkage_reference:
    :ivar saturation_pressure: The saturation (or bubble point) pressure
        measured in this test.
    :ivar separator_conditions: Reference to a separator test element
        that contains the separator conditions (stages) that apply to
        this test.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    correction_method: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CorrectionMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    test_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    dl_test_step: List[FluidDifferentialLiberationTestStep] = field(
        default_factory=list,
        metadata={
            "name": "DlTestStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    shrinkage_reference: Optional[FluidVolumeReference] = field(
        default=None,
        metadata={
            "name": "ShrinkageReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    saturation_pressure: Optional[SaturationPressure] = field(
        default=None,
        metadata={
            "name": "SaturationPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    separator_conditions: Optional[SeparatorConditions] = field(
        default=None,
        metadata={
            "name": "SeparatorConditions",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FacilityIdentifier:
    """
    Contains details about the facility being surveyed, such as name, geographical
    data, etc.

    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    :ivar content:
    """

    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "BusinessUnit",
                    "type": str,
                    "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
                },
                {
                    "name": "Kind",
                    "type": str,
                    "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
                },
                {
                    "name": "Operator",
                    "type": BusinessAssociate,
                    "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
                },
                {
                    "name": "Installation",
                    "type": FacilityIdentifierStruct,
                    "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
                },
                {
                    "name": "ContextFacility",
                    "type": FacilityIdentifierStruct,
                    "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
                },
                {
                    "name": "GeographicContext",
                    "type": GeographicContext,
                    "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
                },
                {
                    "name": "Name",
                    "type": NameStruct,
                    "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
                },
            ),
        },
    )


@dataclass
class FiberOpticalPathNetwork:
    """The sequence of connected items of equipment along the optical path.

    Represented by a flow network.

    :ivar comment: Comment.
    :ivar context_facility: Context facility.
    :ivar dtime_end: DTimeEnd.
    :ivar dtim_max: DTimMax.
    :ivar dtim_min: DTimMin.
    :ivar dtim_start: DTimStart.
    :ivar existence_time: ExistenceTime.
    :ivar external_connect:
    :ivar installation: Installation.
    :ivar network:
    :ivar uid: Unique identifier of this object.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    context_facility: List[FacilityIdentifierStruct] = field(
        default_factory=list,
        metadata={
            "name": "ContextFacility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )
    dtime_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimeEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_max: Optional[EndpointQualifiedDateTime] = field(
        default=None,
        metadata={
            "name": "DTimMax",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_min: Optional[EndpointQualifiedDateTime] = field(
        default=None,
        metadata={
            "name": "DTimMin",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    existence_time: Optional[EndpointQualifiedDateTime] = field(
        default=None,
        metadata={
            "name": "ExistenceTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    external_connect: List[ProductFlowExternalReference] = field(
        default_factory=list,
        metadata={
            "name": "ExternalConnect",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    installation: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "Installation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    network: List[ProductFlowNetwork] = field(
        default_factory=list,
        metadata={
            "name": "Network",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
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
class FluidCharacterizationTableFormatSet:
    """
    A set of table format definitions.
    """

    fluid_characterization_table_format: List[
        FluidCharacterizationTableFormat
    ] = field(
        default_factory=list,
        metadata={
            "name": "FluidCharacterizationTableFormat",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class FluidSampleAcquisition:
    """Information common to any fluid sample taken.

    Additional details can be captured in related data object depending
    on the where the sample was taken, for example: downhole, separator,
    wellhead, of the formation using a wireline formation tester (WFT).
    If the tool used to capture samples has multiple containers, each
    container has a separate instance of fluid sample acquisition.

    :ivar acquisition_gor: The acquisition gas-oil ratio for this fluid
        sample acquisition.
    :ivar acquisition_pressure: The acquisition pressure when this
        sample was taken.
    :ivar acquisition_temperature: The acquisition temperature when this
        sample was taken. .
    :ivar acquisition_volume: The acquisition volume when this sample
        was taken.
    :ivar date: The date when the sample was taken.
    :ivar fluid_sample_container_reference:
    :ivar fluid_sample_reference:
    :ivar formation_pressure: The formation pressure when this sample
        was taken.
    :ivar formation_temperature: The formation temperature when this
        sample was taken.
    :ivar remark: Remarks and comments about this data item.
    :ivar service_company: The service company who took the fluid
        sample.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    acquisition_gor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AcquisitionGOR",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    acquisition_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AcquisitionPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    acquisition_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AcquisitionTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    acquisition_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AcquisitionVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fluid_sample_container_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidSampleContainerReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fluid_sample_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidSampleReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    formation_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FormationPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    formation_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FormationTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: Optional[str] = field(
        default=None,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    service_company: Optional[BusinessAssociate] = field(
        default=None,
        metadata={
            "name": "ServiceCompany",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FluidSeparatorTest:
    """
    FluidSeparator  Test.

    :ivar overall_gas_gravity: The overall gas gravity for this test.
    :ivar remark: Remarks and comments about this data item.
    :ivar reservoir_temperature: The reservoir temperature for this
        test.
    :ivar saturated_oil_density: The saturated oil density for this
        test.
    :ivar saturated_oil_formation_volume_factor: The saturated oil
        formation volume factor for this test.
    :ivar separator_test_gor: The separator test GOR for this test.
    :ivar test_number: A number for this test for purposes of, e.g.,
        tracking lab sequence.
    :ivar separator_test_step:
    :ivar shrinkage_reference:
    :ivar saturation_pressure: The saturation (or bubble point) pressure
        measured in this test.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    overall_gas_gravity: Optional[float] = field(
        default=None,
        metadata={
            "name": "OverallGasGravity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reservoir_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReservoirTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    saturated_oil_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SaturatedOilDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    saturated_oil_formation_volume_factor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SaturatedOilFormationVolumeFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    separator_test_gor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SeparatorTestGOR",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    separator_test_step: List[FluidSeparatorTestStep] = field(
        default_factory=list,
        metadata={
            "name": "SeparatorTestStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    shrinkage_reference: Optional[FluidVolumeReference] = field(
        default=None,
        metadata={
            "name": "ShrinkageReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    saturation_pressure: Optional[SaturationPressure] = field(
        default=None,
        metadata={
            "name": "SaturationPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductFlowPort:
    """
    Product Flow Port Schema.

    :ivar comment: A descriptive remark associated with this port.
    :ivar direction: Defines whether this port is an inlet or outlet.
        This is a nominal intended direction.
    :ivar exposed: True ("true" or "1") indicates that the port is an
        exposed internal port and cannot be used in a connection
        external to the unit. False ("false" or "0") or not given
        indicates a normal port.
    :ivar facility: The name of the facility represented by this
        ProductFlowPort The name can be qualified by a naming system.
        The facility name is assumed to be unique within the context of
        the facility represented by the unit. This also defines the kind
        of facility.
    :ivar facility_alias: An alternative name of a facility. This is
        generally unique within a naming system. The above contextually
        unique name should also be listed as an alias.
    :ivar name: The name of the port within the context of the product
        flow unit.
    :ivar plan_name: The name of a network plan. This indicates a
        planned port. All child network components must all be planned
        and be part of the same plan. The parent unit must be part of
        the same plan or be an actual. Not specified indicates an actual
        port.
    :ivar connected_node: Defines the node to which this port is
        connected. A timestamp activates and deactivates the connection.
        Only one connectedNode should be active at any one point in
        time. There are no semantics for the node except common
        connection. All ports that are connected to a node with the the
        same name are inherently connected to each other. The name of
        the node is only required to be unique within the context of the
        current Product Flow Network (that is, not the overall model).
        All ports must be connected to a node and whether or not any
        other port is connected to the same node depends on the
        requirements of the network. Any node that is internally
        connected to only one port is presumably a candidate to be
        connected to an external node. The behavior of ports connected
        at a common node is as follows: a) There is no pressure drop
        across the node. All ports connected to the node have the same
        pressure. That is, there is an assumption of steady state fluid
        flow. b) Conservation of mass exists across the node. The mass
        into the node via all connected ports equals the mass out of the
        node via all connected ports. c) The flow direction of a port
        connected to the node may be transient. That is, flow direction
        may change toward any port(s) if the relative internal pressure
        of the Product Flow Units change and a new steady state is
        achieved.
    :ivar expected_flow_property: Defines the properties that are
        expected to be measured at this port. This can also specify the
        equipment tag(s) of the sensor that will read the value. Only
        one of each property kind should be active at any point in time.
    :ivar expected_flow_product: Defines the expected flow and product
        pairs to be assigned to this port by a Product Volume report. A
        set of expected qualifiers can be defined for each pair.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    direction: Optional[ProductFlowPortType] = field(
        default=None,
        metadata={
            "name": "Direction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    exposed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Exposed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "Facility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility_alias: List[NameStruct] = field(
        default_factory=list,
        metadata={
            "name": "FacilityAlias",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    plan_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PlanName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    connected_node: List[ConnectedNode] = field(
        default_factory=list,
        metadata={
            "name": "ConnectedNode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )
    expected_flow_property: List[ProductFlowExpectedUnitProperty] = field(
        default_factory=list,
        metadata={
            "name": "ExpectedFlowProperty",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    expected_flow_product: List[ProductFlowQualifierExpected] = field(
        default_factory=list,
        metadata={
            "name": "ExpectedFlowProduct",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductVolumeBalanceDetail:
    """
    Product Volume Balance Detail Schema.

    :ivar account_number: An account identifier for the balance.
    :ivar owner: A pointer to the business unit which owns the product.
    :ivar sample_analysis_result: A pointer to a fluid sample analysis
        result object that is relevant to the balance. This sample may
        have been acquired previous to or after this period and is used
        for determining the allocated characteristics.
    :ivar share: The owner's share of the product.
    :ivar source_unit: Points to the business unit from which the
        product originated.
    :ivar volume_value:
    :ivar event:
    :ivar component_content:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    account_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AccountNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    owner: Optional[str] = field(
        default=None,
        metadata={
            "name": "Owner",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    sample_analysis_result: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SampleAnalysisResult",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    share: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Share",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    source_unit: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SourceUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    volume_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VolumeValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    event: List[ProductVolumeBalanceEvent] = field(
        default_factory=list,
        metadata={
            "name": "Event",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    component_content: List[ProductVolumeComponentContent] = field(
        default_factory=list,
        metadata={
            "name": "ComponentContent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionOperationHse:
    """
    Operational Health, Safety and Environment Schema.

    :ivar alarm_count: The number of system alarms that have occurred.
    :ivar incident_count: The number of incidents or accidents and
        injuries that were reported.
    :ivar medical_treatment_count: The number of medical treatments that
        have occurred.
    :ivar safety_description: A textual description of safety
        considerations.
    :ivar safety_intro_count: The number of personnel safety
        introductions that have occurred.
    :ivar since_defined_situation: The amount of time since the most
        recent defined hazard and accident situation (Norwegian DFU).
    :ivar since_lost_time: The amount of time since the most recent
        lost-time accident.
    :ivar since_prevention_exercise: The amount of time since the most
        recent accident-prevention exercise.
    :ivar safety: Safety information at a specific installatino.
    :ivar weather: Information about the weather at a point in time.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    class Meta:
        name = "ProductionOperationHSE"

    alarm_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "AlarmCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    incident_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "IncidentCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    medical_treatment_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "MedicalTreatmentCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    safety_description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SafetyDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    safety_intro_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "SafetyIntroCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    since_defined_situation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SinceDefinedSituation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    since_lost_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SinceLostTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    since_prevention_exercise: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SincePreventionExercise",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    safety: List[ProductionOperationSafety] = field(
        default_factory=list,
        metadata={
            "name": "Safety",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    weather: List[ProductionOperationWeather] = field(
        default_factory=list,
        metadata={
            "name": "Weather",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionOperationLostProduction:
    """
    Lost Production Schema.
    """

    volume_and_reason: List[LostVolumeAndReason] = field(
        default_factory=list,
        metadata={
            "name": "VolumeAndReason",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    third_party_processing: List[
        ProductionOperationThirdPartyProcessing
    ] = field(
        default_factory=list,
        metadata={
            "name": "ThirdPartyProcessing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class ReportingEntityVolumes:
    """Contains all the volumes for a single reporting entity.

    It contains a reference back to the reporting entity using its UUID
    for reference.

    :ivar duration: the duration of volume produced at facility
    :ivar reporting_entity_reference:
    :ivar start_date: The starting date of the month.
    :ivar disposition:
    :ivar closing_inventory:
    :ivar opening_inventory:
    :ivar deferred_production_event:
    :ivar injection:
    :ivar production:
    """

    duration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Duration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reporting_entity_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReportingEntityReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    start_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "StartDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    disposition: List[AbstractDisposition] = field(
        default_factory=list,
        metadata={
            "name": "Disposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    closing_inventory: List[AbstractProductQuantity] = field(
        default_factory=list,
        metadata={
            "name": "ClosingInventory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    opening_inventory: List[AbstractProductQuantity] = field(
        default_factory=list,
        metadata={
            "name": "OpeningInventory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    deferred_production_event: List[DeferredProductionEvent] = field(
        default_factory=list,
        metadata={
            "name": "DeferredProductionEvent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    injection: List[Injection] = field(
        default_factory=list,
        metadata={
            "name": "Injection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    production: List[Production] = field(
        default_factory=list,
        metadata={
            "name": "Production",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class SlimTubeSpecification:
    """Specifications of the slim tube used during a slim-tube test.

    For definition of a slim tube and slim-tube test, see
    http://www.glossary.oilfield.slb.com/Terms/s/slim-tube_test.aspx

    :ivar cross_section_area: The cross section area of the slim tube.
    :ivar inner_diameter: The inner diameter of the slim tube.
    :ivar length: The length of the slim tube.
    :ivar outer_diameter: The outer diameter of the slim tube.
    :ivar packing_material: The packing material used in the slim tube.
    :ivar permeability: The permeability of the slim tube.
    :ivar pore_volume: The pore volume of the slim tube.
    :ivar porosity: The porosity of the slim tube.
    :ivar remark: Remarks and comments about this data item.
    :ivar injected_gas: Reference to the gas injected into the slim
        tube.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    cross_section_area: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CrossSectionArea",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    inner_diameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InnerDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    length: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    outer_diameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OuterDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    packing_material: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PackingMaterial",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    permeability: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Permeability",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pore_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PoreVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    porosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Porosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    injected_gas: List[InjectedGas] = field(
        default_factory=list,
        metadata={
            "name": "InjectedGas",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class SlimTubeTestVolumeStep:
    """
    Slim-tube test volume step.

    :ivar cumulative_oil_production_perc_ooip: The cumulative oil
        production as a fraction of the original oil in place of the
        slim-tube test volume step.
    :ivar cumulative_oil_production_sto: The cumulative oil production
        of stock stank oil for the slim-tube test volume step.
    :ivar cumulative_produced_gor: The cumulative oil production GOR for
        the slim-tube test volume step.
    :ivar darcy_velocity: The Darcy velocity of the slim-tube test
        volume step.
    :ivar differential_pressure: The differential pressure of the slim-
        tube test volume step.
    :ivar incremental_produced_gor: The incremental produced GOR of the
        slim-tube test volume step.
    :ivar injected_pore_volume_fraction: The injected pore volume
        fraction of the slim-tube test volume step.
    :ivar injection_volume_at_pump_temperature: The injection volume at
        pump temperature of the slim-tube test volume step.
    :ivar injection_volume_at_test_temperature: The injection volume at
        test temperature of the slim-tube test volume step.
    :ivar remark: Remarks and comments about this data item.
    :ivar run_time: The run time of the slim-tube test volume step.
    :ivar step_number: The step number is the index of a (P,T) step in
        the overall test.
    :ivar mass_balance:
    :ivar produced_gas_properties:
    :ivar produced_oil_properties:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    cumulative_oil_production_perc_ooip: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CumulativeOilProductionPercOOIP",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cumulative_oil_production_sto: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CumulativeOilProductionSTO",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cumulative_produced_gor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CumulativeProducedGOR",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    darcy_velocity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DarcyVelocity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    differential_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DifferentialPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    incremental_produced_gor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IncrementalProducedGOR",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    injected_pore_volume_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InjectedPoreVolumeFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    injection_volume_at_pump_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InjectionVolumeAtPumpTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    injection_volume_at_test_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InjectionVolumeAtTestTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    run_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "RunTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    mass_balance: Optional[MassBalance] = field(
        default=None,
        metadata={
            "name": "MassBalance",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    produced_gas_properties: Optional[ProducedGasProperties] = field(
        default=None,
        metadata={
            "name": "ProducedGasProperties",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    produced_oil_properties: Optional[ProducedOilProperties] = field(
        default=None,
        metadata={
            "name": "ProducedOilProperties",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class SwellingTest:
    """
    Swelling test.

    :ivar remark: Remarks and comments about this data item.
    :ivar test_number: An integer number to identify this test in a
        sequence of tests.
    :ivar test_temperature: The temperature of this test.
    :ivar injected_gas: Reference to the gas injected during the
        swelling test.
    :ivar swelling_test_step:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    test_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    injected_gas: List[InjectedGas] = field(
        default_factory=list,
        metadata={
            "name": "InjectedGas",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    swelling_test_step: List[SwellingTestStep] = field(
        default_factory=list,
        metadata={
            "name": "SwellingTestStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class VaporLiquidEquilibriumTest:
    """
    Properties and results for a vapor-liquid equilibrium (VLE) test.

    :ivar atmospheric_flash_test_reference: Reference to the atmospheric
        flash test for this VLE test.
    :ivar gas_solvent_added: The gas solvent added for this VLE test.
    :ivar liquid_composition: The liquid composition for this VLE test.
    :ivar liquid_phase_volume: The liquid phase volume for this VLE
        test.
    :ivar liquid_transport_test_reference: A reference to a liquid
        transport property test associated with this VLE test.
    :ivar mixture_gas_solvent_mole_fraction: The mixture gas solvent
        mole fraction for this VLE test.
    :ivar mixture_gor: The mixture gas-oil ratio for this VLE test.
    :ivar mixture_psat_test_temperature: The mixture saturation pressure
        test temperature for this VLE test.
    :ivar mixture_relative_volume_relative_to_psat: The mixture relative
        volume relative to volume a saturation pressure for this VLE
        test.
    :ivar mixture_volume: The mixture volume for this VLE test.
    :ivar remark: Remarks and comments about this data item.
    :ivar test_number: An integer number to identify this test in a
        sequence of tests.
    :ivar test_pressure: The pressure of this test.
    :ivar test_temperature: The temperature of this test.
    :ivar vapor_composition: The vapor composition for this VLE test.
    :ivar vapor_phase_volume: The vapor phase volume for this VLE test.
    :ivar vapor_transport_test_reference: A reference to a vapor
        transport property test associated with this VLE test.
    :ivar injected_gas_added: Reference to the injected gas added for
        this VLE test.
    :ivar vapor_phase_density: The vapor phase density for this VLE
        test.
    :ivar liquid_phase_density: The liquid phase density for this VLE
        test.
    :ivar vapor_phase_viscosity: The vapor phase viscosity for this VLE
        test.
    :ivar cumulative_gas_added: Reference to the cumulative gas added
        for this VLE test.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    atmospheric_flash_test_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AtmosphericFlashTestReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_solvent_added: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasSolventAdded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_composition: List[LiquidComposition] = field(
        default_factory=list,
        metadata={
            "name": "LiquidComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_phase_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LiquidPhaseVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_transport_test_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LiquidTransportTestReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mixture_gas_solvent_mole_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MixtureGasSolventMoleFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mixture_gor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MixtureGOR",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mixture_psat_test_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MixturePsatTestTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mixture_relative_volume_relative_to_psat: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MixtureRelativeVolumeRelativeToPsat",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mixture_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MixtureVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    test_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    vapor_composition: List[FluidComponent] = field(
        default_factory=list,
        metadata={
            "name": "VaporComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_phase_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VaporPhaseVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_transport_test_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VaporTransportTestReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    injected_gas_added: Optional[InjectedGas] = field(
        default=None,
        metadata={
            "name": "InjectedGasAdded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_phase_density: List[PhaseDensity] = field(
        default_factory=list,
        metadata={
            "name": "VaporPhaseDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )
    liquid_phase_density: Optional[PhaseDensity] = field(
        default=None,
        metadata={
            "name": "LiquidPhaseDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    vapor_phase_viscosity: Optional[PhaseViscosity] = field(
        default=None,
        metadata={
            "name": "VaporPhaseViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    cumulative_gas_added: Optional[RefInjectedGasAdded] = field(
        default=None,
        metadata={
            "name": "CumulativeGasAdded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class WaterAnalysis:
    """
    Water analysis.
    """

    sample_integrity_and_preparation: Optional[
        SampleIntegrityAndPreparation
    ] = field(
        default=None,
        metadata={
            "name": "SampleIntegrityAndPreparation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_analysis_test: List[WaterAnalysisTest] = field(
        default_factory=list,
        metadata={
            "name": "WaterAnalysisTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_sample_component: List[WaterSampleComponent] = field(
        default_factory=list,
        metadata={
            "name": "WaterSampleComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WellContext:
    """
    Within the context of a WITSML Server, this data should duplicate the
    equivalent information in the well object.

    :ivar direction_well: POSC well direction. The direction of flow of
        the fluids in a well facility (generally, injected or produced,
        or some combination).
    :ivar field_value: Name of the field in which the well is located.
    :ivar fluid_well: POSC well fluid. The type of fluid being produced
        from or injected into a well facility.
    :ivar well_alias: An alias name associated with the well. If the
        well name is associated with a naming system then it should be
        included in this list.
    :ivar well_datum:
    """

    direction_well: Optional[WellDirection] = field(
        default=None,
        metadata={
            "name": "DirectionWell",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    field_value: Optional[NameStruct] = field(
        default=None,
        metadata={
            "name": "Field",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_well: Optional[WellFluid] = field(
        default=None,
        metadata={
            "name": "FluidWell",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_alias: List[NameStruct] = field(
        default_factory=list,
        metadata={
            "name": "WellAlias",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_datum: List[WellDatum] = field(
        default_factory=list,
        metadata={
            "name": "WellDatum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WftTestResult:
    """
    A single result derived from analysis of formation tester data.

    :ivar md_bottom: The bottom of the interval to which this result
        applies.
    :ivar md_top: The top of the interval to which this result applies.
    :ivar method: The name of a proprietary, method which generally
        represents a specialization of a result kind.
    :ivar input_parameter: An input parameter to the analysis method.
    :ivar output_parameter: An output (result) parameter from the
        analysis of the test. The aggregate of parameters might
        represent something like the simulated response of the test, to
        compare with actual.
    :ivar input_result_reference: A reference to an outputParameter of
        another result which was used as an input to this result. For a
        test result, the other result will be in the same test (i.e.,
        ../result). For a station result, the other result will be in
        the same station (i.e., ../result) or will be a test result in
        the same station (../test/result) or will be an
        sampleAcquisition in the same station (i.e.,
        ../sampleAcquisition/result). For a wftRun result, the other
        result will be in the same wftRun (i.e., ../result) or will be a
        result in a station (i.e., ../station/result) or will be a
        result in a station's test (i.e., ../station/test/result) or
        will be a result in a station's sampleAcquisition (i.e.,
        ../station/sampleAcquisition/result). The "../result" notation
        means: starting in the parent node, traverse down to the
        appropriate child result using the provided pointers.
    :ivar test_data: A reference to the formation tester data used to
        derive this result.
    :ivar kind: The kind of result represents a combination of test kind
        and analysis method applied. See enum WftTestKindResult.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    md_bottom: Optional[MeasuredDepthCoord] = field(
        default=None,
        metadata={
            "name": "MdBottom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    md_top: Optional[MeasuredDepthCoord] = field(
        default=None,
        metadata={
            "name": "MdTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    method: Optional[str] = field(
        default=None,
        metadata={
            "name": "Method",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    input_parameter: List[WftInOutParameter] = field(
        default_factory=list,
        metadata={
            "name": "InputParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    output_parameter: List[WftInOutParameter] = field(
        default_factory=list,
        metadata={
            "name": "OutputParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    input_result_reference: List[WftResultReference] = field(
        default_factory=list,
        metadata={
            "name": "InputResultReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_data: List[WftTestData] = field(
        default_factory=list,
        metadata={
            "name": "TestData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: Optional[WftTestResultKind] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class AbstractCompositionalModel(AbstractPvtModel):
    """
    Abstract class of compositional model.

    :ivar binary_interaction_coefficient_set:
    :ivar component_property_set:
    :ivar mixing_rule: The mixing rule which was applied in the
        compositional model. Enum. See mixing rule.
    """

    binary_interaction_coefficient_set: Optional[
        BinaryInteractionCoefficientSet
    ] = field(
        default=None,
        metadata={
            "name": "BinaryInteractionCoefficientSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    component_property_set: Optional[ComponentPropertySet] = field(
        default=None,
        metadata={
            "name": "ComponentPropertySet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mixing_rule: Optional[MixingRule] = field(
        default=None,
        metadata={
            "name": "MixingRule",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class AbstractCorrelationModel(AbstractPvtModel):
    """
    Abstract class of correlation model.
    """


@dataclass
class AssetProductionVolumes(AbstractSimpleProductVolume):
    """Contains all volume data for all reporting entities (e.g., area, field,
    wells, etc.).

    Although named "volumes" in line with industry usage, different
    quantities may be reported, such as volume, mass, and energy
    content.

    :ivar end_date: The end date of report period.
    :ivar nominal_period: Nominal period.
    :ivar start_date: The start date of the reporting period.
    :ivar reporting_entity_volumes:
    """

    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"

    end_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "EndDate",
            "type": "Element",
            "required": True,
        },
    )
    nominal_period: Optional[Union[ReportingDurationKind, str]] = field(
        default=None,
        metadata={
            "name": "NominalPeriod",
            "type": "Element",
            "required": True,
        },
    )
    start_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "StartDate",
            "type": "Element",
            "required": True,
        },
    )
    reporting_entity_volumes: List[ReportingEntityVolumes] = field(
        default_factory=list,
        metadata={
            "name": "ReportingEntityVolumes",
            "type": "Element",
        },
    )


@dataclass
class DownholeSampleAcquisition(FluidSampleAcquisition):
    """
    Additional information required for a sample acquired down hole.

    :ivar base_md: The base MD for the interval where this downhole
        sample was taken.
    :ivar production_well_test:
    :ivar sampling_run: The sampling run number for this downhole sample
        acquisition.
    :ivar tool_kind: The kind of tool used to acquire the downhole
        sample.
    :ivar top_md: The top MD for the interval where this downhole sample
        was taken.
    :ivar wellbore_completion_reference: A reference to the wellbore
        completion (WITSML data object) where this sample was taken.
    :ivar wellbore_reference: A reference to the wellbore (a WITSML data
        object) where this downhole sample was taken.
    """

    base_md: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BaseMD",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    production_well_test: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProductionWellTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sampling_run: Optional[str] = field(
        default=None,
        metadata={
            "name": "SamplingRun",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    tool_kind: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ToolKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    top_md: Optional[str] = field(
        default=None,
        metadata={
            "name": "TopMD",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    wellbore_completion_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellboreCompletionReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellbore_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellboreReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FacilitySampleAcquisition(FluidSampleAcquisition):
    """
    Additional information required for a sample taken from a facility.

    :ivar facility:
    :ivar facility_pressure: The facility pressure for this facility
        sample acquisition.
    :ivar facility_temperature: The facility temperature when this
        sample was taken.
    :ivar sampling_point: A reference to the flow port in the facility
        where this sample was taken.
    """

    facility: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Facility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "FacilityPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    facility_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "FacilityTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    sampling_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SamplingPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FiberCommon(AbstractDtsEquipment):
    """
    A specialization of the equipment class containing information on reflectance,
    loss and reason for decommissioning, from which all equipment in the optical
    path inherits.

    :ivar loss: The fraction of incident light that is lost by a fiber
        path component. Measured in dB.
    :ivar reason_for_decommissioning: Any remarks that help understand
        why the optical fiber is no longer in use.
    :ivar reflectance: The fraction of incident light that is reflected
        by a fiber path component. Measured in dB.
    :ivar uid: Unique identifier of this object.
    """

    loss: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Loss",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reason_for_decommissioning: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReasonForDecommissioning",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reflectance: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Reflectance",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FluidCharacterizationModel:
    """
    Fluid characterization model.

    :ivar name: The name of the fluid analysis result.
    :ivar reference_pressure: The reference pressure for this fluid
        characterization.
    :ivar reference_stock_tank_pressure: The reference stock tank
        pressure for this fluid characterization.
    :ivar reference_stock_tank_temperature: The reference stock tank
        temperature for this fluid characterization.
    :ivar reference_temperature: The reference temperature for this
        fluid characterization.
    :ivar remark: Remarks and comments about this data item.
    :ivar model_specification:
    :ivar fluid_characterization_table:
    :ivar reference_separator_stage:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reference_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReferencePressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reference_stock_tank_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReferenceStockTankPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reference_stock_tank_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReferenceStockTankTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reference_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReferenceTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    model_specification: Optional[AbstractPvtModel] = field(
        default=None,
        metadata={
            "name": "ModelSpecification",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_characterization_table: List[FluidCharacterizationTable] = field(
        default_factory=list,
        metadata={
            "name": "FluidCharacterizationTable",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reference_separator_stage: List[ReferenceSeparatorStage] = field(
        default_factory=list,
        metadata={
            "name": "ReferenceSeparatorStage",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class Instrument(AbstractDtsEquipment):
    """
    The general class of an instrument, including vendor information, in the
    installed system.

    :ivar instrument_vendor: Contact information for the person/company
        that provided the equipment
    """

    instrument_vendor: Optional[BusinessAssociate] = field(
        default=None,
        metadata={
            "name": "InstrumentVendor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class ProductFlowUnit:
    """
    Product Flow Unit Schema.

    :ivar comment: A descriptive remark associated with this unit.
    :ivar context_facility: The name and type of a facility whose
        context is relevant to the represented facility.
    :ivar facility: The name of the facility for which this Product Flow
        Unit describes fluid flow connection behavior. The name can be
        qualified by a naming system. This also defines the kind of
        facility.
    :ivar facility_alias:
    :ivar facility_parent1: For facilities whose name is unique within
        the context of another facility, the name of the parent facility
        this named facility. The name can be qualified by a naming
        system. This also defines the kind of facility.
    :ivar facility_parent2: For facilities whose name is unique within
        the context of another facility, the name of the parent facility
        of facilityParent1. The name can be qualified by a naming
        system. This also defines the kind of facility.
    :ivar internal_network_reference: A pointer to the network
        representing the internal behavior of this unit. The names of
        the external ports on the internal network must match the names
        of the ports on this unit. That is they are logically the same
        ports.
    :ivar name: The name of the ProductFlowUnit within the context of
        the ProductFlowNetwork.
    :ivar plan_name: The name of a network plan. This indicates a
        planned unit. All child network components must all be planned
        and be part of the same plan. The parent network must either
        contain the plan (i.e., be an actual) or be part of the same
        plan. Not specified indicates an actual unit.
    :ivar expected_property: Defines an expected property of the
        facility represented by this unit.
    :ivar port: An inlet or outlet port associated with this unit. If
        there is an internal network then the name of this port must
        match the name of an external port for that network. Any
        properties (e.g., volume, pressure, temperature) that are
        assigned to this port are inherently assigned to the
        corresponding external port on the internal network. That is,
        the ports are logically the same port. Similar to a node, there
        is no pressure drop across a port. Also similar to a node,
        conservation of mass exists across the port and the flow
        direction across the port can change over time if the relative
        pressures across connected units change.
    :ivar relative_coordinate: Defines the relative coordinate of the
        unit on a display screen. This is not intended for detailed
        diagrams. Rather it is intended to allow different applications
        to present a user view which has a consistent layout.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    context_facility: List[FacilityIdentifierStruct] = field(
        default_factory=list,
        metadata={
            "name": "ContextFacility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "Facility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility_alias: List[NameStruct] = field(
        default_factory=list,
        metadata={
            "name": "FacilityAlias",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility_parent1: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "FacilityParent1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility_parent2: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "FacilityParent2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    internal_network_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InternalNetworkReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    plan_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PlanName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    expected_property: List[ProductFlowExpectedUnitProperty] = field(
        default_factory=list,
        metadata={
            "name": "ExpectedProperty",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    port: List[ProductFlowPort] = field(
        default_factory=list,
        metadata={
            "name": "Port",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    relative_coordinate: Optional[RelativeCoordinate] = field(
        default=None,
        metadata={
            "name": "RelativeCoordinate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductVolumeBalanceSet:
    """
    Product Flow Balance Set Schema.

    :ivar cargo_batch_number: A cargo batch number. Used if the vessel
        needs to temporarily disconnect for some reason (e.g., weather).
    :ivar cargo_number: A cargo identifier for the product.
    :ivar shipper: The name of the shipper
    :ivar kind: Defines the aspect being described.
    :ivar balance_detail:
    :ivar destination:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    cargo_batch_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "CargoBatchNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cargo_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CargoNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    shipper: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Shipper",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: Optional[BalanceFlowPart] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    balance_detail: List[ProductVolumeBalanceDetail] = field(
        default_factory=list,
        metadata={
            "name": "BalanceDetail",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    destination: Optional[ProductVolumeDestination] = field(
        default=None,
        metadata={
            "name": "Destination",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionOperationActivity:
    """
    Production Activity Schema.

    :ivar alarm: Infomation about an alarm.
    :ivar cargo_ship_operation: Information about a cargo operation.
    :ivar lost_production: Infomation about a lost production.
    :ivar lost_injection: Infomation about a lost injection.
    :ivar marine_operation: Information about a marine operation.
    :ivar operational_comment: A comment about a kind of operation. The
        time of the operation can be specified.
    :ivar shutdown: Infomation about a shutdown event.
    :ivar water_cleaning_quality: Information about the contaminants in
        water, and the general water quality.
    """

    alarm: List[ProductionOperationAlarm] = field(
        default_factory=list,
        metadata={
            "name": "Alarm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cargo_ship_operation: List[ProductionOperationCargoShipOperation] = field(
        default_factory=list,
        metadata={
            "name": "CargoShipOperation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    lost_production: Optional[ProductionOperationLostProduction] = field(
        default=None,
        metadata={
            "name": "LostProduction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    lost_injection: Optional[ProductionOperationLostProduction] = field(
        default=None,
        metadata={
            "name": "LostInjection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    marine_operation: List[ProductionOperationMarineOperation] = field(
        default_factory=list,
        metadata={
            "name": "MarineOperation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    operational_comment: List[ProductionOperationOperationalComment] = field(
        default_factory=list,
        metadata={
            "name": "OperationalComment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    shutdown: List[ProductionOperationShutdown] = field(
        default_factory=list,
        metadata={
            "name": "Shutdown",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_cleaning_quality: List[
        ProductionOperationWaterCleaningQuality
    ] = field(
        default_factory=list,
        metadata={
            "name": "WaterCleaningQuality",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class ProductionWellTest(AbstractSimpleProductVolume):
    """Production well test data is designed to be transferred upon an event
    happening (the well test being conducted)  or on demand, rather than
    periodically as for asset production volumes.

    For this reason, it is standalone object.

    :ivar reporting_entity:
    :ivar validate: Validate.
    :ivar well_test_method: Description or name of the method used to
        conduct the well test.
    :ivar test_condition:
    """

    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"

    reporting_entity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReportingEntity",
            "type": "Element",
        },
    )
    validate: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Validate",
            "type": "Element",
        },
    )
    well_test_method: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellTestMethod",
            "type": "Element",
        },
    )
    test_condition: Optional[TestCondition] = field(
        default=None,
        metadata={
            "name": "TestCondition",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class SeparatorSampleAcquisition(FluidSampleAcquisition):
    """
    Additonal information required from a fluid sample taken from a separator.

    :ivar corrected_gas_rate: The corrected gas rate for this separator
        sample acquisition.
    :ivar corrected_oil_rate: The corrected oil rate for this separator
        sample acquisition.
    :ivar corrected_water_rate: The corrected water rate for this
        separator sample acquisition.
    :ivar measured_gas_rate: The measured gas rate for this separator
        sample acquisition.
    :ivar measured_oil_rate: The measured oil rate for this separator
        sample acquisition.
    :ivar measured_water_rate: The measured water rate for this
        separator sample acquisition.
    :ivar production_well_test:
    :ivar sampling_point: A reference to the flow port in the facility
        where this sample was taken.
    :ivar separator: A reference to the separator where this sample was
        taken.
    :ivar separator_pressure: The separator pressure when this sample
        was taken.
    :ivar separator_temperature: The separator temperature when this
        sample was taken.
    :ivar well_completion_reference: A reference to a well completion
        (WITSML data object) where this sample was taken.
    """

    corrected_gas_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CorrectedGasRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    corrected_oil_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CorrectedOilRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    corrected_water_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CorrectedWaterRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    measured_gas_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MeasuredGasRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    measured_oil_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MeasuredOilRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    measured_water_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MeasuredWaterRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    production_well_test: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProductionWellTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sampling_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SamplingPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    separator: Optional[str] = field(
        default=None,
        metadata={
            "name": "Separator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    separator_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "SeparatorPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    separator_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "SeparatorTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    well_completion_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellCompletionReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class SlimTubeTestStep:
    """
    Slim-tube test step.

    :ivar remark: Remarks and comments about this data item.
    :ivar step_average_pressure: The average pressure for this slim-tube
        test step.
    :ivar step_number: The step number is the index of a (P,T) step in
        the overall test.
    :ivar slim_tube_test_volume_step:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_average_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StepAveragePressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    step_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    slim_tube_test_volume_step: List[SlimTubeTestVolumeStep] = field(
        default_factory=list,
        metadata={
            "name": "SlimTubeTestVolumeStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class TerminalLifting(AbstractSimpleProductVolume):
    """
    Summarizes product import to or export from an asset by ship.

    :ivar certificate_number: The certificate number for the document
        that defines the lifting onto the tanker.
    :ivar destination_terminal_reference:
    :ivar end_time: The date and time when the lifting ended.
    :ivar loading_terminal_reference:
    :ivar start_time: The date and time when the lifting began.
    :ivar tanker_reference:
    :ivar product_quantity: The amount of product lifted.
    """

    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"

    certificate_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "CertificateNumber",
            "type": "Element",
            "required": True,
        },
    )
    destination_terminal_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DestinationTerminalReference",
            "type": "Element",
        },
    )
    end_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "EndTime",
            "type": "Element",
        },
    )
    loading_terminal_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "LoadingTerminalReference",
            "type": "Element",
            "required": True,
        },
    )
    start_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "StartTime",
            "type": "Element",
        },
    )
    tanker_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "TankerReference",
            "type": "Element",
            "required": True,
        },
    )
    product_quantity: List[ProductFluid] = field(
        default_factory=list,
        metadata={
            "name": "ProductQuantity",
            "type": "Element",
        },
    )


@dataclass
class Transfer(AbstractSimpleProductVolume):
    """Information about products transferred across asset group boundaries or
    leaving the jurisdiction of an operator.

    This may include pipeline exports, output to refineries, etc.

    :ivar destination_facility_reference:
    :ivar end_time: Date and time when the transfer ended.
    :ivar source_facility_reference:
    :ivar start_time: The date and time when the transfer began.
    :ivar product_transfer_quantity: The amount of product transferred.
    :ivar transfer_kind: Specifies the kind of transfer. See enum
        TransferKind.
    """

    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"

    destination_facility_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "DestinationFacilityReference",
            "type": "Element",
            "required": True,
        },
    )
    end_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "EndTime",
            "type": "Element",
        },
    )
    source_facility_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "SourceFacilityReference",
            "type": "Element",
            "required": True,
        },
    )
    start_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "StartTime",
            "type": "Element",
        },
    )
    product_transfer_quantity: List[ProductFluid] = field(
        default_factory=list,
        metadata={
            "name": "ProductTransferQuantity",
            "type": "Element",
        },
    )
    transfer_kind: Optional[TransferKind] = field(
        default=None,
        metadata={
            "name": "TransferKind",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class WellProductionParameters(AbstractSimpleProductVolume):
    """
    Captures well production parameters associated with a well reporting entity.

    :ivar end_date: The ending date of the reporting period.
    :ivar nominal_period: Name or identifier for the reporting period to
        which the well production parameters apply.
    :ivar reporting_entity_reference:
    :ivar start_date: The starting date of the reporting period.
    :ivar production_period: Details of production at a specific choke
        setting.
    """

    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"

    end_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "EndDate",
            "type": "Element",
        },
    )
    nominal_period: Optional[Union[ReportingDurationKind, str]] = field(
        default=None,
        metadata={
            "name": "NominalPeriod",
            "type": "Element",
        },
    )
    reporting_entity_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReportingEntityReference",
            "type": "Element",
        },
    )
    start_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "StartDate",
            "type": "Element",
        },
    )
    production_period: List[ProductionWellPeriod] = field(
        default_factory=list,
        metadata={
            "name": "ProductionPeriod",
            "type": "Element",
        },
    )


@dataclass
class WellheadSampleAcquisition(FluidSampleAcquisition):
    """
    Additional information required for a fluid sample taken from a wellhead.

    :ivar production_well_test:
    :ivar sampling_point: A reference to the flow port in the facility
        where this sample was taken.
    :ivar well_completion_reference: A reference to the well completion
        (WITSML data object) where this sample was taken.
    :ivar wellhead_pressure: The wellhead pressure when the sample was
        taken.
    :ivar wellhead_temperature: The wellhead temperature when the sample
        was taken.
    :ivar well_reference: A reference to the well (WITSML data object)
        where this sample was taken.
    """

    production_well_test: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProductionWellTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sampling_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SamplingPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_completion_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellCompletionReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellhead_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellheadPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    wellhead_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellheadTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    well_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WftSampleAcquisition:
    """
    Information about a single formation tester sample acquisition.

    :ivar cushion_pressure: The pressure that was used to charge the
        sample container.
    :ivar dtim_end: Sampling end time.
    :ivar dtim_start: Sampling start time.
    :ivar field_comment: Comments created by the field engineers
        collecting the sample.
    :ivar gross_fluid_kind: The expected kind of the sample, typically
        oil, water or gas.
    :ivar interpretation_comment: Comments created by the engineers
        analyzing the sample.
    :ivar kind: The kind of sample acquisition.
    :ivar sample_carrier_slot_name: An name for the slot in the sample
        carrier where the sample was acquired.
    :ivar sample_container: A reference to a Fluid Sample Container
        object (optional) which can be used as part of the PVT
        functionality of PRODML to track this sample and its container
        through the lab analysis process.
    :ivar sample_container_configuration: A description of the kind of
        sample container used, for example, whether the container is
        pressurized with nitrogen or not.
    :ivar sample_container_name: An name for the sample bottle that was
        used for this acquisition.
    :ivar sample_name: A name assigned to the sample acquired.
    :ivar sample_reference:
    :ivar test: A reference to a test (uid) under the current station.
    :ivar tool_section_name: An name for the formation tester tool
        section that acquired the sample.
    :ivar test_data: A reference to the associated data acquired during
        this acquisition.
    :ivar result: A result of formation tester analysis that applies to
        this acquisition.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    cushion_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CushionPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    field_comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FieldComment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gross_fluid_kind: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GrossFluidKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    interpretation_comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InterpretationComment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sample_carrier_slot_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SampleCarrierSlotName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sample_container: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SampleContainer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sample_container_configuration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SampleContainerConfiguration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sample_container_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SampleContainerName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sample_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SampleName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sample_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SampleReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Test",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tool_section_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ToolSectionName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_data: List[WftTestData] = field(
        default_factory=list,
        metadata={
            "name": "TestData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    result: List[WftTestResult] = field(
        default_factory=list,
        metadata={
            "name": "Result",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class WftSampleAcquisitionJob(FluidSampleAcquisition):
    """
    Information about the job to take a sample directly from the formation using a
    wireline formation tester (WFT).

    :ivar wft_run:
    :ivar wft_sample_acquisition: Reference to the WFT sample within the
        WFT station from where this sample was obtained.
    :ivar wft_station: Reference to the WFT station within the top-level
        WFT run data object  where this sample was obtained.
    """

    wft_run: Optional[str] = field(
        default=None,
        metadata={
            "name": "WftRun",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    wft_sample_acquisition: Optional[str] = field(
        default=None,
        metadata={
            "name": "WftSampleAcquisition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    wft_station: Optional[str] = field(
        default=None,
        metadata={
            "name": "WftStation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class WftTest:
    """
    Information about a single formation tester test.

    :ivar dtim_end: The date and time when the data collection ended for
        this test.
    :ivar dtim_start: The date and time when the data collection started
        for this test.
    :ivar test_kind: Describes whether the test is associated with a
        pressure buildup or a drawdown. See enum WftTestKind.
    :ivar result: A result of formation tester analysis that applies to
        this test.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    dtim_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_kind: Optional[WftTestKind] = field(
        default=None,
        metadata={
            "name": "TestKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    result: List[WftTestResult] = field(
        default_factory=list,
        metadata={
            "name": "Result",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class AbstractCompositionalEoSmodel(AbstractCompositionalModel):
    """
    Abstract class of compositional EoS model.
    """

    class Meta:
        name = "AbstractCompositionalEoSModel "


@dataclass
class AbstractCompositionalViscosityModel(AbstractCompositionalModel):
    """
    Abstract class of compositional viscosity model.

    :ivar phase: The phase the compositional viscosity model applies to.
    """

    class Meta:
        name = "AbstractCompositionalViscosityModel "

    phase: Optional[ThermodynamicPhase] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AbstractCorrelationViscosityModel(AbstractCorrelationModel):
    """
    Abstract class of correlation viscosity  model.

    :ivar molecular_weight: The molecular weight of the fluid for the
        viscosity model.
    """

    molecular_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MolecularWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class CompositionalThermalModel(AbstractCompositionalModel):
    """A class that AbstractCompositionalModel can inherit; it is NOT abstract
    because the concrete model types have not been specified.

    For now, use the non-abstract thermal model, and use the
    CustomPvtModelExtension to add anything needed. Later, it will be
    made abstract and have concrete classes it inherits from, similar to
    EoS.
    """


@dataclass
class CorrelationThermalModel(AbstractCorrelationModel):
    """A class that AbstractCompositionalModel can inherit; it is NOT abstract
    because the concrete model types have not been specified.

    For now, use the non-abstract thermal model, and use the
    CustomPvtModelExtension to add anything needed. Later, it will be
    made abstract and have concrete classes it inherits from, similar to
    EoS.
    """


@dataclass
class FiberConnection(FiberCommon):
    """
    A connection component within the optical path.

    :ivar connector_type: Specifies whether this is a dry mate or wet
        mate.
    :ivar end_type: Describes whether the fiber end is angle polished or
        flat polished.
    """

    connector_type: List[FiberConnectorTypes] = field(
        default_factory=list,
        metadata={
            "name": "ConnectorType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    end_type: List[FiberEndType] = field(
        default_factory=list,
        metadata={
            "name": "EndType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "sequence": 1,
        },
    )


@dataclass
class FiberOtdrinstrumentBox(Instrument):
    """
    Information about an OTDR instrument box taht is used to perform OTDR surveys
    on the optical path.
    """

    class Meta:
        name = "FiberOTDRInstrumentBox"


@dataclass
class FiberOpticalPathSegment(FiberCommon):
    """A single segment of the optical fiber used for distributed temperature
    surveys.

    Multiple such segments may be connected by other types of components
    including connectors, splices and fiber turnarounds.

    :ivar cladded_diameter: The diameter of the core plus the cladding,
        generally measured in microns (um).
    :ivar coating: The type of coating on the fiber.
    :ivar core_diameter: The inner diameter of the core, generally
        measured in microns (um).
    :ivar core_type: Property of the fiber core.
    :ivar fiber_length: The length of fiber in this optical path
        section.
    :ivar jacket: The type of jacket covering the fiber.
    :ivar mode: The mode of fiber. Enum. Values are single- or multi-
        mode fiber, or other/unknown.
    :ivar outside_diameter: The diameter of the cable containing the
        fiber, including all its sheathing layers.
    :ivar over_stuffing: For this fiber segment, the amount of
        "overstuffing", i.e., the excess length of fiber that was
        installed compared to the length of the facility that is to be
        surveyed. Example: if 110 m of fiber were to be installed to
        measure 100 m length of pipeline, the overstuffing would be 10
        m. Overstuffing can be allowed for in the facilityMapping
        section. The overstuffing is assumed to be linear distributed
        along the facility being measured.
    :ivar parameter: Additional parameters to define the fiber as a
        material.
    :ivar spool_length: The length of the fiber on the spool when
        purchased.
    :ivar spool_number_tag: The spool number of the particular spool
        from which this fiber segment was taken. The spool number may
        contain alphanumeric characters.
    :ivar cable_type: Enum. The type of cable used in this segment.
        Example: single-fiber-cable.
    :ivar fiber_conveyance: The means by which this fiber segment is
        conveyed into the well.
    :ivar one_way_attenuation: The power loss for one way travel of a
        beam of light, usually measured in decibels per unit length. It
        is necessary to include both the value (and its unit) and the
        wavelength. The wavelength varies with the refractive index,
        while the frequency remains constant. The wavelength given to
        specify this type is the wavelength in a vacuum (refractive
        index = 1).
    :ivar refractive_index: The refractive index of a material depends
        on the frequency (or wavelength) of the light. Hence it is
        necessary to include both the value (a unitless number) and the
        frequency (or wavelength) it was measured at. The frequency will
        be a quantity type with a frequency unit such as Hz.
    """

    cladded_diameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CladdedDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    coating: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Coating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    core_diameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CoreDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    core_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CoreType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fiber_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "FiberLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    jacket: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Jacket",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mode: Optional[FiberMode] = field(
        default=None,
        metadata={
            "name": "Mode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    outside_diameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OutsideDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    over_stuffing: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OverStuffing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    parameter: List[IndexedObject] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    spool_length: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SpoolLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    spool_number_tag: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SpoolNumberTag",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cable_type: Optional[CableType] = field(
        default=None,
        metadata={
            "name": "CableType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fiber_conveyance: Optional[FiberConveyance] = field(
        default=None,
        metadata={
            "name": "FiberConveyance",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    one_way_attenuation: List[FiberOneWayAttenuation] = field(
        default_factory=list,
        metadata={
            "name": "OneWayAttenuation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    refractive_index: List[FiberRefractiveIndex] = field(
        default_factory=list,
        metadata={
            "name": "RefractiveIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FiberSplice(FiberCommon):
    """
    A splice component within the optical path.

    :ivar bend_angle: The measurement of the bend on the splice.
    :ivar pressure_rating: The pressure rating for which the splice is
        expected to withstand.
    :ivar protector_type: A useful description of the type of protector
        used in the splice.
    :ivar splice_equipment_used_reference: A useful description of the
        equipment used to create the splice.
    :ivar stripping_type: A useful description of the stripping type
        that was conducted.
    :ivar fiber_splice_type: Enum. The type of splice.
    """

    bend_angle: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BendAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pressure_rating: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PressureRating",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    protector_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProtectorType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    splice_equipment_used_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SpliceEquipmentUsedReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    stripping_type: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StrippingType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fiber_splice_type: Optional[FiberSpliceTypes] = field(
        default=None,
        metadata={
            "name": "FiberSpliceType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FiberTerminator(FiberCommon):
    """The terminator of the optical path.

    This may be a component (in the case of a single ended fiber
    installation), or it may be a connection back into the instrument
    box in the case of a double ended fiber installation.

    :ivar termination_type: Information about the termination used for
        the fiber.
    """

    termination_type: Optional[TerminationType] = field(
        default=None,
        metadata={
            "name": "TerminationType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FiberTurnaround(FiberCommon):
    """
    A turnaround component within the optical path.
    """


@dataclass
class ProductVolumePeriod:
    """
    Product Volume Period Schema.

    :ivar comment: A time-stamped remark about the amounts.
    :ivar date_time:
    :ivar kind: The type of period that is being reported. If not
        specified and a time is not given then the period is defined by
        the reporting period.
    :ivar properties:
    :ivar alert: An indication of some sort of abnormal condition
        relative the values in this period.
    :ivar balance_set: Provides the sales context for this period.
    :ivar component_content: The relative amount of a component product
        in the product stream.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    comment: List[DatedComment] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    date_time: Optional[AbstractDateTimeType] = field(
        default=None,
        metadata={
            "name": "DateTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: Optional[ReportingDurationKind] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    properties: Optional[CommonPropertiesProductVolume] = field(
        default=None,
        metadata={
            "name": "Properties",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    alert: Optional[ProductVolumeAlert] = field(
        default=None,
        metadata={
            "name": "Alert",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    balance_set: List[ProductVolumeBalanceSet] = field(
        default_factory=list,
        metadata={
            "name": "BalanceSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    component_content: List[ProductVolumeComponentContent] = field(
        default_factory=list,
        metadata={
            "name": "ComponentContent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionOperationInstallationReport:
    """
    Installation Report Schema.

    :ivar beds_available: Total count of beds available on the
        installation.
    :ivar installation: The installation represented by this report.
    :ivar work: The total cumulative amount of time worked during the
        reporting period. Commonly specified in units of hours. Note
        that a day unit translates to 24 hours worked.
    :ivar work_month_to_date: The total cumulative amount of time worked
        from the beginning of the month to the end of reporting period.
        Commonly specified in units of hours. Note that a day unit
        translates to 24 hours worked.
    :ivar work_year_to_date: The total cumulative amount of time worked
        from the beginning of the year to the end of reporting period.
        Commonly specified in units of hours. Note that a day unit
        translates to 24 hours worked.
    :ivar crew_count:
    :ivar production_activity: Production activities.
    :ivar operational_hse: Health, Safety and Environmenal information.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    beds_available: Optional[int] = field(
        default=None,
        metadata={
            "name": "BedsAvailable",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    installation: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "Installation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    work: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Work",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    work_month_to_date: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WorkMonthToDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    work_year_to_date: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WorkYearToDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    crew_count: List[CrewCount] = field(
        default_factory=list,
        metadata={
            "name": "CrewCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    production_activity: Optional[ProductionOperationActivity] = field(
        default=None,
        metadata={
            "name": "ProductionActivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    operational_hse: List[ProductionOperationHse] = field(
        default_factory=list,
        metadata={
            "name": "OperationalHSE",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class SlimTubeTest:
    """Attributes of a slim-tube test.

    For definition of a slim-tube test, see
    http://www.glossary.oilfield.slb.com/Terms/s/slim-tube_test.aspx

    :ivar pump_temperature: The pump temperature during the slim-tube
        test.
    :ivar remark: Remarks and comments about this data item.
    :ivar test_number: An integer number to identify this test in a
        sequence of tests.
    :ivar test_temperature: The temperature of this test.
    :ivar slim_tube_specification:
    :ivar slim_tube_test_pressure_step:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    pump_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PumpTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    test_temperature: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    slim_tube_specification: List[SlimTubeSpecification] = field(
        default_factory=list,
        metadata={
            "name": "SlimTubeSpecification",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    slim_tube_test_pressure_step: List[SlimTubeTestStep] = field(
        default_factory=list,
        metadata={
            "name": "SlimTubeTestPressureStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class TerminalLiftingDisposition(AbstractDisposition):
    """Use to report  terminal lifting as dispositions within the periodic asset
    production volumes reporting.

    The components of petroleum disposition are stock change, crude oil losses, refinery inputs, exports, and products supplied for domestic consumption (https://www.eia.gov/dnav/pet/TblDefs/pet_sum_crdsnd_tbldef2.asp)
    """

    terminal_lifting: Optional[TerminalLifting] = field(
        default=None,
        metadata={
            "name": "TerminalLifting",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class TransferDisposition(AbstractDisposition):
    """Use to report  a transfer as dispositions within the periodic asset
    production volumes reporting.

    The components of petroleum disposition are stock change, crude oil losses, refinery inputs, exports, and products supplied for domestic consumption (https://www.eia.gov/dnav/pet/TblDefs/pet_sum_crdsnd_tbldef2.asp)
    """

    transfer: Optional[Transfer] = field(
        default=None,
        metadata={
            "name": "Transfer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WftStation:
    """
    Information about a single station in a wireline formation tester run.

    :ivar description: A description of the station.
    :ivar dia_probe: The diameter of the probe used; only valid if
        flowingIntervalKind is equal to "probe".
    :ivar dtim_end: The date and time when the data collection completed
        for this station.
    :ivar dtim_start: The date and time when the data collection started
        for this station.
    :ivar log_reference: A reference a log containing WFT time-series
        data at this station (may be superset of all the test log
        references at this station).
    :ivar md_bottom: - If flowingIntervalKind = packed interval, then
        the bottom depth of the station. - If flowingIntervalKind =
        probe, then the depth of the probe.
    :ivar md_top: - If flowingIntervalKind = packed interval, then the
        top depth of the station. - If flowingIntervalKind = probe, then
        the depth of the probe.
    :ivar station: References a station containing the flowing interval
        in cases where this station is an observation station.
    :ivar event: A formation tester event that occurs during this
        station.
    :ivar flowing_interval_kind: The type of flowing interval. See enum
        WftFlowingIntervalKind.
    :ivar sample_acquisition: A formation tester sample that is
        collected as part of this station.
    :ivar station_kind: The type of the station (such as, conventional,
        observation).
    :ivar test: A formation tester test period that is recorded as part
        of this station.
    :ivar result: A result of formation tester analysis that applies to
        this station.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    description: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dia_probe: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DiaProbe",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    log_reference: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LogReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    md_bottom: Optional[MeasuredDepthCoord] = field(
        default=None,
        metadata={
            "name": "MdBottom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    md_top: Optional[MeasuredDepthCoord] = field(
        default=None,
        metadata={
            "name": "MdTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    station: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Station",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    event: List[WftEvent] = field(
        default_factory=list,
        metadata={
            "name": "Event",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flowing_interval_kind: Optional[WftFlowingIntervalKind] = field(
        default=None,
        metadata={
            "name": "FlowingIntervalKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    sample_acquisition: List[WftSampleAcquisition] = field(
        default_factory=list,
        metadata={
            "name": "SampleAcquisition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    station_kind: Optional[WftStationKind] = field(
        default=None,
        metadata={
            "name": "StationKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    test: List[WftTest] = field(
        default_factory=list,
        metadata={
            "name": "Test",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    result: List[WftTestResult] = field(
        default_factory=list,
        metadata={
            "name": "Result",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class AbstractCorrelationGasViscosityModel(AbstractCorrelationViscosityModel):
    """
    Abstract class of correlation gas viscosity model.

    :ivar gas_viscosity: The gas viscosity output from the gas viscosity
        model.
    :ivar reservoir_temperature: The reservoir temperature for the gas
        viscosity model.
    """

    gas_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reservoir_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReservoirTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class AbstractCorrelationViscosityBubblePointModel(
    AbstractCorrelationViscosityModel
):
    """
    Abstract class of viscosity bubble point model.

    :ivar bubble_point_oil_viscosity: The bubble point viscosity output
        from the bubble point viscosity model.
    :ivar dead_oil_viscosity: The dead oil viscosity input for the
        bubble point viscosity model.
    :ivar solution_gas_oil_rate: The solution gas oil ratio for the
        bubble point viscosity model.
    """

    bubble_point_oil_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BubblePointOilViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dead_oil_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DeadOilViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    solution_gas_oil_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SolutionGasOilRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class AbstractCorrelationViscosityDeadModel(AbstractCorrelationViscosityModel):
    """
    Abstract class of correlation viscosity dead model.

    :ivar dead_oil_viscosity: The dead oil viscosity output from the
        dead oil viscosity model.
    :ivar reservoir_temperature: The reservoir temperature for the dead
        oil viscosity model.
    """

    dead_oil_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DeadOilViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reservoir_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReservoirTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class AbstractCorrelationViscosityUndersaturatedModel(
    AbstractCorrelationViscosityModel
):
    """
    Abstract class of viscosity under-saturated model.

    :ivar bubble_point_oil_viscosity: The bubble point viscosity input
        for the under saturated viscosity model.
    :ivar bubble_point_pressure: The bubble point pressure for the under
        saturated viscosity model.
    :ivar pressure: The pressure for the under saturated viscosity
        model.
    :ivar undersaturated_oil_viscosity: The under saturated viscosity
        output from the under saturated viscosity model.
    """

    bubble_point_oil_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BubblePointOilViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bubble_point_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BubblePointPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Pressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    undersaturated_oil_viscosity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "UndersaturatedOilViscosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class Cspedersen84(AbstractCompositionalViscosityModel):
    """
    CSPedersen84.
    """

    class Meta:
        name = "CSPedersen84"


@dataclass
class Cspedersen87(AbstractCompositionalViscosityModel):
    """
    CSPedersen87.
    """

    class Meta:
        name = "CSPedersen87"


@dataclass
class FiberOtdr:
    """Records the result arrays along with context information for an optical time
    domain reflectometry (OTDR) survey.

    The arrays define the relative scattered power from the Rayleigh
    scattering vs. distance along the fiber. The actual data values are
    recorded in an OTDR file and/or image file, which are referenced in
    sub-elements.

    :ivar data_in_otdrfile: A reference to the external file used to
        record the OTDR data. Note this file will not be in an
        Energistics format but likely in a special OTDR format.
    :ivar dtim_run: The dateTime of the run.
    :ivar extension_name_value: Extensions to the schema based on a
        name-value construct.
    :ivar measurement_contact: Contact for the person who performed the
        OTDR reading
    :ivar name: The name of this object.
    :ivar optical_path_distance_end: The point measured along the
        optical path at which this OTDR survey ends.
    :ivar optical_path_distance_start: The point measured along the
        optical path at which this OTDR survey starts.
    :ivar otdrimage_file: A reference to the well log used to record the
        table of data.
    :ivar wavelength: The wavelength at which this OTDR survey was
        carried out.
    :ivar fiber_otdrinstrument_box:
    :ivar direction: Enum. The direction of the OTDR survey. "Forward"
        means "in the same direction as the positive direction along the
        optical path".
    :ivar reason_for_run: The reason the OTDR test was run. Reasons
        include: - pre-installation, which is before the installation of
        the fiber - post-installation, which is used to validate a
        successful fiber installation - DTS run, a quality check of the
        fiber before a DTS run - Other
    :ivar uid: Unique identifier of this object.
    """

    class Meta:
        name = "FiberOTDR"

    data_in_otdrfile: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DataInOTDRFile",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_run: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DTimRun",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    extension_name_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ExtensionNameValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    measurement_contact: Optional[BusinessAssociate] = field(
        default=None,
        metadata={
            "name": "MeasurementContact",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    optical_path_distance_end: Optional[str] = field(
        default=None,
        metadata={
            "name": "OpticalPathDistanceEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    optical_path_distance_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "OpticalPathDistanceStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    otdrimage_file: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OTDRImageFile",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wavelength: Optional[str] = field(
        default=None,
        metadata={
            "name": "Wavelength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fiber_otdrinstrument_box: Optional[FiberOtdrinstrumentBox] = field(
        default=None,
        metadata={
            "name": "FiberOTDRInstrumentBox",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    direction: Optional[Otdrdirection] = field(
        default=None,
        metadata={
            "name": "Direction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    reason_for_run: Optional[Otdrreason] = field(
        default=None,
        metadata={
            "name": "ReasonForRun",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class FiberOpticalPathInventory:
    """The list of equipment used in the optical path.

    Equipment may be used in the optical path for different periods of
    time, so this inventory contains all items of equipment that are
    used at some period of time.

    :ivar connection: A connection component within the optical path.
    :ivar segment: A single segment of the optical fiber used for
        distributed temperature surveys. Multiple such segments may be
        connected by other types of component including connectors,
        splices and fiber turnarounds.
    :ivar splice: A splice component within the optical path.
    :ivar terminator: The terminator of the optical path. This may be a
        component (in the case of a single ended fiber installation), or
        it may be a connection back into the instrument box in the case
        of a double ended fiber installation.
    :ivar turnaround: A turnaround component within the optical path.
    """

    connection: List[FiberConnection] = field(
        default_factory=list,
        metadata={
            "name": "Connection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    segment: List[FiberOpticalPathSegment] = field(
        default_factory=list,
        metadata={
            "name": "Segment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )
    splice: List[FiberSplice] = field(
        default_factory=list,
        metadata={
            "name": "Splice",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    terminator: Optional[FiberTerminator] = field(
        default=None,
        metadata={
            "name": "Terminator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    turnaround: List[FiberTurnaround] = field(
        default_factory=list,
        metadata={
            "name": "Turnaround",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FrictionTheory(AbstractCompositionalViscosityModel):
    """
    Friction theory.
    """

    prsv_parameter: List[PrsvParameter] = field(
        default_factory=list,
        metadata={
            "name": "PrsvParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class HydrocarbonAnalysis:
    """
    Hydrocarbon fluid analysis.

    :ivar fluid_component_catalog: The fluid component catalog for this
        fluid analysis.
    :ivar atmospheric_flash_test_and_compositional_analysis: An
        atmospheric flash test and compositional analysis test within
        this fluid analysis.
    :ivar constant_composition_expansion_test: A constant composition
        expansion test within this fluid analysis.
    :ivar constant_volume_depletion_test: A constant volume depletion
        test within this fluid analysis.
    :ivar differential_liberation_test: A differential liberation test
        within this fluid analysis.
    :ivar separator_test: A separator test within this fluid analysis.
    :ivar interfacial_tension_test: An interfacial tension test within
        this fluid analysis.
    :ivar multiple_contact_miscibility_test: A multiple contact
        miscibility test within this fluid analysis.
    :ivar transport_test: A transport test within this fluid analysis.
    :ivar sample_integrity_and_preparation: The sample integrity and
        preparation procedure for this fluid analysis.
    :ivar saturation_test: A saturation test within this fluid analysis.
    :ivar slim_tube_test: A slim tube test within this fluid analysis.
    :ivar stoanalysis: An stock tank oil analysis within this fluid
        analysis.
    :ivar swelling_test: A swelling test within this fluid analysis.
    :ivar vapor_liquid_equilibrium_test: A vapor liquid equilibrium test
        within this fluid analysis.
    """

    fluid_component_catalog: Optional[FluidComponentCatalog] = field(
        default=None,
        metadata={
            "name": "FluidComponentCatalog",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    atmospheric_flash_test_and_compositional_analysis: List[
        AtmosphericFlashTestAndCompositionalAnalysis
    ] = field(
        default_factory=list,
        metadata={
            "name": "AtmosphericFlashTestAndCompositionalAnalysis",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    constant_composition_expansion_test: List[
        ConstantCompositionExpansionTest
    ] = field(
        default_factory=list,
        metadata={
            "name": "ConstantCompositionExpansionTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    constant_volume_depletion_test: List[ConstantVolumeDepletionTest] = field(
        default_factory=list,
        metadata={
            "name": "ConstantVolumeDepletionTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    differential_liberation_test: List[DifferentialLiberationTest] = field(
        default_factory=list,
        metadata={
            "name": "DifferentialLiberationTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    separator_test: List[FluidSeparatorTest] = field(
        default_factory=list,
        metadata={
            "name": "SeparatorTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    interfacial_tension_test: List[InterfacialTensionTest] = field(
        default_factory=list,
        metadata={
            "name": "InterfacialTensionTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    multiple_contact_miscibility_test: List[
        MultipleContactMiscibilityTest
    ] = field(
        default_factory=list,
        metadata={
            "name": "MultipleContactMiscibilityTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    transport_test: List[OtherMeasurementTest] = field(
        default_factory=list,
        metadata={
            "name": "TransportTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sample_integrity_and_preparation: Optional[
        SampleIntegrityAndPreparation
    ] = field(
        default=None,
        metadata={
            "name": "SampleIntegrityAndPreparation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    saturation_test: List[SaturationTest] = field(
        default_factory=list,
        metadata={
            "name": "SaturationTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    slim_tube_test: List[SlimTubeTest] = field(
        default_factory=list,
        metadata={
            "name": "SlimTubeTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    stoanalysis: List[Stoanalysis] = field(
        default_factory=list,
        metadata={
            "name": "STOAnalysis",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    swelling_test: List[SwellingTest] = field(
        default_factory=list,
        metadata={
            "name": "SwellingTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_liquid_equilibrium_test: List[VaporLiquidEquilibriumTest] = field(
        default_factory=list,
        metadata={
            "name": "VaporLiquidEquilibriumTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class LohrenzBrayClarkCorrelation(AbstractCompositionalViscosityModel):
    """
    Lohrenz-Bray-ClarkCorrelation.
    """

    class Meta:
        name = "Lohrenz-Bray-ClarkCorrelation"


@dataclass
class PengRobinson76Eos(AbstractCompositionalEoSmodel):
    """
    PengRobinson76_EOS.
    """

    class Meta:
        name = "PengRobinson76_EOS"


@dataclass
class PengRobinson78Eos(AbstractCompositionalEoSmodel):
    """
    PengRobinson78_EOS.
    """

    class Meta:
        name = "PengRobinson78_EOS"


@dataclass
class ProductVolumeProduct:
    """
    Product Volume Product Schema.

    :ivar kind: The type of product that is being reported.
    :ivar mass_fraction: The weight fraction of the product.
    :ivar mole_fraction: The mole fraction of the product.
    :ivar name: The name of product that is being reported. This is
        reserved for generic kinds like chemical.
    :ivar split_factor: This factor describes the fraction of fluid in
        the source flow that is allocated to this product stream. The
        volumes reported here are derived from the source flow based on
        this split factor. This should be an allocation flow.
    :ivar source_flow:
    :ivar properties:
    :ivar component_content: The relative amount of a component product
        in the product stream.
    :ivar period: Product amounts for a specific period.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    kind: Optional[ReportingProduct] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    mass_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mole_fraction: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MoleFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: Optional[NameStruct] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    split_factor: Optional[float] = field(
        default=None,
        metadata={
            "name": "SplitFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_inclusive": 0.0,
            "max_inclusive": 1.0,
        },
    )
    source_flow: Optional[AbstractRefProductFlow] = field(
        default=None,
        metadata={
            "name": "SourceFlow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    properties: Optional[CommonPropertiesProductVolume] = field(
        default=None,
        metadata={
            "name": "Properties",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    component_content: List[ProductVolumeComponentContent] = field(
        default_factory=list,
        metadata={
            "name": "ComponentContent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    period: List[ProductVolumePeriod] = field(
        default_factory=list,
        metadata={
            "name": "Period",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
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
class SrkEos(AbstractCompositionalEoSmodel):
    """
    Srk_EOS.
    """

    class Meta:
        name = "Srk_EOS"


@dataclass
class BerganAndSuttonUndersaturated(
    AbstractCorrelationViscosityUndersaturatedModel
):
    """
    Bergan And Sutton-Undersaturated.
    """

    class Meta:
        name = "BerganAndSutton-Undersaturated"


@dataclass
class BerganSuttonDead(AbstractCorrelationViscosityDeadModel):
    """
    BerganSutton-Dead.

    :ivar dead_oil_viscosity_at100_f: The dead oil viscosity at 100 f
        input to the dead oil viscosity model.
    :ivar dead_oil_viscosity_at210_f: The dead oil viscosity at 210 f
        input to the dead oil viscosity model.
    """

    class Meta:
        name = "BerganSutton-Dead"

    dead_oil_viscosity_at100_f: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DeadOilViscosityAt100F",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dead_oil_viscosity_at210_f: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DeadOilViscosityAt210F",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class BergmanSuttonBubblePoint(AbstractCorrelationViscosityBubblePointModel):
    """
    BergmanSutton-BubblePoint.
    """

    class Meta:
        name = "BergmanSutton-BubblePoint"


@dataclass
class CarrDempsey(AbstractCorrelationGasViscosityModel):
    """
    CarrDempsey.

    :ivar gas_molar_weight: The molecular weight of the gas as an input
        to this viscosity correlation.
    :ivar gas_viscosity_at1_atm: The gas viscosity at 1 atm for the
        viscosity correlation.
    :ivar pseudo_reduced_pressure: The pseudo reduced pressure for the
        viscosity correlation.
    :ivar pseudo_reduced_temperature: The pseudo reducedtemperature for
        the viscosity correlation.
    """

    gas_molar_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasMolarWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_viscosity_at1_atm: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasViscosityAt1Atm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pseudo_reduced_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PseudoReducedPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pseudo_reduced_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PseudoReducedTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DeGhettoBubblePoint(AbstractCorrelationViscosityBubblePointModel):
    """
    DeGhetto-BubblePoint.
    """

    class Meta:
        name = "DeGhetto-BubblePoint"


@dataclass
class DeGhettoDead(AbstractCorrelationViscosityDeadModel):
    """
    DeGhetto-Dead.

    :ivar oil_apiat_stock_tank: The oil API at stock tank for the
        viscosity correlation.
    """

    class Meta:
        name = "DeGhetto-Dead"

    oil_apiat_stock_tank: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilAPIAtStockTank",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DeGhettoUndersaturated(AbstractCorrelationViscosityUndersaturatedModel):
    """
    DeGhetto-Undersaturated.

    :ivar reservoir_temperature: The reservoir temperature for the
        viscosity correlation.
    :ivar solution_gas_oil_ratio: The solution gas-oil ratio for the
        viscosity correlation.
    """

    class Meta:
        name = "DeGhetto-Undersaturated"

    reservoir_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReservoirTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    solution_gas_oil_ratio: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SolutionGasOilRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DindorukChristmanBubblePoint(
    AbstractCorrelationViscosityBubblePointModel
):
    """
    DindorukChristman-BubblePoint.
    """

    class Meta:
        name = "DindorukChristman-BubblePoint"


@dataclass
class DindorukChristmanDead(AbstractCorrelationViscosityDeadModel):
    """
    DindorukChristman-Dead.

    :ivar oil_gravity_at_stock_tank: The oil gravity at stock tank for
        the viscosity correlation.
    """

    class Meta:
        name = "DindorukChristman-Dead"

    oil_gravity_at_stock_tank: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilGravityAtStockTank",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DindorukChristmanUndersaturated(
    AbstractCorrelationViscosityUndersaturatedModel
):
    """
    DindorukChristman-Undersaturated.

    :ivar reservoir_temperature: The reservoir temperature for the
        viscosity correlation.
    :ivar solution_gas_oil_ratio: The solution gas-oil ratio for the
        viscosity correlation.
    """

    class Meta:
        name = "DindorukChristman-Undersaturated"

    reservoir_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReservoirTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    solution_gas_oil_ratio: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SolutionGasOilRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class LeeGonzalez(AbstractCorrelationGasViscosityModel):
    """
    LeeGonzalez.

    :ivar gas_density: The gas density at the conditions for this
        viscosity correlation to be used.
    :ivar gas_molar_weight: The molecular weight of the gas as an input
        to this viscosity correlation.
    """

    gas_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_molar_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasMolarWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class LondonoArcherBlasinggame(AbstractCorrelationGasViscosityModel):
    """
    LondonoArcherBlasinggame.

    :ivar gas_density: The gas density at the conditions for this
        viscosity correlation to be used.
    :ivar gas_viscosity_at1_atm: The gas viscosity at 1 atm for the
        viscosity correlation.
    :ivar gas_viscosity_coefficient1_atm:
    """

    gas_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_viscosity_at1_atm: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasViscosityAt1Atm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_viscosity_coefficient1_atm: List[PvtModelParameter] = field(
        default_factory=list,
        metadata={
            "name": "GasViscosityCoefficient1Atm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class Lucas(AbstractCorrelationGasViscosityModel):
    """
    Lucas.

    :ivar gas_molar_weight: The molecular weight of the gas as an input
        to this viscosity correlation.
    :ivar gas_viscosity_at1_atm: The gas viscosity at 1 atm for the
        viscosity correlation.
    :ivar pseudo_critical_pressure: The pseudo critical pressure for the
        viscosity correlation.
    :ivar pseudo_critical_temperature: The pseudo critical temperature
        for the viscosity correlation.
    :ivar pseudo_reduced_pressure: The pseudo reduced pressure for the
        viscosity correlation.
    :ivar pseudo_reduced_temperature: The pseudo reduced temperature for
        the viscosity correlation.
    """

    gas_molar_weight: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasMolarWeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_viscosity_at1_atm: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasViscosityAt1Atm",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pseudo_critical_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PseudoCriticalPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pseudo_critical_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PseudoCriticalTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pseudo_reduced_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PseudoReducedPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pseudo_reduced_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PseudoReducedTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class PetroskyFarshadBubblePoint(AbstractCorrelationViscosityBubblePointModel):
    """
    PetroskyFarshad-BubblePoint.
    """

    class Meta:
        name = "PetroskyFarshad-BubblePoint"


@dataclass
class PetroskyFarshadDead(AbstractCorrelationViscosityDeadModel):
    """
    PetroskyFarshad-Dead.

    :ivar oil_gravity_at_stock_tank: The oil gravity at stock tank
        conditions for this viscosity correlation.
    """

    class Meta:
        name = "PetroskyFarshad-Dead"

    oil_gravity_at_stock_tank: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilGravityAtStockTank",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class PetroskyFarshadUndersaturated(
    AbstractCorrelationViscosityUndersaturatedModel
):
    """
    PetroskyFarshad-Undersaturated.
    """

    class Meta:
        name = "PetroskyFarshad-Undersaturated"


@dataclass
class ProductVolumeFlow:
    """
    Product Volume Flow Component Schema.

    :ivar direction: Direction.
    :ivar facility: Facility.
    :ivar facility_alias: Facility alias.
    :ivar kind: Indicates the type of flow that is being reported. The
        type of flow is an indication of the overall source or target of
        the flow.  - A production flow has one or more wells as the
        originating source.  - An injection flow has one or more wells
        as the ultimate target.  - An import flow has an offsite source.
        - An export flow has an offsite target. - A consumption flow
        generally has a kind of equipment as a target.
    :ivar name: The name of this flow within the context of this report.
        This might reflect some combination of the kind of flow, port,
        qualifier and related facility.
    :ivar port: Port.
    :ivar qualifier: Qualifies the type of flow that is being reported.
    :ivar source_flow: This is a pointer to the flow from which this
        flow was derived.
    :ivar sub_qualifier: Defines a specialization of the qualifier
        value. This should only be given if a qualifier is given.
    :ivar version: Version.
    :ivar version_source: Identifies the source of the version. This
        will commonly be the name of the software which created the
        version.
    :ivar properties:
    :ivar product: Reports a product flow stream.
    :ivar related_facility:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    direction: Optional[ProductFlowPortType] = field(
        default=None,
        metadata={
            "name": "Direction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "Facility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility_alias: List[NameStruct] = field(
        default_factory=list,
        metadata={
            "name": "FacilityAlias",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kind: Optional[ReportingFlow] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    port: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Port",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    qualifier: Optional[FlowQualifier] = field(
        default=None,
        metadata={
            "name": "Qualifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    source_flow: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SourceFlow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    sub_qualifier: Optional[FlowSubQualifier] = field(
        default=None,
        metadata={
            "name": "SubQualifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    version: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Version",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    version_source: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VersionSource",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    properties: Optional[CommonPropertiesProductVolume] = field(
        default=None,
        metadata={
            "name": "Properties",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    product: List[ProductVolumeProduct] = field(
        default_factory=list,
        metadata={
            "name": "Product",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    related_facility: Optional[ProductVolumeRelatedFacility] = field(
        default=None,
        metadata={
            "name": "RelatedFacility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class StandingBubblePoint(AbstractCorrelationViscosityBubblePointModel):
    """
    Standing-BubblePoint.
    """

    class Meta:
        name = "Standing-BubblePoint"


@dataclass
class StandingDead(AbstractCorrelationViscosityDeadModel):
    """
    Standing-Dead.

    :ivar oil_gravity_at_stock_tank: The oil gravity at stock tank for
        the viscosity model.
    """

    class Meta:
        name = "Standing-Dead"

    oil_gravity_at_stock_tank: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilGravityAtStockTank",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class StandingUndersaturated(AbstractCorrelationViscosityUndersaturatedModel):
    """
    Standing-Undersaturated.

    :ivar reservoir_temperature: The reservoir temperature for the
        viscosity model.
    :ivar solution_gas_oil_ratio: The solution gas oil ratio for the
        viscosity model.
    """

    class Meta:
        name = "Standing-Undersaturated"

    reservoir_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReservoirTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    solution_gas_oil_ratio: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SolutionGasOilRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class ProductVolumeFacility:
    """
    Report Facility Schema.

    :ivar capacity: The storage capacity of the facility (e.g., a tank).
    :ivar comment:
    :ivar downtime_reason:
    :ivar facility_alias: An alternative name of a facility. This is
        generally unique within a naming system. The above contextually
        unique name (that is, within the context of a parent) should
        also be listed as an alias.
    :ivar facility_parent: Facility parent.
    :ivar facility_parent2: Facility parent2.
    :ivar fluid_well: POSC well fluid. The type of fluid being produced
        from or injected into a well facility.
    :ivar name: The name of the facility. The name can be qualified by a
        naming system. This also defines the kind of facility.
    :ivar net_work: Network.
    :ivar operation_time: The amount of time that the facility was
        active during the reporting period.
    :ivar status_well: Status of the well.
    :ivar unit: Unit.
    :ivar well_injecting: True (or 1) indicates that the well is
        injecting. False (or 0) or not given indicates that the well is
        not injecting. This only applies if the facility is a well or
        wellbore.
    :ivar well_producing: True (or 1) indicates that the well is
        producing. False (or 0) or not given indicates that the well is
        not producing. This only applies if the facility is a well or
        wellbore.
    :ivar flow: Reports a flow of a product.
    :ivar parameter_set:
    :ivar operating_method: The lift method being used to operate the
        well.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    capacity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Capacity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    comment: List[DatedComment] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    downtime_reason: List[DatedComment] = field(
        default_factory=list,
        metadata={
            "name": "DowntimeReason",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility_alias: List[NameStruct] = field(
        default_factory=list,
        metadata={
            "name": "FacilityAlias",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility_parent: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "FacilityParent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    facility_parent2: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "FacilityParent2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_well: Optional[WellFluid] = field(
        default=None,
        metadata={
            "name": "FluidWell",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    name: Optional[FacilityIdentifierStruct] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    net_work: List[str] = field(
        default_factory=list,
        metadata={
            "name": "NetWork",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    operation_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OperationTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    status_well: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StatusWell",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    unit: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_injecting: Optional[bool] = field(
        default=None,
        metadata={
            "name": "WellInjecting",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_producing: Optional[bool] = field(
        default=None,
        metadata={
            "name": "WellProducing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flow: List[ProductVolumeFlow] = field(
        default_factory=list,
        metadata={
            "name": "Flow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    parameter_set: List[ProductVolumeParameterSet] = field(
        default_factory=list,
        metadata={
            "name": "ParameterSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    operating_method: Optional[WellOperationMethod] = field(
        default=None,
        metadata={
            "name": "OperatingMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
