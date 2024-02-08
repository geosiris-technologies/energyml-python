from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class AbstractAnalysis:
    """Forces a choice between pressure analysis (PTA) with flow as a boundary
    condition, and flowrate analysis (RTA) with pressure as a boundary condition.

    Applies to the measured data and to the simulation.
    """


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
class AbstractDeconvolutionOutput:
    """Forces a choice between: in some deconvolution methods, multiple individual deconvolution outputs are generated, each specific to a corresponding individual Test Period. In such cases multiple instances of the deconvolutionOutput element will recur. In other cases, there will be only one such output across all Test Periods."""


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
    supplier: List[str] = field(
        default_factory=list,
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
class AbstractFiberFacility:
    """
    The abstract base type of FiberFacility.
    """


@dataclass
class AbstractFluidComponent:
    """
    The Abstract base type of FluidComponent.

    :ivar concentration_relative_to_detectable_limits: This element can
        be used where a measurement for a concentration is only capable
        of a "yes/no" type accuracy. Values can be ADL (meaning the
        measurement was Above Detectable Limits) or BDL (meaning the
        measurement was Below Detectable Limits). If the condition is
        "ADL" then the concentration as reported in Mass Fraction or
        Mole Fraction is expected to represent the maximum value which
        can be distinguished (so that we know the actual value to be
        equal to or greater than that). If the condition is "BDL" then
        the concentration as reported in Mass Fraction or Mole Fraction
        is expected to represent the minimum value which can be
        distinguished (so that we know the actual value to be equal to
        or less than that).
    :ivar mass_fraction: The fluid mass fraction.
    :ivar mole_fraction: The fluid mole fraction.
    :ivar volume_concentration:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    concentration_relative_to_detectable_limits: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConcentrationRelativeToDetectableLimits",
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
    volume_concentration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VolumeConcentration",
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
class AbstractMeasureData:
    """
    The abstract base type of measure data.
    """


@dataclass
class AbstractModelSection:
    """
    The abstract class of model section that forces a choice between a wellbore
    base or a reservoir base.

    :ivar comment: The method used for this section of the results. Text
        description. No semantic meaning.
    :ivar method: The method used for this section of the results. Text
        description. No semantic meaning.
    """

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
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


@dataclass
class AbstractOilVolShrinkage:
    """
    The abstract class of oil volume shrinkage.
    """


@dataclass
class AbstractParameter:
    """Abstract for a single parameter relating to a pressure transient analysis.

    Collected together in Result Section Models. Eg, all the parameters
    needed for a closed boundary model will be found in the
    ClosedRectangleModel.

    :ivar remark: Textual description about the value of this field.
    :ivar source_result_ref_id: This is a reference to a different
        Result, which is the source for this parameter. It therefore
        only applies when the Direction is "input". Example: an estimate
        for permeability may be obtained in one result and then used as
        input to constrain a second result, such as one estimating
        distance to a fault. In this case, the second result would show
        "input" direction for permeability parameter, and its
        SourceResultRefID would point to the first result from which
        permeability was obtained.
    :ivar uid: Unique identifier for this instance of the object.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    source_result_ref_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SourceResultRefID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "name": "Uid",
            "type": "Attribute",
            "required": True,
        },
    )


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
class AbstractRateHistory:
    """
    Forces a choice between a single flowrate and producing time, or a time series
    of rates, for the Rate History of a pressure transient result.
    """


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
class AnalysisLine:
    """
    Describes a straight line on any analysis plot.

    :ivar intercept: The intercept of the line.
    :ivar line_name: The name of the line.
    :ivar remark: Textual description about the value of this field.
    :ivar slope: The slope of the line.
    """

    intercept: Optional[float] = field(
        default=None,
        metadata={
            "name": "Intercept",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    line_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LineName",
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
    slope: Optional[float] = field(
        default=None,
        metadata={
            "name": "Slope",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


class AnionKind(Enum):
    B_OH_4 = "B(OH)4-"
    BR = "Br-"
    CL = "Cl-"
    CO3_2 = "CO3-2"
    F = "F-"
    HCO3 = "HCO3-"
    HS = "HS-"
    I = "I-"
    NO2 = "NO2-"
    NO3_2 = "NO3-2"
    OH = "OH-"
    PO4_3 = "PO4-3"
    S_2 = "S-2"
    SO4_2 = "SO4-2"


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


class Boundary1Type(Enum):
    CONSTANT_PRESSURE = "constant pressure"
    NO_FLOW = "no-flow"


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


class CableKind(Enum):
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
class CalendarMonth:
    """A month of a year (CCYY-MM).

    A time zone is not allowed. This type is meant to capture original
    invariant values. It is not intended to be used in "time math" where
    knowledge of the time zone is needed.
    """


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


class CationKind(Enum):
    AL_3 = "Al+3"
    B_3 = "B+3"
    BA_2 = "Ba+2"
    BE_2 = "Be+2"
    CA_2 = "Ca+2"
    CD_2 = "Cd+2"
    CO_2 = "Co+2"
    CR_3 = "Cr+3"
    CU_2 = "Cu+2"
    FE_2 = "Fe+2"
    FE_3 = "Fe+3"
    K = "K+"
    LI = "Li+"
    MG_2 = "Mg+2"
    MN_2 = "Mn+2"
    MO_6 = "Mo+6"
    NA = "Na+"
    NH4 = "NH4+"
    NI_2 = "Ni+2"
    P_3 = "P+3"
    PB_2 = "Pb+2"
    RB_1 = "Rb+1"
    SE_4 = "Se+4"
    SI_4 = "Si+4"
    SN_4 = "Sn+4"
    SR_2 = "Sr+2"
    TI_4 = "Ti+4"
    TL_1 = "Tl+1"
    V_2 = "V+2"
    ZN_2 = "Zn+2"


@dataclass
class Channel:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class ChannelSet:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


class CompressibilityKind(Enum):
    AVERAGE = "average"
    POINT = "point"


@dataclass
class CompressibilityParameters:
    """
    Compressibility and saturation values.

    :ivar formation_compressibility: Formation Compressibility of the
        reservoir.
    :ivar gas_phase_saturation: Gas Phase Saturation in the reservoir.
    :ivar oil_phase_saturation: Oil Phase Saturation in the reservoir.
    :ivar total_compressibility: Total system compressibility -
        formation compressibility + saturation-weighted fluid
        compressibilities.
    :ivar water_phase_saturation: Water Phase Saturation in the
        reservoir.
    """

    formation_compressibility: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FormationCompressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    gas_phase_saturation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GasPhaseSaturation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    oil_phase_saturation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OilPhaseSaturation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_compressibility: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalCompressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    water_phase_saturation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WaterPhaseSaturation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


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


class ControlLineEncapsulationKind(Enum):
    """
    Specifies the control line encapsulation types.

    :cvar ROUND: round
    :cvar SQUARE: square
    """

    ROUND = "round"
    SQUARE = "square"


class ControlLineEncapsulationSize(Enum):
    """
    Specifies the control line encapsulation sizes.

    :cvar VALUE_11X11: 11x11
    :cvar VALUE_23X11: 23x11
    """

    VALUE_11X11 = "11x11"
    VALUE_23X11 = "23x11"


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


class DasCalibrationColumn(Enum):
    """
    This enum controls the possible types of columns allowed in a Calibration
    record in HDF5.
    """

    FACILITY_LENGTH = "FacilityLength"
    LOCUS_INDEX = "LocusIndex"
    OPTICAL_PATH_DISTANCE = "OpticalPathDistance"


class DasCalibrationInputPointKind(Enum):
    """The kind of calibration point.

    This is an extensible enumeration type. Current enum values are ‘tap
    test’ and ‘other calibration point’. Other commonly used calibration
    points are understood to be packers, sub surface safety valves,
    perforations, all of which give recognizable noise signals observed
    in the DAS data.  At the time of issue of this standard there is not
    a consensus regarding which other values should be regarded as
    standard kinds of calibration input points.

    :cvar OTHER_CALIBRATION_POINT: A Calibration Input Point which is of
        any kind other than a Tap Test.
    :cvar TAP_TEST: A tap test Calibration Input Point.
    """

    OTHER_CALIBRATION_POINT = "other calibration point"
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
        data array stored in the corresponding HDF data file. Time zone
        should be included. Sub-second precision should be included
        where applicable but not zero-padded.
    :ivar part_start_time: The timestamp in human readable, ISO 8601
        format of the first recorded sample in the sub-record of the raw
        data array stored in the corresponding HDF data file. Time zone
        should be included. Sub-second precision should be included
        where applicable but not zero-padded.
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
        the end time of the corresponding data set stored in multiple
        HDF5 files. The end time of the sub-record stored in an
        individual HDF5 file is stored in PartEndTime. Time zone should
        be included. Sub-second precision should be included where
        applicable but not zero-padded.
    :ivar start_time: The timestamp in human readable, ISO 8601 format
        of the last recorded sample in the acquisition. Note that this
        is the start time of the acquisition if a raw dataset is stored
        in multiple HDF files. The end time of the sub-record stored in
        an individual HDF file is stored in PartStartTime.
    :ivar time_array:
    :ivar uom: The unit of measure of the intervals in the time array.
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
            "required": True,
        },
    )
    time_array: Optional[str] = field(
        default=None,
        metadata={
            "name": "TimeArray",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "Uom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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

    end_time: List[str] = field(
        default_factory=list,
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
    start_time: List[str] = field(
        default_factory=list,
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


class DeferredKind(Enum):
    """
    Specifies the deferment status of the event.
    """

    PLANNED = "planned"
    UNPLANNED = "unplanned"


class DetectableLimitRelativeStateKind(Enum):
    ADL = "ADL"
    BDL = "BDL"


class DispositionKind(Enum):
    """
    Specifies the set of categories used to account for how crude oil and petroleum
    products are transferred, distributed, or removed from the supply stream
    (e.g.,stock change, crude oil losses, exports, sales, etc.).

    :cvar BUYBACK: Buyback is the purchase/transfer of hydrocarbon from
        off-lease facilities to the lease for the purpose of using it in
        the lease for operation purposes.
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

    BUYBACK = "buyback"
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
            "required": True,
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
    """
    Forces a choice between a qualifier or one more qualified by flow and product.
    """


@dataclass
class Facility:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


class FacilityKind(Enum):
    """
    The facility kind, (for example, wellbore, pipeline, etc).

    :cvar GENERIC: The calibration affects the acquisition which runs
        neither inside a well or a pipeline.
    :cvar PIPELINE: The calibration affects the acquisition which runs
        inside a pipeline.
    :cvar WELLBORE:
    """

    GENERIC = "generic"
    PIPELINE = "pipeline"
    WELLBORE = "wellbore"


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


class FiberConnectorKind(Enum):
    """
    Specifies the types of fiber connector.

    :cvar DRY_MATE: dry mate
    :cvar WET_MATE: wet mate
    """

    DRY_MATE = "dry mate"
    WET_MATE = "wet mate"


class FiberEndKind(Enum):
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


class FiberSpliceKind(Enum):
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
class FlowTestActivity:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class FlowTestJob:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class FlowTestLocation:
    """Describes the location of the reservoir connection from which pressure and/or flow are being measured.
    BUSINESS RULE: Can be one of: (i) a named wellbore (a WITSML object) together with a MD Interval; (ii) a named Wellbore Completion (a WITSML object with physical details of a completion), (iii) a named well (a WITSML object), (iv) a named Reporting Entity (which is a generic object to represent a location for flow reporting in the PRODML Simple Product Volume Reporting schema), or (v) a Probe on a wireline or LWD formation tester tool, in which case it has single Probe Depth and Probe Diameter.
    A wellbore + MD Interval, or a wellbore completion option would be expected for most tests.  The well, or well completion options could be used for a test commingling flow multiple wellbores or completions.  See the WITSML documentation for Completion for more details. The Reporting Entity option could be used for the testing of some less common combination of sources, eg a cluster of wells.
    NOTE that well, wellbore, well completion, wellbore completion and reporting entity elements are all Data Object References (see Energistics Common documentation). These are used to reference separate data objects which fully describe the real-world facilities concerned.
    However, it is not necessary for the separate data object to exist. The elements can be used as follows:
    - The Title element of the data object reference class is used to identify the name of the real-world facility, eg the well name, as a text string.
    - The mandatory Content Type element would contain the class of the referenced object (the same as the element name).
    - The mandatory  UUID String can contain any dummy uuid-like string.

    :ivar datum: Textual description about the value of this field.
    :ivar md_interval: A reference, using data object reference, to the
        MdInterval which represents this flowing interval.
    :ivar probe_depth: The depth of a probe if this is the connection to
        reservoir in a wireline or LWD formation tester tool. A single
        depth rather than a range.
    :ivar probe_diameter: The diameter of a probe if this is the
        connection to reservoir in a wireline or LWD formation tester
        tool. The probe diameter governs the area open to flow from the
        formation.
    :ivar remark: Textual description about the value of this field.
    :ivar reporting_entity: A reference, using data object reference, to
        the ReportingEntity which represents this flowing interval.
    :ivar well: A reference, using data object reference, to the Well
        which represents this flowing interval.
    :ivar wellbore: A reference, using data object reference, to the
        Wellbore which represents this flowing interval.
    :ivar wellbore_completion: A reference, using data object reference,
        to the WellboreCompletion which represents this flowing
        interval.
    :ivar well_completion: A reference, using data object reference, to
        the WellCompletion which represents this flowing interval.
    """

    datum: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Datum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    md_interval: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MdInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    probe_depth: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProbeDepth",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    probe_diameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProbeDiameter",
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
    reporting_entity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReportingEntity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Well",
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
    wellbore_completion: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellboreCompletion",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_completion: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellCompletion",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


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

    :ivar fluid_analysis:
    :ivar fluid_analysis_test_reference: A reference to a fluid analysis
        test which was used as source data for this fluid
        characterization.
    """

    fluid_analysis: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FluidAnalysis",
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
class FluidComponentFraction:
    """Fractions of a flluid component.

    It's expected but not required that only one of the fractions will
    be populated.

    :ivar concentration_relative_to_detectable_limits: This element can
        be used where a measurement for a concentration is only capable
        of a "yes/no" type accuracy. Values can be ADL (meaning the
        measurement was Above Detectable Limits) or BDL (meaning the
        measurement was Below Detectable Limits). If the condition is
        "ADL" then the concentration as reported in Mass Fraction or
        Mole Fraction is expected to represent the maximum value which
        can be distinguished (so that we know the actual value to be
        equal to or greater than that). If the condition is "BDL" then
        the concentration as reported in Mass Fraction or Mole Fraction
        is expected to represent the minimum value which can be
        distinguished (so that we know the actual value to be equal to
        or less than that).
    :ivar kvalue: K value.
    :ivar mass_fraction: The mass fraction for the fluid component.
    :ivar mole_fraction: The mole fraction for the fluid component.
    :ivar volume_concentration:
    :ivar volume_fraction:
    :ivar fluid_component_reference: Fluid component reference.
    """

    concentration_relative_to_detectable_limits: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConcentrationRelativeToDetectableLimits",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
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
    volume_concentration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VolumeConcentration",
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

    acentric_factor: Optional[float] = field(
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
    volume_shift_parameter: Optional[float] = field(
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
    :ivar end_time:
    :ivar fluid_sample:
    :ivar fluid_sample_container:
    :ivar formation_pressure: The formation pressure when this sample
        was taken.
    :ivar formation_pressure_temperature_datum: The datum depth for
        which the Formation Pressure and Formation Temperature data
        applies.
    :ivar formation_temperature: The formation temperature when this
        sample was taken.
    :ivar remark: Remarks and comments about this data item.
    :ivar start_time: The date when the sample was taken.
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
    end_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fluid_sample: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidSample",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fluid_sample_container: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidSampleContainer",
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
    formation_pressure_temperature_datum: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FormationPressureTemperatureDatum",
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
    start_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartTime",
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
class FluidSampleAcquisitionJob:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class FluidSampleAcquisitionJobSource:
    """
    Reference to the fluid sample acquisition within a fluid sample acquisition job
    which acquired this fluid sample.

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
class FluidSampleContainer:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class FluidSystem:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


class FractureModelType(Enum):
    COMPRESSIBLE_FINITE_CONDUCTIVITY = "compressible finite conductivity"
    FINITE_CONDUCTIVITY = "finite conductivity"
    INFINITE_CONDUCTIVITY = "infinite conductivity"
    UNIFORM_FLUX = "uniform flux"


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


class InterventionConveyanceKind(Enum):
    """
    Specifies the types of intervention conveyance.
    """

    COILED_TUBING = "coiled tubing"
    ROD = "rod"
    SLICKLINE = "slickline"
    WIRELINE = "wireline"


@dataclass
class LocationIn2D:
    """
    A location expressed in terms of X,Y coordinates of some part of a PTA object.

    :ivar coordinate_x: X coordinate of a point.
    :ivar coordinate_y: Y coordinate of a point.
    """

    coordinate_x: Optional[str] = field(
        default=None,
        metadata={
            "name": "CoordinateX",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    coordinate_y: Optional[str] = field(
        default=None,
        metadata={
            "name": "CoordinateY",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


class LogLogPressureTransform(Enum):
    """Enum of the pressure axis transform of a log-log plot.

    "Pressure Function" refers to the pressure as transformed according
    to the choice of pseudo pressure.  See enum
    PressureNonLinearTransformType in the pvtForPTA section for details
    on this choice.

    :cvar DELTA_PRESSURE_FUNCTION: X axis is delta pressure function
        (which may be a pseudo pressure function).
    :cvar DELTA_PRESSURE_FUNCTION_RATE: X axis is delta pressure
        function (which may be a pseudo pressure function) divided by
        flowrate.
    :cvar INTEGRAL_RATE_NORMAL_DELTA_P_FUNCT_TIME: X axis is integral of
        rate normalized delta pressure function (which may be a pseudo
        pressure function) divided by time.
    :cvar RATE_NORMALIZED_DELTA_P_FUNCTION_RATE: X axis is rate
        normalized delta pressure function (which may be a pseudo
        pressure function) divided by rate.
    :cvar OTHER:
    """

    DELTA_PRESSURE_FUNCTION = "delta pressure function"
    DELTA_PRESSURE_FUNCTION_RATE = "delta pressure function/rate"
    INTEGRAL_RATE_NORMAL_DELTA_P_FUNCT_TIME = (
        "integral rate normal delta p funct/time"
    )
    RATE_NORMALIZED_DELTA_P_FUNCTION_RATE = (
        "rate normalized delta p function/rate"
    )
    OTHER = "other"


class LogLogTimeTransform(Enum):
    """Enum of the time axis transform of a log-log plot.

    The choices are between different ways of dealing with superposition
    effects from variable flowrates.
    """

    AGARWAL_TIME = "agarwal time"
    DELTA_TIME = "delta time"
    EQUIVALENT_TIME_CUMULATIVE_FLOWRATE = "equivalent time cumulative/flowrate"
    SUPERPOSITION_TIME = "superposition time"


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


@dataclass
class Otdracquisition:
    class Meta:
        name = "OTDRAcquisition"
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


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


class OrganicAcidKind(Enum):
    COO_22 = "(COO)22-"
    C2_H5_OCOO = "C2H5OCOO-"
    C3_H5_O_COO_33 = "C3H5O(COO)33-"
    CH2_COO_22 = "CH2(COO)22-"
    CH2_OHCOO = "CH2OHCOO-"
    CH3_CH2_2_COO = "CH3(CH2)2COO-"
    CH3_CH2_3_COO = "CH3(CH2)3COO-"
    CH3_CH2_COO = "CH3CH2COO-"
    CH3_COO = "CH3COO-"
    HCOO = "HCOO-"


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
    :cvar NORMALIZED_PSEUDO_PRESSURE: Normalised pseudo pressure derived
        from Pseudo Pressure m(P) as follows Normalized pseudo pressure
        = m(P)*ref viscosity/ref pressure. The reference viscosity and
        pressure used in this normalization should be reported as Table
        Constants in the table in which this Normalized pseudo pressure
        is tabulated versus pressure. Normalized pseudo pressure is used
        in gas well and multi-phase pressure transient analysis.
    :cvar OIL_GAS_RATIO: The oil-gas ratio in a vapour-liquid system.
        UoM: volume/volume.
    :cvar OIL_WATER_INTERFACIAL_TENSION: Oil-water interfacial tension.
    :cvar PARACHOR: Parachor is the quantity defined according to the
        formula: P = ?1/4 M / D. Where ?1/4 is the fourth root of
        surface tension.
    :cvar PRESSURE: Pressure. UoM: pressure.
    :cvar PSEUDO_PRESSURE: Pseudo pressure with measurement units
        pressure^2/viscosity and usual symbol m(P). Tabulated versus
        pressure and used in gas well pressure transient analysis.
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
    NORMALIZED_PSEUDO_PRESSURE = "Normalized Pseudo Pressure"
    OIL_GAS_RATIO = "Oil-Gas Ratio"
    OIL_WATER_INTERFACIAL_TENSION = "Oil-Water Interfacial Tension"
    PARACHOR = "Parachor"
    PRESSURE = "Pressure"
    PSEUDO_PRESSURE = "Pseudo Pressure"
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
    """
    Owner business account.
    """


class PathDefectKind(Enum):
    """
    Specifies the types of fiber zone that can be reported on.

    :cvar DARKENED_FIBER: darkened fiber
    :cvar OTHER: other
    """

    DARKENED_FIBER = "darkened fiber"
    OTHER = "other"


class PermanentCableInstallationKind(Enum):
    """
    Specifies the types of permanent cable installations.
    """

    BURIED_PARALLEL_TO_TUBULAR = "buried parallel to tubular"
    CLAMPED_TO_TUBULAR = "clamped to tubular"
    WRAPPED_AROUND_TUBULAR = "wrapped around tubular"


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


class PlusComponentKind(Enum):
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
class PressureTransientAnalysis:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


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

    dtim: Optional[str] = field(
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
    dtim: List[str] = field(
        default_factory=list,
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
    dtim: Optional[str] = field(
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


class PseudoComponentKind(Enum):
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
    :cvar RSH: Mercaptans/thiols for all alkyl types R.
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
    RSH = "rsh"


@dataclass
class PtaDataPreProcess:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


@dataclass
class PtaDeconvolution:
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"


class PureComponentKind(Enum):
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
    :cvar COS: Carbonyl sulfide with molecular structure OCS.
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
    :cvar RA: Radon
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
    COS = "cos"
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
    RA = "ra"
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
class RecombinedSampleFraction:
    """For a fluid sample that has been recombined from separate samples, each
    sample has its fraction recorded in this class and the source sample is
    referenced.

    E.g., a fraction and reference to an oil sample and a second
    instance with fraction and reference to gas sample.

    :ivar fluid_sample: The fluid sample.
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
class RefInjectedGasAdded:
    """
    A reference to the particular gas quantity injected, using a uid which refers
    to an Injected Gas, and the quantity as a molar ratio injected.

    :ivar injection_gas_reference: Reference by uid to the Injection Gas
        used for this quantity of injected gas.
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
    Relative xyz location offset.

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
    """Contains a relative volume (ie volume/reference volume), and the identity of
    the reference volume and/or volume measurement conditions, by means of a uid.

    This uid will correspond to the uid of the appropriate Fluid Volume
    Reference.

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

    :ivar reporting_entity:
    :ivar child_node:
    :ivar id: The identification of node.
    :ivar name: The entity name.
    """

    reporting_entity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReportingEntity",
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


@dataclass
class ResqmlModelRef:
    """
    A reference to a RESQML Model element containing the data relating to the PTA
    object concerned.

    :ivar resqml_model_ref: Reference to the RESQML model element which
        represents this feature.
    """

    resqml_model_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResqmlModelRef",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


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

    :ivar end_time:
    :ivar mixing_mechanism: The mixing mechanism when the sample is
        restored in preparation for analysis.
    :ivar remark: Remarks and comments about this data item.
    :ivar restoration_pressure: The restoration pressure when the sample
        is restored in preparation for analysis.
    :ivar restoration_temperature: The restoration temperature when the
        sample is restored in preparation for analysis.
    :ivar start_time:
    """

    end_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EndTime",
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
    start_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StartTime",
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


class SaturationKind(Enum):
    """
    Specifies the kinds of saturation.

    :cvar SATURATED: The fluid is saturated.
    :cvar UNDERSATURATED: The fluid is under-saturated.
    """

    SATURATED = "saturated"
    UNDERSATURATED = "undersaturated"


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


class SulfurComponentKind(Enum):
    VALUE_2_3_2_4_DIMETHYL_THIOPHENE = "2-3 & 2-4 dimethyl thiophene"
    VALUE_2_5_DIMETHYL_THIOPHENE = "2-5-dimethyl thiophene"
    VALUE_2_ETHYL_THIOPHENE = "2-ethyl thiophene"
    VALUE_2_METHYL_1_BUTANETHIOL = "2-methyl 1-butanethiol"
    VALUE_2_METHYL_THIPOPHENE = "2-methyl thipophene"
    VALUE_3_4_DIMETHYL_THIOPHENE = "3-4-dimethyl thiophene"
    VALUE_3_ETHYL_THIOPHENE = "3-ethyl thiophene"
    VALUE_3_METHYL_THIPOPHENE = "3-methyl thipophene"
    BENZOTHIOPHENE = "benzothiophene"
    CARBON_DISULFIDE = "carbon disulfide"
    CARBONYL_SULFIDE = "carbonyl sulfide"
    DIBUTYL_SULFIDE = "dibutyl sulfide"
    DIETHYL_DISULFIDE = "diethyl disulfide"
    DIETHYL_SULFIDE = "diethyl sulfide"
    DIMETHYL_DISULFIDE = "dimethyl disulfide"
    DIMETHYL_SULFIDE = "dimethyl sulfide"
    DIPROPYL_SULFIDE = "dipropyl sulfide"
    DI_SEC_BUTYL_SULFIDE = "di-sec.butyl sulfide"
    DITERT_BUTYL_SULFIDE = "ditert.butyl sulfide"
    ETHYL_ISOPROPYL_DISULFIDE = "ethyl isopropyl disulfide"
    ETHYL_MERCAPTAN = "ethyl mercaptan"
    ETHYL_METHYL_SULFIDE = "ethyl-methyl sulfide"
    HYDROGEN_SULFIDE = "hydrogen sulfide"
    ISOBUTYL_MERCAPTAN = "isobutyl mercaptan"
    ISOPENTYL_MERCAPTAN = "isopentyl mercaptan"
    ISOPROPYL_MERCAPTAN = "isopropyl mercaptan"
    METHYL_ISOPROPYL_SULFIDE = "methyl isopropyl sulfide"
    METHYL_MERCAPTAN = "methyl mercaptan"
    N_BUTYL_MERCAPTAN = "n-butyl mercaptan"
    N_HEPTYL_MERCAPTAN = "n-heptyl mercaptan"
    N_HEXYL_MERCAPTAN = "n-hexyl mercaptan"
    N_NONYL_MERCAPTAN = "n-nonyl mercaptan"
    N_OCTYL_MERCAPTAN = "n-octyl mercaptan"
    N_PENTYL_MERCAPTAN = "n-pentyl mercaptan"
    N_PROPYL_MERCAPTAN = "n-propyl mercaptan"
    SEC_BUTYL_MERCAPTAN = "sec-butyl mercaptan"
    TERT_BUTYL_MERCAPTAN = "tert-butyl mercaptan"
    TETRA_HYDRO_THIOPHENE = "tetra-hydro thiophene"
    THIOPHENE = "thiophene"


class TerminationKind(Enum):
    """
    Specifies the types of fiber terminations.
    """

    LOOPED_BACK_TO_INSTRUMENT_BOX = "looped back to instrument box"
    TERMINATION_AT_CABLE = "termination at cable"


class TestPeriodKind(Enum):
    """This is the type of test period: drawdowns or build up for producing flow tests and injection or fall-off for injecting well tests; or observation tests. Producing or injecting can be constant rate or variable rate. The periods where measurements are made but the testing tool is in motion, are covered by the "run in hole" and "pull out of hole" values."""

    BUILDUP = "buildup"
    CONSTANT_RATE_INJECTION = "constant rate injection"
    FALL_OFF = "fall-off"
    POST_TEST_PULL_OUT_OF_HOLE = "post-test pull out of hole"
    PRE_TEST_RUN_IN_HOLE = "pre-test run in hole"
    PRODUCTION_WELL_TEST = "production well test"
    VARIABLE_RATE_INJECTION = "variable rate injection"
    CONSTANT_RATE_DRAWDOWN = "constant rate drawdown"
    SHUT_IN_OBSERVATION = "shut-in observation"
    VARIABLE_RATE_DRAWDOWN = "variable rate drawdown"


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


class TimeSeriesPointRepresentation(Enum):
    """The representation of the points in the time series data: Point By Point meaning instantaneous measurements, or Stepwise Value At End Of Period meaning that the value reported has applied from the previous point up to the time reported."""

    POINT_BY_POINT = "point by point"
    STEPWISE_VALUE_AT_END_OF_PERIOD = "stepwise value at end of period"


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

    d_tim: Optional[str] = field(
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

    :cvar RESERVOIR:
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
    :cvar TEST_STEP:
    :cvar OTHER:
    """

    RESERVOIR = "reservoir"
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
    TEST_STEP = "test step"
    OTHER = "other"


@dataclass
class WellFlowingCondition:
    """
    Describes key conditions of the flowing well during a production well test.

    :ivar base_usable_water: The lowest usable water depth as measured
        from the surface. See TxRRC H-15.
    :ivar bottom_hole_pressure_datum_md: The measure depth datum for
        which the bottomhole pressure is reported.  This will later be
        converted to a TVD for reservoir engineering purpose.
    :ivar bottom_hole_stabilized_pressure: The pressure at the bottom of
        the hole under stabilized conditions (typically at the end of
        the flowing period).
    :ivar bottom_hole_stabilized_temperature: The temperature at the
        bottom of the hole under stabilized conditions (typically at the
        end of the flowing period).
    :ivar casing_head_stabilized_pressure: The pressure at the casing
        head under stabilized conditions (typically at the end of the
        flowing period).
    :ivar casing_head_stabilized_temperature: The temperature at the
        casing head under stabilized conditions (typically at the end of
        the flowing period).
    :ivar choke_orifice_size: The choke diameter.
    :ivar fluid_level: The fluid level achieved in the well. The value
        is given as length units from the well vertical datum.
    :ivar tubing_head_stabilized_pressure: The pressure at the tubing
        head under stabilized conditions (typically at the end of the
        flowing period).
    :ivar tubing_head_stabilized_temperature: The temperature at the
        tubing head under stabilized conditions (typically at the end of
        the flowing period).
    """

    base_usable_water: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BaseUsableWater",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bottom_hole_pressure_datum_md: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BottomHolePressureDatumMd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bottom_hole_stabilized_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BottomHoleStabilizedPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bottom_hole_stabilized_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BottomHoleStabilizedTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    casing_head_stabilized_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CasingHeadStabilizedPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    casing_head_stabilized_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CasingHeadStabilizedTemperature",
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
    fluid_level: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FluidLevel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tubing_head_stabilized_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TubingHeadStabilizedPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tubing_head_stabilized_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TubingHeadStabilizedTemperature",
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
    month: Optional[CalendarMonth] = field(
        default=None,
        metadata={
            "name": "Month",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class AbstractDisposition:
    """
    The Abstract base type of disposition.

    :ivar disposition_quantity: The amount of product to which this
        disposition applies.
    :ivar product_disposition_code: A unique disposition code associated
        within a given naming system. This may be a code specified by a
        regulatory agency.
    :ivar remark: A descriptive remark relating to this disposition.
    :ivar quantity_method: Quantity method.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    disposition_quantity: List[AbstractProductQuantity] = field(
        default_factory=list,
        metadata={
            "name": "DispositionQuantity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
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
class AbstractFlowTestData:
    """
    The abstract class of flow test data from which all flow data components
    inherit.

    :ivar channel_set: A grouping of channels with a compatible index,
        for some purpose. Each channel has its own index. A ‘compatible’
        index simply means that all of the channels are either in time
        or in depth using a common datum.
    :ivar remark: Textual description about the value of this field.
    :ivar time_channel: The Channel containing the Time data.
    :ivar time_series_point_representation: .The representation of the
        points in the time series data: Point By Point meaning
        instantaneous measurements, or Stepwise Value At End Of Period
        meaning that the value reported has applied from the previous
        point up to the time reported.
    :ivar uid: The unique identifier of this Flow Test Data.
    """

    channel_set: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChannelSet",
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
    time_channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "TimeChannel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    time_series_point_representation: Optional[
        TimeSeriesPointRepresentation
    ] = field(
        default=None,
        metadata={
            "name": "TimeSeriesPointRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class AngleBetweenBoundaries(AbstractParameter):
    """In a boundary model with two Intersecting Faults, the angle of intersection.

    90 degress indicates two boundaries which are normal to each other.
    """

    abbreviation: str = field(
        init=False,
        default="AngleBetweenBoundaries",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "Angle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class AveragePressure(AbstractParameter):
    """The average pressure of the fluids in the reservoir layer.

    "Average" is taken to refer to "at the time at which the rate
    history used in the pressure transient analysis ends".
    """

    abbreviation: str = field(
        init=False,
        default="Pbar",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class BinaryInteractionCoefficientSet:
    """
    Binary interaction coefficient set.

    :ivar binary_interaction_coefficient: Binary interaction
        coefficient.
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
class BoundaryBaseModel(AbstractModelSection):
    """
    Abstract boundary model from which the other types are derived.
    """

    pore_volume_of_investigation: Optional[str] = field(
        default=None,
        metadata={
            "name": "PoreVolumeOfInvestigation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    radius_of_investigation: Optional[str] = field(
        default=None,
        metadata={
            "name": "RadiusOfInvestigation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
    :ivar density_value: A possibly temperature and pressure corrected
        desity value.
    :ivar efficiency: The actual volume divided by the potential volume.
    :ivar flow_rate_value: A possibly temperature and pressure corrected
        flow rate value.
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
    :ivar volume_value: A possibly temperature and pressure corrected
        volume value.
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

    :ivar fluid_component_property: The properties of a fluid component.
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
class CompoundExternalArray:
    """Three instances of the Columns element are used to provide the order of the
    columns of data in the associated Compound External Array.

    Each instance will contain one the three enum values: FacilityLength, LocusIndex, OpticalPathDistance, which make up the array.

    :ivar values: Reference to an HDF5 dataset.
    :ivar columns: Specifies the ordering of the columns of a
        Calibration array in the HDF5 file. A Calibration array contains
        columns for the following quantities: Facility Length, Locus
        Index and Optical Path Distance. The order of these columns is
        flexible but is specified by this element. It comprises three
        values, each of which must be one of the values of the enum
        DasCalibrationColumn, which are the three quantities listed
        above.
    """

    values: Optional[str] = field(
        default=None,
        metadata={
            "name": "Values",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    columns: List[DasCalibrationColumn] = field(
        default_factory=list,
        metadata={
            "name": "Columns",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 3,
            "max_occurs": 3,
        },
    )


@dataclass
class ConvergenceSkinRelativeToTotalThickness(AbstractParameter):
    """Dimensionless value, characterizing the restriction to flow (+ve value,
    convergence) or additional capacity for flow (-ve value, fractured or
    horizontal wellbore) owing to the geometry of the wellbore connection to
    reservoir.

    This value is stated with respect to radial flow using the full
    reservoir thickness (h), ie the radial flow or middle time region of
    a pressure transient. It therefore can be added to
    "MechancialSkinRelativeToTotalThickness" to yield the
    "SkinRelativeToTotalThickness".
    """

    abbreviation: str = field(
        init=False,
        default="Sconv",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
class CurveData(AbstractMeasureData):
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
class CustomParameter(AbstractParameter):
    """A single custom parameter relating to a pressure transient analysis.

    This type can be added in the Custom model section elements (for
    wellbore, near wellbore, reservoir and boundary sections of the PTA
    model), or in a Specialized Analysis.  The custom parameter is to
    enable extensibility beyond the types of parameter built in to the
    schema.  It has to have a name (for the parameter, eg
    "AlphaPressure"), an abbreviation (eg "AP") and a measure value
    using the generalMeasureType. This type does not enforce restricted
    units of measure but a uom needs to be specified which it is assumed
    will be used to work out what dimensional type this parameter
    belongs to.

    :ivar abbreviation: The abbreviation of the parameter. Expected to
        be one of the abbreviation elements of the parameters in the
        parameterTypeSet of the "Models loader file" xml.
    :ivar measure_value: The value of the parameter. The measurement
        kind (length etc) is not known since it will vary according to
        parameter type. The UoM attribute is expected to match those for
        the measure class element for this Parameter as specified in the
        "Model loader file" xml for the parameterType concerned.
    :ivar name: The name of the parameter. Expected to be one of the
        name elements of the parameters in the parameterTypeSet of the
        "Models loader file" xml.  The parameter names expected are
        those listed as "parameter" under the model within the category
        of the appropriate result section.
    """

    abbreviation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    measure_value: Optional[GeneralMeasureType] = field(
        default=None,
        metadata={
            "name": "MeasureValue",
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


@dataclass
class CustomPvtModelExtension:
    """
    Custom PVT model extension.

    :ivar description: A description of the custom model.
    :ivar custom_pvt_model_parameter: Custom PVT model parameter.
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
class DasCalibrationInputPoint:
    """This object contains, for a given parent Calibration, the inputs to the
    calibration process.

    Each such point is represented by an instance of this object. Each such instance represents a place where a physical feature of the fiber optical path or the facility can be observed as a signal in the DAS data.  For example, a tap test is where a noise (tapping) is generated at a known place (a known location in the facility), and can be seen in the DAS signal at a specific locus.  This fact is recorded in one instance of this object.  Over time it is expected that other commonly used noise generating locations will be listed in the enum for InputPointType.
    Business Rule: Note that it is possible to have a valid Calibration comprising only a collection of DasCalibrationInputPoint. It is not a requirement to also have the corresponding "look up table" of a collection of FiberLocusDepthPoint.  If the receiving application can create its own interpolation of locus depth points then the collection of DasCalibrationInputPoint is all that is needed.

    :ivar facility_length: The ‘facility length’ corresponding to the
        locus. The ‘facility length’ is the length along the physical
        facility (eg measured depth if the facility is a wellbore). This
        length corrects the optical path distance for the offset from
        previous facilities on the same fiber optical path, surface
        patch cord lengths, overstuffing, additional fiber in
        turnaround-subs or H-splices that increase the optical path
        length on the OTDR, but not the actual facility length. Facility
        length is the value which is required to associate the DAS data
        at a locus with a physical location, but at the time of the
        Calibration this may not be known and so this element is
        optional.
    :ivar locus_index: The locus index for the calibration point. Where
        ‘Locus Index 0’ is generally understood to mean, the acoustic
        sample point at the connector of the measurement instrument.
    :ivar optical_path_distance: The optical path distance (ie, the
        distance along the fiber) from the connector of the measurement
        instrument to the acoustic sample point (with the given locus
        index) of the calibration point. Mandatory since any Calibration
        Input Point must have a known optical oath distance.
    :ivar remark: A brief meaningful description of the type of
        calibration point. This is an extensible enumeration type.
        Current reserved keywords are ‘locus calibration’, ‘tap test’
        and ‘last locus to end of fiber’ for commonly used calibration
        points.
    :ivar input_point_kind: The kind of calibration point. This is an
        extensible enumeration type. Current enum values are ‘tap test’
        and ‘other calibration point’. Other commonly used calibration
        points are understood to be packers, sub surface safety valves,
        perforations, all of which give recognizable noise signals
        observed in the DAS data.  At the time of issue of this standard
        there is not a consensus regarding which other values should be
        regarded as standard kinds of calibration input points.
    """

    facility_length: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FacilityLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    locus_index: Optional[str] = field(
        default=None,
        metadata={
            "name": "LocusIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    optical_path_distance: Optional[str] = field(
        default=None,
        metadata={
            "name": "OpticalPathDistance",
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
    input_point_kind: Optional[
        Union[DasCalibrationInputPointKind, str]
    ] = field(
        default=None,
        metadata={
            "name": "InputPointKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
    :ivar fbe_data_index: The nth (zero-based) count of this DasFbeData
        in the DasFbe.  Recommended if there is more than 1 dataset in
        this FBE.  This index corresponds to the FbeData array number in
        the HDF5 file.
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
class DeferredProductionVolume:
    """
    The production volume deferred for the reporting period.

    :ivar deferred_product_quantity:
    :ivar remark: Remarks and comments about this data item.
    :ivar estimation_method: The method used to estimate deferred
        production. See enum EstimationMethod.
    """

    deferred_product_quantity: Optional[AbstractProductQuantity] = field(
        default=None,
        metadata={
            "name": "DeferredProductQuantity",
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
class DeltaPressureTotalSkin(AbstractParameter):
    """The pressure drop caused by the total skin factor.

    Equal to the difference in pressure at the wellbore between what was
    observed at a flowrate and what would be observed if the radial flow
    regime in the reservoir persisted right into the wellbore. The
    reference flowrate will be the stable flowrate used to analyse a
    drawdown, or the stable last flowrate preceding a buildup.
    """

    abbreviation: str = field(
        init=False,
        default="dP Skin",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DeltaTimeStorageChanges(AbstractParameter):
    """
    In models in which the wellbore storage coefficient changes, the time at which
    the intial wellbore storage coefficient changes to the final coefficient.
    """

    abbreviation: str = field(
        init=False,
        default="dT",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    time: Optional[str] = field(
        default=None,
        metadata={
            "name": "Time",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DistanceFractureToBottomBoundary(AbstractParameter):
    """
    For a horizontal ("pancake") induced hydraulic fracture, the distance between
    the plane of the fracture and the lower boundary of the layer.
    """

    abbreviation: str = field(
        init=False,
        default="Zf",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DistanceMidFractureHeightToBottomBoundary(AbstractParameter):
    """
    For a hydraulic fracture, the distance between the mid-height level of the
    fracture and the lower boundary of the layer.
    """

    abbreviation: str = field(
        init=False,
        default="Zf",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DistanceMidPerforationsToBottomBoundary(AbstractParameter):
    """
    For a partial penetration (a vertical or slant well with less than full layer
    thickness open to flow) , the distance from the mid-perforation point to the
    bottom boundary of the layer.
    """

    abbreviation: str = field(
        init=False,
        default="Zp",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DistanceToBoundary1(AbstractParameter):
    """In any bounded reservoir model, the distance to the Boundary 1.

    The orientation of this can be thought of conceptually (ie in
    relationship to other boundaries in the model, not literally) as
    "East".
    """

    abbreviation: str = field(
        init=False,
        default="L1",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DistanceToBoundary2(AbstractParameter):
    """In any bounded reservoir model, the distance to the Boundary 2.

    The orientation of this can be thought of conceptually (ie in
    relationship to other boundaries in the model, not literally) as
    "North".
    """

    abbreviation: str = field(
        init=False,
        default="L2",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DistanceToBoundary3(AbstractParameter):
    """In any bounded reservoir model, the distance to the Boundary 3.

    The orientation of this can be thought of conceptually (ie in
    relationship to other boundaries in the model, not literally) as
    "West".
    """

    abbreviation: str = field(
        init=False,
        default="L3",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DistanceToBoundary4(AbstractParameter):
    """In any bounded reservoir model, the distance to the Boundary 4.

    The orientation of this can be thought of conceptually (ie in
    relationship to other boundaries in the model, not literally) as
    "South".
    """

    abbreviation: str = field(
        init=False,
        default="L4",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DistanceToMobilityInterface(AbstractParameter):
    """
    In a Radial or Linear Composite model, the distance to the boundary of the
    inner and outer zones.
    """

    abbreviation: str = field(
        init=False,
        default="Li",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DistanceToPinchOut(AbstractParameter):
    """
    In a model where the reservoir model is a Pinch Out, the distance from the
    wellbore to the pinch-out.
    """

    abbreviation: str = field(
        init=False,
        default="Lpinch",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DistanceWellboreToBottomBoundary(AbstractParameter):
    """
    For a horizontal wellbore model, the distance between the horizontal wellbore
    and the lower boundary of the layer.
    """

    abbreviation: str = field(
        init=False,
        default="Zw",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DistributedParametersSubModel:
    """For a Reservoir model in which parameters are spatially distributed, this is
    the model sub class which identifies which parameters have been spatially
    sampled, and provides a reference to the RESQML object containing the sampled
    data.

    This is expected to be a numerical model.

    :ivar is_depth_gridded: Boolean. If True then parameter Depth is
        defined by values distributed on a grid in a RESQML model.  In
        this case the DepthArrayRefID element will provide the location
        of the gridded properties in the RESQML model.
    :ivar is_kv_to_kr_gridded: Boolean. If True then parameter KvToKr is
        defined by values distributed on a grid in a RESQML model.  In
        this case the KvToKrArrayRefID element will provide the location
        of the gridded properties in the RESQML model.
    :ivar is_kx_to_ky_gridded: Boolean. If True then parameter KxToKy is
        defined by values distributed on a grid in a RESQML model.  In
        this case the KxToKyArrayRefID element will provide the location
        of the gridded properties in the RESQML model.
    :ivar is_permeability_gridded: Boolean. If True then parameter
        Permeability is defined by values distributed on a grid in a
        RESQML model.  In this case the PermeabilityArrayRefIDelement
        will provide the location of the gridded properties in the
        RESQML model.
    :ivar is_porosity_gridded: Boolean. If True then parameter Porosity
        is defined by values distributed on a grid in a RESQML model.
        In this case the PorosityArrayRefID element will provide the
        location of the gridded properties in the RESQML model.
    :ivar is_thickness_gridded: Boolean. If True then parameter
        Thickness is defined by values distributed on a grid in a RESQML
        model.  In this case the ThicknessArrayRefID element will
        provide the location of the gridded properties in the RESQML
        model.
    :ivar permeability_array_ref_id: Reference to RESQML grid containing
        Permeability values.
    :ivar thickness_array_ref_id: Reference to RESQML grid containing
        Thickness values.
    :ivar porosity_array_ref_id: Reference to RESQML grid containing
        Porosity values.
    :ivar depth_array_ref_id: Reference to RESQML grid containing Depth
        values.
    :ivar kv_to_kr_array_ref_id: Reference to RESQML grid containing
        KvToKr values.
    :ivar kx_to_ky_array_ref_id: Reference to RESQML grid containing
        KxToKy values.
    """

    is_depth_gridded: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsDepthGridded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    is_kv_to_kr_gridded: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsKvToKrGridded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    is_kx_to_ky_gridded: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsKxToKyGridded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    is_permeability_gridded: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPermeabilityGridded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    is_porosity_gridded: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsPorosityGridded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    is_thickness_gridded: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsThicknessGridded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    permeability_array_ref_id: Optional[ResqmlModelRef] = field(
        default=None,
        metadata={
            "name": "PermeabilityArrayRefID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    thickness_array_ref_id: Optional[ResqmlModelRef] = field(
        default=None,
        metadata={
            "name": "ThicknessArrayRefID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    porosity_array_ref_id: Optional[ResqmlModelRef] = field(
        default=None,
        metadata={
            "name": "PorosityArrayRefID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    depth_array_ref_id: Optional[ResqmlModelRef] = field(
        default=None,
        metadata={
            "name": "DepthArrayRefID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kv_to_kr_array_ref_id: Optional[ResqmlModelRef] = field(
        default=None,
        metadata={
            "name": "KvToKrArrayRefID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    kx_to_ky_array_ref_id: Optional[ResqmlModelRef] = field(
        default=None,
        metadata={
            "name": "KxToKyArrayRefID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DownholeSampleAcquisition(FluidSampleAcquisition):
    """
    Additional information required for a sample acquired down hole.

    :ivar base_md: The base MD for the interval where this downhole
        sample was taken.
    :ivar flow_test_activity:
    :ivar sampling_run: The sampling run number for this downhole sample
        acquisition.
    :ivar tool_kind: The kind of tool used to acquire the downhole
        sample.
    :ivar tool_serial_number:
    :ivar top_md: The top MD for the interval where this downhole sample
        was taken.
    :ivar wellbore: A reference to the wellbore (a WITSML data object)
        where this downhole sample was taken.
    :ivar wellbore_completion: A reference to the wellbore completion
        (WITSML data object) where this sample was taken.
    """

    base_md: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BaseMD",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flow_test_activity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlowTestActivity",
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
    tool_serial_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ToolSerialNumber",
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
    wellbore: Optional[str] = field(
        default=None,
        metadata={
            "name": "Wellbore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    wellbore_completion: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellboreCompletion",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DrainageAreaMeasured(AbstractParameter):
    """In a closed reservoir model, the Drainage Area measured.

    This is to be taken to mean that the analysis yielded a measurement,
    as opposed to the RadiusOfInvestigation or PoreVolumeOfInvestigation
    Parameters which are taken to mean the estimates for these
    parameters derived from diffuse flow theory, but not necessarily
    measured.
    """

    abbreviation: str = field(
        init=False,
        default="A",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    area: Optional[str] = field(
        default=None,
        metadata={
            "name": "Area",
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
    :ivar extension_name_value: WITSML - Extension values Schema. The
        intent is to allow standard WITSML "named" extensions without
        having to modify the schema. A client or server can ignore any
        name that it does not recognize but certain meta data is
        required in order to allow generic clients or servers to process
        the value.
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
    :ivar channel_set: Pointer to a ChannelSet containing the comma-
        delimited list of mnemonics and units, and channel data
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
    channel_set: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChannelSet",
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

    :ivar channel_set: Pointer to a ChannelSet containing the comma-
        delimited list of mnemonics and units, and channel data
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

    channel_set: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChannelSet",
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
            "required": True,
        },
    )
    unit_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "UnitReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FaultConductivity(AbstractParameter):
    """
    In a Linear Composite model where the boundary of the inner and outer zones is
    a leaky and conductive fault, the fault conductivity (ie along the face of the
    fault).
    """

    abbreviation: str = field(
        init=False,
        default="Fc",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    permeability_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "PermeabilityLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
class FiberControlLine(AbstractCable):
    """
    Information regarding the control line into which a fiber cable may be pumped
    to measure a facility.

    :ivar comment: A descriptive remark about the fiber control line.
    :ivar encapsulation_type: Enum of square or round encapsulation for
        a control line. A fiber may be installed inside the control
        line.
    :ivar encapsulation_size: Enum of the size of encapsulation of a
        fiber within a control line.
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
    encapsulation_type: Optional[ControlLineEncapsulationKind] = field(
        default=None,
        metadata={
            "name": "EncapsulationType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
    :ivar wellbore:
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
    wellbore: Optional[str] = field(
        default=None,
        metadata={
            "name": "Wellbore",
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
        },
    )
    optical_path_distance_end: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OpticalPathDistanceEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
    time_end: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TimeEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    time_start: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TimeStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    defect_type: Optional[PathDefectKind] = field(
        default=None,
        metadata={
            "name": "DefectType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
    :ivar report_document: A reference to the report document, which
        will use the Energistics Attachment Object.
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
    report_document: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReportDocument",
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
class FluidCharacterizationParameter:
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
    value: Optional[float] = field(
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
class FluidCharacterizationTableRow:
    """A string containing the contents of a row of the table, as a sequence of
    values, one per Fluid Characterization Table Column which has been defined.

    Values are separated by the Delimiter specified in the Table Format,
    and use Null Values when required, also as specified in the Table
    Format.

    :ivar row: The ID (index) of this row of data in the Table Row.
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
class FluidDensity(AbstractParameter):
    """
    The density of the fluid in the wellbore, generally used for estimations of
    wellbore storage when the tubing is filling up.
    """

    abbreviation: str = field(
        init=False,
        default="Rho",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    density: Optional[str] = field(
        default=None,
        metadata={
            "name": "Density",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FluidSampleChainOfCustodyEvent:
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
    The reference conditions and optionally, reference volume, against which volume
    fractions in test steps are recorded.

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
    kind: Optional[Union[VolumeReferenceKind, str]] = field(
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
class FormationTesterSampleAcquisition(FluidSampleAcquisition):
    """
    Information about the job to take a sample directly from the formation using a
    wireline formation tester (WFT).

    :ivar cushion_pressure:
    :ivar flow_test_activity:
    :ivar gross_fluid_kind:
    :ivar md_base:
    :ivar md_top:
    :ivar sample_carrier_slot_name: Reference to the WFT station within
        the top-level WFT run data object  where this sample was
        obtained.
    :ivar sample_container_configuration:
    :ivar sample_container_name:
    :ivar tool_section_name: Reference to the WFT sample within the WFT
        station from where this sample was obtained.
    :ivar tool_serial_number:
    :ivar wellbore:
    """

    cushion_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CushionPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    flow_test_activity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlowTestActivity",
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
    md_base: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MdBase",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    md_top: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MdTop",
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
    tool_section_name: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ToolSectionName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tool_serial_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ToolSerialNumber",
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
class FractureAngleToWellbore(AbstractParameter):
    """For a multiple fractured horizontal wellbore model, the angle at which
    fractures intersect the wellbore.

    A value of 90 degrees indicates the fracture plane is normal to the
    wellbore trajectory.
    """

    abbreviation: str = field(
        init=False,
        default="FractureAngleToWellbore",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "Angle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FractureConductivity(AbstractParameter):
    """
    For an induced hydraulic fracture, the conductivity of the fracture, equal to
    Fracture Width * Fracture Permeability.
    """

    abbreviation: str = field(
        init=False,
        default="Fc",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    permeability_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "PermeabilityLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FractureFaceSkin(AbstractParameter):
    """Dimensionless value, characterizing the restriction to flow (+ve value,
    damage) or additional capacity for flow (-ve value, eg acidized) due to
    effective permeability across the face of a hydraulic fracture, ie controlling
    flow from reservoir into fracture.

    This value is stated with respect to radial flow using the full
    reservoir thickness (h), ie the radial flow or middle time region of
    a pressure transient. It therefore can be added, in a fractured
    well, to "ConvergenceSkinRelativeToTotalThickness" skin to yield
    "SkinRelativeToTotalThickness".
    """

    abbreviation: str = field(
        init=False,
        default="Sf",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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


@dataclass
class FractureHalfLength(AbstractParameter):
    """
    The half length of an induced hydraulic fracture, measured from the wellbore to
    the tip of one "wing" of the fracture.
    """

    abbreviation: str = field(
        init=False,
        default="Xf",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FractureHeight(AbstractParameter):
    """In any vertical hydraulic fracture model (including the cases where the
    wellbore can be vertical or horizontal), the height of the fractures.

    In the case of a vertical wellbore, the fractures are assumed to
    extend an equal distance above and below the mid perforations depth,
    given by the parameter "DistanceMidPerforationsToBottomBoundary". In
    the case of a horizontal wellbore, the fractures are assumed to
    extend an equal distance above and below the wellbore.
    """

    abbreviation: str = field(
        init=False,
        default="Hf",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FractureRadius(AbstractParameter):
    """
    For a horizontal ("pancake") induced hydraulic fracture, which is assumed to be
    circular in shape in the horizontal plane, the radius of the fracture.
    """

    abbreviation: str = field(
        init=False,
        default="Rf",
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FractureStorativityRatio(AbstractParameter):
    """
    Dimensionless Value characterizing the fraction of the pore volume occupied by
    the fractures to the total of pore volume of (fractures plus reservoir).
    """

    abbreviation: str = field(
        init=False,
        default="etaD",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
class HorizontalAnisotropyKxToKy(AbstractParameter):
    """The Horizontal Anisotropy of permeability, K(x direction)/K(y direction).

    Optional since many models do not account for this parameter.
    """

    abbreviation: str = field(
        init=False,
        default="kxToky",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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


@dataclass
class HorizontalRadialPermeability(AbstractParameter):
    """
    The radial permeability of the reservoir layer in the horizontal plane.
    """

    abbreviation: str = field(
        init=False,
        default="K",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    permeability: Optional[str] = field(
        default=None,
        metadata={
            "name": "Permeability",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class InitialPressure(AbstractParameter):
    """The initial pressure of the fluids in the reservoir layer.

    "Initial" is taken to mean "at the time at which the rate history
    used in the pressure transient analysis starts"
    """

    abbreviation: str = field(
        init=False,
        default="Pi",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class Injection:
    """
    Volume injected per reporting entity.

    :ivar injection_quantity:
    :ivar remark: A descriptive remark relating to any significant
        events.
    :ivar quantity_method: The method in which the quantity/volume was
        determined. See enum QuantityMethod.
    """

    injection_quantity: List[AbstractProductQuantity] = field(
        default_factory=list,
        metadata={
            "name": "InjectionQuantity",
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
class InnerToOuterZoneDiffusivityRatio(AbstractParameter):
    """
    In a Radial or Linear Composite model, the diffusivity
    (permeability/(porosity*viscosity*total compressibility) ratio of inner
    zone/outer zone.
    """

    abbreviation: str = field(
        init=False,
        default="D",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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


@dataclass
class InnerToOuterZoneMobilityRatio(AbstractParameter):
    """
    In a Radial or Linear Composite model, the mobility (permeability/viscosity)
    ratio of inner zone/outer zone.
    """

    abbreviation: str = field(
        init=False,
        default="M",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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


@dataclass
class Instrument(AbstractDtsEquipment):
    """
    The general class of an instrument, including vendor information, in the
    installed system.

    :ivar instrument_vendor: Contact information for the person/company
        that provided the equipment
    """

    instrument_vendor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InstrumentVendor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
    :ivar interfacial_tension_test_step: The interfacial tension test
        step.
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
class InterporosityFlowParameter(AbstractParameter):
    """The dimensionless interporosity flow parameter, known as Lambda.

    In dual porosity, represents the ability of the matrix to flow into
    the fissure network. In dual permeability or other multi-layer
    cases, represents the ability of flow to move from one layer to
    another.
    """

    abbreviation: str = field(
        init=False,
        default="Lambda",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
    intervention_conveyance_type: Optional[InterventionConveyanceKind] = field(
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
class Layer2Thickness(AbstractParameter):
    """
    In a two-layer model, the Thickness (h) of layer 2.
    """

    abbreviation: str = field(
        init=False,
        default="h layer 2",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class LeakSkin(AbstractParameter):
    """In Spivey (a) Packer and (c) Fissure models of wellbore storage, the Leak Skin controls the pressure communication through the packer (a), or between the wellbore and the high permeability region (b - second application of model a), or between the high permeability channel/fissures and the reservoir (c). In  case c, the usual Skin parameter characterizes the pressure communication between the wellbore and the high permeability channel/fissures."""

    abbreviation: str = field(
        init=False,
        default="Sl",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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


@dataclass
class LengthHorizontalWellboreFlowing(AbstractParameter):
    """
    For a horizontal wellbore model, the length of the flowing section of the
    wellbore.
    """

    abbreviation: str = field(
        init=False,
        default="hw",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class LiquidComposition:
    """
    The composition of liquid.

    :ivar remark: Remarks and comments about this data item.
    :ivar liquid_component_fraction:
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    liquid_component_fraction: List[FluidComponentFraction] = field(
        default_factory=list,
        metadata={
            "name": "LiquidComponentFraction",
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
            "required": True,
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
class MechanicalSkinRelativeToTotalThickness(AbstractParameter):
    """Dimensionless value, characterizing the restriction to flow (+ve value,
    damage) or additional capacity for flow (-ve value, eg acidized) due to
    effective permeability around the wellbore.

    This value is stated with respect to radial flow using the full
    reservoir thickness (h), ie the radial flow or middle time region of
    a pressure transient. It therefore can be added to
    "ConvergenceSkinRelativeToTotalThickness" skin to yield
    "SkinRelativeToTotalThickness".
    """

    abbreviation: str = field(
        init=False,
        default="Smech",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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


@dataclass
class ModelName(AbstractParameter):
    """The name of the model.

    Available only for Custom Models to identify name of the model.
    """

    abbreviation: str = field(
        init=False,
        default="ModelName",
        metadata={
            "name": "Abbreviation",
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
class NearWellboreBaseModel(AbstractModelSection):
    """
    Abstract near-wellbore response model from which the other near wellbore
    response model types are derived.
    """

    delta_pressure_total_skin: Optional[str] = field(
        default=None,
        metadata={
            "name": "DeltaPressureTotalSkin",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    rate_dependent_skin_factor: Optional[str] = field(
        default=None,
        metadata={
            "name": "RateDependentSkinFactor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    ratio_dp_skin_to_total_drawdown: Optional[str] = field(
        default=None,
        metadata={
            "name": "RatioDpSkinToTotalDrawdown",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class NumberOfFractures(AbstractParameter):
    """For a multiple fractured horizontal wellbore model, the number of fractures
    which originate from the wellbore.

    In a "HorizontalWellboreMultipleEqualFracturedModel" these fractures
    are identical and equally spaced, including one fracture at each end
    of the length represented by "LengthHorizontalWellboreFlowing".
    """

    abbreviation: str = field(
        init=False,
        default="Nf",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    number: Optional[int] = field(
        default=None,
        metadata={
            "name": "Number",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
    :ivar north_sea_offshore: A type of offshore location that captures
        the North Sea offshore terminology.
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
            "required": True,
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
            "required": True,
        },
    )


@dataclass
class OrientationOfAnisotropyXdirection(AbstractParameter):
    """In the case where there is horizontal anisotropy, the orientation of the x
    direction represented in the local CRS.

    Optional since many models do not account for this parameter.
    """

    class Meta:
        name = "OrientationOfAnisotropyXDirection"

    abbreviation: str = field(
        init=False,
        default="OrientationOfAnisotropy_XDirection",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "Angle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class OrientationOfFracturePlane(AbstractParameter):
    """
    For an induced hydraulic fracture which is assumed for PTA purposes to be
    planar, the azimuth of the fracture in the horizontal plane represented in the
    CRS.
    """

    abbreviation: str = field(
        init=False,
        default="OrientationOfFracturePlane",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "Angle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class OrientationOfLinearFront(AbstractParameter):
    """
    In a Linear Composite model, the orientation of the boundary of the inner and
    outer zones represented in the local CRS.
    """

    abbreviation: str = field(
        init=False,
        default="OrientationOfLinearFront",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "Angle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class OrientationOfNormalToBoundary1(AbstractParameter):
    """In any bounded reservoir model, the orientation of the normal to Boundary 1.

    This is an absolute orientation in the local CRS.
    """

    abbreviation: str = field(
        init=False,
        default="OrientationOfNormalToBoundary1",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "Angle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class OrientationWellTrajectory(AbstractParameter):
    """For a slant wellbore or horizontal wellbore model, the azimuth of the
    wellbore in the horizontal plane, represented in the local CRS.

    This is intended to be a value representative of the azimuth for the
    purposes of PTA. It is not necessarily the azimuth which would be
    recorded in a survey of the wellbore trajectory.
    """

    abbreviation: str = field(
        init=False,
        default="OrientationWellTrajectory",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "Angle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
    :ivar fluid_component_fraction: Fluid component.
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_component_fraction: List[FluidComponentFraction] = field(
        default_factory=list,
        metadata={
            "name": "FluidComponentFraction",
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
class PerforatedLength(AbstractParameter):
    """
    For a partial penetration (a vertical or slant well with less than full layer
    thickness open to flow) or a hydraulically fractured model, the length of the
    perforated section of the wellbore.
    """

    abbreviation: str = field(
        init=False,
        default="hp",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
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
        PermanentCableInstallationKind
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
class PermeabilityThicknessProduct(AbstractParameter):
    """
    The product of the radial permeability of the reservoir layer in the horizontal
    plane * the total thickness of the layer.
    """

    abbreviation: str = field(
        init=False,
        default="k.h",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    permeability_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "PermeabilityLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
    kind: Optional[Union[PlusComponentKind, str]] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class PoreVolumeMeasured(AbstractParameter):
    """In a closed reservoir model, the Pore Volume measured.

    This is to be taken to mean that the analysis yielded a measurement,
    as opposed to the RadiusOfInvestigation or PoreVolumeOfInvestigation
    Parameters which are taken to mean the estimates for these
    parameters derived from diffuse flow theory, but not necessarily
    measured.
    """

    abbreviation: str = field(
        init=False,
        default="PVmeas",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "Volume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class PoreVolumeOfInvestigation(AbstractParameter):
    """
    For any transient test, the estimated pore volume of investigation of the test.
    """

    abbreviation: str = field(
        init=False,
        default="PVinv",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "Volume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class Porosity(AbstractParameter):
    """
    The porosity of the reservoir layer.
    """

    abbreviation: str = field(
        init=False,
        default="Phi",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    volume_per_volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolumePerVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class PressureDatumTvd(AbstractParameter):
    """The depth TVD of the datum at which reservoir pressures are reported for
    this layer.

    Note, this depth may not exist inside the layer at the Test Location
    but it is the reference depth to which pressures will be corrected.
    """

    class Meta:
        name = "PressureDatumTVD"

    abbreviation: str = field(
        init=False,
        default="datum",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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

    dtim_start: Optional[str] = field(
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
    :ivar product_fluid_kind: Information about the product that the
        product quantity represents. See enum ProductFluidKind (in the
        ProdmlCommon package).
    :ivar remark: Remarks and comments about this data item.
    :ivar volume_flow_rate: Volume flow rate.
    :ivar product_fluid_reference: A reference (using uid) to a fluid
        component contained in the Fluid Component Catalog.
    """

    mass_flow_rate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassFlowRate",
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
    product_fluid_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProductFluidReference",
            "type": "Attribute",
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
    :ivar ownership_business_acct: Owner business account
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

    dtim: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DTim",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dtim_end: List[str] = field(
        default_factory=list,
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
    measure_data_type: List[AbstractMeasureData] = field(
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

    :ivar production_quantity:
    :ivar remark: Remarks and comments about this data item.
    :ivar quantity_method: The method in which the quantity/volume was
        determined. See enum QuantityMethod.
    """

    production_quantity: List[AbstractProductQuantity] = field(
        default_factory=list,
        metadata={
            "name": "ProductionQuantity",
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
    kind: Optional[Union[PseudoComponentKind, str]] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
            "required": True,
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
    kind: Optional[Union[PureComponentKind, str]] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
class RadiusOfInvestigation(AbstractParameter):
    """
    For any transient test, the estimated radius of investigation of the test.
    """

    abbreviation: str = field(
        init=False,
        default="Ri",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class RateDependentSkinFactor(AbstractParameter):
    """Value characterizing the rate at which an apparent skin effect, due to
    additional pressure drop, due to turbulent flow, grows as a function of
    flowrate.

    The additional flowrate-dependent Skin is this value D * Flowrate.
    The total measured Skin factor would then be S + DQ, where Q is the
    flowrate.
    """

    abbreviation: str = field(
        init=False,
        default="D",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    inverse_flowrate: Optional[str] = field(
        default=None,
        metadata={
            "name": "InverseFlowrate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class RatioDpSkinToTotalDrawdown(AbstractParameter):
    """The ratio of the DeltaPressureTotalSkin to the total drawdown pressure.

    Indicates the fraction of the total pressure drawdown due to
    completion effects such as convergence, damage, etc.  The remaining
    pressure drop is due to radial flow in the reservoir.
    """

    abbreviation: str = field(
        init=False,
        default="Ratio dP Skin To Total",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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


@dataclass
class RatioInitialToFinalWellboreStorage(AbstractParameter):
    """
    In models in which the wellbore storage coefficient changes, the ratio of
    intial to final wellbore storage coefficients.
    """

    abbreviation: str = field(
        init=False,
        default="Ci/Cs",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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


@dataclass
class RatioLayer1ToTotalPermeabilityThicknessProduct(AbstractParameter):
    """
    In a two-layer model, the ratio of layer 1 to the total PermeabilityThickness.
    """

    abbreviation: str = field(
        init=False,
        default="Kappa",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
            "required": True,
        },
    )


@dataclass
class Region2Thickness(AbstractParameter):
    """
    In a Linear Composite model where the thickness of the inner and outer zones is
    different, the thickness h of the outer region (2).
    """

    abbreviation: str = field(
        init=False,
        default="h region 2",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class ReservoirBaseModel(AbstractModelSection):
    """
    Abstract reservoir model from which the other types are derived.
    """

    average_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "AveragePressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    horizontal_anisotropy_kx_to_ky: Optional[str] = field(
        default=None,
        metadata={
            "name": "HorizontalAnisotropyKxToKy",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    horizontal_radial_permeability: Optional[str] = field(
        default=None,
        metadata={
            "name": "HorizontalRadialPermeability",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    initial_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "InitialPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    lower_boundary_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "LowerBoundaryType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    orientation_of_anisotropy_xdirection: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfAnisotropyXDirection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    permeability_thickness_product: Optional[str] = field(
        default=None,
        metadata={
            "name": "PermeabilityThicknessProduct",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    porosity: Optional[str] = field(
        default=None,
        metadata={
            "name": "Porosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    pressure_datum_tvd: Optional[str] = field(
        default=None,
        metadata={
            "name": "PressureDatumTVD",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "TotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    upper_boundary_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "UpperBoundaryType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vertical_anisotropy_kv_to_kr: Optional[str] = field(
        default=None,
        metadata={
            "name": "VerticalAnisotropyKvToKr",
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
    :ivar sara: SARA analysis results. SARA stands for saturates,
        asphaltenes, resins and aromatics.
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
class SeparatorSampleAcquisition(FluidSampleAcquisition):
    """
    Additonal information required from a fluid sample taken from a separator.

    :ivar corrected_gas_rate: The corrected gas rate for this separator
        sample acquisition.
    :ivar corrected_oil_rate: The corrected oil rate for this separator
        sample acquisition.
    :ivar corrected_water_rate: The corrected water rate for this
        separator sample acquisition.
    :ivar flow_test_activity:
    :ivar measured_gas_rate: The measured gas rate for this separator
        sample acquisition.
    :ivar measured_oil_rate: The measured oil rate for this separator
        sample acquisition.
    :ivar measured_water_rate: The measured water rate for this
        separator sample acquisition.
    :ivar sampling_point: A reference to the flow port in the facility
        where this sample was taken.
    :ivar separator: A reference to the separator where this sample was
        taken.
    :ivar separator_pressure: The separator pressure when this sample
        was taken.
    :ivar separator_temperature: The separator temperature when this
        sample was taken.
    :ivar well_completion: A reference to a well completion (WITSML data
        object) where this sample was taken.
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
    flow_test_activity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlowTestActivity",
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
    well_completion: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellCompletion",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
        },
    )


@dataclass
class SingleBoundarySubModel:
    """For a Boundary model which has an arbitrary number, orientation and type of
    external boundaries, this is the model sub class which describes each boundary.

    There will be as many instances of this as there are boundaries.
    This is expected to be a numerical model. The other, regular
    geometries of boundaries may well be represented by analytical
    models.

    :ivar type_of_boundary: In any bounded reservoir model, the type of
        Boundary 1. Enumeration with choice of "no-flow" or "constant
        pressure".
    :ivar fault_ref_id: The reference to a RESQML model representation
        of this fault.
    """

    type_of_boundary: Optional[Boundary1Type] = field(
        default=None,
        metadata={
            "name": "TypeOfBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fault_ref_id: Optional[ResqmlModelRef] = field(
        default=None,
        metadata={
            "name": "FaultRefID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class SingleFlowrateData(AbstractRateHistory):
    """
    Contains the data for a simple representation of flowrate comprising a single
    rate and a flowing time.

    :ivar effective_producing_time_used: If a single flowrate and
        effective producing time was used, this is the effective
        producing time used in the analysis. Usually abbreviated Tpeff.
    :ivar single_flowrate: If a single flowrate and effective producing
        time was used, this is the single flowrate value used in the
        analysis.
    """

    effective_producing_time_used: Optional[str] = field(
        default=None,
        metadata={
            "name": "EffectiveProducingTimeUsed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    single_flowrate: Optional[str] = field(
        default=None,
        metadata={
            "name": "SingleFlowrate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class SkinLayer2RelativeToTotalThickness(AbstractParameter):
    """In a two-layer model with both layers flowing into the wellbore, the skin
    factor of the second layer.

    This value is stated with respect to radial flow using the full
    layer thickness (h), ie the "reservoir radial flow" or "middle time
    region" of a pressure transient.
    """

    abbreviation: str = field(
        init=False,
        default="S2",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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


@dataclass
class SkinRelativeToTotalThickness(AbstractParameter):
    """Dimensionless value, characterizing the restriction to flow (+ve value) or
    extra capacity for flow (-ve value) into the wellbore.

    This value is stated with respect to radial flow using the full
    layer thickness (h), ie the "reservoir radial flow" or "middle time
    region" of a pressure transient. It comprises the sum of
    "MechanicalSkinRelativeToTotalThickness" and
    "ConvergenceSkinRelativeToTotalThickness" both of which also are
    expressed in terms of h.
    """

    abbreviation: str = field(
        init=False,
        default="S",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
class StorativityRatio(AbstractParameter):
    """The dimensionless storativity ratio, known as Omega equal to the fracture
    storativity divided by total storativity.

    Storativity = porosity * total compressibility.
    """

    abbreviation: str = field(
        init=False,
        default="Omega",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
class SulfurFluidComponent(AbstractFluidComponent):
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
    kind: Optional[Union[SulfurComponentKind, str]] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class TestPeriodsFlowrateData(AbstractRateHistory):
    """
    :ivar test_period_ref: Choice available for rate history where the
        test period(s) used to form the rate history are referenced (by
        uid).
    """

    test_period_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestPeriodRef",
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

    d_tim: Optional[str] = field(
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
class TotalThickness(AbstractParameter):
    """
    The total thickness of the layer of reservoir layer.
    """

    abbreviation: str = field(
        init=False,
        default="h",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class TransmissibilityReductionFactorOfLinearFront(AbstractParameter):
    """The transmissibility reduction factor of a fault in a Linear Composite model
    where the boundary of the inner and outer zones is a leaky fault.

    If T is the complete transmissibility which would be computed
    without any fault between point A and point B (T is a function of
    permeability, etc), then Tf = T * leakage. Therefore: leakage = 1
    implies that the fault is not a barrier to flow at all, leakage = 0
    implies that the fault is sealing (no transmissibility anymore at
    all between points A and B).
    """

    abbreviation: str = field(
        init=False,
        default="Leakage",
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class TubingInteralDiameter(AbstractParameter):
    """
    Internal diameter of the tubing, generally used for estimations of wellbore
    storage when the tubing is filling up.
    """

    abbreviation: str = field(
        init=False,
        default="ID",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class VaporComposition:
    """
    Vapor composition.

    :ivar remark: Remarks and comments about this data item.
    :ivar vapor_component_fraction:
    """

    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    vapor_component_fraction: List[FluidComponentFraction] = field(
        default_factory=list,
        metadata={
            "name": "VaporComponentFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class VerticalAnisotropyKvToKr(AbstractParameter):
    """The Vertical Anisotropy of permeability, K(vertical)/K(radial).

    K(radial) is the effective horizontal permeability, which in
    anisotropic horizontal permeability equals square root (Kx^2+Ky^2).
    Optional since many models do not account for this parameter. It
    will be mandatory in some models however, e.g. limited entry or
    horizontal wellbore models.
    """

    abbreviation: str = field(
        init=False,
        default="kvTokr",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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


@dataclass
class WaterSampleComponent:
    """
    Water sample component.

    :ivar equivalent_concentration: The equivalent concentration of
        CaCO3 of the water sample component.
    :ivar mass_concentration: The mass concentration of the water sample
        component.
    :ivar molar_concentration:
    :ivar remark:
    :ivar test_method:
    :ivar volume_concentration:
    :ivar anion:
    :ivar cation:
    :ivar concentration_relative_to_detectable_limits: This element can
        be used where a measurement for a concentration is only capable
        of a "yes/no" type accuracy. Values can be ADL (meaning the
        measurement was Above Detectable Limits) or BDL (meaning the
        measurement was Below Detectable Limits). If the condition is
        "ADL" then the concentration as reported in Mass Fraction or
        Mole Fraction is expected to represent the maximum value which
        can be distinguished (so that we know the actual value to be
        equal to or greater than that). If the condition is "BDL" then
        the concentration as reported in Mass Fraction or Mole Fraction
        is expected to represent the minimum value which can be
        distinguished (so that we know the actual value to be equal to
        or less than that).
    :ivar organic_acid:
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
    mass_concentration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MassConcentration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    molar_concentration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MolarConcentration",
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
    test_method: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    volume_concentration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "VolumeConcentration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    anion: Optional[Union[AnionKind, str]] = field(
        default=None,
        metadata={
            "name": "Anion",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cation: Optional[Union[CationKind, str]] = field(
        default=None,
        metadata={
            "name": "Cation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    concentration_relative_to_detectable_limits: Optional[
        DetectableLimitRelativeStateKind
    ] = field(
        default=None,
        metadata={
            "name": "ConcentrationRelativeToDetectableLimits",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    organic_acid: Optional[Union[OrganicAcidKind, str]] = field(
        default=None,
        metadata={
            "name": "OrganicAcid",
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
class WellboreBaseModel(AbstractModelSection):
    """
    Abstract wellbore response model from which the other wellbore response model
    types are derived.
    """

    fluid_density: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidDensity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    tubing_interal_diameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "TubingInteralDiameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellbore_deviation_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellboreDeviationAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellbore_fluid_compressibility: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellboreFluidCompressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellbore_radius: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellboreRadius",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    wellbore_storage_coefficient: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellboreStorageCoefficient",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    wellbore_storage_mechanism_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellboreStorageMechanismType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellbore_volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellboreVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class WellboreDeviationAngle(AbstractParameter):
    """
    The angle of deviation from vertical of the wellbore, generally used for
    estimations of wellbore storage when the tubing is filling up.
    """

    abbreviation: str = field(
        init=False,
        default="Deviation",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    plane_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "PlaneAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class WellboreFluidCompressibility(AbstractParameter):
    """
    The compressibility of the fluid in the wellbore, such that this value *
    wellbore volume = wellbore storage coefficient.
    """

    abbreviation: str = field(
        init=False,
        default="Cw",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    compressibility: Optional[str] = field(
        default=None,
        metadata={
            "name": "Compressibility",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class WellboreRadius(AbstractParameter):
    """
    The radius of the wellbore, generally taken to represent the open hole size.
    """

    abbreviation: str = field(
        init=False,
        default="Rw",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "name": "Length",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class WellboreStorageCoefficient(AbstractParameter):
    """The wellbore storage coefficient equal to the volume which flows into the
    wellbore per unit change in pressure in the wellbore.

    NOTE that by setting this parameter to = 0, the model becomes
    equivalent to a "No Wellbore Storage" model.
    """

    abbreviation: str = field(
        init=False,
        default="Cs",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    volume_per_pressure: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolumePerPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class WellboreVolume(AbstractParameter):
    """The volume of the wellbore equipment which influences the wellbore storage.

    It will be sum of volumes of all components open to the reservoir up
    to the shut off valve.
    """

    abbreviation: str = field(
        init=False,
        default="Vw",
        metadata={
            "name": "Abbreviation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    volume: Optional[str] = field(
        default=None,
        metadata={
            "name": "Volume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class WellheadSampleAcquisition(FluidSampleAcquisition):
    """
    Additional information required for a fluid sample taken from a wellhead.

    :ivar flow_test_activity:
    :ivar sampling_point: A reference to the flow port in the facility
        where this sample was taken.
    :ivar well: A reference to the well (WITSML data object) where this
        sample was taken.
    :ivar well_completion: A reference to the well completion (WITSML
        data object) where this sample was taken.
    :ivar wellhead_pressure: The wellhead pressure when the sample was
        taken.
    :ivar wellhead_temperature: The wellhead temperature when the sample
        was taken.
    """

    flow_test_activity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlowTestActivity",
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
    well: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Well",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_completion: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellCompletion",
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


@dataclass
class AbstractPtaFlowData(AbstractFlowTestData):
    """
    Actual measured flow data.

    :ivar flow_channel: The Channel containing the Flow data.
    :ivar fluid_phase_measured_kind: An enum of which phases are being
        measured by this flow data Channel.
    """

    flow_channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowChannel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fluid_phase_measured_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidPhaseMeasuredKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class AbstractPtaPressureData(AbstractFlowTestData):
    """
    The abstract class of pressure data from which all flow test data components
    inherit.

    :ivar datum: The datum (which is an enum of type Datum in WITSML)
        from which the element PressureReferenceDepth is measured.
    :ivar pressure_channel: A channel is a series of individual data
        points. A channel is comparable to a log curve; more generally,
        it is comparable to a tag in a process historian. Channels
        organize their data points according to one or more channel
        indexes, in this case, pressure.
    :ivar pressure_derivative_channel: A channel is a series of
        individual data points. A channel is comparable to a log curve;
        more generally, it is comparable to a tag in a process
        historian. Channels organize their data points according to one
        or more channel indexes, in this case, derived from another
        pressure channel.
    :ivar pressure_reference_depth: A depth relative to a base or datum.
    """

    datum: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Datum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pressure_channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "PressureChannel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    pressure_derivative_channel: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PressureDerivativeChannel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pressure_reference_depth: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PressureReferenceDepth",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class Calibration:
    """This object contains, for a single facility (defined by its parent Facility
    Calibration), a single Calibration, ie, details of the calibration process and
    results whereby each locus (an acquired data point along the fiber optical
    path) is mapped to a physical location in the facility.

    It is common in DAS processing for such calibrations to be refined
    over time as further data become available.  Each such successive
    calibration can be described using an instance of this object.

    :ivar creation: Date and time the Calibration was created in the
        source application or, if that information is not available,
        when it was saved to the file. This is the equivalent of the ISO
        19115 CI_Date where the CI_DateTypeCode = "creation" Format:
        YYYY-MM-DDThh:mm:ssZ[+/-]hh:mm Legacy DCGroup - created
    :ivar editor: Name (or other human-readable identifier) of the last
        person who updated the Calibration. This is the equivalent in
        ISO 19115 to the CI_Individual.name or the CI_Organization.name
        of the citedResponsibleParty whose role is "editor". Legacy
        DCGroup - contributor
    :ivar last_locus_to_end_of_fiber: This element records the length,
        which can be observed in the DAS data, between the last locus in
        a fiber optical path, and the end of the fiber. As such, this
        distance is a useful input to the calibration process. There
        will only be one such measurement along a fiber optical path,
        that on the last facility before the end of the fiber (eg at the
        bottom a wellbore, in the event that say a flowline and then a
        wellbore are being measured using the same fiber optical path).
        For this reason this element is optional.
    :ivar last_update: Date and time the Calibration was last modified
        in the source application or, if that information is not
        available, when it was last saved to the format file. This is
        the equivalent of the ISO 19115 CI_Date where the
        CI_DateTypeCode = "lastUpdate" Format: YYYY-MM-
        DDThh:mm:ssZ[+/-]hh:mm Legacy DCGroup - modified
    :ivar originator: Name (or other human-readable identifier) of the
        person who initially originated the Calbration. If that
        information is not available, then this is the user who created
        the format file. The originator remains the same as the object
        is subsequently edited. This is the equivalent in ISO 19115 to
        the CI_Individual.name or the CI_Organization.name of the
        citedResponsibleParty whose role is "originator". Legacy DCGroup
        - author
    :ivar otdr: If a OTDR (optical time domain reflectometry) survey is
        carried out, a top level object called OTDR Acquisition can be
        created to report the results.  In the event that such a survey
        is used as the input to a Calibration, then a Data Object
        Reference to that object can be inserted with this element.
    :ivar pipeline_datum: In the event that the facility kind is a
        pipeline, this element is used to record the datum from which
        facility (pipeline) length is referenced.  The type is a string
        since there is currently no standard enum for this type of data.
        It is expected that the value would be a string to describe, eg
        one end of the pipe from which measurement is made.
    :ivar remark: Textual description about the value of this field.
    :ivar wellbore_datum: In the event that the facility kind is a
        wellbore, this element is used to record the datum from which
        measured depth is referenced.  The type is
        WellboreDatumReference, an enum in the Energistics Common
        package (example value, kelly bushing).
    :ivar locus_depth_point: This array must have a compound data type
        consisting of three data types: LocusIndex (int64),
        OpticalPathDistance (float64), FacilityLength (float64)
    :ivar calibration_input_point:
    """

    creation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Creation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    editor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Editor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    last_locus_to_end_of_fiber: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LastLocusToEndOfFiber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    last_update: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LastUpdate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    originator: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Originator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    otdr: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OTDR",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pipeline_datum: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PipelineDatum",
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
    wellbore_datum: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellboreDatum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    locus_depth_point: Optional[CompoundExternalArray] = field(
        default=None,
        metadata={
            "name": "LocusDepthPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    calibration_input_point: List[DasCalibrationInputPoint] = field(
        default_factory=list,
        metadata={
            "name": "CalibrationInputPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class ChangingStorageFairModel(WellboreBaseModel):
    """
    Changing wellbore storage model using the Fair model.
    """

    delta_time_storage_changes: Optional[str] = field(
        default=None,
        metadata={
            "name": "DeltaTimeStorageChanges",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    ratio_initial_to_final_wellbore_storage: Optional[str] = field(
        default=None,
        metadata={
            "name": "RatioInitialToFinalWellboreStorage",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class ChangingStorageHegemanModel(WellboreBaseModel):
    """
    Changing wellbore storage model using the Hegeman model.
    """

    delta_time_storage_changes: Optional[str] = field(
        default=None,
        metadata={
            "name": "DeltaTimeStorageChanges",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    ratio_initial_to_final_wellbore_storage: Optional[str] = field(
        default=None,
        metadata={
            "name": "RatioInitialToFinalWellboreStorage",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class ChangingStorageSpiveyFissuresModel(WellboreBaseModel):
    """
    Changing wellbore storage model using the Spivey Packer model.
    """

    leak_skin: Optional[str] = field(
        default=None,
        metadata={
            "name": "LeakSkin",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    ratio_initial_to_final_wellbore_storage: Optional[str] = field(
        default=None,
        metadata={
            "name": "RatioInitialToFinalWellboreStorage",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class ChangingStorageSpiveyPackerModel(WellboreBaseModel):
    """
    Changing wellbore storage model using the Spivey Fissures model.
    """

    leak_skin: Optional[str] = field(
        default=None,
        metadata={
            "name": "LeakSkin",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    ratio_initial_to_final_wellbore_storage: Optional[str] = field(
        default=None,
        metadata={
            "name": "RatioInitialToFinalWellboreStorage",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class ClosedCircleModel(BoundaryBaseModel):
    """
    Closed circle boundary model.
    """

    boundary1_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary1Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class ClosedRectangleModel(BoundaryBaseModel):
    """Closed rectangle boundary model.

    Four faults bound the reservoir in a rectangular shape.
    """

    boundary1_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary1Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    boundary2_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary2Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    boundary3_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary3Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    boundary4_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary4Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    distance_to_boundary1: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToBoundary1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    distance_to_boundary2: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToBoundary2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    distance_to_boundary3: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToBoundary3",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    distance_to_boundary4: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToBoundary4",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    drainage_area_measured: Optional[str] = field(
        default=None,
        metadata={
            "name": "DrainageAreaMeasured",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    orientation_of_normal_to_boundary1: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfNormalToBoundary1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pore_volume_measured: Optional[str] = field(
        default=None,
        metadata={
            "name": "PoreVolumeMeasured",
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
        test step. This is the volume of liquid divided by a reference
        volume. Refer to the documentation for the Relative Volume Ratio
        and Fluid Volume Reference classes.
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
class ConstantStorageModel(WellboreBaseModel):
    """
    Constant wellbore storage model.
    """


@dataclass
class CustomBoundaryModel(BoundaryBaseModel):
    """
    Boundary Model allowing for the addition of custom parameters to support
    extension of the model library provided.
    """

    any_parameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AnyParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    custom_parameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CustomParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    model_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ModelName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class CustomNearWellboreModel(NearWellboreBaseModel):
    """
    Near Wellbore Model allowing for the addition of custom parameters to support
    extension of the model library provided.
    """

    any_parameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AnyParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    custom_parameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CustomParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    model_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ModelName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class CustomReservoirModel(ReservoirBaseModel):
    """
    Reservoir Model allowing for the addition of custom parameters to support
    extension of the model library provided.
    """

    any_parameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AnyParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    custom_parameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CustomParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    model_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ModelName",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class CustomWellboreModel(WellboreBaseModel):
    """
    Wellbore Storage Model allowing for the addition of custom parameters to
    support extension of the model library provided.
    """

    any_parameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AnyParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    custom_parameter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CustomParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    model_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ModelName",
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
    :ivar fbe_index: The nth (zero-based) count of this FBE instance in
        the Acquisition.  Recommended if there is more than 1 FBE
        instance in this Acquisition.  This index corresponds to the FBE
        array number in the HDF5 file.
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
    start_locus_index: Optional[int] = field(
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
    :ivar raw_index: The nth (zero-based) count of this Raw instance in
        the Acquisition.  Recommended if there is more than 1 Raw
        instance in this Acquisition.  This index corresponds to the Raw
        array number in the HDF5 file.
    :ivar start_locus_index: The first ‘locus’ acquired by the
        interrogator unit. Where ‘Locus Index 0’ is the acoustic sample
        point at the connector of the measurement instrument.
    :ivar custom:
    :ivar raw_data: A DAS array object containing the raw DAS data.
    :ivar raw_data_time: A DAS array object containing the sample times
        corresponding to a single ‘scan’ of the fiber. In a single
        ‘scan’, the DAS measurement system acquires raw data samples for
        all the loci specified by StartLocusIndex. The ‘scan’ frequency
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
    start_locus_index: Optional[int] = field(
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
    :ivar spectra_index: The nth (zero-based) count of this Spectra
        instance in the acquisition. Recommended if there is more than 1
        Spectra instance in this acquisition.  This index corresponds to
        the Spectra array number in the HDF5 file.
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
    start_locus_index: Optional[int] = field(
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
    :ivar remark: A brief meaningful description about the event.
    :ivar start_date: The start date of the event.
    :ivar deferred_kind: Indicates whether event is planned or unplanned
    :ivar deferred_production_volume: The production volume deferred for
        the reporting period.
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
    end_date: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EndDate",
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
    start_date: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StartDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    deferred_kind: Optional[DeferredKind] = field(
        default=None,
        metadata={
            "name": "DeferredKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    deferred_production_volume: List[DeferredProductionVolume] = field(
        default_factory=list,
        metadata={
            "name": "DeferredProductionVolume",
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
class DualPermeabilityWithCrossflowModel(ReservoirBaseModel):
    """
    Dual Permeability reservoir model, with Cross-Flow between the two layers.
    """

    interporosity_flow_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "InterporosityFlowParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    layer2_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "Layer2Thickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    ratio_layer1_to_total_permeability_thickness_product: Optional[
        str
    ] = field(
        default=None,
        metadata={
            "name": "RatioLayer1ToTotalPermeabilityThicknessProduct",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    storativity_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "StorativityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DualPorosityPseudoSteadyStateModel(ReservoirBaseModel):
    """
    Dual Porosity reservoir model, with Pseudo-Steady-State flow between the two
    porosity systems.
    """

    interporosity_flow_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "InterporosityFlowParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    storativity_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "StorativityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DualPorosityTransientSlabsModel(ReservoirBaseModel):
    """
    Dual Porosity reservoir model, with transient flow between the two porosity
    systems, and assuming slab shaped matrix blocks.
    """

    interporosity_flow_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "InterporosityFlowParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    storativity_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "StorativityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DualPorosityTransientSpheresModel(ReservoirBaseModel):
    """
    Dual Porosity reservoir model, with transient flow between the two porosity
    systems, and assuming spherical shaped matrix blocks.
    """

    interporosity_flow_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "InterporosityFlowParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    storativity_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "StorativityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
            "required": True,
        },
    )


@dataclass
class FiberConnection(FiberCommon):
    """
    A connection component within the optical path.

    :ivar connector_type: Specifies whether this is a dry mate or wet
        mate.
    :ivar end_type: Describes whether the fiber end is angle polished or
        flat polished.
    """

    connector_type: Optional[FiberConnectorKind] = field(
        default=None,
        metadata={
            "name": "ConnectorType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    end_type: Optional[FiberEndKind] = field(
        default=None,
        metadata={
            "name": "EndType",
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
    time_end: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TimeEnd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    time_start: Optional[str] = field(
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
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
    parameter: List[str] = field(
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
    cable_type: Optional[CableKind] = field(
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
    fiber_splice_type: Optional[FiberSpliceKind] = field(
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

    termination_type: Optional[TerminationKind] = field(
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
class FiniteRadiusModel(NearWellboreBaseModel):
    """
    Finite radius model with radial flow into wellbore with skin factor.
    """

    skin_layer2_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkinLayer2RelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FlashedGas:
    """
    Flashed gas.

    :ivar gas_density: This density is measured at the standard
        conditions for this Fluid Analysis.
    :ivar gas_gravity: The gas gravity of the flashed gas in this
        atmospheric flash test.
    :ivar gas_molecular_weight: The molecular weight of the gas phase at
        this test step.
    :ivar gas_zfactor: The gas Z factor value at this test step.
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
    :ivar vapor_composition: The vapor composition of the flashed gas in
        this atmospheric flash test.
    """

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
    gas_zfactor: Optional[float] = field(
        default=None,
        metadata={
            "name": "GasZFactor",
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
    :ivar liquid_density: This density is measured at the standard
        conditions for this Fluid Analysis.
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
    liquid_density: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LiquidDensity",
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
class FluidCharacterizationParameterSet:
    """
    The constant definition used in the table.

    :ivar fluid_characterization_parameter: The constant definition used
        in the table.
    """

    fluid_characterization_parameter: List[
        FluidCharacterizationParameter
    ] = field(
        default_factory=list,
        metadata={
            "name": "FluidCharacterizationParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
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
    table_constant: List[FluidCharacterizationParameter] = field(
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

    :ivar delimiter: The delimiter for this fluid characterization table
        format.
    :ivar null_value: The null value for this fluid characterization
        table format.
    :ivar table_column:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    delimiter: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Delimiter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
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
    :ivar sulfur_fluid_component:
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
    sulfur_fluid_component: List[SulfurFluidComponent] = field(
        default_factory=list,
        metadata={
            "name": "SulfurFluidComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FluidCvdTestStep:
    """
    The CVD test steps.

    :ivar cumulative_fluid_produced_fraction: The cumulative fluid
        produced, expressed as a molar fraction of the initial quantity,
        up to and including this test step.
    :ivar cumulative_stock_tank_gor: The cumulative GOR at stock tank
        conditions, of all the fluid produced up and including this test
        step.
    :ivar fluid_produced_gor: The GOR of the fluid produced at this test
        step
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
        test step. This is the volume of liquid divided by a reference
        volume. Refer to the documentation for the Relative Volume Ratio
        and Fluid Volume Reference classes.
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
    cumulative_stock_tank_gor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CumulativeStockTankGOR",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_produced_gor: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FluidProducedGOR ",
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

    :ivar cumulative_stock_tank_gor: The cumulative stock tank GOR
        (corrected to conditions specified in the element Shrinkage
        Reference) at this test step.
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
        volume factor (corrected to conditions specified in the element
        Shrinkage Reference) at this test step.
    :ivar oil_viscosity: The viscosity of the oil phase at this test
        step.
    :ivar overall_composition: The overall composition at this test
        step.
    :ivar phases_present: The phases present at this test step.
    :ivar remark: Remarks and comments about this data item.
    :ivar residual_apigravity: The residual API gravity at this test
        step.
    :ivar solution_gorcorrected: The solution GOR (corrected to
        conditions specified in the element Shrinkage Reference) at this
        test step.
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
    solution_gorcorrected: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SolutionGORCorrected",
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
    :ivar oil_formation_volume_factor_corrected: The stage Oil Formation
        Volume Factor (separator corrected) for this test step.
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
        (separator corrected) for this test step.
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
class FracturedFiniteConductivityModel(NearWellboreBaseModel):
    """Fracture model, with vertical fracture flow.

    Finite Conductivity Model.
    """

    distance_mid_fracture_height_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceMidFractureHeightToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_conductivity: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureConductivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_face_skin: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureFaceSkin",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_half_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureHalfLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_height: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureHeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    orientation_of_fracture_plane: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfFracturePlane",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    skin_layer2_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkinLayer2RelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FracturedHorizontalFiniteConductivityModel(NearWellboreBaseModel):
    """Fracture model, with  horizontal fracture (sometimes called "pancake
    fracture") flow.

    Finite Conductivity Model.
    """

    distance_fracture_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceFractureToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_conductivity: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureConductivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_radius: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureRadius",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FracturedHorizontalInfiniteConductivityModel(NearWellboreBaseModel):
    """Fracture model, with  horizontal fracture (sometimes called "pancake
    fracture") flow.

    Infinite Conductivity Model.
    """

    distance_fracture_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceFractureToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_radius: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureRadius",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FracturedHorizontalUniformFluxModel(NearWellboreBaseModel):
    """Fracture model, with  horizontal fracture (sometimes called "pancake
    fracture") flow.

    Unform Flux Model.
    """

    distance_fracture_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceFractureToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_radius: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureRadius",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class FracturedInfiniteConductivityModel(NearWellboreBaseModel):
    """Fracture model, with vertical fracture flow.

    Infinite Conductivity Model.
    """

    distance_mid_fracture_height_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceMidFractureHeightToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_face_skin: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureFaceSkin",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_half_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureHalfLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_height: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureHeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    orientation_of_fracture_plane: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfFracturePlane",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    skin_layer2_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkinLayer2RelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class FracturedUniformFluxModel(NearWellboreBaseModel):
    """Fracture model, with vertical fracture flow.

    Unform Flux Model.
    """

    distance_mid_fracture_height_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceMidFractureHeightToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_face_skin: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureFaceSkin",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_half_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureHalfLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_height: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureHeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    orientation_of_fracture_plane: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfFracturePlane",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    skin_layer2_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkinLayer2RelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
    :ivar field_value: The name of the field within whose context the
        report exists.
    :ivar state: The state or province within the country.
    :ivar offshore_location: A generic type of offshore location. This
        allows an offshore location to be given by an area name, and up
        to four block names. A comment is also allowed.
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
    field_value: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Field",
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
    offshore_location: Optional[OffshoreLocation] = field(
        default=None,
        metadata={
            "name": "OffshoreLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class HomogeneousModel(ReservoirBaseModel):
    """
    Homogeneous reservoir model.
    """


@dataclass
class HorizontalWellbore2LayerModel(NearWellboreBaseModel):
    """
    Horizontal wellbore model with wellbore positioned at arbitary distance from
    lower surface of reservoir layer, and with additional upper layer parallel to
    layer containing wellbore.
    """

    convergence_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConvergenceSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    distance_wellbore_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceWellboreToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length_horizontal_wellbore_flowing: Optional[str] = field(
        default=None,
        metadata={
            "name": "LengthHorizontalWellboreFlowing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    mechanical_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "MechanicalSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    orientation_well_trajectory: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationWellTrajectory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class HorizontalWellboreModel(NearWellboreBaseModel):
    """
    Horizontal wellbore model with wellbore positioned at arbitary distance from
    lower surface of reservoir layer.
    """

    convergence_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConvergenceSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    distance_wellbore_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceWellboreToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    length_horizontal_wellbore_flowing: Optional[str] = field(
        default=None,
        metadata={
            "name": "LengthHorizontalWellboreFlowing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    mechanical_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "MechanicalSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    orientation_well_trajectory: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationWellTrajectory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class HorizontalWellboreMultipleEqualFracturedModel(NearWellboreBaseModel):
    """
    Horizontal wellbore model with wellbore positioned at arbitary distance from
    lower surface of reservoir layer, containing a number "n" of equally spaced
    identical vertical fractures.
    """

    convergence_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConvergenceSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    distance_mid_fracture_height_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceMidFractureHeightToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    distance_wellbore_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceWellboreToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_angle_to_wellbore: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureAngleToWellbore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_conductivity: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureConductivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_face_skin: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureFaceSkin",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_half_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureHalfLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_height: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureHeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_model_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureModelType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_storativity_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "FractureStorativityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    length_horizontal_wellbore_flowing: Optional[str] = field(
        default=None,
        metadata={
            "name": "LengthHorizontalWellboreFlowing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    mechanical_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "MechanicalSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    number_of_fractures: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumberOfFractures",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    orientation_well_trajectory: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationWellTrajectory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class HorizontalWellboreMultipleVariableFracturedModel(NearWellboreBaseModel):
    """Horizontal wellbore model with wellbore positioned at arbitary distance from
    lower surface of reservoir layer, containing a number "n" of non-identical
    vertical fractures.

    These may be unequally spaced and each may have its own orientation
    with respect to the wellbore, and its own height. Expected to be
    modelled numerically.
    """

    convergence_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConvergenceSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    distance_wellbore_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceWellboreToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    length_horizontal_wellbore_flowing: Optional[str] = field(
        default=None,
        metadata={
            "name": "LengthHorizontalWellboreFlowing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    mechanical_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "MechanicalSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    number_of_fractures: Optional[str] = field(
        default=None,
        metadata={
            "name": "NumberOfFractures",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    orientation_well_trajectory: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationWellTrajectory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    single_fracture_sub_model: List[str] = field(
        default_factory=list,
        metadata={
            "name": "singleFractureSubModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class InfiniteBoundaryModel(BoundaryBaseModel):
    """Infinite boundary model - there are no boundaries around the reservoir."""


@dataclass
class InjectedGas:
    """The composition of a single injected gas used in the swelling test.

    This type of gas has a uid which is used to refer to this gas being
    injected, in each Swelling Test Step.

    :ivar vapor_composition: The composition of injected gas (vapor) for
        this test.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    vapor_composition: Optional[VaporComposition] = field(
        default=None,
        metadata={
            "name": "VaporComposition",
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
class IntegerData(AbstractMeasureData):
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
class InternalFaultSubModel:
    """Internal Fault sub model describes each internal fault within the reservoir.

    There will be as many instances of this as there are internal
    faults.  This is expected to be a numerical model.

    :ivar conductivity: For a finite conductivity fault, the
        conductivity of the fault (which may be regarded as a fracture),
        equal to Fracture Width * Fracture Permeability.
    :ivar is_conductive: Boolean - value of True means that the fault is
        conductive. If the boolean IsFiniteConductive is also True, then
        the parameter Conductivity should be used to quantify this. If
        IsFiniteConductive is False, then the fault is regarded as
        infinite conductive, and the parameter Conductivity is not
        required.
    :ivar is_finite_conductive: Boolean - value of True means that the
        fault is finite conductive and the parameter Conductivity should
        be used to quantify this. If IsFiniteConductive is False, then
        the fault is regarded as infinite conductive, and the parameter
        Conductivity is not required.
    :ivar is_leaky: Boolean - value of True means that the fault is
        leaky and therefore that the parameter Leakage should be used to
        quantify this.
    :ivar transmissibility_reduction_ratio_of_linear_front: The
        transmissibility reduction factor of a fault in a Linear
        Composite model where the boundary of the inner and outer zones
        is a leaky fault. If T is the complete transmissibility which
        would be computed without any fault between point A and point B
        (T is a function of permeability, etc), then Tf = T * leakage.
        Therefore: leakage = 1 implies that the fault is not a barrier
        to flow at all, leakage = 0 implies that the fault is sealing
        (no transmissibility anymore at all between points A and B).
    :ivar fault_ref_id: The reference to a RESQML model representation
        of this fault.
    """

    conductivity: Optional[FractureConductivity] = field(
        default=None,
        metadata={
            "name": "Conductivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    is_conductive: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsConductive",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    is_finite_conductive: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsFiniteConductive",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    is_leaky: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsLeaky",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    transmissibility_reduction_ratio_of_linear_front: Optional[
        TransmissibilityReductionFactorOfLinearFront
    ] = field(
        default=None,
        metadata={
            "name": "TransmissibilityReductionRatioOfLinearFront ",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fault_ref_id: Optional[ResqmlModelRef] = field(
        default=None,
        metadata={
            "name": "FaultRefID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class LayerToLayerConnection:
    """Data about other layers to which this layer connects in terms of a flow
    connection.

    Comprises the identity of the other layer, and the inter-layer flow
    coefficient.

    :ivar connected_layer_ref_id: Reference to another layer to which
        this layer is connected for flow.
    :ivar inter_layer_connectivity: The Flow Parameter value between the
        two Layers.
    """

    connected_layer_ref_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConnectedLayerRefID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    inter_layer_connectivity: Optional[InterporosityFlowParameter] = field(
        default=None,
        metadata={
            "name": "InterLayerConnectivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class LinearCompositeModel(ReservoirBaseModel):
    """Linear Composite reservoir model in which the producing wellbore is in a
    homogeneous reservoir, infinite in all directions except one where the
    reservoir and/or fluid characteristics change across a linear front.

    On the farther side of the interface the reservoir is homogeneous
    and infinite but with a different mobility and/or storativity.
    There is no pressure loss at the interface between the two zones.
    """

    distance_to_mobility_interface: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToMobilityInterface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    inner_to_outer_zone_diffusivity_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "InnerToOuterZoneDiffusivityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    inner_to_outer_zone_mobility_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "InnerToOuterZoneMobilityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    orientation_of_linear_front: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfLinearFront",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class LinearCompositeWithChangingThicknessAcrossLeakyFaultModel(
    ReservoirBaseModel
):
    """Linear Composite reservoir model in which the producing wellbore is in a
    homogeneous reservoir, infinite in all directions except one where the
    reservoir and/or fluid characteristics change across a linear front.

    On the farther side of the interface the reservoir is homogeneous
    and infinite but with a different mobility and/or storativity and
    thickness.  There is a fault or barrier at the interface between the
    two zones, but this is "leaky", allowing flow across it.
    """

    distance_to_mobility_interface: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToMobilityInterface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    orientation_of_linear_front: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfLinearFront",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    region2_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "Region2Thickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    transmissibility_reduction_factor_of_linear_front: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransmissibilityReductionFactorOfLinearFront",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class LinearCompositeWithConductiveFaultModel(ReservoirBaseModel):
    """Linear Composite reservoir model in which the producing wellbore is in a
    homogeneous reservoir, infinite in all directions except one where the
    reservoir and/or fluid characteristics change across a linear front.

    On the farther side of the interface the reservoir is homogeneous
    and infinite but with a different mobility and/or storativity.
    There is a fault or barrier at the interface between the two zones,
    but this is "leaky", allowing flow across it and conductive,
    allowing flow along it. It can be thought of as a non-intersecting
    fracture.
    """

    distance_to_mobility_interface: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToMobilityInterface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fault_conductivity: Optional[str] = field(
        default=None,
        metadata={
            "name": "FaultConductivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    inner_to_outer_zone_diffusivity_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "InnerToOuterZoneDiffusivityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    inner_to_outer_zone_mobility_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "InnerToOuterZoneMobilityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    orientation_of_linear_front: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfLinearFront",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    transmissibility_reduction_factor_of_linear_front: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransmissibilityReductionFactorOfLinearFront",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class LinearCompositeWithLeakyFaultModel(ReservoirBaseModel):
    """Linear Composite reservoir model in which the producing wellbore is in a
    homogeneous reservoir, infinite in all directions except one where the
    reservoir and/or fluid characteristics change across a linear front.

    On the farther side of the interface the reservoir is homogeneous
    and infinite but with a different mobility and/or storativity.
    There is a fault or barrier at the interface between the two zones,
    but this is "leaky", allowing flow across it.
    """

    distance_to_mobility_interface: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToMobilityInterface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    inner_to_outer_zone_diffusivity_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "InnerToOuterZoneDiffusivityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    inner_to_outer_zone_mobility_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "InnerToOuterZoneMobilityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    orientation_of_linear_front: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfLinearFront",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    transmissibility_reduction_factor_of_linear_front: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransmissibilityReductionFactorOfLinearFront",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class NonHydrocarbonTest:
    """
    :ivar analysis_method:
    :ivar cell_id:
    :ivar instrument_id:
    :ivar non_hydrocarbon_concentrations:
    :ivar other_measured_properties: A generic measurement which does
        not result in a concentration measurement can be reported using
        this element with variable measure class. Example, radioactivity
        measured in units of radioactivity per unit volume.
    :ivar phases_tested:
    :ivar remark:
    :ivar sampling_point:
    :ivar test_number:
    :ivar test_pressure:
    :ivar test_temperature:
    :ivar test_time:
    :ivar test_volume:
    """

    analysis_method: List[str] = field(
        default_factory=list,
        metadata={
            "name": "AnalysisMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    cell_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "CellId",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    instrument_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InstrumentId",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    non_hydrocarbon_concentrations: Optional[OverallComposition] = field(
        default=None,
        metadata={
            "name": "NonHydrocarbonConcentrations",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    other_measured_properties: List[str] = field(
        default_factory=list,
        metadata={
            "name": "OtherMeasuredProperties",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    phases_tested: Optional[str] = field(
        default=None,
        metadata={
            "name": "PhasesTested",
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
    sampling_point: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SamplingPoint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_number: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestNumber",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
    test_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class NumericalBoundaryModel(BoundaryBaseModel):
    """
    Numerical boundary model in which any arbitrary outer shape of the reservoir
    boundary can be imposed by use of any number of straight line segments which
    together define the boundary.
    """

    drainage_area_measured: Optional[str] = field(
        default=None,
        metadata={
            "name": "DrainageAreaMeasured",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    pore_volume_measured: Optional[str] = field(
        default=None,
        metadata={
            "name": "PoreVolumeMeasured",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    single_boundary_sub_model: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SingleBoundarySubModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class NumericalDualPorosityReservoirModel(ReservoirBaseModel):
    """Numerical model with dual porosity reservoir.

    This model may have constant value or reference a grid of geometrically distributed values for the following parameters: permeability (k), thickness (h), porosity (phi), depth (Z), vertical anisotropy (KvToKr) and horizontal anisotropy (KyTokx).  Internal faults can be positioned in this reservoir.
    """

    distributed_parameters_sub_model: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistributedParametersSubModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    internal_fault_sub_model: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InternalFaultSubModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    interporosity_flow_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "InterporosityFlowParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    reservoir_zone_sub_model: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReservoirZoneSubModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    storativity_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "StorativityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class NumericalHomogeneousReservoirModel(ReservoirBaseModel):
    """Numerical model with homogeneous reservoir.

    This model may have constant value or reference a grid of geometrically distributed values for the following parameters: permeability (k), thickness (h), porosity (phi), depth (Z), vertical anisotropy (KvToKr) and horizontal anisotropy (KyTokx). Internal faults can be positioned in this reservoir.
    """

    distributed_parameters_sub_model: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistributedParametersSubModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    internal_fault_sub_model: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InternalFaultSubModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reservoir_zone_sub_model: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ReservoirZoneSubModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class OtherData(AbstractFlowTestData):
    """
    Other flow data measurements.

    :ivar data_channel: The Channel containing the Data.
    """

    data_channel: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataChannel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class OtherMeasurementTest:
    """
    Other measurement test.

    :ivar fluid_characterization_table: Fluid characterization table.
    :ivar fluid_characterization_table_format_set: A set of table format
        definitions.
    :ivar remark: Remarks and comments about this data item.
    :ivar test_number: An integer number to identify this test in a
        sequence of tests.
    :ivar other_measurement_test_step: Other measurement test step.
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
class PartiallyPenetratingModel(NearWellboreBaseModel):
    """
    Partially Penetrating model, with flowing length of wellbore less than total
    thickness of reservoir layer (as measured along wellbore).
    """

    convergence_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConvergenceSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    distance_mid_perforations_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceMidPerforationsToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    mechanical_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "MechanicalSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    perforated_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforatedLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    skin_layer2_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkinLayer2RelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class PinchOutModel(BoundaryBaseModel):
    """Pinch Out boundary model.

    The upper and lower bounding surfaces of the reservoir are sub-
    parallel and intersect some distance from the wellbore. Other
    directions are unbounded.
    """

    distance_to_pinch_out: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToPinchOut",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    orientation_of_normal_to_boundary1: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfNormalToBoundary1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
    :ivar expected_flow_qualifier: Forces a choice between a qualifier
        or one more qualified by flow and product.
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
    tag_alias: List[str] = field(
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
    :ivar overall_composition: Overall composition.
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
    :ivar safety_count: A zero-based count of a type of safety item.
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
    :ivar product_rate: The production rate of the product.
    :ivar remark: A descriptive remark relating to any significant
        events during this period.
    :ivar reporting_entity:
    :ivar start_time: The start time at a given choke setting.
    :ivar well_flowing_condition: The status of the well.
    :ivar well_status: The status of the well.
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
    product_rate: List[ProductRate] = field(
        default_factory=list,
        metadata={
            "name": "ProductRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
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
    reporting_entity: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReportingEntity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    start_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
    well_status: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellStatus",
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
class RadialCompositeModel(ReservoirBaseModel):
    """Radial Composite reservoir model, in which the wellbore is at the center of
    a circular homogeneous zone, communicating with an infinite homogeneous
    reservoir.

    The inner and outer zones have different reservoir and/or fluid
    characteristics. There is no pressure loss at the interface between
    the two zones.
    """

    distance_to_mobility_interface: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToMobilityInterface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    inner_to_outer_zone_diffusivity_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "InnerToOuterZoneDiffusivityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    inner_to_outer_zone_mobility_ratio: Optional[str] = field(
        default=None,
        metadata={
            "name": "InnerToOuterZoneMobilityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class ReservoirZoneSubModel:
    """Enables a zone within the reservoir model to be defined.

    This will have local properties which may vary from the rest of the
    reservoir model.  The zone is bounded by a polygon comprising a
    number of 2D points. It is left to the software application to
    verify these comprise a closed polygon, within which the zone
    properties apply.

    :ivar permeability: Horizontal Permeability within this zone. Note
        that this value should be used to represent any mobility changes
        in the zone, which may be due to effective permeability and
        viscosity changeds, eg for the inner region of an injection
        well.  If absent, the zone is assumed to have the same property
        as the overall reservoir model.
    :ivar porosity: Porosity within this zone.  If absent, the zone is
        assumed to have the same property as the overall reservoir
        model.
    :ivar thickness: Thickness within this zone.  If absent, the zone is
        assumed to have the same property as the overall reservoir
        model.
    :ivar bounding_polygon_point: The zone is bounded by a polygon
        comprising a number of 2D points, each one is represented by
        this 2D coordinate pair.
    """

    permeability: Optional[HorizontalRadialPermeability] = field(
        default=None,
        metadata={
            "name": "Permeability",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    porosity: Optional[Porosity] = field(
        default=None,
        metadata={
            "name": "Porosity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    thickness: Optional[TotalThickness] = field(
        default=None,
        metadata={
            "name": "Thickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    bounding_polygon_point: List[LocationIn2D] = field(
        default_factory=list,
        metadata={
            "name": "BoundingPolygonPoint",
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
    :ivar stoflashed_liquid: Stock tank oil flashed liquid properties
        and composition.
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
    :ivar sample_of_contaminant:
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
    sample_of_contaminant: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SampleOfContaminant",
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
    Sample integrity and preparation information.

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
    :ivar sample_restoration: Sample restoration.
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
class SampleRecombinationSpecification:
    """
    For a fluid sample that has been recombined from separate samples, e.g. liquid
    sample and vapor sample, this class records the specified: recombination
    conditions, the saturation pressure and  overall recombined sample composition,
    whichever of these are appropriate for this recombination.

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
    :ivar recombined_sample_fraction: Fluid sample points to a mixture
        from other samples.
    """

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
    recombined_sample_fraction: List[RecombinedSampleFraction] = field(
        default_factory=list,
        metadata={
            "name": "RecombinedSampleFraction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 2,
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
class SingleFaultModel(BoundaryBaseModel):
    """Single fault boundary model.

    A single linear boundary runs along one side of the reservoir.
    """

    boundary1_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary1Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    distance_to_boundary1: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToBoundary1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    orientation_of_normal_to_boundary1: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfNormalToBoundary1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class SingleFractureSubModel:
    """For a Horizontal Wellbore Multiple Variable Fractured Model, this is the
    model sub class which describes each fracture.

    There will be as many instances of this as there are fractures. This
    is expected to be a numerical model.

    :ivar distance_mid_fracture_height_to_bottom_boundary: For a
        hydraulic fracture, the distance between the mid-height level of
        the fracture and the lower boundary of the layer.
    :ivar fracture_conductivity: For an induced hydraulic fracture, the
        conductivity of the fracture, equal to Fracture Width * Fracture
        Permeability
    :ivar fracture_face_skin: Dimensionless value, characterizing the
        restriction to flow (+ve value, damage) or additional capacity
        for flow (-ve value, eg acidized) due to effective permeability
        across the face of a hydraulic fracture, ie controlling flow
        from reservoir into fracture. This value is stated with respect
        to radial flow using the full reservoir thickness (h), ie the
        radial flow or middle time region of a pressure transient. It
        therefore can be added, in a fractured well, to
        "ConvergenceSkinRelativeToTotalThickness" skin to yield
        "SkinRelativeToTotalThickness".
    :ivar fracture_height: In the vertical hydraulic fracture model
        (where the wellbore is horizontal), the height of the fracture.
        In the case of a horizontal wellbore, the fractures are assumed
        to extend an equal distance above and below the wellbore.
    :ivar fracture_model_type: For a Horizontal Wellbore Multiple
        Fractured Model, the model type which applies to this fracture.
        Enumeration with choices of infinite conductivity, uniform flux,
        finite conductivity, or compressible fracture finite
        conductivity.
    :ivar fracture_storativity_ratio: Dimensionless Value characterizing
        the fraction of the pore volume occupied by the fractures to the
        total of pore volume of (fractures plus reservoir).
    :ivar fracture_tip1_location: The location of the first tip of the
        fracture in the local CRS.
    :ivar fracture_tip2_location: The location of the second tip of the
        fracture (opposite side of the wellbore to the first) in the
        local CRS.
    """

    distance_mid_fracture_height_to_bottom_boundary: Optional[
        DistanceMidFractureHeightToBottomBoundary
    ] = field(
        default=None,
        metadata={
            "name": "DistanceMidFractureHeightToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_conductivity: Optional[FractureConductivity] = field(
        default=None,
        metadata={
            "name": "FractureConductivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_face_skin: Optional[FractureFaceSkin] = field(
        default=None,
        metadata={
            "name": "FractureFaceSkin",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_height: Optional[FractureHeight] = field(
        default=None,
        metadata={
            "name": "FractureHeight",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_model_type: Optional[FractureModelType] = field(
        default=None,
        metadata={
            "name": "FractureModelType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_storativity_ratio: Optional[FractureStorativityRatio] = field(
        default=None,
        metadata={
            "name": "FractureStorativityRatio",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fracture_tip1_location: Optional[LocationIn2D] = field(
        default=None,
        metadata={
            "name": "FractureTip1Location",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    fracture_tip2_location: Optional[LocationIn2D] = field(
        default=None,
        metadata={
            "name": "FractureTip2Location",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class SlantedFullyPenetratingModel(NearWellboreBaseModel):
    """
    Slanted wellbore model, with full penetrating length of wellbore open to flow.
    """

    convergence_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConvergenceSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    mechanical_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "MechanicalSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    orientation_well_trajectory: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationWellTrajectory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    skin_layer2_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkinLayer2RelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellbore_deviation_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellboreDeviationAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class SlantedPartiallyPenetratingModel(NearWellboreBaseModel):
    """
    Slanted wellbore model, with flowing length of wellbore less than total
    thickness of reservoir layer (as measured along wellbore).
    """

    convergence_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConvergenceSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    distance_mid_perforations_to_bottom_boundary: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceMidPerforationsToBottomBoundary",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    mechanical_skin_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "MechanicalSkinRelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    orientation_well_trajectory: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationWellTrajectory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    perforated_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "PerforatedLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    skin_layer2_relative_to_total_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "SkinLayer2RelativeToTotalThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    wellbore_deviation_angle: Optional[str] = field(
        default=None,
        metadata={
            "name": "WellboreDeviationAngle",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class StringData(AbstractMeasureData):
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
    :ivar incremental_gas_added: The amount of an injected gas for this
        step, and a reference to which Injected Gas composition it
        consists of. Note, multiple gases of different compositions may
        be injected at each test step.
    :ivar cumulative_gas_added: The cumulative amount of an injected gas
        up to and including this step, and a reference to which Injected
        Gas composition it consists of. Note, multiple gases of
        different compositions may be injected at each test step, and
        this element tracks the cumulative quantity of each of them.
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
class TestPeriod:
    """
    Test conditions for a production well test.

    :ivar end_time: The date and time when the test  began.
    :ivar remark: Remarks and comments about this data item.
    :ivar start_time: The date and time when the test  began.
    :ivar product_rate: The production rate of the product.
    :ivar test_period_kind: The duration of the test.
    :ivar well_flowing_condition: The duration of the test.
    :ivar uid: Unique identifier for this instance of the object.
    """

    end_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndTime",
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
    start_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
    test_period_kind: Optional[TestPeriodKind] = field(
        default=None,
        metadata={
            "name": "TestPeriodKind",
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
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
            "namespace": "",
            "required": True,
        },
    )
    threshold_minimum: Optional[EndpointQuantity] = field(
        default=None,
        metadata={
            "name": "ThresholdMinimum",
            "type": "Element",
            "namespace": "",
        },
    )
    threshold_maximum: Optional[EndpointQuantity] = field(
        default=None,
        metadata={
            "name": "ThresholdMaximum",
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass
class TwoIntersectingFaultsModel(BoundaryBaseModel):
    """Two intersecting faults boundary model.

    Two linear non-parallel boundaries run along adjacent sides of the
    reservoir and intersect at an arbitrary angle.
    """

    angle_between_boundaries: Optional[str] = field(
        default=None,
        metadata={
            "name": "AngleBetweenBoundaries",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    boundary1_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary1Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    boundary2_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary2Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    distance_to_boundary1: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToBoundary1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    distance_to_boundary2: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToBoundary2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    orientation_of_normal_to_boundary1: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfNormalToBoundary1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class TwoParallelFaultsModel(BoundaryBaseModel):
    """Two parallel faults boundary model.

    Two linear parallel boundaries run along opposite side of the
    reservoir.
    """

    boundary1_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary1Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    boundary3_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary3Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    distance_to_boundary1: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToBoundary1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    distance_to_boundary3: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToBoundary3",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    orientation_of_normal_to_boundary1: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfNormalToBoundary1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class UshapedFaultsModel(BoundaryBaseModel):
    """U-shaped faults boundary model.

    Three linear faults intersecting at 90 degrees bound the reservoir
    on three sides with the fourth side unbounded.
    """

    class Meta:
        name = "UShapedFaultsModel"

    boundary1_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary1Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    boundary2_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary2Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    boundary3_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Boundary3Type",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    distance_to_boundary1: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToBoundary1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    distance_to_boundary2: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToBoundary2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    distance_to_boundary3: Optional[str] = field(
        default=None,
        metadata={
            "name": "DistanceToBoundary3",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    orientation_of_normal_to_boundary1: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationOfNormalToBoundary1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class AbstractPvtModel:
    """
    Abstract class of  PVT model.

    :ivar custom_pvt_model_extension: Custom PVT model extension.
    :ivar pvt_model_parameter_set: A collection of parameters.
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
    :ivar fluid_component_catalog: Fluid component catalog.
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
    operator: List[str] = field(
        default_factory=list,
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

    :ivar avg_molecular_weight: The average molecular weight of the
        sample for this test.
    :ivar date: The date when this test was performed.
    :ivar density_at_flash_from_pressure_and_temperature: The density of
        the sample at the pressure and temperature conditions of this
        test.
    :ivar flash_from_pressure: This is the starting pressure for the
        sample having the Atmospheric Flash Test.
    :ivar flash_from_temperature: This is the starting temperature for
        the sample having the Atmospheric Flash Test.
    :ivar flash_gor: The gas-oil ratio of the flash in this analysis.
    :ivar flash_to_pressure: The pressure to which the sample is flashed
        in this analysis. This pressure may differ from the Standard
        Conditions at which the results are reported. Standard
        Conditions are reported for all the Analyses in the parent
        element FluidAnalysis.
    :ivar flash_to_temperature: The temperature to which the sample is
        flashed in this analysis. This temperature may differ from the
        Standard Conditions at which the results are reported. Standard
        Conditions are reported for all the Analyses in the parent
        element FluidAnalysis.
    :ivar oil_formation_volume_factor: The formation volume factor for
        the oil (liquid) phase at the conditions of this test--volume at
        test conditions/volume at standard conditions.
    :ivar overall_composition: Overall composition.
    :ivar remark: Remarks and comments about this data item.
    :ivar test_number: An integer number to identify this test in a
        sequence of tests.
    :ivar flashed_gas: Flashed gas.
    :ivar flashed_liquid: Flashed liquid.
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

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
    density_at_flash_from_pressure_and_temperature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DensityAtFlashFromPressureAndTemperature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ChannelFlowrateData(AbstractRateHistory):
    """
    This choice should be made when the Rate History is a multiple rate history, ie
    a time series of flowrates.

    :ivar input_flowrate: Flow data.
    """

    input_flowrate: Optional[AbstractPtaFlowData] = field(
        default=None,
        metadata={
            "name": "InputFlowrate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
        (generally). At each Test Step, Liquid Fraction is the liquid
        volume at this step divided by the reference volume at the
        conditions stated in this element. An actual volume at the
        reference conditions is optional. If the reference volume is the
        total volume at that test step (i.e., it varies per test step),
        then the value "test step" would be used.
    :ivar relative_volume_reference: Volume reference for the relative
        volume ratio in a constant composition expansion
        test. Referenced to liquid volume at saturation pressure
        (generally). At each Test Step, Relative Volume Ratio is the
        total volume at this step divided by the reference volume at the
        conditions stated in this element. An actual volume at the
        reference conditions is optional.
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
    :ivar liquid_fraction_reference:
    :ivar saturation_pressure:
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
    liquid_fraction_reference: List[FluidVolumeReference] = field(
        default_factory=list,
        metadata={
            "name": "LiquidFractionReference",
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
class DeconvolvedFlowData(AbstractPtaFlowData):
    """
    :ivar deconvolution: In cases where the abstract Pta pressure data
        has type: deconvolved pressure data, this is a reference, using
        data object reference, to the Deconvolution data-object
        containing details of the deconvolution process.
    """

    deconvolution: Optional[str] = field(
        default=None,
        metadata={
            "name": "Deconvolution",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DeconvolvedPressureData(AbstractPtaPressureData):
    """
    :ivar deconvolution: In cases where the abstract Pta pressure data
        has type: deconvolved pressure data, this is a reference, using
        data object reference, to the Deconvolution data-object
        containing details of the deconvolution process.
    """

    deconvolution: Optional[str] = field(
        default=None,
        metadata={
            "name": "Deconvolution",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
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
class FacilityCalibration:
    """This object contains, for a single facility, details of the calibration
    process and results whereby each locus (an acquired data point along the fiber
    optical path) is mapped to a physical location in the facility.

    This object should repeat for each distinct facility along the fiber
    optical path. Eg, a fiber optical path which runs along a flowline
    and then down a wellbore spans two facilities (flowline and
    wellbore), and each of these will have an instance of this object.

    :ivar facility_length_unit: Unit of measurement of FacilityLength
        values in DasCalibrationInputPoint and FiberLocusDepthPoint
        elements. Required for the HDF5 file attributes since HDF5 files
        do not include units of measure as standard Energistics XML
        does. This element is a duplication therefore, in the XML files.
    :ivar facility_name: This element contains the facility name.
    :ivar optical_path_distance_unit: Unit of measurement of
        OpticalPathDistance values in DasCalibrationInputPoint and
        FiberLocusDepthPoint elements. Required for the HDF5 file
        attributes since HDF5 files do not include units of measure as
        standard Energistics XML does. This element is a duplication
        therefore, in the XML files.
    :ivar remark: Textual description about the value of this field.
    :ivar wellbore: If the facility is a wellbore then optionally this
        can be used to define a Data Object Reference to a WITSML
        Wellbore object.
    :ivar calibration:
    :ivar facility_kind: The facility kind, (for example, wellbore,
        pipeline, etc).
    """

    facility_length_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "FacilityLengthUnit",
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
    optical_path_distance_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "OpticalPathDistanceUnit",
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
    wellbore: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Wellbore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    calibration: List[Calibration] = field(
        default_factory=list,
        metadata={
            "name": "Calibration",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
                    "name": "Name",
                    "type": str,
                    "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
                },
                {
                    "name": "Operator",
                    "type": str,
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
            ),
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
    dtime_end: List[str] = field(
        default_factory=list,
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
    dtim_start: List[str] = field(
        default_factory=list,
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
class FlowTestMeasurementSet:
    """This contains all the measurements associated with flow and/or measurements
    at one interval, e.g., a Wireline Formation Tester Station, a Drill Stem Test,
    a Rate Transient data set.

    There is a mandatory Location. There are any number of Test Periods.
    There are any number of Time Series of data, each of which contains
    point data in a Channel data object.

    :ivar fluid_component_catalog: Fluid component catalog.
    :ivar measured_pressure:
    :ivar remark: Textual description about the value of this field.
    :ivar measured_flow_rate:
    :ivar location: Describes the location of the reservoir connection
        from which pressure and/or flow are being measured. BUSINESS
        RULE: Can be one of: (i) a named wellbore (a WITSML object)
        together with a MD Interval; (ii) a named Wellbore Completion (a
        WITSML object with physical details of a completion), (iii) a
        named well (a WITSML object), (iv) a named Reporting Entity
        (which is a generic object to represent a location for flow
        reporting in the PRODML Simple Product Volume Reporting schema),
        or (v) a Probe on a wireline or LWD formation tester tool, in
        which case it has single Probe Depth and Probe Diameter. A
        wellbore + MD Interval, or a wellbore completion option would be
        expected for most tests.  The well, or well completion options
        could be used for a test commingling flow multiple wellbores or
        completions.  See the WITSML documentation for Completion for
        more details. The Reporting Entity option could be used for the
        testing of some less common combination of sources, eg a cluster
        of wells. NOTE that well, wellbore, well completion, wellbore
        completion and reporting entity elements are all Data Object
        References (see Energistics Common documentation). These are
        used to reference separate data objects which fully describe the
        real-world facilities concerned. However, it is not necessary
        for the separate data object to exist. The elements can be used
        as follows: - The Title element of the data object reference
        class is used to identify the name of the real-world facility,
        eg the well name, as a text string. - The mandatory Content Type
        element would contain the class of the referenced object (the
        same as the element name). - The mandatory  UUID String can
        contain any dummy uuid-like string.
    :ivar other_data:
    :ivar test_period: Test conditions for a production well test.
    :ivar uid: Unique identifier for this instance of the object.
    """

    fluid_component_catalog: Optional[FluidComponentCatalog] = field(
        default=None,
        metadata={
            "name": "FluidComponentCatalog",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    measured_pressure: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MeasuredPressure",
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
    measured_flow_rate: List[AbstractPtaFlowData] = field(
        default_factory=list,
        metadata={
            "name": "MeasuredFlowRate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    location: Optional[FlowTestLocation] = field(
        default=None,
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    other_data: List[OtherData] = field(
        default_factory=list,
        metadata={
            "name": "OtherData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_period: Optional[TestPeriod] = field(
        default=None,
        metadata={
            "name": "TestPeriod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class FluidCharacterizationTableFormatSet:
    """
    A set of table format definitions.

    :ivar fluid_characterization_table_format: Fluid characterization
        table format.
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
class LayerModel:
    """Contains the data about a layer model for PTA or Inflow analysis.

    This class contains common parameters and then model sections each
    report the parameter values for the pressure transient model used to
    describe the later. These are: near wellbore, reservoir, and
    boundary sections. Example: closed reservoir boundary section model
    will report 4 distances to boundaries.

    :ivar aggregate_layers_model: If set to True, indicates that this
        layer represents the analysis of the total number of individual
        layers at this Test Location. Example: it will represent the
        total Kh (permeability-thickness product) and Total Skin of the
        Test Location. If False then this layer represents just one of
        the total number of reservoir layer(s) tested at this Test
        Location.
    :ivar boundary_model: For this layer model, the Boundary Model which
        is used - which will be a child node of this layer model.
    :ivar geologic_feature: The name of the geology feature (typically,
        layer or layers) to which this model layer corresponds.
    :ivar layer_laminar_flow_coefficient: This is the coefficient for
        laminar flow pressure drop.
    :ivar layer_productivity_index: This is the productivity Index of
        the layer, expressed in terms of flowrate/pressure.
    :ivar layer_turbulent_flow_coefficient: This is the coefficient for
        turbulent flow pressure drop in the Inflow Performance
        Relationship.  In which dP=J*Q+F*Q**2. This parameter is F and
        the Productivity Index is J.
    :ivar md_bottom_layer: The measured depth bottom of this layer, as
        seen along the wellbore.
    :ivar md_top_layer: The measured depth top of this layer, as seen
        along the wellbore.
    :ivar name: The name of the layer for which this later model
        applies.  Probably a geologically meaningful name.
    :ivar near_wellbore_model: For this layer model, the Near Wellbore
        Model which is used - which will be a child node of this layer
        model.
    :ivar reservoir_model: For this layer model, the Reservoir Model
        which is used - which will be a child node of this layer model.
    :ivar layer_to_layer_connection:
    :ivar uid: Unique identifier for this instance of the object.
    """

    aggregate_layers_model: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AggregateLayersModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    boundary_model: Optional[BoundaryBaseModel] = field(
        default=None,
        metadata={
            "name": "BoundaryModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    geologic_feature: List[str] = field(
        default_factory=list,
        metadata={
            "name": "GeologicFeature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    layer_laminar_flow_coefficient: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LayerLaminarFlowCoefficient",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    layer_productivity_index: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LayerProductivityIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    layer_turbulent_flow_coefficient: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LayerTurbulentFlowCoefficient",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    md_bottom_layer: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MdBottomLayer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    md_top_layer: List[str] = field(
        default_factory=list,
        metadata={
            "name": "MdTopLayer",
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
    near_wellbore_model: Optional[NearWellboreBaseModel] = field(
        default=None,
        metadata={
            "name": "NearWellboreModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    reservoir_model: Optional[ReservoirBaseModel] = field(
        default=None,
        metadata={
            "name": "ReservoirModel",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    layer_to_layer_connection: List[LayerToLayerConnection] = field(
        default_factory=list,
        metadata={
            "name": "LayerToLayerConnection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class LogLogAnalysis:
    """
    Contains the result data needed to plot or overlay measured data and simulated
    data for PTA in a standard log-log axes plot.

    :ivar derivative_smoothing_factor_l: The smoothing factor for the
        derivative curve. Common symbolized as L.
    :ivar remark: Textual description about the value of this field.
    :ivar analysis_pressure: The transformed pressure and derivative
        (contained in referenced Channels) (to log-log transform) used
        in this log-log analysis.
    :ivar analysis_line:
    :ivar log_log_pressure_transform: Describes the type of transform
        applied to the pressure axis of the log log plot. Enum. Options:
        pressure, and various pressure/flowrate functions.
    :ivar log_log_time_data_transform: Describes the type of transform
        applied to the time axis of the log log plot. Enum. Options:
        delta-time (ie, no tranform) and various superposition time
        functions (ie, time transformed to represent equivalent drawdown
        time using superposition).
    """

    derivative_smoothing_factor_l: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DerivativeSmoothingFactorL",
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
    analysis_pressure: Optional[AbstractPtaPressureData] = field(
        default=None,
        metadata={
            "name": "AnalysisPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    analysis_line: List[AnalysisLine] = field(
        default_factory=list,
        metadata={
            "name": "AnalysisLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    log_log_pressure_transform: Optional[LogLogPressureTransform] = field(
        default=None,
        metadata={
            "name": "LogLogPressureTransform",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    log_log_time_data_transform: Optional[LogLogTimeTransform] = field(
        default=None,
        metadata={
            "name": "LogLogTimeDataTransform",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class MeasuredFlowData(AbstractPtaFlowData):
    """
    Pressure data measured during the flow test.
    """


@dataclass
class MeasuredPressureData(AbstractPtaPressureData):
    """
    Pressure data measured during the flow test.
    """


@dataclass
class NonHydrocarbonAnalysis:
    flow_test_activity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FlowTestActivity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    fluid_sample: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FluidSample",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    non_hydrocarbon_test: List[NonHydrocarbonTest] = field(
        default_factory=list,
        metadata={
            "name": "NonHydrocarbonTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class OutputFlowData(AbstractPtaFlowData):
    """."""


@dataclass
class OutputPressureData(AbstractPtaPressureData):
    """."""


@dataclass
class PreProcessedFlowData(AbstractPtaFlowData):
    """
    :ivar pre_process: In cases where the abstract Pta pressure data has
        type: deconvolved pressure data, this is a reference, using data
        object reference, to the PtaDataPreProcess data-object
        containing details of the pre-processing applied.
    """

    pre_process: Optional[str] = field(
        default=None,
        metadata={
            "name": "PreProcess",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class PreProcessedPressureData(AbstractPtaPressureData):
    """
    :ivar pre_process: In cases where the abstract Pta pressure data has
        type: deconvolved pressure data, this is a reference, using data
        object reference, to the PtaDataPreProcess data-object
        containing details of the pre-processing applied.
    """

    pre_process: Optional[str] = field(
        default=None,
        metadata={
            "name": "PreProcess",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
    facility_alias: List[str] = field(
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
    :ivar volume_value: A possibly temperature and pressure corrected
        volume value.
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

    :ivar closing_inventory:
    :ivar duration: the duration of volume produced at facility
    :ivar opening_inventory:
    :ivar reporting_entity: Reporting Entity: The top-level entity in
        hierarchy structure.
    :ivar start_date: The starting date of the month.
    :ivar disposition:
    :ivar deferred_production_event: Information about the event or
        incident that caused production to be deferred.
    :ivar injection: Volume injected per reporting entity.
    :ivar production: Product volume that is produce from a reporting
        entity.
    """

    closing_inventory: List[AbstractProductQuantity] = field(
        default_factory=list,
        metadata={
            "name": "ClosingInventory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    duration: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Duration",
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
    reporting_entity: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReportingEntity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    start_date: List[str] = field(
        default_factory=list,
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
class SpecializedAnalysis:
    """This is an analysis not defined by a PTA model but performed on some
    specialized plot.

    It can report using AnyParameter which allows use of any parameter
    as used in the PTA models, or report Custom Parameters. See these
    classes for more information.

    :ivar any_parameter: Allows Parameters from the library included in
        the schema to be added to the Specialized Analysis. Type is
        AbstractParameter and the concrete instances are all Parameters.
    :ivar custom_parameter: Allows Custom Parameters to be added to the
        Specialized Analysis. See Custom Parameter for how its
        properties are defined.
    :ivar remark: Textual description about the value of this field.
    :ivar specialized_analysis_type: The type of specialized analysis.
        Descriptive text. These are not cataloged in the data model.
    :ivar specialized_xaxis_description: The transform of X axis data
        described textually, for the Specialized Analysis concerned.
    :ivar specialized_yaxis_description: The transform of Y axis data
        described textually, for the Specialized Analysis concerned.
    :ivar analysis_pressure_function: The transformed pressure and
        derivative (contained in referenced Channels) (transformed to
        the trasnform of this specialized analysis) used in this
        analysis. The transforms of Y and X axes are described textually
        in the Specialized [X orY] Axis Description elements.
    :ivar analysis_line:
    """

    any_parameter: List[AbstractParameter] = field(
        default_factory=list,
        metadata={
            "name": "AnyParameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    custom_parameter: List[CustomParameter] = field(
        default_factory=list,
        metadata={
            "name": "CustomParameter",
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
    specialized_analysis_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecializedAnalysisType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    specialized_xaxis_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecializedXAxisDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    specialized_yaxis_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecializedYAxisDescription",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    analysis_pressure_function: Optional[AbstractPtaPressureData] = field(
        default=None,
        metadata={
            "name": "AnalysisPressureFunction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    analysis_line: List[AnalysisLine] = field(
        default_factory=list,
        metadata={
            "name": "AnalysisLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
    :ivar injected_gas: The composition of one or more injected gases
        used in the swelling test.
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
    vapor_composition: List[FluidComponentFraction] = field(
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
class WaterAnalysisTestStep:
    """
    Water analysis test step.

    :ivar dissolved_co2:
    :ivar dissolved_h2_s:
    :ivar dissolved_o2:
    :ivar p_h:
    :ivar remark: Remarks and comments about this data item.
    :ivar resistivity:
    :ivar solution_gas_water_ratio: The solution gas-water ratio for the
        water analysis test step.
    :ivar step_number: The step number is the index of a (P,T) step in
        the overall test.
    :ivar step_pressure: The pressure for this test step.
    :ivar step_temperature: The temperature for this test step.
    :ivar turbidity:
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
    :ivar flashed_gas:
    :ivar uid: A unique identifier for this data element. It is not
        globally unique (not a uuid) and only need be unique within the
        context of the parent top-level object.
    """

    dissolved_co2: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DissolvedCO2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dissolved_h2_s: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DissolvedH2S",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    dissolved_o2: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DissolvedO2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    p_h: List[str] = field(
        default_factory=list,
        metadata={
            "name": "pH",
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
    turbidity: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Turbidity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
    flashed_gas: Optional[FlashedGas] = field(
        default=None,
        metadata={
            "name": "FlashedGas",
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
class AbstractCompositionalModel(AbstractPvtModel):
    """
    Abstract class of compositional model.

    :ivar binary_interaction_coefficient_set: Binary interaction
        coefficient set.
    :ivar component_property_set: Component property set.
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
    :ivar reporting_entity_volumes: Contains all the volumes for a
        single reporting entity. It contains a reference back to the
        reporting entity using its UUID for reference.
    """

    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"

    end_date: Optional[str] = field(
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
    start_date: Optional[str] = field(
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
class DeconvolutionOutput:
    """
    This contains the output curves from a deconvolution.

    :ivar deconvolution_reference_flowrate_value: The reference flow
        condition at which the corresponding deconvolved pressure
        constant drawdown response is calculated.
    :ivar deconvolved_pressure: The result of deconvolution: a
        deconvolved pressure which corresponds to the constant rate
        drawdown response at the reference flow condition.
    """

    deconvolution_reference_flowrate_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "DeconvolutionReferenceFlowrateValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    deconvolved_pressure: Optional[DeconvolvedPressureData] = field(
        default=None,
        metadata={
            "name": "DeconvolvedPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class DrillStemTest:
    """
    Typically performed using tools conveyed on the drill string, one interval at a
    time.
    """

    interval_measurement_set: Optional[FlowTestMeasurementSet] = field(
        default=None,
        metadata={
            "name": "IntervalMeasurementSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
    :ivar fluid_characterization_parameter_set: The constant definition
        used in the table.
    :ivar fluid_characterization_table: Fluid characterization table.
    :ivar reference_separator_stage: Reference to the separator stage.
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
    fluid_characterization_parameter_set: Optional[
        FluidCharacterizationParameterSet
    ] = field(
        default=None,
        metadata={
            "name": "FluidCharacterizationParameterSet",
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
class FormationTesterStation:
    """Performed using formation tester tools conveyed on wireline, one interval at
    a time.

    A normal job would consist of multiple interval tests, each is
    represented by its own Flow Test Activity, which are collected in
    the Flow Test Job.

    :ivar tie_in_log: References a log containing a wireline formation
        test  tie-in (e.g. gamma ray curve) vs. depth data.
    :ivar interval_measurement_set:
    """

    tie_in_log: Optional[str] = field(
        default=None,
        metadata={
            "name": "TieInLog",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    interval_measurement_set: Optional[FlowTestMeasurementSet] = field(
        default=None,
        metadata={
            "name": "IntervalMeasurementSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class InjectionFlowTest:
    """Regularly  performed using the well's permanent production string,  as a
    steady-state test to assess long-term well performance and as an input for
    reservoir management.

    Optionally, this is can include  a transient test, normally a fall-
    off test.

    :ivar effective_date: The date and time from which this well test is
        used in production allocation processes as representative of the
        well’s performance
    :ivar validated: A flag which is to be set if this test is validated
        and therefore able to used in processes such as production
        allocation.
    :ivar well_test_method: Description or name of the method used to
        conduct the well test.
    :ivar interval_measurement_set:
    """

    effective_date: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EffectiveDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    validated: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Validated",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_test_method: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellTestMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    interval_measurement_set: Optional[FlowTestMeasurementSet] = field(
        default=None,
        metadata={
            "name": "IntervalMeasurementSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class InterferingFlowTestInterval:
    """
    Measurements pertaining to the interfering flow, in the case of an interference
    test.

    :ivar flow_test_measurement_set_ref: A reference (using uid) to the
        flow test measurement set which contains the data concerning the
        interfering flow, in the case of an interference test. (This
        other flow test measurement set will be in the same Flow Test
        Activity top level object and will contain the location, flow
        rates etc of the intefering flow).
    :ivar interfering_flowrate_ref: A reference (using uid) to the flow
        rate which is the measurement of the interfering flow, in the
        case of an interference test.
    :ivar simulated_interference_pressure_removed: A flag to indicate if
        the Simulated Interference Pressure for this intefering flow
        interval, has been removed from the measured data. If true, then
        the corrected measured data should be analysable without having
        to consider the intererence effect further.
    :ivar test_period_ref: A reference (using uid) to the test period(s)
        whose effect the interfering flow is being allowed for, in the
        case of an interference test. If unspecified, it should be
        assumed that all test periods can potentially give rise to an
        interference effect.
    :ivar simulated_interference_pressure: The simulated interference
        pressure (which will be at the observation interval), in the
        case of an interference test.
    :ivar uid: Unique identifier for this instance of the object.
    """

    flow_test_measurement_set_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowTestMeasurementSetRef",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    interfering_flowrate_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "InterferingFlowrateRef",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    simulated_interference_pressure_removed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "SimulatedInterferencePressureRemoved",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    test_period_ref: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestPeriodRef",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    simulated_interference_pressure: Optional[OutputPressureData] = field(
        default=None,
        metadata={
            "name": "SimulatedInterferencePressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class InterwellTest:
    """
    Performed on multiple  wellbores, where an interval in one wellbore is flowing
    and one or more intervals in other wellbores are observing the interfering
    pressure.
    """

    interval_measurement_set: List[FlowTestMeasurementSet] = field(
        default_factory=list,
        metadata={
            "name": "IntervalMeasurementSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
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
    facility_alias: List[str] = field(
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
class ProductionFlowTest:
    """Regularly  performed using the well's permanent production string,  as a
    steady-state test to assess long-term well performance and as an input to
    production allocation.

    This is NOT expected to be a transient test.

    :ivar effective_date: The date and time from which this well test is
        used in production allocation processes as representative of the
        well’s performance
    :ivar validated: A flag which is to be set if this test is validated
        and therefore able to used in processes such as production
        allocation.
    :ivar well_test_method: Description or name of the method used to
        conduct the well test.
    :ivar interval_measurement_set:
    """

    effective_date: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EffectiveDate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    validated: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Validated",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    well_test_method: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellTestMethod",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    interval_measurement_set: Optional[FlowTestMeasurementSet] = field(
        default=None,
        metadata={
            "name": "IntervalMeasurementSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
class ProductionTransientTest:
    """
    Typically performed using the well's permanent production string,  one interval
    at a time.
    """

    interval_measurement_set: Optional[FlowTestMeasurementSet] = field(
        default=None,
        metadata={
            "name": "IntervalMeasurementSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class ProductionWellTests(AbstractSimpleProductVolume):
    """
    This is the collection of ProductionWellTests.

    :ivar end_date: Validate.
    :ivar flow_test_activity: BUSINESS RULE: In this usage, this link is
        expected to be a  type of  Production Flow Test or Injection
        Flow Test. The Production Flow Test has  validation and
        effective date for allocation purposes. Flow Test Location is
        expected to be a Reporting Entity (same as a volume, etc) in
        standard SPVR usage
    :ivar nominal_period_kind: Validate.
    :ivar start_date: Description or name of the method used to conduct
        the well test.
    """

    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"

    end_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "EndDate",
            "type": "Element",
            "required": True,
        },
    )
    flow_test_activity: Optional[str] = field(
        default=None,
        metadata={
            "name": "FlowTestActivity",
            "type": "Element",
            "required": True,
        },
    )
    nominal_period_kind: Optional[Union[ReportingDurationKind, str]] = field(
        default=None,
        metadata={
            "name": "NominalPeriodKind",
            "type": "Element",
            "required": True,
        },
    )
    start_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "StartDate",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class PtaAnalysis(AbstractAnalysis):
    """Contains the input and output (simulated) data needed for analysis of
    pressure (PTA) (ie where flowrate is the boundary condition).

    Can contain log log plots of the data. Can contain Specialized
    Analyses and their plots of the data.  The Model data itself is
    contained in the WellboreModel and LayerModel elements of the
    TestLocationAnalysis.

    :ivar initial_pressure_p0_for_impulse_test: Only required for
        Impulse type tests: P0 (Pressure at time zero), the instant
        pressure at the start of the test.
    :ivar simulated_pressure_gauge_drift: Optional element to report the
        addition of gauge drift to the pressure signal for Test Design
        purposes.  The value is equal to the magnitude of the gauge
        drift in terms of units of pressure per unit of time, applied
        across the time duration of this Result. A negative sign means
        the drift is negative, ie the gauge is drifting to read a less
        positive value than the correct value as time passes.
    :ivar simulated_pressure_gauge_noise: Optional element to report the
        addition of noise to the pressure signal for Test Design
        purposes.  The value is equal to the magnitude of the random
        noise added. Ie, if value is "x" then random noise distributed
        within +/-x has been added.
    :ivar simulated_pressure_gauge_resolution: Optional element to
        report the addition of gauge resolution to the pressure signal
        for Test Design purposes.  The value is equal to the magnitude
        of the gauge resolution.
    :ivar input_pressure: The pressure (in a Channel) which is being
        analysed in this PTA.
    :ivar rate_history: Choice between full rate history (time series)
        and single flowrate and time (Q &amp; tp).
    :ivar measured_log_log_data:
    :ivar simulated_log_log_data:
    :ivar simulated_pressure: Reference to the UID of the Output
        Pressure Data from this Analysis. This will be a simulated
        response. For Test Design this will be the only pressure time
        series present.
    :ivar specialized_analysis:
    """

    initial_pressure_p0_for_impulse_test: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InitialPressureP0ForImpulseTest",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    simulated_pressure_gauge_drift: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SimulatedPressureGaugeDrift",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    simulated_pressure_gauge_noise: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SimulatedPressureGaugeNoise",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    simulated_pressure_gauge_resolution: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SimulatedPressureGaugeResolution",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    input_pressure: Optional[AbstractPtaPressureData] = field(
        default=None,
        metadata={
            "name": "InputPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    rate_history: Optional[AbstractRateHistory] = field(
        default=None,
        metadata={
            "name": "RateHistory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    measured_log_log_data: Optional[LogLogAnalysis] = field(
        default=None,
        metadata={
            "name": "MeasuredLogLogData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    simulated_log_log_data: Optional[LogLogAnalysis] = field(
        default=None,
        metadata={
            "name": "SimulatedLogLogData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    simulated_pressure: Optional[OutputPressureData] = field(
        default=None,
        metadata={
            "name": "SimulatedPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    specialized_analysis: List[SpecializedAnalysis] = field(
        default_factory=list,
        metadata={
            "name": "SpecializedAnalysis",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )


@dataclass
class RtaAnalysis(AbstractAnalysis):
    """
    Contains the input data needed for analysis of flowrate (RTA) (ie where
    pressure is the boundary condition).

    :ivar input_flowrate_data: The flow rate (in a Channel) which is
        being analysed in this RTA.
    :ivar input_pressure: The pressure (in a Channel) which is being
        analysed in this RTA.
    :ivar simulated_log_log_data:
    :ivar measured_log_log_data:
    :ivar simulated_flowrate: The simulated flow rate (in a Channel)
        which is the output of this RTA.
    :ivar specialized_analysis:
    """

    input_flowrate_data: Optional[AbstractPtaFlowData] = field(
        default=None,
        metadata={
            "name": "InputFlowrateData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    input_pressure: Optional[AbstractPtaPressureData] = field(
        default=None,
        metadata={
            "name": "InputPressure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    simulated_log_log_data: Optional[LogLogAnalysis] = field(
        default=None,
        metadata={
            "name": "SimulatedLogLogData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    measured_log_log_data: Optional[LogLogAnalysis] = field(
        default=None,
        metadata={
            "name": "MeasuredLogLogData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    simulated_flowrate: Optional[OutputFlowData] = field(
        default=None,
        metadata={
            "name": "SimulatedFlowrate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    specialized_analysis: List[SpecializedAnalysis] = field(
        default_factory=list,
        metadata={
            "name": "SpecializedAnalysis",
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
    :ivar destination_terminal:
    :ivar end_time: The date and time when the lifting ended.
    :ivar loading_terminal:
    :ivar product_quantity: The amount of product lifted.
    :ivar start_time: The date and time when the lifting began.
    :ivar tanker:
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
    destination_terminal: List[str] = field(
        default_factory=list,
        metadata={
            "name": "DestinationTerminal",
            "type": "Element",
        },
    )
    end_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EndTime",
            "type": "Element",
        },
    )
    loading_terminal: Optional[str] = field(
        default=None,
        metadata={
            "name": "LoadingTerminal",
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
    start_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StartTime",
            "type": "Element",
        },
    )
    tanker: Optional[str] = field(
        default=None,
        metadata={
            "name": "Tanker",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Transfer(AbstractSimpleProductVolume):
    """Information about products transferred across asset group boundaries or
    leaving the jurisdiction of an operator.

    This may include pipeline exports, output to refineries, etc.

    :ivar destination_facility:
    :ivar end_time: Date and time when the transfer ended.
    :ivar product_transfer_quantity: The amount of product transferred.
    :ivar source_facility:
    :ivar start_time: The date and time when the transfer began.
    :ivar transfer_kind: Specifies the kind of transfer. See enum
        TransferKind.
    """

    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"

    destination_facility: Optional[str] = field(
        default=None,
        metadata={
            "name": "DestinationFacility",
            "type": "Element",
            "required": True,
        },
    )
    end_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EndTime",
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
    source_facility: Optional[str] = field(
        default=None,
        metadata={
            "name": "SourceFacility",
            "type": "Element",
            "required": True,
        },
    )
    start_time: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StartTime",
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
class VerticalInterferenceTest:
    """
    Performed on multiple intervals in the same wellbore, where one interval is
    flowing and one or more intervals are observing the interfering pressure.

    :ivar tie_in_log: References a log containing a wireline formation
        test  tie-in (e.g. gamma ray curve) vs. depth data.
    :ivar interval_measurement_set:
    """

    tie_in_log: Optional[str] = field(
        default=None,
        metadata={
            "name": "TieInLog",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    interval_measurement_set: List[FlowTestMeasurementSet] = field(
        default_factory=list,
        metadata={
            "name": "IntervalMeasurementSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class WaterAnalysisTest:
    """
    Water analysis test.

    :ivar liquid_gravity: The liquid gravity for the water analysis
        test.
    :ivar remark: Remarks and comments about this data item.
    :ivar salinity_per_mass: The salinity for the water analysis test.
    :ivar salinity_per_volume:
    :ivar test_method:
    :ivar test_number: An integer number to identify this test in a
        sequence of tests.
    :ivar total_alkalinity_per_mass:
    :ivar total_alkalinity_per_volume:
    :ivar total_dissolved_solids_per_mass: The total dissolved solids
        for the water analysis test.
    :ivar total_dissolved_solids_per_volume:
    :ivar total_hardness_per_mass: The total water hardness for the
        water analysis test.
    :ivar total_hardness_per_volume:
    :ivar total_sediment_solids_per_mass:
    :ivar total_sediment_solids_per_volume:
    :ivar total_suspended_solids_per_mass: The total suspended solids
        for the water analysis test.
    :ivar total_suspended_solids_per_volume:
    :ivar water_analysis_test_step: Water analysis test step.
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
    remark: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Remark",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    salinity_per_mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SalinityPerMass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    salinity_per_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SalinityPerVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    test_method: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TestMethod",
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
    total_alkalinity_per_mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalAlkalinityPerMass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_alkalinity_per_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalAlkalinityPerVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_dissolved_solids_per_mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalDissolvedSolidsPerMass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_dissolved_solids_per_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalDissolvedSolidsPerVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_hardness_per_mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalHardnessPerMass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_hardness_per_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalHardnessPerVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_sediment_solids_per_mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalSedimentSolidsPerMass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_sediment_solids_per_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalSedimentSolidsPerVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_suspended_solids_per_mass: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalSuspendedSolidsPerMass",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
        },
    )
    total_suspended_solids_per_volume: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TotalSuspendedSolidsPerVolume ",
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
class WaterLevelTest:
    """The test to monitor the water level, sometimes required for regulatory
    purpose.

    For example, see TxRRC H-15.
    """

    interval_measurement_set: Optional[FlowTestMeasurementSet] = field(
        default=None,
        metadata={
            "name": "IntervalMeasurementSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
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
            "min_occurs": 1,
        },
    )


@dataclass
class AbstractCompositionalEoSmodel(AbstractCompositionalModel):
    """
    Abstract class of compositional EoS model.
    """

    class Meta:
        name = "AbstractCompositionalEoSModel"


@dataclass
class AbstractCompositionalViscosityModel(AbstractCompositionalModel):
    """
    Abstract class of compositional viscosity model.

    :ivar phase: The phase the compositional viscosity model applies to.
    """

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
class DeconvolutionMultipleOutput(AbstractDeconvolutionOutput):
    """
    This element is chosen when separate individual deconvolution outputs apply to
    corresponding individual Test Periods.

    :ivar test_period_output_ref_id: Where deconvolution has been
        performed to generate deconvolved pressure over multiple time
        periods, this is the uid of the time period for this deconvolved
        pressure channel.
    :ivar deconvolution_multiple_output:
    """

    test_period_output_ref_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TestPeriodOutputRefId",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )
    deconvolution_multiple_output: Optional[DeconvolutionOutput] = field(
        default=None,
        metadata={
            "name": "DeconvolutionMultipleOutput",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


@dataclass
class DeconvolutionSingleOutput(AbstractDeconvolutionOutput):
    """
    This element is chosen when a single deconvolution output applies across all
    Test Periods.
    """

    deconvolution_single_output: Optional[DeconvolutionOutput] = field(
        default=None,
        metadata={
            "name": "DeconvolutionSingleOutput",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/prodmlv2",
            "required": True,
        },
    )


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
    :ivar crew_count: A one-based count of personnel on a type of crew.
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
class WaterAnalysis:
    """
    A collection of any one or more fluid analyses on water.

    :ivar fluid_sample:
    :ivar sample_integrity_and_preparation:
    :ivar water_analysis_test: Water analysis test.
    :ivar water_sample_component:
    """

    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"

    fluid_sample: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidSample",
            "type": "Element",
            "required": True,
        },
    )
    sample_integrity_and_preparation: Optional[
        SampleIntegrityAndPreparation
    ] = field(
        default=None,
        metadata={
            "name": "SampleIntegrityAndPreparation",
            "type": "Element",
        },
    )
    water_analysis_test: List[WaterAnalysisTest] = field(
        default_factory=list,
        metadata={
            "name": "WaterAnalysisTest",
            "type": "Element",
        },
    )
    water_sample_component: List[WaterSampleComponent] = field(
        default_factory=list,
        metadata={
            "name": "WaterSampleComponent",
            "type": "Element",
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
    :ivar solution_gas_oil_ratio: The solution gas oil ratio for the
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
    solution_gas_oil_ratio: List[str] = field(
        default_factory=list,
        metadata={
            "name": "SolutionGasOilRatio",
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
class FrictionTheory(AbstractCompositionalViscosityModel):
    """
    Friction theory.

    :ivar prsv_parameter: PRSV parameter.
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
    A collection of any one or more fluid analyses on hydrocarbons.

    :ivar fluid_sample:
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

    class Meta:
        namespace = "http://www.energistics.org/energyml/data/prodmlv2"

    fluid_sample: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidSample",
            "type": "Element",
            "required": True,
        },
    )
    atmospheric_flash_test_and_compositional_analysis: List[
        AtmosphericFlashTestAndCompositionalAnalysis
    ] = field(
        default_factory=list,
        metadata={
            "name": "AtmosphericFlashTestAndCompositionalAnalysis",
            "type": "Element",
        },
    )
    constant_composition_expansion_test: List[
        ConstantCompositionExpansionTest
    ] = field(
        default_factory=list,
        metadata={
            "name": "ConstantCompositionExpansionTest",
            "type": "Element",
        },
    )
    constant_volume_depletion_test: List[ConstantVolumeDepletionTest] = field(
        default_factory=list,
        metadata={
            "name": "ConstantVolumeDepletionTest",
            "type": "Element",
        },
    )
    differential_liberation_test: List[DifferentialLiberationTest] = field(
        default_factory=list,
        metadata={
            "name": "DifferentialLiberationTest",
            "type": "Element",
        },
    )
    separator_test: List[FluidSeparatorTest] = field(
        default_factory=list,
        metadata={
            "name": "SeparatorTest",
            "type": "Element",
        },
    )
    interfacial_tension_test: List[InterfacialTensionTest] = field(
        default_factory=list,
        metadata={
            "name": "InterfacialTensionTest",
            "type": "Element",
        },
    )
    multiple_contact_miscibility_test: List[
        MultipleContactMiscibilityTest
    ] = field(
        default_factory=list,
        metadata={
            "name": "MultipleContactMiscibilityTest",
            "type": "Element",
        },
    )
    transport_test: List[OtherMeasurementTest] = field(
        default_factory=list,
        metadata={
            "name": "TransportTest",
            "type": "Element",
        },
    )
    sample_integrity_and_preparation: Optional[
        SampleIntegrityAndPreparation
    ] = field(
        default=None,
        metadata={
            "name": "SampleIntegrityAndPreparation",
            "type": "Element",
        },
    )
    saturation_test: List[SaturationTest] = field(
        default_factory=list,
        metadata={
            "name": "SaturationTest",
            "type": "Element",
        },
    )
    slim_tube_test: List[SlimTubeTest] = field(
        default_factory=list,
        metadata={
            "name": "SlimTubeTest",
            "type": "Element",
        },
    )
    stoanalysis: List[Stoanalysis] = field(
        default_factory=list,
        metadata={
            "name": "STOAnalysis",
            "type": "Element",
        },
    )
    swelling_test: List[SwellingTest] = field(
        default_factory=list,
        metadata={
            "name": "SwellingTest",
            "type": "Element",
        },
    )
    vapor_liquid_equilibrium_test: List[VaporLiquidEquilibriumTest] = field(
        default_factory=list,
        metadata={
            "name": "VaporLiquidEquilibriumTest",
            "type": "Element",
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
    name: List[str] = field(
        default_factory=list,
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
    facility_alias: List[str] = field(
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
    facility_alias: List[str] = field(
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
