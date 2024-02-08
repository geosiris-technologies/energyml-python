from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class AbstractContactRepresentationPart:
    """
    Parent class of the sealed and nonsealed contact elements.

    :ivar index: The index of the contact. Indicates identity of the
        contact in the surface framework context. It is used for contact
        identities and to find the interpretation of this particular
        contact.
    """

    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class AbstractParameterKey:
    """Abstract class describing a key used to identify a parameter value.

    When multiple values are provided for a given parameter, provides a way to identify the parameter through its association with an object, a time index...
    """


@dataclass
class AbstractParametricLineArray:
    """Defines an array of parametric lines.

    The array size is obtained from context. In the current schema, this
    may be as simple as a 1D array (#Lines=count) or a 2D array #Lines =
    NIL x NJL for an IJK grid representation.
    """


@dataclass
class AbstractPoint3DArray:
    """The abstract class of 3D points implemented in a single fashion for the
    schema.

    Abstraction allows a variety of instantiations for efficiency or to
    implicitly provide additional geometric information about a data-
    object. For example, parametric points can be used to implicitly
    define a wellbore trajectory using an underlying parametric line, by
    the specification of the control points along the parametric line.
    The dimensionality of the array of 3D points is based on context
    within an instance.
    """

    class Meta:
        name = "AbstractPoint3dArray"


@dataclass
class AbstractPropertyKind:
    pass


@dataclass
class AbstractSeismicCoordinates:
    """Parent class is used to associate horizon and fault representations to
    seismic 2D and seismic 3D technical features.

    It stores a 1-to-1 mapping between geometry coordinates (usually X,
    Y, Z) and trace or inter-trace positions on a seismic survey.
    """

    seismic_support: Optional[str] = field(
        default=None,
        metadata={
            "name": "SeismicSupport",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class AbstractValueArray:
    """Generic representation of an array of numeric, Boolean, and string values.

    Each derived element provides specialized implementation for
    specific content types or for optimization of the representation.
    """


class BoundaryRelation(Enum):
    """
    The enumerated attributes of a horizon.

    :cvar CONFORMABLE: If used uniquely, then it means the horizon is
        conformable above and below. If used with unconformity, then it
        means partial unconformity.
    :cvar UNCONFORMABLE_BELOW_AND_ABOVE:
    :cvar UNCONFORMABLE_ABOVE: If used with conformable, then it means
        partial unconformity.
    :cvar UNCONFORMABLE_BELOW: If used with conformable, then it means
        partial unconformity.
    """

    CONFORMABLE = "conformable"
    UNCONFORMABLE_BELOW_AND_ABOVE = "unconformable below and above"
    UNCONFORMABLE_ABOVE = "unconformable above"
    UNCONFORMABLE_BELOW = "unconformable below"


class CellShape(Enum):
    """Used to indicate that all cells are of a uniform topology, i.e., have the
    same number of nodes per cell.

    This information is supplied by the RESQML writer to indicate the complexity of the grid geometry, as an aide to the RESQML reader.
    If a specific cell shape is not appropriate, then use polyhedral.
    BUSINESS RULE: Should be consistent with the actual geometry of the grid.

    :cvar TETRAHEDRAL: All grid cells are constrained to have only 4
        nodes/cell with 4 faces/cell, 3 nodes/face, 4 nodes/cell for all
        cells (degeneracy allowed).
    :cvar PYRAMIDAL: All grid cells are constrained to have only 5
        nodes/cell with 5 faces/cell, with 1 quadrilateral face and 4
        triangular faces.
    :cvar PRISM: All grid cells are constrained to have 6 nodes/cell
        with 5 faces/cell, with 3 quadrilateral faces and 2 non-adjacent
        triangular faces, as in a column layer grid with triangular
        columns.
    :cvar HEXAHEDRAL: All grid cells are constrained to have 8
        nodes/cell with 6 faces/cell, 4 nodes/face, 8 nodes/cell for all
        cells (degeneracy allowed). Equivalent to IJK grid cells.
    :cvar POLYHEDRAL: If the cell geometry is not of a more specific
        kind, use polyhedral.
    """

    TETRAHEDRAL = "tetrahedral"
    PYRAMIDAL = "pyramidal"
    PRISM = "prism"
    HEXAHEDRAL = "hexahedral"
    POLYHEDRAL = "polyhedral"


@dataclass
class ChronostratigraphicRank:
    """The chronostratigraphic ranking of "well known" stratigraphic unit features
    in the global chronostratigraphic column.

    The ranks are organized from container to contained, e.g., (eon=1), (era=2), (period=3)
    The units are ranked by using age as ordering criteria, from oldest to youngest.
    These stratigraphic units have no associated interpretations or representations.
    BUSINESS RULE: The name must reference a well-known stratigraphic unit feature (such as "Jurassic"), for example, from the International Commission on Stratigraphy (http://www.stratigraphy.org).

    :ivar name: Name of the chrono rank such as "epoch, era, ..."
    :ivar contains:
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    contains: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Contains",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


class ColumnShape(Enum):
    """Used to indicate that all columns are of a uniform topology, i.e., have the
    same number of faces per column.

    This information is supplied by the RESQML writer to indicate the complexity of the grid geometry, as an aide to the RESQML reader.
    If a specific column shape is not appropriate, then use polygonal.
    BUSINESS RULE: Should be consistent with the actual geometry of the grid.

    :cvar TRIANGULAR: All grid columns have 3 sides.
    :cvar QUADRILATERAL: All grid columns have 4 sides. Includes tartan
        and corner point grids.
    :cvar POLYGONAL: At least one grid column is a polygon, N&gt;4.
    """

    TRIANGULAR = "triangular"
    QUADRILATERAL = "quadrilateral"
    POLYGONAL = "polygonal"


class ContactMode(Enum):
    BASELAP = "baselap"
    EROSION = "erosion"
    EXTENDED = "extended"
    PROPORTIONAL = "proportional"


class ContactRelationship(Enum):
    """
    The enumerations that specify the role of the contacts in a contact
    interpretation as described in the attributes below.

    :cvar FRONTIER_FEATURE_TO_FRONTIER_FEATURE: A contact between two
        frontier features to close a volume of interest.
    :cvar GENETIC_BOUNDARY_TO_FRONTIER_FEATURE: A linear contact between
        a genetic boundary interpretation and a frontier feature
        (horizon/frontier contact).
    :cvar GENETIC_BOUNDARY_TO_GENETIC_BOUNDARY: A linear contact between
        two genetic boundary interpretations (horizon/horizon contact).
    :cvar GENETIC_BOUNDARY_TO_TECTONIC_BOUNDARY: A linear contact
        between a genetic boundary interpretation and a tectonic
        boundary interpretation (horizon/fault contact).
    :cvar STRATIGRAPHIC_UNIT_TO_FRONTIER_FEATURE: A surface contact
        between a stratigraphic unit interpretation and a frontier
        feature (contact closing a volume on a frontier feature that is
        a technical feature).
    :cvar STRATIGRAPHIC_UNIT_TO_STRATIGRAPHIC_UNIT: A surface contact
        between two stratigraphic unit interpretations (unit/unit
        contact).
    :cvar TECTONIC_BOUNDARY_TO_FRONTIER_FEATURE: A linear contact
        between a tectonic boundary interpretation and a frontier
        feature (fault/frontier contact).
    :cvar TECTONIC_BOUNDARY_TO_GENETIC_BOUNDARY: A linear contact
        between a tectonic boundary interpretation and a genetic
        boundary interpretation (fault/horizon contact).
    :cvar TECTONIC_BOUNDARY_TO_TECTONIC_BOUNDARY: A linear contact
        between two tectonic boundary interpretations (fault/fault
        contact).
    """

    FRONTIER_FEATURE_TO_FRONTIER_FEATURE = (
        "frontier feature to frontier feature"
    )
    GENETIC_BOUNDARY_TO_FRONTIER_FEATURE = (
        "genetic boundary to frontier feature"
    )
    GENETIC_BOUNDARY_TO_GENETIC_BOUNDARY = (
        "genetic boundary to genetic boundary"
    )
    GENETIC_BOUNDARY_TO_TECTONIC_BOUNDARY = (
        "genetic boundary to tectonic boundary"
    )
    STRATIGRAPHIC_UNIT_TO_FRONTIER_FEATURE = (
        "stratigraphic unit to frontier feature"
    )
    STRATIGRAPHIC_UNIT_TO_STRATIGRAPHIC_UNIT = (
        "stratigraphic unit to stratigraphic unit"
    )
    TECTONIC_BOUNDARY_TO_FRONTIER_FEATURE = (
        "tectonic boundary to frontier feature"
    )
    TECTONIC_BOUNDARY_TO_GENETIC_BOUNDARY = (
        "tectonic boundary to genetic boundary"
    )
    TECTONIC_BOUNDARY_TO_TECTONIC_BOUNDARY = (
        "tectonic boundary to tectonic boundary"
    )


class ContactSide(Enum):
    """Enumeration that specifies the location of the contacts, chosen from the
    attributes listed below.

    For example, if you specify contact between a horizon and a fault, you can specify if the contact is on the foot wall side or the hanging wall side of the fault, and if the fault is splitting both sides of a horizon or the older side only.
    From Wikipedia: http://en.wikipedia.org/wiki/Foot_wall
    CC-BY-SA-3.0-MIGRATED; GFDL-WITH-DISCLAIMERS
    Released under the GNU Free Documentation License.

    :cvar FOOTWALL: The footwall side of the fault. See picture.
    :cvar HANGING_WALL: The hanging wall side of the fault. See picture.
    :cvar NORTH: For a vertical fault, specification of the north side.
    :cvar SOUTH: For a vertical fault, specification of the south side.
    :cvar EAST: For a vertical fault, specification of the east side.
    :cvar WEST: For a vertical fault, specification of the west side.
    :cvar YOUNGER: Indicates that a fault splits a genetic boundary on
        its younger side.
    :cvar OLDER: Indicates that a fault splits a genetic boundary on its
        older side.
    :cvar BOTH: Indicates that a fault splits both sides of a genetic
        feature.
    """

    FOOTWALL = "footwall"
    HANGING_WALL = "hanging wall"
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    YOUNGER = "younger"
    OLDER = "older"
    BOTH = "both"


class ContactVerb(Enum):
    """
    Enumerations for the verbs that can be used to define the impact on the
    construction of the model of the geological event that created the binary
    contact.

    :cvar SPLITS: Specifies that the fault has opened a pair of fault
        lips in a horizon.
    :cvar INTERRUPTS: Operation on which an "unconformable" genetic
        boundary interpretation interrupts another genetic boundary
        interpretation or a stratigraphic unit interpretation.
    :cvar CONTAINS: Precise use of this attribute to be determined
        during testing.
    :cvar CONFORMS: Defines surface contact between two stratigraphic
        units.
    :cvar ERODES: Defines surface contact between two stratigraphic
        units.
    :cvar STOPS_AT: Defines if a tectonic boundary interpretation stops
        at another tectonic boundary interpretation. Also used for
        genetic unit to frontier feature, fault to frontier feature, and
        sedimentary unit to frontier feature.
    :cvar CROSSES: Defines if a tectonic boundary interpretation crosses
        another tectonic boundary interpretation.
    :cvar INCLUDES: Precise use of this attribute will be determined
        during testing.
    """

    SPLITS = "splits"
    INTERRUPTS = "interrupts"
    CONTAINS = "contains"
    CONFORMS = "conforms"
    ERODES = "erodes"
    STOPS_AT = "stops at"
    CROSSES = "crosses"
    INCLUDES = "includes"


class DepositionMode(Enum):
    """
    The enumerated attributes of a horizon.
    """

    PROPORTIONAL_BETWEEN_TOP_AND_BOTTOM = "proportional between top and bottom"
    PARALLEL_TO_BOTTOM = "parallel to bottom"
    PARALLEL_TO_TOP = "parallel to top"
    PARALLEL_TO_ANOTHER_BOUNDARY = "parallel to another boundary"


class Domain(Enum):
    """
    Enumeration for the feature interpretation to specify if the measurement is in
    the seismic time or depth domain or if it is derived from a laboratory
    measurement.

    :cvar DEPTH: Position defined by measurements in the depth domain.
    :cvar TIME: Position based on geophysical measurements in two-way
        time (TWT).
    :cvar MIXED:
    """

    DEPTH = "depth"
    TIME = "time"
    MIXED = "mixed"


@dataclass
class DoubleLookup:
    """
    (key,value) pairs for a lookup table.

    :ivar key: Input to a table lookup.
    :ivar value: Output from a table lookup.
    """

    key: Optional[float] = field(
        default=None,
        metadata={
            "name": "Key",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    value: Optional[float] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


class Facet(Enum):
    """Enumerations of the type of qualifier that applies to a property type to
    provide additional context about the nature of the property.

    For example, may include conditions, direction, qualifiers, or
    statistics. Facets are used in RESQML to provide qualifiers to
    existing property types, which minimizes the need to create
    specialized property types.

    :cvar CONDITIONS: Indicates condition of how the property was
        acquired, e.g., distinguishing surface condition of a fluid
        compared to reservoir conditions.
    :cvar DIRECTION: Indicates that the property is directional. Common
        values are X, Y, or Z for vectors; I, J, or K for properties on
        a grid; or tensorial coordinates, e.g., XX or IJ. For example,
        vertical permeability vs. horizontal permeability.
    :cvar NETGROSS: Indicates that the property is of kind net or gross,
        i.e., indicates that the spatial support of a property is
        averaged only over the net rock or all of the rock. rock or all
        of the rock.
    :cvar QUALIFIER: Used to capture any other context not covered by
        the other facet types listed here.
    :cvar STATISTICS: Indicates values such as minimum, maximum,
        average, etc.
    :cvar WHAT: Indicates the element that is measured, for example, the
        concentration of a mineral.
    """

    CONDITIONS = "conditions"
    DIRECTION = "direction"
    NETGROSS = "netgross"
    QUALIFIER = "qualifier"
    STATISTICS = "statistics"
    WHAT = "what"


class FluidContact(Enum):
    """Enumerated values used to indicate a specific type of fluid boundary
    feature.

    See attributes below.

    :cvar FREE_WATER_CONTACT: A surface defined by vanishing capillary
        pressure between the water and hydrocarbon phases.
    :cvar GAS_OIL_CONTACT: A surface defined by vanishing capillary
        pressure between the gas and oil hydrocarbon phases.
    :cvar GAS_WATER_CONTACT: A surface defined by vanishing capillary
        pressure between the water and gas hydrocarbon phases.
    :cvar SEAL: Identifies a break in the hydrostatic column.
    :cvar WATER_OIL_CONTACT: A surface defined by vanishing capillary
        pressure between the water and oil hydrocarbon phases.
    """

    FREE_WATER_CONTACT = "free water contact"
    GAS_OIL_CONTACT = "gas oil contact"
    GAS_WATER_CONTACT = "gas water contact"
    SEAL = "seal"
    WATER_OIL_CONTACT = "water oil contact"


class FluidMarker(Enum):
    """
    The various fluid a well marker can indicate.
    """

    GAS_DOWN_TO = "gas down to"
    GAS_UP_TO = "gas up to"
    OIL_DOWN_TO = "oil down to"
    OIL_UP_TO = "oil up to"
    WATER_DOWN_TO = "water down to"
    WATER_UP_TO = "water up to"


class GeneticBoundaryKind(Enum):
    """Enumerations used to indicate a specific type of genetic boundary feature.

    See attributes below. Note that a genetic boundary has a younger
    side and an older side.

    :cvar GEOBODY_BOUNDARY: An interface between a geobody and other
        geologic objects.
    :cvar HORIZON: An interface associated with a stratigraphic unit,
        which could be the top or bottom of the unit.
    """

    GEOBODY_BOUNDARY = "geobody boundary"
    HORIZON = "horizon"


class Geobody3DShape(Enum):
    """
    The enumerated attributes of a horizon.
    """

    DYKE = "dyke"
    SILT = "silt"
    DOME = "dome"
    SHEETH = "sheeth"
    DIAPIR = "diapir"
    BATHOLITH = "batholith"
    CHANNEL = "channel"
    DELTA = "delta"
    DUNE = "dune"
    FAN = "fan"
    REEF = "reef"
    WEDGE = "wedge"


class GeologicBoundaryKind(Enum):
    """
    The various geologic boundary a well marker can indicate.
    """

    FAULT = "fault"
    GEOBODY = "geobody"
    HORIZON = "horizon"


class GeologicUnitComposition(Enum):
    INTRUSIVE_CLAY = "intrusive clay "
    ORGANIC = "organic"
    INTRUSIVE_MUD = "intrusive mud "
    EVAPORITE_SALT = "evaporite salt"
    EVAPORITE_NON_SALT = "evaporite non salt"
    SEDIMENTARY_SILICLASTIC = "sedimentary siliclastic"
    CARBONATE = "carbonate"
    MAGMATIC_INTRUSIVE_GRANITOID = "magmatic intrusive granitoid"
    MAGMATIC_INTRUSIVE_PYROCLASTIC = "magmatic intrusive pyroclastic"
    MAGMATIC_EXTRUSIVE_LAVA_FLOW = "magmatic extrusive lava flow"
    OTHER_CHEMICHAL_ROCK = "other chemichal rock"
    SEDIMENTARY_TURBIDITE = "sedimentary turbidite"


@dataclass
class GeologicUnitInterpretationIndex:
    """Element that lets you index and order rock feature interpretations.

    For possible ordering criteria, see OrderingCriteria.

    :ivar index: An index value associated to an instance of this type
        interpretation, given a specific ordering criteria.
    :ivar unit:
    """

    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


class GeologicUnitMaterialImplacement(Enum):
    """
    The enumerated attributes of a horizon.
    """

    AUTOCHTONOUS = "autochtonous"
    ALLOCHTONOUS = "allochtonous"


class GridGeometryAttachment(Enum):
    """
    Indexable grid elements to which point geometry may be attached to describe
    additional grid geometry.

    :cvar CELLS: Geometry may be attached to cells to distort the
        geometry of that specific cell, only (finite element grid).
    :cvar EDGES: Geometry may be attached to edges to distort the
        geometry of all cells that refer to that edge (finite element
        grid). BUSINESS RULE: The edges indexing must be known or
        defined in the grid representation if geometry is attached to
        the edges.
    :cvar FACES: Geometry may be attached to faces to distort the
        geometry of all cells that refer to that face (finite element
        grid). BUSINESS RULE: The faces indexing must be known or
        defined in the grid representation if geometry is attached to
        the faces.
    :cvar HINGE_NODE_FACES: For column layer grids, these are the K
        faces. For unstructured grids these faces are enumerated as the
        hinge node faces.
    :cvar NODES: Additional grid geometry may be attached to split or
        truncated node patches for column layer grids. All other node
        geometry attachment should be done through the Points array of
        the AbstractGridGeometry, not through the additional grid
        geometry.
    :cvar RADIAL_ORIGIN_POLYLINE: NKL points must be attached to the
        radial origin polyline for a grid with radial interpolation.
        BUSINESS RULE: The optional radialGridIsComplete element must be
        defined in the grid representation if geometry is attached to
        the radial origin polyline.
    :cvar SUBNODES: Geometry may be attached to subnodes to distort the
        geometry of all cells that refer to that subnode (finite element
        grid). BUSINESS RULE: An optional subnode patch object must be
        defined in the grid representation if geometry is attached to
        the subnodes.
    """

    CELLS = "cells"
    EDGES = "edges"
    FACES = "faces"
    HINGE_NODE_FACES = "hinge node faces"
    NODES = "nodes"
    RADIAL_ORIGIN_POLYLINE = "radial origin polyline"
    SUBNODES = "subnodes"


@dataclass
class HorizonInterpretationIndex:
    """Element that lets you index and order horizon interpretations.

    For possible ordering criteria, see OrderingCriteria.

    :ivar index: An index value associated to an instance of this type
        of interpretation, given a specific ordering criteria
    :ivar stratigraphic_rank: Number of the stratigraphic rank on which
        the previous indices have been defined.
    :ivar horizon:
    """

    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    stratigraphic_rank: Optional[int] = field(
        default=None,
        metadata={
            "name": "StratigraphicRank",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    horizon: Optional[str] = field(
        default=None,
        metadata={
            "name": "Horizon",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


class IdentityKind(Enum):
    """
    Enumeration of the identity kinds for the element identities (ElementIdentity).

    :cvar COLOCATION: A set of (sub)representations is collocated if
        there is bijection between the simple elements of all of the
        participating (sub)representations. This definition implies
        there is the same number of simple elements. NOTE: The geometric
        location of each set of simple elements mapped through the
        bijection is intended to be identical even if the numeric values
        of the associated geometries differ, i.e., due to loss of
        spatial resolution.
    :cvar PREVIOUS_COLOCATION: The participating (sub)representations
        were collocated at some time in the geologic past—but not
        necessarily in the present day earth model.
    :cvar EQUIVALENCE: A set of (sub)representations is equivalent if
        there is a map giving an association between some of the simple
        topological elements of the participating (sub)representations.
    :cvar PREVIOUS_EQUIVALENCE: The participating (sub)representations
        were equivalent at some time in the geologic past—but not
        necessarily in the present day earth model.
    """

    COLOCATION = "colocation"
    PREVIOUS_COLOCATION = "previous colocation"
    EQUIVALENCE = "equivalence"
    PREVIOUS_EQUIVALENCE = "previous equivalence"


class IndexableElements(Enum):
    """Indexable elements for the different representations. The indexing of each
    element depends upon the specific representation. To order and reference the
    elements of a representation, RESQML makes extensive use of the concept of
    indexing. Both one-dimensional and multi-dimensional arrays of elements are
    used. So that all elements may be referenced in a consistent and uniform
    fashion, each multi-dimensional index must have a well-defined 1D index.
    Attributes below identify the IndexableElements, though not all elements apply
    to all types of representations.

    Indexable elements are used to:
    - attach geometry and properties to a representation.
    - identify portions of a representation when expressing a representation identity.
    - construct a sub-representation from an existing representation.
    See the RESQML Overview Guide for the table of indexable elements and the representations to which they apply.

    :cvar CELLS:
    :cvar COLUMN_EDGES:
    :cvar COLUMNS:
    :cvar CONTACTS:
    :cvar COORDINATE_LINES:
    :cvar EDGES:
    :cvar EDGES_PER_COLUMN:
    :cvar ENUMERATED_ELEMENTS:
    :cvar FACES:
    :cvar FACES_PER_CELL:
    :cvar INTERVAL_EDGES: Count = NKL (Column Layer Grids, only)
    :cvar INTERVALS:
    :cvar I0: Count = NI (IJK Grids, only)
    :cvar I0_EDGES: Count = NIL (IJK Grids, only)
    :cvar J0: Count = NJ (IJK Grids, only)
    :cvar J0_EDGES: Count = NJL (IJK Grids, only)
    :cvar LAYERS: Count = NK  (Column Layer Grids, only)
    :cvar NODES:
    :cvar NODES_PER_CELL:
    :cvar NODES_PER_EDGE:
    :cvar NODES_PER_FACE:
    :cvar PATCHES:
    :cvar PILLARS:
    :cvar REGIONS:
    :cvar REPRESENTATION:
    :cvar SUBNODES:
    :cvar TRIANGLES:
    """

    CELLS = "cells"
    COLUMN_EDGES = "column edges"
    COLUMNS = "columns"
    CONTACTS = "contacts"
    COORDINATE_LINES = "coordinate lines"
    EDGES = "edges"
    EDGES_PER_COLUMN = "edges per column"
    ENUMERATED_ELEMENTS = "enumerated elements"
    FACES = "faces"
    FACES_PER_CELL = "faces per cell"
    INTERVAL_EDGES = "interval edges"
    INTERVALS = "intervals"
    I0 = "I0"
    I0_EDGES = "I0 edges"
    J0 = "J0"
    J0_EDGES = "J0 edges"
    LAYERS = "layers"
    NODES = "nodes"
    NODES_PER_CELL = "nodes per cell"
    NODES_PER_EDGE = "nodes per edge"
    NODES_PER_FACE = "nodes per face"
    PATCHES = "patches"
    PILLARS = "pillars"
    REGIONS = "regions"
    REPRESENTATION = "representation"
    SUBNODES = "subnodes"
    TRIANGLES = "triangles"


class Kdirection(Enum):
    """Enumeration used to specify if the direction of the coordinate lines is
    uniquely defined for a grid.

    If not uniquely defined, e.g., for over-turned reservoirs, then
    indicate that the K direction is not monotonic.

    :cvar DOWN: K is increasing with depth, dot(tangent,gradDepth)&gt;0.
    :cvar UP: K is increasing with elevation,
        dot(tangent,gradDepth)&lt;0.
    :cvar NOT_MONOTONIC: K is not monotonic with elevation, e.g., for
        over-turned structures.
    """

    DOWN = "down"
    UP = "up"
    NOT_MONOTONIC = "not monotonic"


class LineRole(Enum):
    """
    Indicates the various roles that a polyline topology can have in a
    representation.

    :cvar FAULT_CENTER_LINE: Usually used to represent fault lineaments
        on horizons. These lines can represent nonsealed contact
        interpretation parts defined by a horizon/fault intersection.
    :cvar PICK: Used to represent all types of nonsealed contact
        interpretation parts defined by a horizon/fault intersection.
    :cvar INNER_RING: Closed polyline that delineates a hole in a
        surface patch.
    :cvar OUTER_RING: Closed polyline that delineates the extension of a
        surface patch.
    :cvar TRAJECTORY: Polyline that is used to represent a well
        trajectory representation.
    :cvar INTERPRETATION_LINE: Line corresponding to a digitalization
        along an earth model section.
    :cvar CONTACT: Used to represent nonsealed contact interpretation
        parts defined by a horizon/fault intersection.
    :cvar DEPOSITIONAL_LINE: Used to represent nonsealed contact
        interpretation parts defined by a horizon/horizon intersection.
    :cvar EROSION_LINE: Used to represent nonsealed contact
        interpretation parts defined by a horizon/horizon intersection.
    :cvar CONTOURING: Used to obtain sets of 3D x, y, z points to
        represent any boundary interpretation.
    :cvar PILLAR:
    """

    FAULT_CENTER_LINE = "fault center line"
    PICK = "pick"
    INNER_RING = "inner ring"
    OUTER_RING = "outer ring"
    TRAJECTORY = "trajectory"
    INTERPRETATION_LINE = "interpretation line"
    CONTACT = "contact"
    DEPOSITIONAL_LINE = "depositional line"
    EROSION_LINE = "erosion line"
    CONTOURING = "contouring"
    PILLAR = "pillar"


class MdDomain(Enum):
    """
    Different types of measured depths.

    :cvar DRILLER: The original depths recorded while drilling a well or
        LWD or MWD.
    :cvar LOGGER: Depths recorded when logging a well, which are in
        general considered to be more accurate than driller's depth.
    """

    DRILLER = "driller"
    LOGGER = "logger"


class MdReference(Enum):
    """Reference location for the measured depth datum (MdDatum).

    The type of local or permanent reference datum for vertical gravity
    based (i.e., elevation and vertical depth) and measured depth
    coordinates within the context of a well. This list includes local
    points (e.g., kelly bushing) used as a datum and vertical reference
    datums (e.g., mean sea level).

    :cvar GROUND_LEVEL:
    :cvar KELLY_BUSHING:
    :cvar MEAN_SEA_LEVEL: A tidal datum. The arithmetic mean of hourly
        heights observed over the National Tidal Datum Epoch (19 years).
    :cvar DERRICK_FLOOR:
    :cvar CASING_FLANGE: A flange affixed to the top of the casing
        string used to attach production equipment.
    :cvar ARBITRARY_POINT: This value should not be used for drilled
        wells. All reasonable attempts should be made to determine the
        appropriate value.
    :cvar CROWN_VALVE:
    :cvar ROTARY_BUSHING:
    :cvar ROTARY_TABLE:
    :cvar SEA_FLOOR:
    :cvar LOWEST_ASTRONOMICAL_TIDE: The lowest tide level over the
        duration of the National Tidal Datum Epoch (19 years).
    :cvar MEAN_HIGHER_HIGH_WATER: A tidal datum. The average of the
        higher high water height of each tidal day observed over the
        National Tidal Datum Epoch (19 years).
    :cvar MEAN_HIGH_WATER: A tidal datum. The average of all the high
        water heights observed over the National Tidal Datum Epoch (19
        years).
    :cvar MEAN_LOWER_LOW_WATER: A tidal datum. The average of the lower
        low water height of each tidal day observed over the National
        Tidal Datum Epoch (19 years ).
    :cvar MEAN_LOW_WATER: A tidal datum. The average of all the low
        water heights observed over the National Tidal Datum Epoch (19
        years).
    :cvar MEAN_TIDE_LEVEL: A tidal datum. The arithmetic mean of mean
        high water and mean low water. Same as half-tide level.
    :cvar KICKOFF_POINT: This value is not expected to be used in most
        typical situations. All reasonable attempts should be made to
        determine the appropriate value.
    """

    GROUND_LEVEL = "ground level"
    KELLY_BUSHING = "kelly bushing"
    MEAN_SEA_LEVEL = "mean sea level"
    DERRICK_FLOOR = "derrick floor"
    CASING_FLANGE = "casing flange"
    ARBITRARY_POINT = "arbitrary point"
    CROWN_VALVE = "crown valve"
    ROTARY_BUSHING = "rotary bushing"
    ROTARY_TABLE = "rotary table"
    SEA_FLOOR = "sea floor"
    LOWEST_ASTRONOMICAL_TIDE = "lowest astronomical tide"
    MEAN_HIGHER_HIGH_WATER = "mean higher high water"
    MEAN_HIGH_WATER = "mean high water"
    MEAN_LOWER_LOW_WATER = "mean lower low water"
    MEAN_LOW_WATER = "mean low water"
    MEAN_TIDE_LEVEL = "mean tide level"
    KICKOFF_POINT = "kickoff point"


@dataclass
class NameValuePair:
    """
    Complementary optional metadata information, which may be added to any data-
    object to qualify it.

    :ivar name: Name of the metadata information.
    :ivar value: Value of the metadata information.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


class OrderingCriteria(Enum):
    """
    Enumeration used to specify the order of an abstract stratigraphic organization
    or a structural organization interpretation.

    :cvar AGE: From youngest to oldest period (increasing age).
    :cvar APPARENT_DEPTH: From surface to subsurface.
    :cvar MEASURED_DEPTH: From well head to wellbore bottom/total depth
        (TD).
    """

    AGE = "age"
    APPARENT_DEPTH = "apparent depth"
    MEASURED_DEPTH = "measured depth"


class OrganizationKind(Enum):
    """Enumerations used to indicate a specific type of organization.

    See attributes below.

    :cvar EARTH_MODEL: An organization composed of the other types of
        organizations listed here.
    :cvar FLUID: A volume organization composed of fluid boundaries and
        phase units.
    :cvar STRATIGRAPHIC: A volume organization composed of geologic
        features, such as geobodies, stratigraphic units, and
        boundaries.
    :cvar STRUCTURAL: A surface organization composed of geologic
        features, such as faults, horizons, and frontier boundaries.
    """

    EARTH_MODEL = "earth model"
    FLUID = "fluid"
    STRATIGRAPHIC = "stratigraphic"
    STRUCTURAL = "structural"


@dataclass
class OrientedMacroFace:
    """An element of a volume shell that is defined by a set of oriented faces
    belonging to boundable patches.

    A macroface may describe a contact between:
    - two structural, stratigraphic, or fluid units
    - one boundary feature (fault or frontier) and a unit.
    A face is a bounded open subset of a plane or a curved surface in 3D, delimited by an outer contour and zero, one, or more inner contours describing holes.

    :ivar patch_index_of_representation: Create the triangulation and 2D
        grid representation for which the patches match the macro faces.
    :ivar representation_index: Identifies the representation by its
        index, in the list of representations contained in the
        organization.
    :ivar side_is_plus:
    """

    patch_index_of_representation: Optional[int] = field(
        default=None,
        metadata={
            "name": "PatchIndexOfRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    representation_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "RepresentationIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    side_is_plus: Optional[bool] = field(
        default=None,
        metadata={
            "name": "SideIsPlus",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


class ParameterKind(Enum):
    DATA_OBJECT = "dataObject"
    FLOATING_POINT = "floatingPoint"
    INTEGER = "integer"
    STRING = "string"
    TIMESTAMP = "timestamp"
    SUB_ACTIVITY = "subActivity"


@dataclass
class Patch:
    """Set or range of one kind of topological element used to define part of a
    data-object; this concept exists for grid and structural data-objects.

    Subset of a specified kind of indexable element of a representation,
    associated with a patch index. The patch index is used to define the
    relative order for the elements. It may also be used to access
    patches of indexable elements directly for geometry, properties, or
    relationships. Patches are used to remove any ambiguity in data
    ordering among the indexable elements. For example, the triangle
    indexing of a triangulated set representation consists of multiple
    triangles, each with a patch index. This index specifies the
    relative ordering of the triangle patches. Those data-objects that
    inherit a patch index from the abstract class of patches all include
    the word "Patch" as part of their name, e.g., TrianglePatch.

    :ivar patch_index: Local index of the patch, making it unique within
        the representation.
    """

    patch_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "PatchIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class PatchBoundaries:
    """Defines the boundaries of an indexed patch.

    These boundaries are outer and inner rings.

    :ivar inner_ring: A hole inside a representation patch. Inside the
        ring, the representation patch is not defined, outside it is. In
        case of contact, inner ring polyline representations should be
        typed as an erosion line, deposition line, or contact. BUSINESS
        RULE: Must be a polyline reference to a polyline representation,
        either a single polyline representation or a subrepresentation.
        Must be closed.
    :ivar outer_ring: The extension of a representation patch. Inside
        the ring, the representation patch is defined, outside it is
        not. BUSINESS RULE: Must be a reference to a polyline, either a
        single polyline representation or a subrepresentation. Must be
        closed.
    :ivar referenced_patch: UUID of the referenced topological patch.
    """

    inner_ring: List[str] = field(
        default_factory=list,
        metadata={
            "name": "InnerRing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    outer_ring: Optional[str] = field(
        default=None,
        metadata={
            "name": "OuterRing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    referenced_patch: Optional[int] = field(
        default=None,
        metadata={
            "name": "ReferencedPatch",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


class Phase(Enum):
    """The enumeration of the possible RockFluid Unit phase  in a hydrostatic
    column.

    The seal is considered here as a part ( the coverage phase) of an
    hydrostatic column.

    :cvar AQUIFER: Volume of the hydrostatic column for which only the
        aqueous phase is mobile. Typically below the Pc(hydrocarbon-
        water)=0 free fluid surface.
    :cvar GAS_CAP: Volume of the hydrostatic column for which only the
        gaseous phase is mobile. Typically above the Pc(gas-oil)=0 free
        fluid surface.
    :cvar OIL_COLUMN: Volume of the hydrostatic column for which only
        the oleic and aqueous phases may be mobile. Typically below the
        gas-oil Pc=0 free fluid surface.Pc(gas-oil)=0 free fluid
        surface.
    :cvar SEAL: Impermeable volume which provides the seal for a
        hydrostatic fluid column.
    """

    AQUIFER = "aquifer"
    GAS_CAP = "gas cap"
    OIL_COLUMN = "oil column"
    SEAL = "seal"


class PillarShape(Enum):
    """Used to indicate that all pillars are of a uniform kind, i.e., may be
    represented using the same number of nodes per pillar.

    This information is supplied by the RESQML writer to indicate the complexity of the grid geometry, as an aide to the RESQML reader.
    If a combination of vertical and straight, then use straight.
    If a specific pillar shape is not appropriate, then use curved.
    BUSINESS RULE: Should be consistent with the actual geometry of the grid.

    :cvar VERTICAL: If represented by a parametric line, requires only a
        single control point per line.
    :cvar STRAIGHT: If represented by a parametric line, requires 2
        control points per line.
    :cvar CURVED: If represented by a parametric line, requires 3 or
        more control points per line.
    """

    VERTICAL = "vertical"
    STRAIGHT = "straight"
    CURVED = "curved"


@dataclass
class Point3D:
    """
    Defines a point using coordinates in 3D space.

    :ivar coordinate1: X Coordinate
    :ivar coordinate2: Y Coordinate
    :ivar coordinate3: Either Z or T Coordinate
    """

    class Meta:
        name = "Point3d"

    coordinate1: Optional[float] = field(
        default=None,
        metadata={
            "name": "Coordinate1",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    coordinate2: Optional[float] = field(
        default=None,
        metadata={
            "name": "Coordinate2",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    coordinate3: Optional[float] = field(
        default=None,
        metadata={
            "name": "Coordinate3",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


class ResqmlPropertyKind(Enum):
    """
    Enumeration of the standard set of RESQML property kinds.

    :cvar ABSORBED_DOSE: The amount of energy absorbed per mass.
    :cvar ACCELERATION_LINEAR:
    :cvar ACTIVITY_OF_RADIOACTIVITY: A measure of the radiation being
        emitted.
    :cvar AMOUNT_OF_SUBSTANCE: Molar amount of a substance.
    :cvar AMPLITUDE: Amplitude of the acoustic signal recorded. It is
        not a physical property, only a value.
    :cvar ANGLE_PER_LENGTH:
    :cvar ANGLE_PER_TIME: The angular velocity. The rate of change of an
        angle.
    :cvar ANGLE_PER_VOLUME:
    :cvar ANGULAR_ACCELERATION:
    :cvar AREA:
    :cvar AREA_PER_AREA: A dimensionless quantity where the basis of the
        ratio is area.
    :cvar AREA_PER_VOLUME:
    :cvar ATTENUATION: A logarithmic, fractional change of some measure,
        generally power or amplitude, over a standard range. This is
        generally used for frequency attenuation over an octave.
    :cvar ATTENUATION_PER_LENGTH:
    :cvar AZIMUTH: Angle between the North and the projection of the
        normal to the horizon surface estimated on a local area of the
        interface.
    :cvar BUBBLE_POINT_PRESSURE: The pressure at which the first gas
        bubble appears while decreasing pressure on a fluid sample.
    :cvar BULK_MODULUS: Bulk modulus, K
    :cvar CAPACITANCE:
    :cvar CATEGORICAL: The abstract supertype of all enumerated string
        properties.
    :cvar CELL_LENGTH: distance from cell face center to cell face
        center in the specified direction, DI, DJ, DK
    :cvar CHARGE_DENSITY:
    :cvar CHEMICAL_POTENTIAL:
    :cvar CODE: A discrete code.
    :cvar COMPRESSIBILITY:
    :cvar CONCENTRATION_OF_B: molar concentration of a substance.
    :cvar CONDUCTIVITY:
    :cvar CONTINUOUS: The abstract supertype of all floating point
        properties.
    :cvar CROSS_SECTION_ABSORPTION:
    :cvar CURRENT_DENSITY:
    :cvar DARCY_FLOW_COEFFICIENT:
    :cvar DATA_TRANSMISSION_SPEED: used primarily for computer
        transmission rates.
    :cvar DELTA_TEMPERATURE: Delta temperature refers to temperature
        differences. For non-zero offset temperature scales, Fahrenheit
        and Celsius, the conversion formulas are different than for
        absolute temperatures.
    :cvar DENSITY:
    :cvar DEPTH: The perpendicular measurement downward from a surface.
        Also, the direct linear measurement from the point of viewing
        usually from front to back.
    :cvar DIFFUSION_COEFFICIENT:
    :cvar DIGITAL_STORAGE:
    :cvar DIMENSIONLESS: A dimensionless quantity is the ratio of two
        dimensional quantities. The quantity types are not apparent from
        the basic dimensionless class, but may be apparent in variations
        - such as area per area, volume per volume, or mass per mass.
    :cvar DIP: In the azimuth direction, Angle between an horizon plane
        and an estimated plane on a local area of the interface.
    :cvar DISCRETE: The abstract supertype of all integer properties.
    :cvar DOSE_EQUIVALENT:
    :cvar DOSE_EQUIVALENT_RATE:
    :cvar DYNAMIC_VISCOSITY:
    :cvar ELECTRIC_CHARGE:
    :cvar ELECTRIC_CONDUCTANCE:
    :cvar ELECTRIC_CURRENT:
    :cvar ELECTRIC_DIPOLE_MOMENT:
    :cvar ELECTRIC_FIELD_STRENGTH:
    :cvar ELECTRIC_POLARIZATION:
    :cvar ELECTRIC_POTENTIAL:
    :cvar ELECTRICAL_RESISTIVITY:
    :cvar ELECTROCHEMICAL_EQUIVALENT: An electrochemical equivalent
        differs from molarity in that the valence (oxidation reduction
        potential) of the element is also considered.
    :cvar ELECTROMAGNETIC_MOMENT:
    :cvar ENERGY_LENGTH_PER_AREA:
    :cvar ENERGY_LENGTH_PER_TIME_AREA_TEMPERATURE:
    :cvar ENERGY_PER_AREA:
    :cvar ENERGY_PER_LENGTH:
    :cvar EQUIVALENT_PER_MASS:
    :cvar EQUIVALENT_PER_VOLUME:
    :cvar EXPOSURE_RADIOACTIVITY:
    :cvar FLUID_VOLUME: Volume of fluid
    :cvar FORCE:
    :cvar FORCE_AREA:
    :cvar FORCE_LENGTH_PER_LENGTH:
    :cvar FORCE_PER_FORCE: A dimensionless quantity where the basis of
        the ratio is force.
    :cvar FORCE_PER_LENGTH:
    :cvar FORCE_PER_VOLUME:
    :cvar FORMATION_VOLUME_FACTOR: Ratio of volumes at subsurface and
        surface conditions
    :cvar FREQUENCY:
    :cvar FREQUENCY_INTERVAL: An octave is a doubling of a frquency.
    :cvar GAMMA_RAY_API_UNIT: This class is defined by the API, and is
        used for units of gamma ray log response.
    :cvar HEAT_CAPACITY:
    :cvar HEAT_FLOW_RATE:
    :cvar HEAT_TRANSFER_COEFFICIENT: PRESSURE PER VELOCITY PER AREA
    :cvar ILLUMINANCE:
    :cvar INDEX: Serial ordering
    :cvar IRRADIANCE:
    :cvar ISOTHERMAL_COMPRESSIBILITY:
    :cvar KINEMATIC_VISCOSITY:
    :cvar LAMBDA_RHO: Product of Lame constant and density, LR
    :cvar LAME_CONSTANT: Lame constant, Lambda
    :cvar LENGTH:
    :cvar LENGTH_PER_LENGTH: A dimensionless quantity where the basis of
        the ratio is length.
    :cvar LENGTH_PER_TEMPERATURE:
    :cvar LENGTH_PER_VOLUME:
    :cvar LEVEL_OF_POWER_INTENSITY:
    :cvar LIGHT_EXPOSURE:
    :cvar LINEAR_THERMAL_EXPANSION:
    :cvar LUMINANCE:
    :cvar LUMINOUS_EFFICACY:
    :cvar LUMINOUS_FLUX:
    :cvar LUMINOUS_INTENSITY:
    :cvar MAGNETIC_DIPOLE_MOMENT:
    :cvar MAGNETIC_FIELD_STRENGTH:
    :cvar MAGNETIC_FLUX:
    :cvar MAGNETIC_INDUCTION:
    :cvar MAGNETIC_PERMEABILITY:
    :cvar MAGNETIC_VECTOR_POTENTIAL:
    :cvar MASS: M/L2T
    :cvar MASS_ATTENUATION_COEFFICIENT:
    :cvar MASS_CONCENTRATION: A dimensionless quantity where the basis
        of the ratio is mass.
    :cvar MASS_FLOW_RATE:
    :cvar MASS_LENGTH:
    :cvar MASS_PER_ENERGY:
    :cvar MASS_PER_LENGTH: M /L4T
    :cvar MASS_PER_TIME_PER_AREA:
    :cvar MASS_PER_TIME_PER_LENGTH:
    :cvar MASS_PER_VOLUME_PER_LENGTH:
    :cvar MOBILITY:
    :cvar MODULUS_OF_COMPRESSION:
    :cvar MOLAR_CONCENTRATION: molar concentration of a substance.
    :cvar MOLAR_HEAT_CAPACITY:
    :cvar MOLAR_VOLUME:
    :cvar MOLE_PER_AREA:
    :cvar MOLE_PER_TIME:
    :cvar MOLE_PER_TIME_PER_AREA:
    :cvar MOMENT_OF_FORCE:
    :cvar MOMENT_OF_INERTIA:
    :cvar MOMENT_OF_SECTION:
    :cvar MOMENTUM:
    :cvar MU_RHO: Product of Shear modulus and density, MR
    :cvar NET_TO_GROSS_RATIO: Ratio of net rock volume to gross rock
        volume, NTG
    :cvar NEUTRON_API_UNIT:
    :cvar NON_DARCY_FLOW_COEFFICIENT:
    :cvar OPERATIONS_PER_TIME:
    :cvar PARACHOR:
    :cvar PER_AREA:
    :cvar PER_ELECTRIC_POTENTIAL:
    :cvar PER_FORCE:
    :cvar PER_LENGTH:
    :cvar PER_MASS:
    :cvar PER_VOLUME:
    :cvar PERMEABILITY_LENGTH:
    :cvar PERMEABILITY_ROCK:
    :cvar PERMEABILITY_THICKNESS: Product of permeability and thickness
    :cvar PERMEANCE:
    :cvar PERMITTIVITY:
    :cvar P_H: The pH is a class that measures the hydrogen ion
        concentration (acidity).
    :cvar PLANE_ANGLE:
    :cvar POISSON_RATIO: Poisson's ratio, Sigma
    :cvar PORE_VOLUME: Volume of the Pore Space of the Rock
    :cvar POROSITY: porosity
    :cvar POTENTIAL_DIFFERENCE_PER_POWER_DROP:
    :cvar POWER:
    :cvar POWER_PER_VOLUME:
    :cvar PRESSURE:
    :cvar PRESSURE_PER_TIME:
    :cvar PRESSURE_SQUARED:
    :cvar PRESSURE_SQUARED_PER_FORCE_TIME_PER_AREA:
    :cvar PRESSURE_TIME_PER_VOLUME:
    :cvar PRODUCTIVITY_INDEX:
    :cvar PROPERTY_MULTIPLIER: Unitless multiplier to apply to any
        property
    :cvar QUANTITY: The abstract supertype of all floating point
        properties with a unit of measure.
    :cvar QUANTITY_OF_LIGHT:
    :cvar RADIANCE:
    :cvar RADIANT_INTENSITY:
    :cvar RELATIVE_PERMEABILITY: Ratio of phase permeability, which is a
        function of saturation, to the rock permeability
    :cvar RELATIVE_POWER: A dimensionless quantity where the basis of
        the ratio is power.
    :cvar RELATIVE_TIME: A dimensionless quantity where the basis of the
        ratio is time.
    :cvar RELUCTANCE:
    :cvar RESISTANCE:
    :cvar RESISTIVITY_PER_LENGTH:
    :cvar RESQML_ROOT_PROPERTY: The abstract supertype of all
        properties. This property does not have a parent.
    :cvar ROCK_IMPEDANCE: Acoustic impedence, Ip, Is
    :cvar ROCK_PERMEABILITY: See "permeability rock"
    :cvar ROCK_VOLUME: Rock Volume
    :cvar SATURATION: Ratio of phase fluid volume to pore volume
    :cvar SECOND_MOMENT_OF_AREA:
    :cvar SHEAR_MODULUS: Shear modulus, Mu
    :cvar SOLID_ANGLE:
    :cvar SOLUTION_GAS_OIL_RATIO: Ratio of solution gas volume to oil
        volume at reservoir conditions
    :cvar SPECIFIC_ACTIVITY_OF_RADIOACTIVITY:
    :cvar SPECIFIC_ENERGY:
    :cvar SPECIFIC_HEAT_CAPACITY:
    :cvar SPECIFIC_PRODUCTIVITY_INDEX:
    :cvar SPECIFIC_VOLUME:
    :cvar SURFACE_DENSITY:
    :cvar TEMPERATURE_PER_LENGTH:
    :cvar TEMPERATURE_PER_TIME:
    :cvar THERMAL_CONDUCTANCE:
    :cvar THERMAL_CONDUCTIVITY:
    :cvar THERMAL_DIFFUSIVITY:
    :cvar THERMAL_INSULANCE:
    :cvar THERMAL_RESISTANCE:
    :cvar THERMODYNAMIC_TEMPERATURE:
    :cvar THICKNESS: Distance measured in a volume between two surfaces
        ( e.G. Geological Top Boundary and Geological Bottom Boundary of
        a Geological unit).
    :cvar TIME:
    :cvar TIME_PER_LENGTH:
    :cvar TIME_PER_VOLUME:
    :cvar TRANSMISSIBILITY: Volumetric flux per unit area per unit
        pressure drop for unit viscosity fluid
    :cvar UNIT_PRODUCTIVITY_INDEX:
    :cvar UNITLESS: The abstract supertype of all floating point
        properties with NO unit of measure. In order to allow the unit
        information to be required for all continuous properties, the
        special unit of measure of "NONE" has been assigned to all
        children of this class. In addition, the special dimensional
        class of "0" has been assigned to all children of this class.
    :cvar VAPOR_OIL_GAS_RATIO: Ratio of oil vapor volume to gas volume
        at reservoir conditions
    :cvar VELOCITY:
    :cvar VOLUME:
    :cvar VOLUME_FLOW_RATE:
    :cvar VOLUME_LENGTH_PER_TIME:
    :cvar VOLUME_PER_AREA:
    :cvar VOLUME_PER_LENGTH:
    :cvar VOLUME_PER_TIME_PER_AREA:
    :cvar VOLUME_PER_TIME_PER_LENGTH:
    :cvar VOLUME_PER_TIME_PER_TIME:
    :cvar VOLUME_PER_TIME_PER_VOLUME:
    :cvar VOLUME_PER_VOLUME: A dimensionless quantity where the basis of
        the ratio is volume.
    :cvar VOLUMETRIC_HEAT_TRANSFER_COEFFICIENT:
    :cvar VOLUMETRIC_THERMAL_EXPANSION:
    :cvar WORK:
    :cvar YOUNG_MODULUS: Young's modulus, E
    """

    ABSORBED_DOSE = "absorbed dose"
    ACCELERATION_LINEAR = "acceleration linear"
    ACTIVITY_OF_RADIOACTIVITY = "activity (of radioactivity)"
    AMOUNT_OF_SUBSTANCE = "amount of substance"
    AMPLITUDE = "amplitude"
    ANGLE_PER_LENGTH = "angle per length"
    ANGLE_PER_TIME = "angle per time"
    ANGLE_PER_VOLUME = "angle per volume"
    ANGULAR_ACCELERATION = "angular acceleration"
    AREA = "area"
    AREA_PER_AREA = "area per area"
    AREA_PER_VOLUME = "area per volume"
    ATTENUATION = "attenuation"
    ATTENUATION_PER_LENGTH = "attenuation per length"
    AZIMUTH = "azimuth"
    BUBBLE_POINT_PRESSURE = "bubble point pressure"
    BULK_MODULUS = "bulk modulus"
    CAPACITANCE = "capacitance"
    CATEGORICAL = "categorical"
    CELL_LENGTH = "cell length"
    CHARGE_DENSITY = "charge density"
    CHEMICAL_POTENTIAL = "chemical potential"
    CODE = "code"
    COMPRESSIBILITY = "compressibility"
    CONCENTRATION_OF_B = "concentration of B"
    CONDUCTIVITY = "conductivity"
    CONTINUOUS = "continuous"
    CROSS_SECTION_ABSORPTION = "cross section absorption"
    CURRENT_DENSITY = "current density"
    DARCY_FLOW_COEFFICIENT = "Darcy flow coefficient"
    DATA_TRANSMISSION_SPEED = "data transmission speed"
    DELTA_TEMPERATURE = "delta temperature"
    DENSITY = "density"
    DEPTH = "depth"
    DIFFUSION_COEFFICIENT = "diffusion coefficient"
    DIGITAL_STORAGE = "digital storage"
    DIMENSIONLESS = "dimensionless"
    DIP = "dip"
    DISCRETE = "discrete"
    DOSE_EQUIVALENT = "dose equivalent"
    DOSE_EQUIVALENT_RATE = "dose equivalent rate"
    DYNAMIC_VISCOSITY = "dynamic viscosity"
    ELECTRIC_CHARGE = "electric charge"
    ELECTRIC_CONDUCTANCE = "electric conductance"
    ELECTRIC_CURRENT = "electric current"
    ELECTRIC_DIPOLE_MOMENT = "electric dipole moment"
    ELECTRIC_FIELD_STRENGTH = "electric field strength"
    ELECTRIC_POLARIZATION = "electric polarization"
    ELECTRIC_POTENTIAL = "electric potential"
    ELECTRICAL_RESISTIVITY = "electrical resistivity"
    ELECTROCHEMICAL_EQUIVALENT = "electrochemical equivalent"
    ELECTROMAGNETIC_MOMENT = "electromagnetic moment"
    ENERGY_LENGTH_PER_AREA = "energy length per area"
    ENERGY_LENGTH_PER_TIME_AREA_TEMPERATURE = (
        "energy length per time area temperature"
    )
    ENERGY_PER_AREA = "energy per area"
    ENERGY_PER_LENGTH = "energy per length"
    EQUIVALENT_PER_MASS = "equivalent per mass"
    EQUIVALENT_PER_VOLUME = "equivalent per volume"
    EXPOSURE_RADIOACTIVITY = "exposure (radioactivity)"
    FLUID_VOLUME = "fluid volume"
    FORCE = "force"
    FORCE_AREA = "force area"
    FORCE_LENGTH_PER_LENGTH = "force length per length"
    FORCE_PER_FORCE = "force per force"
    FORCE_PER_LENGTH = "force per length"
    FORCE_PER_VOLUME = "force per volume"
    FORMATION_VOLUME_FACTOR = "formation volume factor"
    FREQUENCY = "frequency"
    FREQUENCY_INTERVAL = "frequency interval"
    GAMMA_RAY_API_UNIT = "gamma ray API unit"
    HEAT_CAPACITY = "heat capacity"
    HEAT_FLOW_RATE = "heat flow rate"
    HEAT_TRANSFER_COEFFICIENT = "heat transfer coefficient"
    ILLUMINANCE = "illuminance"
    INDEX = "index"
    IRRADIANCE = "irradiance"
    ISOTHERMAL_COMPRESSIBILITY = "isothermal compressibility"
    KINEMATIC_VISCOSITY = "kinematic viscosity"
    LAMBDA_RHO = "Lambda Rho"
    LAME_CONSTANT = "Lame constant"
    LENGTH = "length"
    LENGTH_PER_LENGTH = "length per length"
    LENGTH_PER_TEMPERATURE = "length per temperature"
    LENGTH_PER_VOLUME = "length per volume"
    LEVEL_OF_POWER_INTENSITY = "level of power intensity"
    LIGHT_EXPOSURE = "light exposure"
    LINEAR_THERMAL_EXPANSION = "linear thermal expansion"
    LUMINANCE = "luminance"
    LUMINOUS_EFFICACY = "luminous efficacy"
    LUMINOUS_FLUX = "luminous flux"
    LUMINOUS_INTENSITY = "luminous intensity"
    MAGNETIC_DIPOLE_MOMENT = "magnetic dipole moment"
    MAGNETIC_FIELD_STRENGTH = "magnetic field strength"
    MAGNETIC_FLUX = "magnetic flux"
    MAGNETIC_INDUCTION = "magnetic induction"
    MAGNETIC_PERMEABILITY = "magnetic permeability"
    MAGNETIC_VECTOR_POTENTIAL = "magnetic vector potential"
    MASS = "mass"
    MASS_ATTENUATION_COEFFICIENT = "mass attenuation coefficient"
    MASS_CONCENTRATION = "mass concentration"
    MASS_FLOW_RATE = "mass flow rate"
    MASS_LENGTH = "mass length"
    MASS_PER_ENERGY = "mass per energy"
    MASS_PER_LENGTH = "mass per length"
    MASS_PER_TIME_PER_AREA = "mass per time per area"
    MASS_PER_TIME_PER_LENGTH = "mass per time per length"
    MASS_PER_VOLUME_PER_LENGTH = "mass per volume per length"
    MOBILITY = "mobility"
    MODULUS_OF_COMPRESSION = "modulus of compression"
    MOLAR_CONCENTRATION = "molar concentration"
    MOLAR_HEAT_CAPACITY = "molar heat capacity"
    MOLAR_VOLUME = "molar volume"
    MOLE_PER_AREA = "mole per area"
    MOLE_PER_TIME = "mole per time"
    MOLE_PER_TIME_PER_AREA = "mole per time per area"
    MOMENT_OF_FORCE = "moment of force"
    MOMENT_OF_INERTIA = "moment of inertia"
    MOMENT_OF_SECTION = "moment of section"
    MOMENTUM = "momentum"
    MU_RHO = "Mu Rho"
    NET_TO_GROSS_RATIO = "net to gross ratio"
    NEUTRON_API_UNIT = "neutron API unit"
    NON_DARCY_FLOW_COEFFICIENT = "nonDarcy flow coefficient"
    OPERATIONS_PER_TIME = "operations per time"
    PARACHOR = "parachor"
    PER_AREA = "per area"
    PER_ELECTRIC_POTENTIAL = "per electric potential"
    PER_FORCE = "per force"
    PER_LENGTH = "per length"
    PER_MASS = "per mass"
    PER_VOLUME = "per volume"
    PERMEABILITY_LENGTH = "permeability length"
    PERMEABILITY_ROCK = "permeability rock"
    PERMEABILITY_THICKNESS = "permeability thickness"
    PERMEANCE = "permeance"
    PERMITTIVITY = "permittivity"
    P_H = "pH"
    PLANE_ANGLE = "plane angle"
    POISSON_RATIO = "Poisson ratio"
    PORE_VOLUME = "pore volume"
    POROSITY = "porosity"
    POTENTIAL_DIFFERENCE_PER_POWER_DROP = "potential difference per power drop"
    POWER = "power"
    POWER_PER_VOLUME = "power per volume"
    PRESSURE = "pressure"
    PRESSURE_PER_TIME = "pressure per time"
    PRESSURE_SQUARED = "pressure squared"
    PRESSURE_SQUARED_PER_FORCE_TIME_PER_AREA = (
        "pressure squared per force time per area"
    )
    PRESSURE_TIME_PER_VOLUME = "pressure time per volume"
    PRODUCTIVITY_INDEX = "productivity index"
    PROPERTY_MULTIPLIER = "property multiplier"
    QUANTITY = "quantity"
    QUANTITY_OF_LIGHT = "quantity of light"
    RADIANCE = "radiance"
    RADIANT_INTENSITY = "radiant intensity"
    RELATIVE_PERMEABILITY = "relative permeability"
    RELATIVE_POWER = "relative power"
    RELATIVE_TIME = "relative time"
    RELUCTANCE = "reluctance"
    RESISTANCE = "resistance"
    RESISTIVITY_PER_LENGTH = "resistivity per length"
    RESQML_ROOT_PROPERTY = "RESQML root property"
    ROCK_IMPEDANCE = "Rock Impedance"
    ROCK_PERMEABILITY = "rock permeability"
    ROCK_VOLUME = "rock volume"
    SATURATION = "saturation"
    SECOND_MOMENT_OF_AREA = "second moment of area"
    SHEAR_MODULUS = "shear modulus"
    SOLID_ANGLE = "solid angle"
    SOLUTION_GAS_OIL_RATIO = "solution gas-oil ratio"
    SPECIFIC_ACTIVITY_OF_RADIOACTIVITY = "specific activity (of radioactivity)"
    SPECIFIC_ENERGY = "specific energy"
    SPECIFIC_HEAT_CAPACITY = "specific heat capacity"
    SPECIFIC_PRODUCTIVITY_INDEX = "specific productivity index"
    SPECIFIC_VOLUME = "specific volume"
    SURFACE_DENSITY = "surface density"
    TEMPERATURE_PER_LENGTH = "temperature per length"
    TEMPERATURE_PER_TIME = "temperature per time"
    THERMAL_CONDUCTANCE = "thermal conductance"
    THERMAL_CONDUCTIVITY = "thermal conductivity"
    THERMAL_DIFFUSIVITY = "thermal diffusivity"
    THERMAL_INSULANCE = "thermal insulance"
    THERMAL_RESISTANCE = "thermal resistance"
    THERMODYNAMIC_TEMPERATURE = "thermodynamic temperature"
    THICKNESS = "thickness"
    TIME = "time"
    TIME_PER_LENGTH = "time per length"
    TIME_PER_VOLUME = "time per volume"
    TRANSMISSIBILITY = "transmissibility"
    UNIT_PRODUCTIVITY_INDEX = "unit productivity index"
    UNITLESS = "unitless"
    VAPOR_OIL_GAS_RATIO = "vapor oil-gas ratio"
    VELOCITY = "velocity"
    VOLUME = "volume"
    VOLUME_FLOW_RATE = "volume flow rate"
    VOLUME_LENGTH_PER_TIME = "volume length per time"
    VOLUME_PER_AREA = "volume per area"
    VOLUME_PER_LENGTH = "volume per length"
    VOLUME_PER_TIME_PER_AREA = "volume per time per area"
    VOLUME_PER_TIME_PER_LENGTH = "volume per time per length"
    VOLUME_PER_TIME_PER_TIME = "volume per time per time"
    VOLUME_PER_TIME_PER_VOLUME = "volume per time per volume"
    VOLUME_PER_VOLUME = "volume per volume"
    VOLUMETRIC_HEAT_TRANSFER_COEFFICIENT = (
        "volumetric heat transfer coefficient"
    )
    VOLUMETRIC_THERMAL_EXPANSION = "volumetric thermal expansion"
    WORK = "work"
    YOUNG_MODULUS = "Young modulus"


class ResqmlUom(Enum):
    VALUE = "%"
    AREA = "%[area]"
    MASS = "%[mass]"
    MOLAR = "%[molar]"
    VOL = "%[vol]"
    BBL_D_BBL_D = "(bbl/d)/(bbl/d)"
    M3_D_M3_D = "(m3/d)/(m3/d)"
    M3_S_M3_S = "(m3/s)/(m3/s)"
    VALUE_0_001_BBL_FT3 = "0.001 bbl/ft3"
    VALUE_0_001_BBL_M3 = "0.001 bbl/m3"
    VALUE_0_001_D_FT3 = "0.001 d/ft3"
    VALUE_0_001_GAL_UK_BBL = "0.001 gal[UK]/bbl"
    VALUE_0_001_GAL_UK_GAL_UK = "0.001 gal[UK]/gal[UK]"
    VALUE_0_001_GAL_US_BBL = "0.001 gal[US]/bbl"
    VALUE_0_001_GAL_US_FT3 = "0.001 gal[US]/ft3"
    VALUE_0_001_GAL_US_GAL_US = "0.001 gal[US]/gal[US]"
    VALUE_0_001_H_FT = "0.001 h/ft"
    VALUE_0_001_K_PA2_C_P = "0.001 kPa2/cP"
    VALUE_0_001_LBM_BBL = "0.001 lbm/bbl"
    VALUE_0_001_LBM_GAL_UK = "0.001 lbm/gal[UK]"
    VALUE_0_001_LBM_GAL_US = "0.001 lbm/gal[US]"
    VALUE_0_001_PSI_FT = "0.001 psi/ft"
    VALUE_0_001_PT_UK_BBL = "0.001 pt[UK]/bbl"
    VALUE_0_001_SECA = "0.001 seca"
    VALUE_0_01_BBL_BBL = "0.01 bbl/bbl"
    VALUE_0_01_DEGA_FT = "0.01 dega/ft"
    VALUE_0_01_DEG_F_FT = "0.01 degF/ft"
    VALUE_0_01_DM3_KM = "0.01 dm3/km"
    VALUE_0_01_FT_FT = "0.01 ft/ft"
    VALUE_0_01_GRAIN_FT3 = "0.01 grain/ft3"
    VALUE_0_01_L_KG = "0.01 L/kg"
    VALUE_0_01_L_KM = "0.01 L/km"
    VALUE_0_01_LBF_FT = "0.01 lbf/ft"
    VALUE_0_01_LBF_FT2 = "0.01 lbf/ft2"
    VALUE_0_01_LBM_FT2 = "0.01 lbm/ft2"
    VALUE_0_01_PSI_FT = "0.01 psi/ft"
    VALUE_0_1_FT = "0.1 ft"
    VALUE_0_1_FT_US = "0.1 ft[US]"
    VALUE_0_1_GAL_US_BBL = "0.1 gal[US]/bbl"
    VALUE_0_1_IN = "0.1 in"
    VALUE_0_1_L_BBL = "0.1 L/bbl"
    VALUE_0_1_LBM_BBL = "0.1 lbm/bbl"
    VALUE_0_1_PT_US_BBL = "0.1 pt[US]/bbl"
    VALUE_0_1_YD = "0.1 yd"
    VALUE_1_KG_S = "1/(kg.s)"
    VALUE_1_16_IN = "1/16 in"
    VALUE_1_2_FT = "1/2 ft"
    VALUE_1_2_MS = "1/2 ms"
    VALUE_1_30_CM3_MIN = "1/30 cm3/min"
    VALUE_1_30_DEGA_FT = "1/30 dega/ft"
    VALUE_1_30_DEGA_M = "1/30 dega/m"
    VALUE_1_30_LBF_M = "1/30 lbf/m"
    VALUE_1_30_M_M = "1/30 m/m"
    VALUE_1_30_N_M = "1/30 N/m"
    VALUE_1_32_IN = "1/32 in"
    VALUE_1_64_IN = "1/64 in"
    VALUE_1_A = "1/a"
    VALUE_1_ANGSTROM = "1/angstrom"
    VALUE_1_BAR = "1/bar"
    VALUE_1_BBL = "1/bbl"
    VALUE_1_CM = "1/cm"
    VALUE_1_D = "1/d"
    VALUE_1_DEG_C = "1/degC"
    VALUE_1_DEG_F = "1/degF"
    VALUE_1_DEG_R = "1/degR"
    VALUE_1_FT = "1/ft"
    VALUE_1_FT2 = "1/ft2"
    VALUE_1_FT3 = "1/ft3"
    VALUE_1_G = "1/g"
    VALUE_1_GAL_UK = "1/gal[UK]"
    VALUE_1_GAL_US = "1/gal[US]"
    VALUE_1_H = "1/H"
    VALUE_1_H_1 = "1/h"
    VALUE_1_IN = "1/in"
    VALUE_1_K = "1/K"
    VALUE_1_KG = "1/kg"
    VALUE_1_KM2 = "1/km2"
    VALUE_1_K_PA = "1/kPa"
    VALUE_1_L = "1/L"
    VALUE_1_LBF = "1/lbf"
    VALUE_1_LBM = "1/lbm"
    VALUE_1_M = "1/m"
    VALUE_1_M2 = "1/m2"
    VALUE_1_M3 = "1/m3"
    VALUE_1_MI = "1/mi"
    VALUE_1_MI2 = "1/mi2"
    VALUE_1_MIN = "1/min"
    VALUE_1_MM = "1/mm"
    VALUE_1_MS = "1/ms"
    VALUE_1_N = "1/N"
    VALUE_1_NM = "1/nm"
    VALUE_1_PA = "1/Pa"
    VALUE_1_P_PA = "1/pPa"
    VALUE_1_PSI = "1/psi"
    VALUE_1_S = "1/s"
    VALUE_1_UPSI = "1/upsi"
    VALUE_1_US = "1/us"
    VALUE_1_U_V = "1/uV"
    VALUE_1_V = "1/V"
    VALUE_1_WK = "1/wk"
    VALUE_1_YD = "1/yd"
    VALUE_10_FT = "10 ft"
    VALUE_10_IN = "10 in"
    VALUE_10_KM = "10 km"
    VALUE_10_K_N = "10 kN"
    VALUE_10_MG_M3 = "10 Mg/m3"
    VALUE_100_FT = "100 ft"
    VALUE_100_KA_T = "100 ka[t]"
    VALUE_100_KM = "100 km"
    VALUE_1000_BBL = "1000 bbl"
    VALUE_1000_BBL_FT_D = "1000 bbl.ft/d"
    VALUE_1000_BBL_D = "1000 bbl/d"
    VALUE_1000_FT = "1000 ft"
    VALUE_1000_FT_H = "1000 ft/h"
    VALUE_1000_FT_S = "1000 ft/s"
    VALUE_1000_FT3 = "1000 ft3"
    VALUE_1000_FT3_D_FT = "1000 ft3/(d.ft)"
    VALUE_1000_FT3_PSI_D = "1000 ft3/(psi.d)"
    VALUE_1000_FT3_BBL = "1000 ft3/bbl"
    VALUE_1000_FT3_D = "1000 ft3/d"
    VALUE_1000_GAL_UK = "1000 gal[UK]"
    VALUE_1000_GAL_US = "1000 gal[US]"
    VALUE_1000_LBF_FT = "1000 lbf.ft"
    VALUE_1000_M3 = "1000 m3"
    VALUE_1000_M3_D_M = "1000 m3/(d.m)"
    VALUE_1000_M3_H_M = "1000 m3/(h.m)"
    VALUE_1000_M3_D = "1000 m3/d"
    VALUE_1000_M3_H = "1000 m3/h"
    VALUE_1000_M3_M3 = "1000 m3/m3"
    VALUE_1000_M4_D = "1000 m4/d"
    VALUE_1_E_6_ACRE_FT_BBL = "1E-6 acre.ft/bbl"
    VALUE_1_E_6_BBL_FT3 = "1E-6 bbl/ft3"
    VALUE_1_E_6_BBL_M3 = "1E-6 bbl/m3"
    VALUE_1_E_6_GAL_US = "1E-6 gal[US]"
    VALUE_1_E_6_M3_M3_DEG_C = "1E-6 m3/(m3.degC)"
    VALUE_1_E_6_M3_M3_DEG_F = "1E-6 m3/(m3.degF)"
    VALUE_1_E_9_1_FT = "1E-9 1/ft"
    VALUE_1_E12_FT3 = "1E12 ft3"
    VALUE_1_E6_FT3_D_BBL_D = "1E6 (ft3/d)/(bbl/d)"
    VALUE_1_E6_BBL = "1E6 bbl"
    VALUE_1_E6_BBL_ACRE_FT = "1E6 bbl/(acre.ft)"
    VALUE_1_E6_BBL_ACRE = "1E6 bbl/acre"
    VALUE_1_E6_BBL_D = "1E6 bbl/d"
    VALUE_1_E6_BTU_IT = "1E6 Btu[IT]"
    VALUE_1_E6_BTU_IT_H = "1E6 Btu[IT]/h"
    VALUE_1_E6_FT3 = "1E6 ft3"
    VALUE_1_E6_FT3_ACRE_FT = "1E6 ft3/(acre.ft)"
    VALUE_1_E6_FT3_BBL = "1E6 ft3/bbl"
    VALUE_1_E6_FT3_D = "1E6 ft3/d"
    VALUE_1_E6_LBM_A = "1E6 lbm/a"
    VALUE_1_E6_M3 = "1E6 m3"
    VALUE_1_E6_M3_D = "1E6 m3/d"
    VALUE_1_E9_BBL = "1E9 bbl"
    VALUE_1_E9_FT3 = "1E9 ft3"
    VALUE_30_FT = "30 ft"
    VALUE_30_M = "30 m"
    A = "A"
    A_1 = "a"
    A_H = "A.h"
    A_M2 = "A.m2"
    A_S = "A.s"
    A_S_KG = "A.s/kg"
    A_S_M3 = "A.s/m3"
    A_CM2 = "A/cm2"
    A_FT2 = "A/ft2"
    A_M = "A/m"
    A_M2_1 = "A/m2"
    A_MM = "A/mm"
    A_MM2 = "A/mm2"
    A_T = "a[t]"
    ACRE = "acre"
    ACRE_FT = "acre.ft"
    AG = "ag"
    A_J = "aJ"
    ANGSTROM = "angstrom"
    AT_1 = "at"
    ATM = "atm"
    ATM_FT = "atm/ft"
    ATM_H = "atm/h"
    ATM_HM = "atm/hm"
    ATM_M = "atm/m"
    B = "b"
    B_1 = "B"
    B_W = "B.W"
    B_CM3 = "b/cm3"
    B_M = "B/m"
    B_O = "B/O"
    BAR = "bar"
    BAR_H = "bar/h"
    BAR_KM = "bar/km"
    BAR_M = "bar/m"
    BAR2 = "bar2"
    BAR2_C_P = "bar2/cP"
    BBL = "bbl"
    BBL_ACRE_FT = "bbl/(acre.ft)"
    BBL_D_ACRE_FT = "bbl/(d.acre.ft)"
    BBL_D_FT = "bbl/(d.ft)"
    BBL_FT_PSI_D = "bbl/(ft.psi.d)"
    BBL_K_PA_D = "bbl/(kPa.d)"
    BBL_PSI_D = "bbl/(psi.d)"
    BBL_ACRE = "bbl/acre"
    BBL_BBL = "bbl/bbl"
    BBL_D = "bbl/d"
    BBL_D2 = "bbl/d2"
    BBL_FT = "bbl/ft"
    BBL_FT3 = "bbl/ft3"
    BBL_H = "bbl/h"
    BBL_H2 = "bbl/h2"
    BBL_IN = "bbl/in"
    BBL_M3 = "bbl/m3"
    BBL_MI = "bbl/mi"
    BBL_MIN = "bbl/min"
    BBL_PSI = "bbl/psi"
    BBL_TON_UK = "bbl/ton[UK]"
    BBL_TON_US = "bbl/ton[US]"
    BD = "Bd"
    BIT = "bit"
    BIT_S = "bit/s"
    BQ = "Bq"
    BQ_KG = "Bq/kg"
    BTU_IT = "Btu[IT]"
    BTU_IT_IN_H_FT2_DEG_F = "Btu[IT].in/(h.ft2.degF)"
    BTU_IT_H_FT_DEG_F = "Btu[IT]/(h.ft.degF)"
    BTU_IT_H_FT2 = "Btu[IT]/(h.ft2)"
    BTU_IT_H_FT2_DEG_F = "Btu[IT]/(h.ft2.degF)"
    BTU_IT_H_FT2_DEG_R = "Btu[IT]/(h.ft2.degR)"
    BTU_IT_H_FT3 = "Btu[IT]/(h.ft3)"
    BTU_IT_H_FT3_DEG_F = "Btu[IT]/(h.ft3.degF)"
    BTU_IT_H_M2_DEG_C = "Btu[IT]/(h.m2.degC)"
    BTU_IT_HP_H = "Btu[IT]/(hp.h)"
    BTU_IT_LBM_DEG_F = "Btu[IT]/(lbm.degF)"
    BTU_IT_LBM_DEG_R = "Btu[IT]/(lbm.degR)"
    BTU_IT_LBMOL_DEG_F = "Btu[IT]/(lbmol.degF)"
    BTU_IT_S_FT2 = "Btu[IT]/(s.ft2)"
    BTU_IT_S_FT2_DEG_F = "Btu[IT]/(s.ft2.degF)"
    BTU_IT_S_FT3 = "Btu[IT]/(s.ft3)"
    BTU_IT_S_FT3_DEG_F = "Btu[IT]/(s.ft3.degF)"
    BTU_IT_BBL = "Btu[IT]/bbl"
    BTU_IT_FT3 = "Btu[IT]/ft3"
    BTU_IT_GAL_UK = "Btu[IT]/gal[UK]"
    BTU_IT_GAL_US = "Btu[IT]/gal[US]"
    BTU_IT_H = "Btu[IT]/h"
    BTU_IT_LBM = "Btu[IT]/lbm"
    BTU_IT_LBMOL = "Btu[IT]/lbmol"
    BTU_IT_MIN = "Btu[IT]/min"
    BTU_IT_S = "Btu[IT]/s"
    BTU_TH = "Btu[th]"
    BTU_UK = "Btu[UK]"
    BYTE = "byte"
    BYTE_S = "byte/s"
    C = "C"
    C_M = "C.m"
    C_CM2 = "C/cm2"
    C_CM3 = "C/cm3"
    C_G = "C/g"
    C_KG = "C/kg"
    C_M2 = "C/m2"
    C_M3 = "C/m3"
    C_MM2 = "C/mm2"
    C_MM3 = "C/mm3"
    CA = "ca"
    C_A_1 = "cA"
    CAL_IT = "cal[IT]"
    CAL_TH = "cal[th]"
    CAL_TH_G_K = "cal[th]/(g.K)"
    CAL_TH_H_CM_DEG_C = "cal[th]/(h.cm.degC)"
    CAL_TH_H_CM2 = "cal[th]/(h.cm2)"
    CAL_TH_H_CM2_DEG_C = "cal[th]/(h.cm2.degC)"
    CAL_TH_H_CM3 = "cal[th]/(h.cm3)"
    CAL_TH_MOL_DEG_C = "cal[th]/(mol.degC)"
    CAL_TH_S_CM_DEG_C = "cal[th]/(s.cm.degC)"
    CAL_TH_S_CM2_DEG_C = "cal[th]/(s.cm2.degC)"
    CAL_TH_S_CM3 = "cal[th]/(s.cm3)"
    CAL_TH_CM3 = "cal[th]/cm3"
    CAL_TH_G = "cal[th]/g"
    CAL_TH_H = "cal[th]/h"
    CAL_TH_KG = "cal[th]/kg"
    CAL_TH_LBM = "cal[th]/lbm"
    CAL_TH_M_L = "cal[th]/mL"
    CAL_TH_MM3 = "cal[th]/mm3"
    C_C = "cC"
    CCAL_TH = "ccal[th]"
    CCGR = "ccgr"
    CD = "cd"
    CD_M2 = "cd/m2"
    C_EUC = "cEuc"
    CE_V = "ceV"
    C_F = "cF"
    CG_1 = "cg"
    CGAUSS = "cgauss"
    CGR = "cgr"
    C_GY = "cGy"
    C_H = "cH"
    CHAIN = "chain"
    CHAIN_BN_A = "chain[BnA]"
    CHAIN_BN_B = "chain[BnB]"
    CHAIN_CLA = "chain[Cla]"
    CHAIN_IND37 = "chain[Ind37]"
    CHAIN_SE = "chain[Se]"
    CHAIN_SE_T = "chain[SeT]"
    CHAIN_US = "chain[US]"
    C_HZ = "cHz"
    CI = "Ci"
    C_J = "cJ"
    CM_1 = "cm"
    CM_A = "cm/a"
    CM_S = "cm/s"
    CM_S2 = "cm/s2"
    CM2_1 = "cm2"
    CM2_G = "cm2/g"
    CM2_S = "cm2/s"
    CM3_1 = "cm3"
    CM3_CM3 = "cm3/cm3"
    CM3_G = "cm3/g"
    CM3_H = "cm3/h"
    CM3_L = "cm3/L"
    CM3_M3 = "cm3/m3"
    CM3_MIN = "cm3/min"
    CM3_S = "cm3/s"
    CM4 = "cm4"
    CM_H2_O_4DEG_C = "cmH2O[4degC]"
    C_N = "cN"
    COHM = "cohm"
    C_P = "cP"
    C_PA = "cPa"
    CRD = "crd"
    C_S = "cS"
    CS_1 = "cs"
    C_ST = "cSt"
    CT = "ct"
    C_T_1 = "cT"
    CU = "cu"
    C_V = "cV"
    C_W = "cW"
    C_WB = "cWb"
    CWT_UK = "cwt[UK]"
    CWT_US = "cwt[US]"
    D = "d"
    D_1 = "D"
    D_FT = "D.ft"
    D_M = "D.m"
    D_PA_S = "D/(Pa.s)"
    D_BBL = "d/bbl"
    D_C_P = "D/cP"
    D_FT3 = "d/ft3"
    D_M3 = "d/m3"
    D_API = "D[API]"
    D_A = "dA"
    DAM = "dam"
    DA_N = "daN"
    DA_N_M = "daN.m"
    D_API_1 = "dAPI"
    D_B = "dB"
    D_B_MW = "dB.MW"
    D_B_M_W_1 = "dB.mW"
    D_B_W = "dB.W"
    D_B_FT = "dB/ft"
    D_B_KM = "dB/km"
    D_B_M = "dB/m"
    D_B_O = "dB/O"
    D_C = "dC"
    DCAL_TH = "dcal[th]"
    DEGA = "dega"
    DEGA_FT = "dega/ft"
    DEGA_H = "dega/h"
    DEGA_M = "dega/m"
    DEGA_MIN = "dega/min"
    DEGA_S = "dega/s"
    DEG_C = "degC"
    DEG_C_M2_H_KCAL_TH = "degC.m2.h/kcal[th]"
    DEG_C_FT = "degC/ft"
    DEG_C_H = "degC/h"
    DEG_C_HM = "degC/hm"
    DEG_C_KM = "degC/km"
    DEG_C_K_PA = "degC/kPa"
    DEG_C_M = "degC/m"
    DEG_C_MIN = "degC/min"
    DEG_C_S = "degC/s"
    DEG_F = "degF"
    DEG_F_FT2_H_BTU_IT = "degF.ft2.h/Btu[IT]"
    DEG_F_FT = "degF/ft"
    DEG_F_H = "degF/h"
    DEG_F_M = "degF/m"
    DEG_F_MIN = "degF/min"
    DEG_F_PSI = "degF/psi"
    DEG_F_S = "degF/s"
    DEG_R = "degR"
    D_EUC = "dEuc"
    DE_V = "deV"
    D_F = "dF"
    DGAUSS = "dgauss"
    D_GY = "dGy"
    D_H = "dH"
    D_HZ = "dHz"
    D_J = "dJ"
    DM_1 = "dm"
    DM_S = "dm/s"
    DM3_1 = "dm3"
    DM3_K_W_H = "dm3/(kW.h)"
    DM3_KG = "dm3/kg"
    DM3_KMOL = "dm3/kmol"
    DM3_M = "dm3/m"
    DM3_M3 = "dm3/m3"
    DM3_MJ = "dm3/MJ"
    DM3_S = "dm3/s"
    DM3_S2 = "dm3/s2"
    DM3_T = "dm3/t"
    D_N = "dN"
    D_N_M = "dN.m"
    DOHM = "dohm"
    D_P = "dP"
    D_PA = "dPa"
    DRD = "drd"
    DS = "ds"
    D_S_1 = "dS"
    D_T = "dT"
    D_V = "dV"
    D_W = "dW"
    D_WB = "dWb"
    DYNE = "dyne"
    DYNE_CM2 = "dyne.cm2"
    DYNE_S_CM2 = "dyne.s/cm2"
    DYNE_CM = "dyne/cm"
    DYNE_CM2_1 = "dyne/cm2"
    EA = "EA"
    EA_T = "Ea[t]"
    EC = "EC"
    ECAL_TH = "Ecal[th]"
    EEUC = "EEuc"
    EE_V = "EeV"
    EF = "EF"
    EG = "Eg"
    EGAUSS = "Egauss"
    EGY = "EGy"
    EH = "EH"
    EHZ = "EHz"
    EJ = "EJ"
    EJ_A = "EJ/a"
    EM = "Em"
    EN = "EN"
    EOHM = "Eohm"
    EP = "EP"
    EPA = "EPa"
    ERD = "Erd"
    ERG = "erg"
    ERG_A = "erg/a"
    ERG_CM2 = "erg/cm2"
    ERG_CM3 = "erg/cm3"
    ERG_G = "erg/g"
    ERG_KG = "erg/kg"
    ERG_M3 = "erg/m3"
    ES = "ES"
    ET = "ET"
    EUC = "Euc"
    E_V = "eV"
    EW = "EW"
    EWB = "EWb"
    F = "F"
    F_M = "F/m"
    FA = "fa"
    F_A_1 = "fA"
    FATHOM = "fathom"
    F_C = "fC"
    FCAL_TH = "fcal[th]"
    F_EUC = "fEuc"
    FE_V = "feV"
    F_F = "fF"
    FG = "fg"
    FGAUSS = "fgauss"
    F_GY = "fGy"
    F_H = "fH"
    F_HZ = "fHz"
    F_J = "fJ"
    FLOZ_UK = "floz[UK]"
    FLOZ_US = "floz[US]"
    FM_1 = "fm"
    F_N = "fN"
    FOHM = "fohm"
    FOOTCANDLE = "footcandle"
    FOOTCANDLE_S = "footcandle.s"
    F_P = "fP"
    F_PA = "fPa"
    FRD = "frd"
    F_S = "fS"
    FT = "ft"
    F_T_1 = "fT"
    FT_BBL = "ft/bbl"
    FT_D = "ft/d"
    FT_DEG_F = "ft/degF"
    FT_FT = "ft/ft"
    FT_FT3 = "ft/ft3"
    FT_GAL_US = "ft/gal[US]"
    FT_H = "ft/h"
    FT_IN = "ft/in"
    FT_LBM = "ft/lbm"
    FT_M = "ft/m"
    FT_MI = "ft/mi"
    FT_MIN = "ft/min"
    FT_MS = "ft/ms"
    FT_PSI = "ft/psi"
    FT_S = "ft/s"
    FT_S2 = "ft/s2"
    FT_US = "ft/us"
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
    FT_US_1 = "ft[US]"
    FT2 = "ft2"
    FT2_H = "ft2/h"
    FT2_IN3 = "ft2/in3"
    FT2_LBM = "ft2/lbm"
    FT2_S = "ft2/s"
    FT3 = "ft3"
    FT3_D_FT = "ft3/(d.ft)"
    FT3_FT_PSI_D = "ft3/(ft.psi.d)"
    FT3_MIN_FT2 = "ft3/(min.ft2)"
    FT3_S_FT2 = "ft3/(s.ft2)"
    FT3_BBL = "ft3/bbl"
    FT3_D = "ft3/d"
    FT3_D2 = "ft3/d2"
    FT3_FT = "ft3/ft"
    FT3_FT2 = "ft3/ft2"
    FT3_FT3 = "ft3/ft3"
    FT3_H = "ft3/h"
    FT3_H2 = "ft3/h2"
    FT3_KG = "ft3/kg"
    FT3_LBM = "ft3/lbm"
    FT3_LBMOL = "ft3/lbmol"
    FT3_MIN = "ft3/min"
    FT3_MIN2 = "ft3/min2"
    FT3_RAD = "ft3/rad"
    FT3_S = "ft3/s"
    FT3_S2 = "ft3/s2"
    FT3_SACK_94LBM = "ft3/sack[94lbm]"
    FUR_US = "fur[US]"
    F_V = "fV"
    F_W = "fW"
    F_WB = "fWb"
    G = "g"
    G_FT_CM3_S = "g.ft/(cm3.s)"
    G_M_CM3_S = "g.m/(cm3.s)"
    G_CM3 = "g/cm3"
    G_CM4 = "g/cm4"
    G_DM3 = "g/dm3"
    G_GAL_UK = "g/gal[UK]"
    G_GAL_US = "g/gal[US]"
    G_KG = "g/kg"
    G_L = "g/L"
    G_M3 = "g/m3"
    G_MOL = "g/mol"
    G_S = "g/s"
    G_T = "g/t"
    GA = "GA"
    GA_T = "Ga[t]"
    GAL = "Gal"
    GAL_UK = "gal[UK]"
    GAL_UK_H_FT = "gal[UK]/(h.ft)"
    GAL_UK_H_FT2 = "gal[UK]/(h.ft2)"
    GAL_UK_H_IN = "gal[UK]/(h.in)"
    GAL_UK_H_IN2 = "gal[UK]/(h.in2)"
    GAL_UK_MIN_FT = "gal[UK]/(min.ft)"
    GAL_UK_MIN_FT2 = "gal[UK]/(min.ft2)"
    GAL_UK_D = "gal[UK]/d"
    GAL_UK_FT3 = "gal[UK]/ft3"
    GAL_UK_H = "gal[UK]/h"
    GAL_UK_H2 = "gal[UK]/h2"
    GAL_UK_LBM = "gal[UK]/lbm"
    GAL_UK_MI = "gal[UK]/mi"
    GAL_UK_MIN = "gal[UK]/min"
    GAL_UK_MIN2 = "gal[UK]/min2"
    GAL_US = "gal[US]"
    GAL_US_H_FT = "gal[US]/(h.ft)"
    GAL_US_H_FT2 = "gal[US]/(h.ft2)"
    GAL_US_H_IN = "gal[US]/(h.in)"
    GAL_US_H_IN2 = "gal[US]/(h.in2)"
    GAL_US_MIN_FT = "gal[US]/(min.ft)"
    GAL_US_MIN_FT2 = "gal[US]/(min.ft2)"
    GAL_US_BBL = "gal[US]/bbl"
    GAL_US_D = "gal[US]/d"
    GAL_US_FT = "gal[US]/ft"
    GAL_US_FT3 = "gal[US]/ft3"
    GAL_US_H = "gal[US]/h"
    GAL_US_H2 = "gal[US]/h2"
    GAL_US_LBM = "gal[US]/lbm"
    GAL_US_MI = "gal[US]/mi"
    GAL_US_MIN = "gal[US]/min"
    GAL_US_MIN2 = "gal[US]/min2"
    GAL_US_SACK_94LBM = "gal[US]/sack[94lbm]"
    GAL_US_TON_UK = "gal[US]/ton[UK]"
    GAL_US_TON_US = "gal[US]/ton[US]"
    G_API = "gAPI"
    GAUSS = "gauss"
    GAUSS_CM = "gauss/cm"
    GBQ = "GBq"
    GC = "GC"
    GCAL_TH = "Gcal[th]"
    GEUC = "GEuc"
    GE_V = "GeV"
    GF = "gf"
    GF_1 = "GF"
    GG = "Gg"
    GGAUSS = "Ggauss"
    GGY = "GGy"
    GH = "GH"
    GHZ = "GHz"
    GJ = "GJ"
    GM = "Gm"
    GN = "gn"
    GN_1 = "GN"
    GOHM = "Gohm"
    GON = "gon"
    GP = "GP"
    GPA = "GPa"
    GPA_CM = "GPa/cm"
    GPA2 = "GPa2"
    GRAIN = "grain"
    GRAIN_FT3 = "grain/ft3"
    GRAIN_GAL_US = "grain/gal[US]"
    GRD = "Grd"
    GS_1 = "GS"
    GT_1 = "GT"
    GV = "GV"
    GW = "GW"
    GW_H = "GW.h"
    GWB = "GWb"
    GY = "Gy"
    H = "H"
    H_1 = "h"
    H_FT3 = "h/ft3"
    H_KM = "h/km"
    H_M = "H/m"
    H_M3 = "h/m3"
    HA = "ha"
    HA_M = "ha.m"
    HBAR = "hbar"
    HG = "hg"
    H_L = "hL"
    HM_1 = "hm"
    H_N = "hN"
    HP = "hp"
    HP_H = "hp.h"
    HP_H_BBL = "hp.h/bbl"
    HP_H_LBM = "hp.h/lbm"
    HP_FT3 = "hp/ft3"
    HP_IN2 = "hp/in2"
    HP_ELEC = "hp[elec]"
    HP_HYD = "hp[hyd]"
    HP_HYD_IN2 = "hp[hyd]/in2"
    HP_METRIC = "hp[metric]"
    HP_METRIC_H = "hp[metric].h"
    HS = "hs"
    HZ = "Hz"
    IN = "in"
    IN_IN_DEG_F = "in/(in.degF)"
    IN_A = "in/a"
    IN_MIN = "in/min"
    IN_S = "in/s"
    IN_S2 = "in/s2"
    IN_US = "in[US]"
    IN2 = "in2"
    IN2_FT2 = "in2/ft2"
    IN2_IN2 = "in2/in2"
    IN2_S = "in2/s"
    IN3 = "in3"
    IN3_FT = "in3/ft"
    IN4 = "in4"
    IN_H2_O_39DEG_F = "inH2O[39degF]"
    IN_H2_O_60DEG_F = "inH2O[60degF]"
    IN_HG_32DEG_F = "inHg[32degF]"
    IN_HG_60DEG_F = "inHg[60degF]"
    J = "J"
    J_M_S_M2_K = "J.m/(s.m2.K)"
    J_M_M2 = "J.m/m2"
    J_G_K = "J/(g.K)"
    J_KG_K = "J/(kg.K)"
    J_MOL_K = "J/(mol.K)"
    J_S_M2_DEG_C = "J/(s.m2.degC)"
    J_CM2 = "J/cm2"
    J_DM3 = "J/dm3"
    J_G = "J/g"
    J_K = "J/K"
    J_KG = "J/kg"
    J_M = "J/m"
    J_M2 = "J/m2"
    J_M3 = "J/m3"
    J_MOL = "J/mol"
    J_S = "J/s"
    K = "K"
    K_M2_K_W = "K.m2/kW"
    K_M2_W = "K.m2/W"
    K_KM = "K/km"
    K_M = "K/m"
    K_PA = "K/Pa"
    K_S = "K/s"
    K_W = "K/W"
    K_A = "kA"
    KA_T = "ka[t]"
    K_C = "kC"
    KCAL_TH = "kcal[th]"
    KCAL_TH_M_CM2 = "kcal[th].m/cm2"
    KCAL_TH_H_M_DEG_C = "kcal[th]/(h.m.degC)"
    KCAL_TH_H_M2_DEG_C = "kcal[th]/(h.m2.degC)"
    KCAL_TH_KG_DEG_C = "kcal[th]/(kg.degC)"
    KCAL_TH_CM3 = "kcal[th]/cm3"
    KCAL_TH_G = "kcal[th]/g"
    KCAL_TH_H = "kcal[th]/h"
    KCAL_TH_KG = "kcal[th]/kg"
    KCAL_TH_M3 = "kcal[th]/m3"
    KCAL_TH_MOL = "kcal[th]/mol"
    KCD = "kcd"
    KDYNE = "kdyne"
    K_EUC = "kEuc"
    KE_V = "keV"
    K_F = "kF"
    KG = "kg"
    KG_M = "kg.m"
    KG_M_CM2 = "kg.m/cm2"
    KG_M_S = "kg.m/s"
    KG_M2 = "kg.m2"
    KG_K_W_H = "kg/(kW.h)"
    KG_M_S_1 = "kg/(m.s)"
    KG_M2_S = "kg/(m2.s)"
    KG_D = "kg/d"
    KG_DM3 = "kg/dm3"
    KG_DM4 = "kg/dm4"
    KG_H = "kg/h"
    KG_J = "kg/J"
    KG_KG = "kg/kg"
    KG_L = "kg/L"
    KG_M_1 = "kg/m"
    KG_M2_1 = "kg/m2"
    KG_M3 = "kg/m3"
    KG_M4 = "kg/m4"
    KG_MIN = "kg/min"
    KG_MJ = "kg/MJ"
    KG_MOL = "kg/mol"
    KG_S = "kg/s"
    KG_SACK_94LBM = "kg/sack[94lbm]"
    KG_T = "kg/t"
    KGAUSS = "kgauss"
    KGF = "kgf"
    KGF_M = "kgf.m"
    KGF_M_CM2 = "kgf.m/cm2"
    KGF_M_M = "kgf.m/m"
    KGF_M2 = "kgf.m2"
    KGF_S_M2 = "kgf.s/m2"
    KGF_CM = "kgf/cm"
    KGF_CM2 = "kgf/cm2"
    KGF_KGF = "kgf/kgf"
    KGF_M2_1 = "kgf/m2"
    KGF_MM2 = "kgf/mm2"
    K_GY = "kGy"
    K_H = "kH"
    K_HZ = "kHz"
    KIBYTE = "Kibyte"
    K_J = "kJ"
    K_J_M_H_M2_K = "kJ.m/(h.m2.K)"
    K_J_H_M2_K = "kJ/(h.m2.K)"
    K_J_KG_K = "kJ/(kg.K)"
    K_J_KMOL_K = "kJ/(kmol.K)"
    K_J_DM3 = "kJ/dm3"
    K_J_KG = "kJ/kg"
    K_J_KMOL = "kJ/kmol"
    K_J_M3 = "kJ/m3"
    KLBF = "klbf"
    KLBM = "klbm"
    KLBM_IN = "klbm/in"
    KLX = "klx"
    KM_1 = "km"
    KM_CM = "km/cm"
    KM_DM3 = "km/dm3"
    KM_H = "km/h"
    KM_L = "km/L"
    KM_S = "km/s"
    KM2 = "km2"
    KM3 = "km3"
    KMOL = "kmol"
    KMOL_H = "kmol/h"
    KMOL_M3 = "kmol/m3"
    KMOL_S = "kmol/s"
    K_N = "kN"
    K_N_M = "kN.m"
    K_N_M2 = "kN.m2"
    K_N_M_1 = "kN/m"
    K_N_M2_1 = "kN/m2"
    KNOT = "knot"
    KOHM = "kohm"
    KOHM_M = "kohm.m"
    K_P = "kP"
    K_PA_1 = "kPa"
    K_PA_S_M = "kPa.s/m"
    K_PA_H = "kPa/h"
    K_PA_HM = "kPa/hm"
    K_PA_M = "kPa/m"
    K_PA_MIN = "kPa/min"
    K_PA2 = "kPa2"
    K_PA2_C_P = "kPa2/cP"
    KPSI = "kpsi"
    KPSI2 = "kpsi2"
    KRAD = "krad"
    KRD = "krd"
    K_S_1 = "kS"
    K_S_M = "kS/m"
    K_T = "kT"
    K_V = "kV"
    K_W_1 = "kW"
    K_W_H = "kW.h"
    K_W_H_KG_DEG_C = "kW.h/(kg.degC)"
    K_W_H_DM3 = "kW.h/dm3"
    K_W_H_KG = "kW.h/kg"
    K_W_H_M3 = "kW.h/m3"
    K_W_M2_K = "kW/(m2.K)"
    K_W_M3_K = "kW/(m3.K)"
    K_W_CM2 = "kW/cm2"
    K_W_M2 = "kW/m2"
    K_W_M3 = "kW/m3"
    K_WB = "kWb"
    L = "L"
    L_BAR_MIN = "L/(bar.min)"
    L_H = "L/h"
    L_KG = "L/kg"
    L_KMOL = "L/kmol"
    L_M = "L/m"
    L_M3 = "L/m3"
    L_MIN = "L/min"
    L_MOL = "L/mol"
    L_S = "L/s"
    L_S2 = "L/s2"
    L_T = "L/t"
    L_TON_UK = "L/ton[UK]"
    LBF = "lbf"
    LBF_FT = "lbf.ft"
    LBF_FT_BBL = "lbf.ft/bbl"
    LBF_FT_GAL_US = "lbf.ft/gal[US]"
    LBF_FT_IN = "lbf.ft/in"
    LBF_FT_IN2 = "lbf.ft/in2"
    LBF_FT_LBM = "lbf.ft/lbm"
    LBF_FT_MIN = "lbf.ft/min"
    LBF_FT_S = "lbf.ft/s"
    LBF_IN = "lbf.in"
    LBF_IN_IN = "lbf.in/in"
    LBF_IN2 = "lbf.in2"
    LBF_S_FT2 = "lbf.s/ft2"
    LBF_S_IN2 = "lbf.s/in2"
    LBF_FT_1 = "lbf/ft"
    LBF_FT2 = "lbf/ft2"
    LBF_FT3 = "lbf/ft3"
    LBF_GAL_US = "lbf/gal[US]"
    LBF_IN_1 = "lbf/in"
    LBF_LBF = "lbf/lbf"
    LBM = "lbm"
    LBM_FT = "lbm.ft"
    LBM_FT_S = "lbm.ft/s"
    LBM_FT2 = "lbm.ft2"
    LBM_FT2_S2 = "lbm.ft2/s2"
    LBM_FT_H = "lbm/(ft.h)"
    LBM_FT_S_1 = "lbm/(ft.s)"
    LBM_FT2_H = "lbm/(ft2.h)"
    LBM_FT2_S = "lbm/(ft2.s)"
    LBM_GAL_UK_FT = "lbm/(gal[UK].ft)"
    LBM_GAL_US_FT = "lbm/(gal[US].ft)"
    LBM_HP_H = "lbm/(hp.h)"
    LBM_BBL = "lbm/bbl"
    LBM_D = "lbm/d"
    LBM_FT_1 = "lbm/ft"
    LBM_FT2_1 = "lbm/ft2"
    LBM_FT3 = "lbm/ft3"
    LBM_FT4 = "lbm/ft4"
    LBM_GAL_UK = "lbm/gal[UK]"
    LBM_GAL_US = "lbm/gal[US]"
    LBM_H = "lbm/h"
    LBM_IN3 = "lbm/in3"
    LBM_LBMOL = "lbm/lbmol"
    LBM_MIN = "lbm/min"
    LBM_S = "lbm/s"
    LBMOL = "lbmol"
    LBMOL_H_FT2 = "lbmol/(h.ft2)"
    LBMOL_S_FT2 = "lbmol/(s.ft2)"
    LBMOL_FT3 = "lbmol/ft3"
    LBMOL_GAL_UK = "lbmol/gal[UK]"
    LBMOL_GAL_US = "lbmol/gal[US]"
    LBMOL_H = "lbmol/h"
    LBMOL_S = "lbmol/s"
    LINK = "link"
    LINK_BN_A = "link[BnA]"
    LINK_BN_B = "link[BnB]"
    LINK_CLA = "link[Cla]"
    LINK_SE = "link[Se]"
    LINK_SE_T = "link[SeT]"
    LINK_US = "link[US]"
    LM_1 = "lm"
    LM_S = "lm.s"
    LM_M2 = "lm/m2"
    LM_W = "lm/W"
    LX = "lx"
    LX_S = "lx.s"
    M = "m"
    M_M_K = "m/(m.K)"
    M_CM = "m/cm"
    M_D = "m/d"
    M_H = "m/h"
    M_K = "m/K"
    M_KG = "m/kg"
    M_KM = "m/km"
    M_K_PA = "m/kPa"
    M_M = "m/m"
    M_M3 = "m/m3"
    M_MIN = "m/min"
    M_MS = "m/ms"
    M_PA = "m/Pa"
    M_S = "m/s"
    M_S2 = "m/s2"
    M_GER = "m[Ger]"
    M2 = "m2"
    M2_K_PA_D = "m2/(kPa.d)"
    M2_PA_S = "m2/(Pa.s)"
    M2_CM3 = "m2/cm3"
    M2_D = "m2/d"
    M2_G = "m2/g"
    M2_H = "m2/h"
    M2_KG = "m2/kg"
    M2_M2 = "m2/m2"
    M2_M3 = "m2/m3"
    M2_MOL = "m2/mol"
    M2_S = "m2/s"
    M3 = "m3"
    M3_BAR_D = "m3/(bar.d)"
    M3_BAR_H = "m3/(bar.h)"
    M3_BAR_MIN = "m3/(bar.min)"
    M3_D_M = "m3/(d.m)"
    M3_H_M = "m3/(h.m)"
    M3_HA_M = "m3/(ha.m)"
    M3_K_PA_D = "m3/(kPa.d)"
    M3_K_PA_H = "m3/(kPa.h)"
    M3_K_W_H = "m3/(kW.h)"
    M3_M3_K = "m3/(m3.K)"
    M3_PA_S = "m3/(Pa.s)"
    M3_PSI_D = "m3/(psi.d)"
    M3_S_FT = "m3/(s.ft)"
    M3_S_M = "m3/(s.m)"
    M3_S_M2 = "m3/(s.m2)"
    M3_S_M3 = "m3/(s.m3)"
    M3_BBL = "m3/bbl"
    M3_D = "m3/d"
    M3_D2 = "m3/d2"
    M3_G = "m3/g"
    M3_H = "m3/h"
    M3_J = "m3/J"
    M3_KG = "m3/kg"
    M3_KM = "m3/km"
    M3_KMOL = "m3/kmol"
    M3_K_PA = "m3/kPa"
    M3_M = "m3/m"
    M3_M2 = "m3/m2"
    M3_M3 = "m3/m3"
    M3_MIN = "m3/min"
    M3_MOL = "m3/mol"
    M3_PA = "m3/Pa"
    M3_RAD = "m3/rad"
    M3_REV = "m3/rev"
    M3_S = "m3/s"
    M3_S2 = "m3/s2"
    M3_T = "m3/t"
    M3_TON_UK = "m3/ton[UK]"
    M3_TON_US = "m3/ton[US]"
    M4 = "m4"
    M4_S = "m4/s"
    M_A = "mA"
    MA_1 = "MA"
    M_A_CM2 = "mA/cm2"
    M_A_FT2 = "mA/ft2"
    MA_T = "Ma[t]"
    MBAR = "mbar"
    MBQ = "MBq"
    M_C = "mC"
    MC_1 = "MC"
    M_C_M2 = "mC/m2"
    MCAL_TH = "Mcal[th]"
    MCAL_TH_1 = "mcal[th]"
    M_CI = "mCi"
    M_D_1 = "mD"
    M_D_FT = "mD.ft"
    M_D_FT2_LBF_S = "mD.ft2/(lbf.s)"
    M_D_IN2_LBF_S = "mD.in2/(lbf.s)"
    M_D_M = "mD.m"
    M_D_PA_S = "mD/(Pa.s)"
    M_D_C_P = "mD/cP"
    MEUC = "MEuc"
    M_EUC_1 = "mEuc"
    ME_V = "meV"
    ME_V_1 = "MeV"
    M_F = "mF"
    MF_1 = "MF"
    MG = "Mg"
    MG_1 = "mg"
    MG_A = "Mg/a"
    MG_D = "Mg/d"
    MG_DM3 = "mg/dm3"
    MG_G = "mg/g"
    MG_GAL_US = "mg/gal[US]"
    MG_H = "Mg/h"
    MG_IN = "Mg/in"
    MG_J = "mg/J"
    MG_KG = "mg/kg"
    MG_L = "mg/L"
    MG_M2 = "Mg/m2"
    MG_M3 = "Mg/m3"
    MG_M3_1 = "mg/m3"
    MG_MIN = "Mg/min"
    M_GAL = "mGal"
    MGAUSS = "Mgauss"
    MGAUSS_1 = "mgauss"
    MGF = "Mgf"
    MGN = "mgn"
    MGY = "MGy"
    M_GY_1 = "mGy"
    MH_1 = "MH"
    M_H_2 = "mH"
    M_HZ = "mHz"
    MHZ_1 = "MHz"
    MI = "mi"
    MI_GAL_UK = "mi/gal[UK]"
    MI_GAL_US = "mi/gal[US]"
    MI_H = "mi/h"
    MI_IN = "mi/in"
    MI_NAUT = "mi[naut]"
    MI_NAUT_UK = "mi[nautUK]"
    MI_US = "mi[US]"
    MI_US_2 = "mi[US]2"
    MI2 = "mi2"
    MI3 = "mi3"
    MIBYTE = "Mibyte"
    MIL = "mil"
    MIL_A = "mil/a"
    MILA_1 = "mila"
    MIN = "min"
    MIN_FT = "min/ft"
    MIN_M = "min/m"
    MINA = "mina"
    M_J = "mJ"
    MJ_1 = "MJ"
    MJ_A = "MJ/a"
    M_J_CM2 = "mJ/cm2"
    MJ_KG = "MJ/kg"
    MJ_KMOL = "MJ/kmol"
    MJ_M = "MJ/m"
    M_J_M2 = "mJ/m2"
    MJ_M3 = "MJ/m3"
    M_L = "mL"
    M_L_GAL_UK = "mL/gal[UK]"
    M_L_GAL_US = "mL/gal[US]"
    M_L_M_L = "mL/mL"
    MM_1 = "Mm"
    MM_4 = "mm"
    MM_MM_K = "mm/(mm.K)"
    MM_A = "mm/a"
    MM_S_1 = "mm/s"
    MM2 = "mm2"
    MM2_MM2 = "mm2/mm2"
    MM2_S = "mm2/s"
    MM3_1 = "mm3"
    MM3_J = "mm3/J"
    MM_HG_0DEG_C = "mmHg[0degC]"
    MMOL = "mmol"
    M_N = "mN"
    MN_1 = "MN"
    M_N_M2 = "mN.m2"
    M_N_KM = "mN/km"
    M_N_M = "mN/m"
    MOHM = "mohm"
    MOHM_1 = "Mohm"
    MOL = "mol"
    MOL_M2_MOL_S = "mol.m2/(mol.s)"
    MOL_S_M2 = "mol/(s.m2)"
    MOL_M2 = "mol/m2"
    MOL_M3 = "mol/m3"
    MOL_MOL = "mol/mol"
    MOL_S = "mol/s"
    M_P = "mP"
    MP_1 = "MP"
    MPA_1 = "MPa"
    M_PA_2 = "mPa"
    M_PA_S = "mPa.s"
    MPA_S_M = "MPa.s/m"
    MPA_H = "MPa/h"
    MPA_M = "MPa/m"
    MPSI = "Mpsi"
    MRAD = "mrad"
    MRAD_1 = "Mrad"
    MRD = "Mrd"
    MRD_1 = "mrd"
    MREM = "mrem"
    MREM_H = "mrem/h"
    MS_1 = "MS"
    M_S_3 = "mS"
    MS_4 = "ms"
    MS_CM = "ms/cm"
    M_S_CM_1 = "mS/cm"
    MS_FT = "ms/ft"
    MS_IN = "ms/in"
    M_S_M = "mS/m"
    MS_M_1 = "ms/m"
    MS_S = "ms/s"
    M_SV = "mSv"
    M_SV_H = "mSv/h"
    M_T = "mT"
    M_T_DM = "mT/dm"
    MV = "MV"
    M_V_1 = "mV"
    M_V_FT = "mV/ft"
    M_V_M = "mV/m"
    MW = "MW"
    M_W_1 = "mW"
    MW_H = "MW.h"
    MW_H_KG = "MW.h/kg"
    MW_H_M3 = "MW.h/m3"
    M_W_M2 = "mW/m2"
    M_WB = "mWb"
    MWB_1 = "MWb"
    N = "N"
    N_M = "N.m"
    N_M_M = "N.m/m"
    N_M2 = "N.m2"
    N_S_M2 = "N.s/m2"
    N_M_1 = "N/m"
    N_M2_1 = "N/m2"
    N_M3 = "N/m3"
    N_MM2 = "N/mm2"
    N_N = "N/N"
    N_A = "nA"
    NA_1 = "na"
    N_API = "nAPI"
    N_C = "nC"
    NCAL_TH = "ncal[th]"
    N_CI = "nCi"
    N_EUC = "nEuc"
    NE_V = "neV"
    N_F = "nF"
    NG = "ng"
    NG_G = "ng/g"
    NG_MG = "ng/mg"
    NGAUSS = "ngauss"
    N_GY = "nGy"
    N_H = "nH"
    N_HZ = "nHz"
    N_J = "nJ"
    NM_4 = "nm"
    NM_S = "nm/s"
    N_N_1 = "nN"
    NOHM = "nohm"
    NOHM_MIL2_FT = "nohm.mil2/ft"
    NOHM_MM2_M = "nohm.mm2/m"
    N_P = "nP"
    N_PA = "nPa"
    NRD = "nrd"
    N_S = "nS"
    NS_1 = "ns"
    NS_FT = "ns/ft"
    NS_M = "ns/m"
    N_T = "nT"
    N_V = "nV"
    N_W = "nW"
    N_WB = "nWb"
    O = "O"
    OE = "Oe"
    OHM = "ohm"
    OHM_CM = "ohm.cm"
    OHM_M = "ohm.m"
    OHM_M2_M = "ohm.m2/m"
    OHM_M_1 = "ohm/m"
    OZF = "ozf"
    OZM = "ozm"
    OZM_TROY = "ozm[troy]"
    P = "P"
    P_A = "pA"
    PA_1 = "Pa"
    PA_S = "Pa.s"
    PA_S_M3_KG = "Pa.s.m3/kg"
    PA_S_M3 = "Pa.s/m3"
    PA_S2_M3 = "Pa.s2/m3"
    PA_H = "Pa/h"
    PA_M = "Pa/m"
    PA_M3 = "Pa/m3"
    PA_S_1 = "Pa/s"
    PA2 = "Pa2"
    PA2_PA_S = "Pa2/(Pa.s)"
    P_C = "pC"
    PCAL_TH = "pcal[th]"
    P_CI = "pCi"
    P_CI_G = "pCi/g"
    PDL = "pdl"
    PDL_CM2 = "pdl.cm2"
    PDL_FT = "pdl.ft"
    PDL_CM = "pdl/cm"
    P_EUC = "pEuc"
    PE_V = "peV"
    P_F = "pF"
    PG = "pg"
    PGAUSS = "pgauss"
    P_GY = "pGy"
    P_HZ = "pHz"
    P_J = "pJ"
    PM = "pm"
    P_N = "pN"
    POHM = "pohm"
    P_P = "pP"
    P_PA = "pPa"
    PPK = "ppk"
    PPM = "ppm"
    PPM_MASS = "ppm[mass]"
    PPM_VOL = "ppm[vol]"
    PPM_VOL_DEG_C = "ppm[vol]/degC"
    PPM_VOL_DEG_F = "ppm[vol]/degF"
    PRD = "prd"
    PS = "ps"
    P_S_1 = "pS"
    PSI = "psi"
    PSI_D_BBL = "psi.d/bbl"
    PSI_S = "psi.s"
    PSI_FT = "psi/ft"
    PSI_H = "psi/h"
    PSI_M = "psi/m"
    PSI_MIN = "psi/min"
    PSI2 = "psi2"
    PSI2_D_C_P_FT3 = "psi2.d/(cP.ft3)"
    PSI2_C_P = "psi2/cP"
    P_T = "pT"
    PT_UK = "pt[UK]"
    PT_UK_HP_H = "pt[UK]/(hp.h)"
    PT_US = "pt[US]"
    P_V = "pV"
    P_W = "pW"
    P_WB = "pWb"
    QT_UK = "qt[UK]"
    QT_US = "qt[US]"
    QUAD = "quad"
    QUAD_A = "quad/a"
    RAD = "rad"
    RAD_FT = "rad/ft"
    RAD_FT3 = "rad/ft3"
    RAD_M = "rad/m"
    RAD_M3 = "rad/m3"
    RAD_S = "rad/s"
    RAD_S2 = "rad/s2"
    RD = "rd"
    REM = "rem"
    REM_H = "rem/h"
    REV = "rev"
    REV_FT = "rev/ft"
    REV_M = "rev/m"
    REV_S = "rev/s"
    ROD_US = "rod[US]"
    RPM = "rpm"
    RPM_S = "rpm/s"
    S = "S"
    S_1 = "s"
    S_CM = "s/cm"
    S_FT = "s/ft"
    S_FT3 = "s/ft3"
    S_IN = "s/in"
    S_KG = "s/kg"
    S_L = "s/L"
    S_M = "S/m"
    S_M_1 = "s/m"
    S_M3 = "s/m3"
    S_QT_UK = "s/qt[UK]"
    S_QT_US = "s/qt[US]"
    S_S = "s/s"
    SACK_94LBM = "sack[94lbm]"
    SECA = "seca"
    SECTION = "section"
    SR = "sr"
    ST = "St"
    SV = "Sv"
    SV_H = "Sv/h"
    SV_S = "Sv/s"
    T = "t"
    T_1 = "T"
    T_A = "t/a"
    T_D = "t/d"
    T_H = "t/h"
    T_M = "T/m"
    T_M3 = "t/m3"
    T_MIN = "t/min"
    TA_1 = "TA"
    TA_T = "Ta[t]"
    TBQ = "TBq"
    TC = "TC"
    TCAL_TH = "Tcal[th]"
    TD_API = "TD[API]"
    TD_API_M = "TD[API].m"
    TD_API_PA_S = "TD[API]/(Pa.s)"
    TEUC = "TEuc"
    TE_V = "TeV"
    TF = "TF"
    TG = "Tg"
    TGAUSS = "Tgauss"
    TGY = "TGy"
    TH_1 = "TH"
    THERM_EC = "therm[EC]"
    THERM_UK = "therm[UK]"
    THERM_US = "therm[US]"
    THZ = "THz"
    TJ = "TJ"
    TJ_A = "TJ/a"
    TM_1 = "Tm"
    TN = "TN"
    TOHM = "Tohm"
    TON_UK = "ton[UK]"
    TON_UK_A = "ton[UK]/a"
    TON_UK_D = "ton[UK]/d"
    TON_UK_H = "ton[UK]/h"
    TON_UK_MIN = "ton[UK]/min"
    TON_US = "ton[US]"
    TON_US_A = "ton[US]/a"
    TON_US_D = "ton[US]/d"
    TON_US_FT2 = "ton[US]/ft2"
    TON_US_H = "ton[US]/h"
    TON_US_MIN = "ton[US]/min"
    TONF_UK = "tonf[UK]"
    TONF_UK_FT2 = "tonf[UK].ft2"
    TONF_UK_FT = "tonf[UK]/ft"
    TONF_UK_FT2_1 = "tonf[UK]/ft2"
    TONF_US = "tonf[US]"
    TONF_US_FT = "tonf[US].ft"
    TONF_US_FT2 = "tonf[US].ft2"
    TONF_US_MI = "tonf[US].mi"
    TONF_US_MI_BBL = "tonf[US].mi/bbl"
    TONF_US_MI_FT = "tonf[US].mi/ft"
    TONF_US_FT_1 = "tonf[US]/ft"
    TONF_US_FT2_1 = "tonf[US]/ft2"
    TONF_US_IN2 = "tonf[US]/in2"
    TON_REFRIG = "tonRefrig"
    TORR = "torr"
    TP = "TP"
    TPA = "TPa"
    TRD = "Trd"
    TS = "TS"
    TT = "TT"
    TV = "TV"
    TW = "TW"
    TW_H = "TW.h"
    TWB = "TWb"
    U_A = "uA"
    U_A_CM2 = "uA/cm2"
    U_A_IN2 = "uA/in2"
    UBAR = "ubar"
    U_C = "uC"
    UCAL_TH = "ucal[th]"
    UCAL_TH_S_CM2 = "ucal[th]/(s.cm2)"
    UCAL_TH_S = "ucal[th]/s"
    U_CI = "uCi"
    U_EUC = "uEuc"
    UE_V = "ueV"
    U_F = "uF"
    U_F_M = "uF/m"
    UG = "ug"
    UG_CM3 = "ug/cm3"
    UG_G = "ug/g"
    UG_MG = "ug/mg"
    UGAUSS = "ugauss"
    U_GY = "uGy"
    U_H = "uH"
    U_H_M = "uH/m"
    U_HZ = "uHz"
    U_J = "uJ"
    UM = "um"
    UM_S = "um/s"
    UM2 = "um2"
    UM2_M = "um2.m"
    UM_HG_0DEG_C = "umHg[0degC]"
    UMOL = "umol"
    U_N = "uN"
    UOHM = "uohm"
    UOHM_FT = "uohm/ft"
    UOHM_M = "uohm/m"
    U_P = "uP"
    U_PA = "uPa"
    UPSI = "upsi"
    URAD = "urad"
    URD = "urd"
    US = "us"
    U_S_1 = "uS"
    US_FT = "us/ft"
    US_IN = "us/in"
    US_M = "us/m"
    U_T = "uT"
    U_V = "uV"
    U_V_FT = "uV/ft"
    U_V_M = "uV/m"
    U_W = "uW"
    U_W_M3 = "uW/m3"
    U_WB = "uWb"
    V = "V"
    V_B = "V/B"
    V_D_B = "V/dB"
    V_M = "V/m"
    W = "W"
    W_M2_K_J_K = "W.m2.K/(J.K)"
    W_M_K = "W/(m.K)"
    W_M2_K = "W/(m2.K)"
    W_M2_SR = "W/(m2.sr)"
    W_M3_K = "W/(m3.K)"
    W_CM2 = "W/cm2"
    W_K = "W/K"
    W_K_W = "W/kW"
    W_M2 = "W/m2"
    W_M3 = "W/m3"
    W_MM2 = "W/mm2"
    W_SR = "W/sr"
    W_W = "W/W"
    WB = "Wb"
    WB_M = "Wb.m"
    WB_M_1 = "Wb/m"
    WB_MM = "Wb/mm"
    WK_1 = "wk"
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
    YD2 = "yd2"
    YD3 = "yd3"


@dataclass
class RockFluidUnitInterpretationIndex:
    """
    An element that allows ordering of fluid feature interpretations in a fluid
    organization interpretation.

    :ivar index: Index of the fluid feature interpretation.
    :ivar rock_fluid_unit:
    """

    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    rock_fluid_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "RockFluidUnit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


class SequenceStratigraphySurface(Enum):
    """
    The enumerated attributes of a horizon.
    """

    FLOODING = "flooding"
    RAVINEMENT = "ravinement"
    MAXIMUM_FLOODING = "maximum flooding"
    TRANSGRESSIVE = "transgressive"


@dataclass
class StratigraphicUnitInterpretationIndex:
    """Element that lets you index and order stratigraphic unit interpretations.

    For possible ordering criteria, see OrderingCriteria.

    :ivar index: An index value associated to an instance of this type
        of interpretation, given a specific ordering criteria.
    :ivar unit:
    """

    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


class StreamlineFlux(Enum):
    """
    Enumeration of the usual streamline fluxes.

    :cvar OIL: Oil Phase flux
    :cvar GAS: Gas Phase flux
    :cvar WATER: Water Phase flux
    :cvar TOTAL: Sum of (Water + Oil + Gas) Phase fluxes
    :cvar OTHER: Used to indicate that another flux is being traced.
        BUSINESS RULE: OtherFlux should appear if this value is
        specified.
    """

    OIL = "oil"
    GAS = "gas"
    WATER = "water"
    TOTAL = "total"
    OTHER = "other"


@dataclass
class StringLookup:
    """
    Defines an element inside a string-to-integer lookup table.

    :ivar key: The corresponding integer value. This value is used in
        HDF5 instead of the string value. The value of null integer
        value must be reserved for NULL. The size of this value is
        constrained by the size of the format used in HDF5,
    :ivar value: A string value. Output from the lookup table.
    """

    key: Optional[int] = field(
        default=None,
        metadata={
            "name": "Key",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


class SubnodeNodeObject(Enum):
    """SubnodeNodeObject is used to specify the node object that supports the
    subnodes.

    This determines the number of nodes per subnode and the continuity
    of the associated geometry or property. For instance, for hexahedral
    cells, cell indicates a fixed value of 8, while for an unstructured
    column layer grid, cell indicates that this count varies from column
    to column.

    :cvar CELL: If geometry or properties are discontinuous from cell to
        cell (i.e., their spatial support is cell), then attach them to
        cell subnodes. BUSINESS RULE: If this object kind is selected,
        then an ordered list of nodes per cell must be specified or
        otherwise known.
    :cvar FACE: If geometry or properties are continuous between cells
        that share the same face (i.e., their spatial support is the
        face), then attach them to face subnodes. BUSINESS RULE: If this
        object kind is selected, then an ordered list of nodes per face
        must be specified or otherwise known.
    :cvar EDGE: If geometry and properties are continuous between cells
        that share the same edge of a face (i.e. their spatial support
        is the edge), then attach them to edge subnodes. BUSINESS RULE:
        If this object kind is selected, then an ordered list of nodes
        per edge must be specified or otherwise known.
    """

    CELL = "cell"
    FACE = "face"
    EDGE = "edge"


class SurfaceRole(Enum):
    """
    Indicates the various roles that a surface topology can have.

    :cvar MAP: Representation support for properties.
    :cvar PICK: Representation support for 3D points picked in 2D or 3D.
    """

    MAP = "map"
    PICK = "pick"


class TectonicBoundaryKind(Enum):
    """
    Enumeration of the types of tectonic boundaries.

    :cvar FAULT: Fracture with displacement
    :cvar FRACTURE: Fracture
    """

    FAULT = "fault"
    FRACTURE = "fracture"


class ThrowKind(Enum):
    """
    Enumerations that characterize the throw of the fault interpretation.
    """

    REVERSE = "reverse"
    NORMAL = "normal"
    THRUST = "thrust"
    STRIKE_AND_SLIP = "strike and slip"
    SCISSOR = "scissor"
    VARIABLE = "variable"


@dataclass
class TimeIndex:
    """Index into a time series.

    Used to specify time. (Not to be confused with time step.)

    :ivar index: The index of the time in the time series.
    :ivar time_series:
    """

    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    time_series: Optional[str] = field(
        default=None,
        metadata={
            "name": "TimeSeries",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class TimeInterval:
    """Geological time during which a geological event (e.g., deposition, erosion,
    fracturation, faulting, intrusion) occurred.

    BUSINESS RULE: All rock features that are present in the global chronostratigraphic column feature must have a time interval.
    """

    chrono_bottom: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChronoBottom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    chrono_top: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChronoTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


class TimeSetKind(Enum):
    """
    Indicates that the collection of properties shares this time relationship, if
    any.

    :cvar SINGLE_TIME: Indicates that the collection contains only
        property values associated with a single time index, i.e., time
        identity can be ascertained from the time index itself, without
        knowledge of the time.
    :cvar EQUIVALENT_TIMES: Indicates that the collection of properties
        is at equivalent times, e.g., a 4D seismic data set and a
        reservoir simulation model at comparable times. For a more
        specific relationship, select single time.
    :cvar NOT_A_TIME_SET: Indicates that the property collection is not
        related by time.
    """

    SINGLE_TIME = "single time"
    EQUIVALENT_TIMES = "equivalent times"
    NOT_A_TIME_SET = "not a time set"


@dataclass
class Timestamp:
    """
    Time.

    :ivar date_time: A date which can be represented according to the
        W3CDTF format.
    :ivar year_offset: Indicates that the dateTime attribute must be
        translated according to this value.
    """

    date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DateTime",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    year_offset: Optional[int] = field(
        default=None,
        metadata={
            "name": "YearOffset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class WellboreTrajectoryParentIntersection:
    """
    For a wellbore trajectory in a multi-lateral well, indicates the MD of the
    kickoff point where the trajectory begins and the corresponding MD of the
    parent trajectory.
    """

    kickoff_md: Optional[float] = field(
        default=None,
        metadata={
            "name": "KickoffMd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_md: Optional[float] = field(
        default=None,
        metadata={
            "name": "ParentMd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_trajectory: Optional[str] = field(
        default=None,
        metadata={
            "name": "ParentTrajectory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class WitsmlWellboreReference:
    """
    Reference to the WITSML wellbore that this wellbore feature is based on.
    """

    witsml_well: Optional[str] = field(
        default=None,
        metadata={
            "name": "WitsmlWell",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    witsml_wellbore: Optional[str] = field(
        default=None,
        metadata={
            "name": "WitsmlWellbore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class AbstractActivityParameter:
    """
    General parameter value used in one instance of activity.

    :ivar title: Name of the parameter, used to identify it in the
        activity. Must have an equivalent in the activity descriptor
        parameters.
    :ivar index: When parameter is an array, used to indicate the index
        in the array
    :ivar selection: Textual description about how this parameter was
        selected.
    :ivar key:
    """

    title: Optional[str] = field(
        default=None,
        metadata={
            "name": "Title",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    selection: Optional[str] = field(
        default=None,
        metadata={
            "name": "Selection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    key: List[AbstractParameterKey] = field(
        default_factory=list,
        metadata={
            "name": "Key",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class AbstractBooleanArray(AbstractValueArray):
    """Generic representation of an array of Boolean values.

    Each derived element provides a specialized implementation to allow
    specific optimization of the representation.
    """


@dataclass
class AbstractContactInterpretationPart:
    """The parent class of an atomic, linear, or surface geologic contact
    description.

    When the contact is between two surface representations (e.g.,
    fault/fault, horizon/fault, horizon/horizon), then the contact is a
    line. When the contact is between two volume representations
    (stratigraphic unit/stratigraphic unit), then the contact is a
    surface. A contact interpretation can be associated with other
    contact interpretations in an organization interpretation. To define
    a contact representation, you must first define a contact
    interpretation.

    :ivar contact_relationship:
    :ivar index: contact index
    :ivar part_of:
    """

    contact_relationship: Optional[ContactRelationship] = field(
        default=None,
        metadata={
            "name": "ContactRelationship",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    part_of: Optional[str] = field(
        default=None,
        metadata={
            "name": "PartOf",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class AbstractDoubleArray(AbstractValueArray):
    """Generic representation of an array of double values.

    Each derived element provides specialized implementation to allow
    specific optimization of the representation.
    """


@dataclass
class AbstractGeometry:
    """
    The base class for all geometric values, which is always associated with a
    representation.
    """

    time_index: Optional[TimeIndex] = field(
        default=None,
        metadata={
            "name": "TimeIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    local_crs: Optional[str] = field(
        default=None,
        metadata={
            "name": "LocalCrs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class AbstractIntegerArray(AbstractValueArray):
    """Generic representation of an array of integer values.

    Each derived element provides specialized implementation to allow
    specific optimization of the representation.
    """


@dataclass
class AbstractResqmlDataObject:
    """The parent class for all top-level elements in RESQML.

    Inherits from AbstractCitedDataObject in the commonV2 package of the
    model.
    """

    extra_metadata: List[NameValuePair] = field(
        default_factory=list,
        metadata={
            "name": "ExtraMetadata",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class AdditionalGridPoints:
    """
    Geometry given by means of points attached to additional elements of a grid.

    :ivar representation_patch_index: Used to remove ambiguity in
        geometry attachment, if the attachment element is not
        sufficient. Usually required for subnodes and for the general
        purpose grid, but not otherwise.
    :ivar attachment:
    :ivar points:
    """

    representation_patch_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "RepresentationPatchIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    attachment: Optional[GridGeometryAttachment] = field(
        default=None,
        metadata={
            "name": "Attachment",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    points: Optional[AbstractPoint3DArray] = field(
        default=None,
        metadata={
            "name": "Points",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ContactElementReference:
    """A reference to either a geologic feature interpretation or a frontier
    feature.

    BUSINESS RULE: The ContentType of the corresponding data-object reference must be a geological feature interpretation or a frontier feature.
    """

    qualifier: Optional[ContactSide] = field(
        default=None,
        metadata={
            "name": "Qualifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    secondary_qualifier: Optional[ContactMode] = field(
        default=None,
        metadata={
            "name": "SecondaryQualifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ContactRepresentationReference(AbstractContactRepresentationPart):
    """
    Used when the contact already exists as a top level element representation.
    """

    representation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Representation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class FaultThrow:
    """
    Identifies the characteristic of the throw of a fault interpretation.
    """

    throw: List[ThrowKind] = field(
        default_factory=list,
        metadata={
            "name": "Throw",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )
    has_occured_during: Optional[TimeInterval] = field(
        default=None,
        metadata={
            "name": "HasOccuredDuring",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class LocalPropertyKind(AbstractPropertyKind):
    local_property_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "LocalPropertyKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjectParameterKey(AbstractParameterKey):
    """
    :ivar data_object: Is actually a reference and not a containment
        relationship.
    """

    data_object: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataObject",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class Patch1D(Patch):
    """
    A patch with a single 1D index count.

    :ivar count: Number of items in the patch.
    """

    class Meta:
        name = "Patch1d"

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class PatchOfPoints:
    """A patch of points.

    In RESQML, a patch is a set or range of one kind of topological
    elements used to define part of a data-object, such as grids or
    structural data-objects.

    :ivar representation_patch_index: Optional patch index used to
        attach properties to a specific patch of the indexable elements.
    :ivar points: Geometric points (or vectors) to be attached to the
        specified indexable elements.
    """

    representation_patch_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "RepresentationPatchIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    points: Optional[AbstractPoint3DArray] = field(
        default=None,
        metadata={
            "name": "Points",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class PatchOfValues:
    """
    A patch of values.

    :ivar representation_patch_index: Patch index used to attach
        properties to a specific patch of the indexable elements.
    :ivar values: Values to be attached to the indexable elements.
    """

    representation_patch_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "RepresentationPatchIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    values: Optional[AbstractValueArray] = field(
        default=None,
        metadata={
            "name": "Values",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class Point2DHdf5Array(AbstractPoint3DArray):
    """An array of explicit XY points stored as two coordinates in an HDF5 dataset.

    If needed, the implied Z coordinate is uniformly 0.

    :ivar coordinates: Reference to an HDF5 2D dataset of XY points. The
        2 coordinates are stored sequentially in HDF5, i.e., a multi-
        dimensional array of points is stored as a 2 x ... HDF5 array.
    """

    class Meta:
        name = "Point2dHdf5Array"

    coordinates: Optional[str] = field(
        default=None,
        metadata={
            "name": "Coordinates",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class Point3DHdf5Array(AbstractPoint3DArray):
    """
    N array of explicit XYZ points stored as three coordinates in an HDF5 dataset.

    :ivar coordinates: Reference to an HDF5 3D dataset of XYZ points.
        The 3 coordinates are stored sequentially in HDF5, i.e., a
        multi-dimensional array of points is stored as a 3 x ... HDF5
        array.
    """

    class Meta:
        name = "Point3dHdf5Array"

    coordinates: Optional[str] = field(
        default=None,
        metadata={
            "name": "Coordinates",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class PropertyKindFacet:
    """Qualifiers for property values, which allows users to semantically
    specialize a property without creating a new property kind.

    For the list of enumerations, see Facet.

    :ivar facet: Facet of the property kind (see the enumeration)
    :ivar value: Property facet value.
    """

    facet: Optional[Facet] = field(
        default=None,
        metadata={
            "name": "Facet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class PropertyValuesPatch:
    patch_uid: Optional[int] = field(
        default=None,
        metadata={
            "name": "patchUid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    values: Optional[AbstractValueArray] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class StandardPropertyKind(AbstractPropertyKind):
    """A standard property kind is defined in the Energistics catalog.

    It has an unique name.
    """

    kind: Optional[ResqmlPropertyKind] = field(
        default=None,
        metadata={
            "name": "Kind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class StringHdf5Array(AbstractValueArray):
    """Used to store explicit string values, i.e., values that are not double,
    boolean or integers.

    The datatype of the values will be identified by means of the HDF5
    API.

    :ivar values: Reference to HDF5 array of integer or double
    """

    values: Optional[str] = field(
        default=None,
        metadata={
            "name": "Values",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class SubnodePatch(Patch):
    """Each patch of subnodes is defined independently of the others.

    Number of nodes per object is determined by the subnode kind.

    :ivar subnode_node_object:
    :ivar node_weights_per_subnode: Node weights for each subnode. Count
        of nodes per subnode is known for each specific subnode
        construction. Data order consists of all the nodes for each
        subnode in turn. For example, if uniform and stored as a multi-
        dimensional array, the node index cycles first. BUSINESS RULE:
        Weights must be non-negative. BUSINESS RULE: Length of array
        must be consistent with the sum of nodeCount x subnodeCount per
        object, e.g., for 3 subnodes per edge (uniform), there are 6
        weights.
    """

    subnode_node_object: Optional[SubnodeNodeObject] = field(
        default=None,
        metadata={
            "name": "SubnodeNodeObject",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    node_weights_per_subnode: Optional[AbstractValueArray] = field(
        default=None,
        metadata={
            "name": "NodeWeightsPerSubnode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ThreePoint3D:
    """
    List of three 3D points.
    """

    class Meta:
        name = "ThreePoint3d"

    point3d: List[Point3D] = field(
        default_factory=list,
        metadata={
            "name": "Point3d",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 3,
            "max_occurs": 3,
        },
    )


@dataclass
class TimeIndexParameterKey(AbstractParameterKey):
    time_index: Optional[TimeIndex] = field(
        default=None,
        metadata={
            "name": "TimeIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class TimeSeriesParentage:
    """
    Indicates that a time series has the associated time series as a parent, i.e.,
    that the series continues from the parent time series.

    :ivar has_overlap: Used to indicate that a time series overlaps with
        its parent time series, e.g., as may be done for simulation
        studies, where the end state of one calculation is the initial
        state of the next.
    :ivar parent_time_index:
    """

    has_overlap: Optional[bool] = field(
        default=None,
        metadata={
            "name": "HasOverlap",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_time_index: Optional[TimeIndex] = field(
        default=None,
        metadata={
            "name": "ParentTimeIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class VolumeShell:
    """
    The shell or envelope of a structural, stratigraphic, or fluid unit.
    """

    shell_uid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ShellUid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    macro_faces: List[OrientedMacroFace] = field(
        default_factory=list,
        metadata={
            "name": "MacroFaces",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class AbstractFeature(AbstractResqmlDataObject):
    """Something that has physical existence at some point during the exploration,
    development, production or abandonment of a reservoir.

    For example: It can be a boundary, a rock volume, a basin area, but also extends to a drilled well, a drilling rig, an injected or produced fluid, or a 2D, 3D, or 4D seismic survey.
    Features are divided into these categories: geologic or technical.
    """


@dataclass
class AbstractFeatureInterpretation(AbstractResqmlDataObject):
    """
    The main class that contains all of the other feature interpretations included
    in this interpreted model.
    """

    domain: Optional[Domain] = field(
        default=None,
        metadata={
            "name": "Domain",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    interpreted_feature: Optional[str] = field(
        default=None,
        metadata={
            "name": "InterpretedFeature",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    has_occured_during: Optional[TimeInterval] = field(
        default=None,
        metadata={
            "name": "HasOccuredDuring",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class AbstractLocal3DCrs(AbstractResqmlDataObject):
    """Defines a local 2D+1D coordinate reference system, by translation and
    rotation, whose origin is located at the (X,Y,Z) Offset from the Projected and
    Vertical 2D+1D CRS. The units of measure in XY follow the Projected Crs. The
    units of measure of the third coordinate is determined in the depth or concrete
    type. ArealRotation is a plane angle.

    Defines a local 3D CRS is subject to the following restrictions:
    - The projected 2d CRS must have orthogonal axes
    - The vertical 1d CRS must be chosen so that it is orthogonal to the plane defined by the projected 2d CRS
    As a consequence of the definition:
    - The local CRS forms a Cartesian system of axes.
    - The local areal axes are in the plane of the projected system.
    - The local areal axes are orthogonal to each other.
    This 3D system is semantically equivalent to a compound CRS composed of a local 2D areal system and a local 1D vertical system.
    The labels associated with the axes on this local system are X, Y, Z or X, Y, T.
    The relative orientation of the local Y axis with respect to the local X axis is identical to that of the global axes.

    :ivar yoffset: The Y offset of the origin of the local areal axes
        relative to the projected CRS origin. The value MUST represent
        the second axis of the coordinate system. The unit of measure is
        defined by the unit of measure for the projected 2D CRS.
    :ivar zoffset: The Z offset of the origin of the local vertical axis
        relative to the vertical CRS origin. According to CRS type
        (depth or time) it corresponds to the depth or time datum The
        value MUST represent the third axis of the coordinate system.
        The unit of measure is defined by the unit of measure for the
        vertical CRS.
    :ivar areal_rotation: The rotation of the local Y axis relative to
        the projected Y axis. - A positive value indicates a clockwise
        rotation from the projected Y axis. - A negative value indicates
        a counter-clockwise rotation form the projected Y axis.
    :ivar projected_axis_order: Defines the coordinate system axis order
        of the global projected CRS when the projected CRS is an unknown
        CRS, else it must be correspond to the axis order of the
        projected  CRS.
    :ivar projected_uom: Unit of measure of the associated Projected
        CRS. When the projected CRS is not unknown, it must be the same
        than the unit defined by the Projected CRS.
    :ivar vertical_uom: Unit of measure of the associated Vertical CRS.
        When the vertical CRS is not unknown, it must be the same than
        the unit defined by the Vertical CRS.
    :ivar xoffset: The X location of the origin of the local areal axes
        relative to the projected CRS origin. The value MUST represent
        the first axis of the coordinate system. The unit of measure is
        defined by the unit of measure for the projected 2D CRS.
    :ivar zincreasing_downward: Indicates that Z values correspond to
        depth values and are increasing downward, as opposite to
        elevation values increasing upward. When the vertical CRS is not
        an unknown, it must correspond to the axis orientation of the
        vertical CRS.
    :ivar vertical_crs:
    :ivar projected_crs:
    """

    class Meta:
        name = "AbstractLocal3dCrs"

    yoffset: Optional[float] = field(
        default=None,
        metadata={
            "name": "YOffset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    zoffset: Optional[float] = field(
        default=None,
        metadata={
            "name": "ZOffset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    areal_rotation: Optional[str] = field(
        default=None,
        metadata={
            "name": "ArealRotation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    projected_axis_order: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProjectedAxisOrder",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    projected_uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProjectedUom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    vertical_uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "VerticalUom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    xoffset: Optional[float] = field(
        default=None,
        metadata={
            "name": "XOffset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    zincreasing_downward: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ZIncreasingDownward",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    vertical_crs: Optional[str] = field(
        default=None,
        metadata={
            "name": "VerticalCrs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    projected_crs: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProjectedCrs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class AbstractParametricLineGeometry(AbstractGeometry):
    """
    The abstract class for defining a single parametric line.
    """


@dataclass
class AbstractPlaneGeometry(AbstractGeometry):
    """
    The abstract class for all geometric values defined by planes.
    """


@dataclass
class AbstractProperty(AbstractResqmlDataObject):
    """Base class for storing all property values on representations, except
    current geometry location.

    Values attached to a given element can be either a scalar or a
    vector. The size of the vector is constant on all elements, and it
    is assumed that all elements of the vector have identical property
    types and share the same unit of measure.

    :ivar count: Number of elements in a 1D list of properties. When
        used in a multi-dimensional array, count is always the fastest.
    :ivar indexable_element:
    :ivar realization_index: Optional element indicating the realization
        index (metadata). Used if the property is the result of a multi-
        realization process.
    :ivar time_step: Indicates that the property is the output of a
        specific time step from a flow simulator. Time step is metadata
        that makes sense in the context of a specific simulation run,
        and should not be confused with the time index.
    :ivar time_index:
    :ivar supporting_representation:
    :ivar local_crs:
    :ivar property_kind:
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    indexable_element: Optional[IndexableElements] = field(
        default=None,
        metadata={
            "name": "IndexableElement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    realization_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "RealizationIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    time_step: Optional[int] = field(
        default=None,
        metadata={
            "name": "TimeStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    time_index: Optional[TimeIndex] = field(
        default=None,
        metadata={
            "name": "TimeIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    supporting_representation: Optional[str] = field(
        default=None,
        metadata={
            "name": "SupportingRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    local_crs: Optional[str] = field(
        default=None,
        metadata={
            "name": "LocalCrs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    property_kind: Optional[AbstractPropertyKind] = field(
        default=None,
        metadata={
            "name": "PropertyKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class AbstractPropertyLookup(AbstractResqmlDataObject):
    """Generic representation of a property lookup table.

    Each derived element provides specific lookup methods for different
    data types.
    """


@dataclass
class AbstractRepresentation(AbstractResqmlDataObject):
    """The parent class of all specialized digital descriptions, which may provide
    a representation of a feature interpretation or a technical feature. It may be
    either of these:

    - based on a topology and contains the geometry of this digital description.
    - based on the topology or the geometry of another representation.
    Not all representations require a defined geometry. For example, it is not required for block-centered grids or wellbore frames. For representations without geometry, a software writer may provide null (NaN) values in the local 3D CRS, which is mandatory.
    TimeIndex is provided to describe time-dependent geometry.
    """

    represented_interpretation: Optional[str] = field(
        default=None,
        metadata={
            "name": "RepresentedInterpretation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class Activation:
    """Used to activate and deactivate the referencing object at the times
    indicated.

    If the activation object is not present, then the referencing object
    is always active. If the activation object is present, then the
    referencing object is not active until activated.

    :ivar activation_toggle_indices: The index in the time series at
        which the state of the referencing object is changed. Toggle
        will change state from inactive to active, or toggle will change
        state from active to inactive.
    :ivar time_series:
    """

    activation_toggle_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ActivationToggleIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    time_series: Optional[str] = field(
        default=None,
        metadata={
            "name": "TimeSeries",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class BinaryContactInterpretationPart(AbstractContactInterpretationPart):
    """The main class for data describing an opinion of the contact between two
    geologic feature interpretations.

    A contact interpretation between two surface geological boundaries
    is usually a line. A contact interpretation between two volumes
    (rock feature interpretation) is usually a surface. This class
    allows you to build a formal sentence—in the pattern of subject-
    verb-direct object—which is used to describe the construction of a
    node, line, or surface contact. It is also possible to attach a
    primary and a secondary qualifier to the subject and to the direct
    object. For example, one contact interpretation can be described by
    a sentence such as: The interpreted fault named F1 interp on its
    hanging wall side splits the interpreted horizon named H1 Interp on
    both its sides. Subject = F1 Interp, with qualifier "hanging wall
    side" Verb = splits Direct Object = H1 Interp, with qualifier "on
    both sides"

    :ivar direct_object: Data-object reference (by UUID link) to a
        geologic feature interpretation, which is the direct object of
        the sentence that defines how the contact was constructed.
    :ivar verb:
    :ivar subject: Data-object reference (by UUID link) to a geologic
        feature interpretation, which is the subject of the sentence
        that defines how the contact was constructed.
    """

    direct_object: Optional[ContactElementReference] = field(
        default=None,
        metadata={
            "name": "DirectObject",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    verb: Optional[ContactVerb] = field(
        default=None,
        metadata={
            "name": "Verb",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    subject: Optional[ContactElementReference] = field(
        default=None,
        metadata={
            "name": "Subject",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class BooleanArrayFromDiscretePropertyArray(AbstractBooleanArray):
    """An array of Boolean values that is explicitly defined by indicating which
    indices in the array are either true or false.

    This class is used to represent very sparse true or false data,
    based on a discrete property.

    :ivar value: Integer to match for the value to be considered true
    :ivar property:
    """

    value: Optional[int] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    property: Optional[str] = field(
        default=None,
        metadata={
            "name": "Property",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class BooleanArrayFromIndexArray(AbstractBooleanArray):
    """An array of Boolean values defined by specifying explicitly which indices in
    the array are either true or false.

    This class is used to represent very sparse true or false data.

    :ivar count: Total number of Boolean elements in the array. This
        number is different from the number of indices used to represent
        the array.
    :ivar indices: Array of integer indices. BUSINESS RULE: Must be non-
        negative.
    :ivar index_is_true: Indicates whether the specified elements are
        true or false.
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "Indices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    index_is_true: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IndexIsTrue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class BooleanConstantArray(AbstractBooleanArray):
    """Represents an array of Boolean values where all values are identical.

    This an optimization for which an array of explicit Boolean values
    is not required.

    :ivar value: Value inside all the elements of the array.
    :ivar count: Size of the array.
    """

    value: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class BooleanHdf5Array(AbstractBooleanArray):
    """
    Array of boolean values provided explicitly by an HDF5 dataset.

    :ivar values: Reference to an HDF5 array of values.
    """

    values: Optional[str] = field(
        default=None,
        metadata={
            "name": "Values",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class CellFluidPhaseUnits:
    """
    A mapping from cells to fluid phase unit interpretation to describe the initial
    hydrostatic fluid column.

    :ivar phase_unit_indices: Index of the phase unit kind within a
        given fluid phase organization for each cell. Follows the
        indexing defined by the PhaseUnit enumeration. When applied to
        the wellbore frame representation, the indexing is identical to
        the number of intervals. Use null (-1) if no fluid phase is
        present, e.g., within the seal. BUSINESS RULE: Array length is
        equal to the number of cells in the representation (grid,
        wellbore frame or blocked well).
    :ivar fluid_organization:
    """

    phase_unit_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "PhaseUnitIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    fluid_organization: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidOrganization",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class CellStratigraphicUnits:
    """
    A mapping from cell to stratigraphic unit interpretation for a representations
    (grids or blocked wells).

    :ivar unit_indices: Index of the stratigraphic unit of a given
        stratigraphic column for each cell. Use null (-1) if no
        stratigraphic column, e.g., within salt BUSINESS RULE: Array
        length is the number of cells in the grid or the blocked well
    :ivar stratigraphic_organization:
    """

    unit_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "UnitIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    stratigraphic_organization: Optional[str] = field(
        default=None,
        metadata={
            "name": "StratigraphicOrganization",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ColumnLayerSplitColumnEdges:
    """Column edges are needed to construct the indices for the cell faces for
    column layer grids.

    For split column layer grids, the column edge indices must be
    defined explicitly. Column edges are not required to describe the
    lowest order grid geometry, but may be required for higher order
    geometries or properties.

    :ivar count: Number of split column edges in this grid. Must be
        positive.
    :ivar parent_column_edge_indices: Parent unsplit column edge index
        for each of the split column edges. Used to implicitly define
        split face indexing.
    :ivar column_per_split_column_edge: Column index for each of the
        split column edges. Used to implicitly define column and cell
        faces. List-of-lists construction not required since each split
        column edge must be in a single column.
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_column_edge_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ParentColumnEdgeIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    column_per_split_column_edge: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ColumnPerSplitColumnEdge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ColumnSubnodePatch(SubnodePatch):
    """
    Use this subnode construction if the number of subnodes per object varies from
    column to column, but does not vary from layer to layer.

    :ivar subnode_count_per_object: Number of subnodes per object, with
        a different number in each column of the grid.
    """

    subnode_count_per_object: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "SubnodeCountPerObject",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ContactIdentity:
    """Indicates identity between two (or more) contacts.

    For possible types of identities, see IdentityKind.

    :ivar identity_kind:
    :ivar list_of_contact_representations: The contact representations
        that share common identity as specified by their indices
    :ivar list_of_identical_nodes: Indicates which nodes (identified by
        their common index in all contact representations) of the
        contact representations are identical. If this list is not
        present, then it indicates that all nodes in each representation
        are identical, on an element by element level.
    """

    identity_kind: Optional[IdentityKind] = field(
        default=None,
        metadata={
            "name": "IdentityKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    list_of_contact_representations: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ListOfContactRepresentations",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    list_of_identical_nodes: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ListOfIdenticalNodes",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ContactPatch(Patch1D):
    """
    A subset of topological elements of an existing contact representation part
    (sealed or non-sealed contact).

    :ivar representation_index: Identifies a representation by its
        index, in the list of representations contained in the
        organization.
    :ivar supporting_representation_nodes: The ordered list of nodes
        (identified by their global index) in the supporting
        representation, which constitutes the contact patch.
    """

    representation_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "RepresentationIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    supporting_representation_nodes: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "SupportingRepresentationNodes",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class DataObjectParameter(AbstractActivityParameter):
    """
    Parameter referencing to a top level object.

    :ivar data_object: Is actually a reference and not a containment
        relationship.
    """

    data_object: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataObject",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class DoubleConstantArray(AbstractDoubleArray):
    """Represents an array of double values where all values are identical.

    This an optimization for which an array of explicit double values is
    not required.

    :ivar value: Values inside all the elements of the array.
    :ivar count: Size of the array.
    """

    value: Optional[float] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class DoubleHdf5Array(AbstractDoubleArray):
    """An array of double values provided explicitly by an HDF5 dataset.

    By convention, the null value is NaN.

    :ivar values: Reference to an HDF5 array of doubles.
    """

    values: Optional[str] = field(
        default=None,
        metadata={
            "name": "Values",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class EdgePatch(Patch1D):
    """Describes edges that are not linked to any other edge.

    Because edges do not have indices, a consecutive pair of nodes is
    used to identify each edge. The split edges dataset is a set of
    nodes (2 nodes per edge). Each patch has a set of 2 nodes.

    :ivar split_edges: An array of split edges to define patches. It
        points to an HDF5 dataset, which must be a 2D array of non-
        negative integers with dimensions 2 x numSplitEdges. integers
        with dimensions {2, numSplitEdges}
    """

    split_edges: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "SplitEdges",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class Edges:
    """Unstructured cell grids require the definition of edges if the subnode
    attachment is of kind edges.

    Use Case: Finite elements, especially for higher order geometry.
    BUSINESS RULE: Edges must be defined for unstructured cell grids if subnode nodes of kind edges are used.

    :ivar count: Number of edges. Must be positive.
    :ivar nodes_per_edge: Defines a list of 2 nodes per edge. Count = 2
        x EdgeCount
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    nodes_per_edge: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "NodesPerEdge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ElementIdentity:
    """Indicates the nature of the relationship between 2 or more representations,
    specifically if they are partially or totally identical.

    For possible types of relationships, see IdentityKind. Commonly used
    to identify contacts between representations in model descriptions.
    May also be used to relate the components of a grid (e.g., pillars)
    to those of a structural framework.

    :ivar element_indices: Indicates which elements are identical based
        on their indices in the (sub)representation. If not given, then
        the selected indexable elements of each of the selected
        representations are identical at the element by element level.
        If not given, then all elements are specified to be identical.
        BUSINESS RULE: Number of identical elements must equal
        identicalElementCount for each representation.
    :ivar identity_kind:
    :ivar indexable_element:
    :ivar representation:
    :ivar from_time_index:
    :ivar to_time_index:
    """

    element_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ElementIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    identity_kind: Optional[IdentityKind] = field(
        default=None,
        metadata={
            "name": "IdentityKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    indexable_element: Optional[IndexableElements] = field(
        default=None,
        metadata={
            "name": "IndexableElement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    representation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Representation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    from_time_index: Optional[TimeIndex] = field(
        default=None,
        metadata={
            "name": "FromTimeIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    to_time_index: Optional[TimeIndex] = field(
        default=None,
        metadata={
            "name": "ToTimeIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ElementIndices:
    """
    Index into the indexable elements selected.
    """

    indexable_element: Optional[IndexableElements] = field(
        default=None,
        metadata={
            "name": "IndexableElement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "Indices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class FloatingPointQuantityParameter(AbstractActivityParameter):
    """
    Parameter containing a double value.

    :ivar value: Double value
    :ivar uom: Unit of measure associated with the value
    """

    value: Optional[float] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    uom: Optional[ResqmlUom] = field(
        default=None,
        metadata={
            "name": "Uom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class IntegerArrayFromBooleanMaskArray(AbstractIntegerArray):
    """
    One-dimensional array of integer values obtained from the true elements of the
    Boolean mask.

    :ivar total_index_count: Total number of integer elements in the
        array. This number is different from the number of Boolean mask
        values used to represent the array.
    :ivar mask: Boolean mask. A true element indicates that the index is
        included on the list of integer values.
    """

    total_index_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "TotalIndexCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    mask: Optional[AbstractBooleanArray] = field(
        default=None,
        metadata={
            "name": "Mask",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class IntegerConstantArray(AbstractIntegerArray):
    """Represents an array of integer values where all values are identical.

    This an optimization for which an array of explicit integer values
    is not required.

    :ivar value: Values inside all the elements of the array.
    :ivar count: Size of the array.
    """

    value: Optional[int] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class IntegerHdf5Array(AbstractIntegerArray):
    """Array of integer values provided explicitly by a HDF5 dataset.

    The null value is explicitly provided. WHERE IS THE NULL VALUE
    SPECIFIED?

    :ivar null_value:
    :ivar values: Reference to an HDF5 array of integers or doubles.
    """

    null_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "NullValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    values: Optional[str] = field(
        default=None,
        metadata={
            "name": "Values",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class IntegerQuantityParameter(AbstractActivityParameter):
    """
    Parameter containing an integer value.

    :ivar value: Integer value
    """

    value: Optional[int] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class IntegerRangeArray(AbstractIntegerArray):
    """Defines an array as a range of integers.

    The range is defined by an initial value and a count defining the
    size of the range.

    :ivar count: Size of the array.
    :ivar value: Start value for the range. End value is start+count-1.
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    value: Optional[int] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class IntervalGridCells:
    """Specifies the (Grid,Cell) intersection of each Interval of the
    representation, if any.

    The information allows you to locate, on one or several grids, the
    intersection of volume (cells) and surface (faces) elements with a
    wellbore trajectory (existing or planned), streamline trajectories,
    or any polyline set.

    :ivar cell_count: The number of non-null entries in the grid indices
        array.
    :ivar grid_indices: Size of array = IntervalCount. Null values of -1
        signify that that interval is not within a grid. BUSINESS RULE:
        The cell count must equal the number of non-null entries in this
        array.
    :ivar cell_indices: The cell index for each interval of a
        representation. The grid index is specified by grid index array,
        to give the (Grid,Cell) index pair. BUSINESS RULE: Array length
        must equal cell count.
    :ivar local_face_pair_per_cell_indices: For each cell, these are the
        entry and exit intersection faces of the trajectory in the cell.
        Use null (-1) for missing intersections, e.g., when a trajectory
        originates or terminates within a cell. The local face-per-cell
        index is used because a global face index need not have been
        defined on the grid. BUSINESS RULE: The array dimensions must
        equal 2 x CellCount.
    :ivar grids:
    """

    cell_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "CellCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    grid_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "GridIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    cell_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "CellIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    local_face_pair_per_cell_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "LocalFacePairPerCellIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    grids: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Grids",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class IntervalStratigraphicUnits:
    """
    A mapping from intervals to stratigraphic units for representations (grids or
    wellbore frames).

    :ivar unit_indices: Index of the stratigraphic unit per interval, of
        a given stratigraphic column. Notes: 1.) For grids, intervals =
        layers + K gaps. 2.) If there is no stratigraphic column, e.g.,
        within salt, use null (-1) BUSINESS RULE: Array length must
        equal the number of INTERVALS.
    :ivar stratigraphic_organization:
    """

    unit_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "UnitIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    stratigraphic_organization: Optional[str] = field(
        default=None,
        metadata={
            "name": "StratigraphicOrganization",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class Intervals:
    """Refinement and/or Coarsening per interval.

    If there is a 1:1 correspondence between the parent and child cells,
    then this object is not needed.

    :ivar interval_count: The number of intervals in the regrid
        description. Must be positive.
    :ivar parent_count_per_interval: The number of parent cells in each
        interval. BUSINESS RULES: 1.) The array length must be equal to
        intervalCount. 2.) For the given parentIndex, the total count of
        parent cells should not extend beyond the boundary of the parent
        grid.
    :ivar child_count_per_interval: The number of child cells in each
        interval. If the child grid type is not commensurate with the
        parent type, then this attribute is ignored by a reader, and its
        value should be set to null (-1). For example, for a parent IJK
        grid with a child unstructured column layer grid, then the child
        count is non-null for a K regrid, but null for an I or J regrid.
        BUSINESS RULES: 1.) The array length must be equal to
        intervalCount. 2.) If the child grid type is commensurate with
        the parent grid, then the sum of values over all intervals must
        be equal to the corresponding child grid dimension.
    :ivar child_cell_weights: Weights that are proportional to the
        relative sizes of child cells within each interval. The weights
        need not be normalized.
    """

    interval_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "IntervalCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_count_per_interval: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ParentCountPerInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    child_count_per_interval: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ChildCountPerInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    child_cell_weights: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "ChildCellWeights",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class Kgaps:
    """Optional object used to indicate that there are global gaps between layers
    in the grid.

    With K gaps, the bottom of one layer need not be continuous with the
    top of the next layer, so the resulting number of intervals is
    greater than the number of layers.

    :ivar count: Number of gaps between layers. Must be positive. Number
        of INTERVALS = gapCount + NK.
    :ivar gap_after_layer: Boolean array of length NK-1. TRUE if there
        is a gap after the corresponding layer. NKL = NK + gapCount + 1
        BUSINESS RULE: gapCount must be consistent with the number of
        gaps specified by the gapAfterLayer array.
    """

    class Meta:
        name = "KGaps"

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    gap_after_layer: Optional[AbstractBooleanArray] = field(
        default=None,
        metadata={
            "name": "GapAfterLayer",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class MultipleContactInterpretationPart(AbstractContactInterpretationPart):
    """Describes multiple interface contacts of geologic feature interpretations
    (compared to a binary contact).

    A composition of several contact interpretations.

    :ivar with_value: Indicates a list of binary contacts (by their
        UUIDs) that participate in this multiple contact.
    """

    with_value: List[int] = field(
        default_factory=list,
        metadata={
            "name": "With",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class OverlapVolume:
    """Optional parent-child cell overlap volume information.

    If not present, then the CellOverlap data-object lists the overlaps,
    but with no additional information.

    :ivar volume_uom: Units of measure for the overlapVolume.
    :ivar overlap_volumes: Parent-child cell volume overlap. BUSINESS
        RULE: Length of array must equal the cell overlap count.
    """

    volume_uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "VolumeUom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    overlap_volumes: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "OverlapVolumes",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ParameterTemplate:
    """
    Description of one parameter that participate in one type of activity.

    :ivar key_constraint: Allows you to indicate that, in the same
        activity, this parameter template must be associated to another
        parameter template identified by its title.
    :ivar is_input: Indicates if the parameter is an input of the
        activity. If the parameter is a data object and is also an
        output of the activity, it is strongly advised to use two
        parameters : one for input and one for output. The reason is to
        be able to give two different versions strings for the input and
        output dataobject which has got obviously the same UUID.
    :ivar allowed_kind: If no allowed type is given, then all kind of
        datatypes is allowed.
    :ivar is_output: Indicates if the parameter is an output of the
        activity. If the parameter is a data object and is also an input
        of the activity, it is strongly advised to use two parameters :
        one for input and one for output. The reason is to be able to
        give two different versions strings for the input and output
        dataobject which has got obviously the same UUID.
    :ivar title: Name of the parameter in the activity. Key to identify
        parameter.
    :ivar data_object_content_type: When parameter is limited to data
        object of given types, describe the allowed types. Used only
        when ParameterType is dataObject
    :ivar max_occurs: Maximum number of parameters of this type allowed
        in the activity. -1 means "infinite".
    :ivar min_occurs: Minimum number of parameters of this type required
        by the activity. -1 means "infinite".
    :ivar constraint: Textual description of additional constraint
        associated with the parameter. (note that it will be better to
        have a formal description of the constraint)
    :ivar default_value:
    """

    key_constraint: List[str] = field(
        default_factory=list,
        metadata={
            "name": "KeyConstraint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    is_input: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsInput",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    allowed_kind: List[ParameterKind] = field(
        default_factory=list,
        metadata={
            "name": "AllowedKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    is_output: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsOutput",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "name": "Title",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    data_object_content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataObjectContentType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    max_occurs: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxOccurs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    min_occurs: Optional[int] = field(
        default=None,
        metadata={
            "name": "MinOccurs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    constraint: Optional[str] = field(
        default=None,
        metadata={
            "name": "Constraint",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    default_value: List[AbstractActivityParameter] = field(
        default_factory=list,
        metadata={
            "name": "DefaultValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ParametricLineIntersections:
    """Used to specify the intersections between parametric lines.

    This information is purely geometric and is not required for the
    evaluation of the parametric point locations on these lines. The
    information required for that purpose is stored in the parametric
    points array.

    :ivar count: Number of parametric line intersections. Must be
        positive.
    :ivar intersection_line_pairs: Intersected line index pair for (line
        1, line 2). Size = 2 x count
    :ivar parameter_value_pairs: Intersected line parameter value pairs
        for (line 1, line 2). Size = 2 x count
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    intersection_line_pairs: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "IntersectionLinePairs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parameter_value_pairs: Optional[AbstractValueArray] = field(
        default=None,
        metadata={
            "name": "ParameterValuePairs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class PatchOfGeometry:
    """
    Indicates which patch of the representation has a new geometry.

    :ivar representation_patch_index: Patch index for the geometry
        attachment, if required
    :ivar geometry:
    """

    representation_patch_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "RepresentationPatchIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    geometry: Optional[AbstractGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class Point3DOffset:
    """Defines the size and sampling in each dimension (direction) of the point 3D
    lattice array.

    Sampling can be uniform or irregular.

    :ivar offset: The direction of the axis of this lattice dimension.
        This is a relative offset vector instead of an absolute 3D
        point.
    :ivar spacing: A lattice of N offset points is described by a
        spacing array of size N-1. The offset between points is given by
        the spacing value multiplied by the offset vector. For example,
        the first offset is 0. The second offset is the first spacing *
        offset. The second offset is (first spacing + second spacing) *
        offset, etc.
    """

    class Meta:
        name = "Point3dOffset"

    offset: Optional[Point3D] = field(
        default=None,
        metadata={
            "name": "Offset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    spacing: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "Spacing",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class Point3DParametricArray(AbstractPoint3DArray):
    """
    A parametric specification of an array of XYZ points.

    :ivar parameters: A multi-dimensional array of parametric values
        that implicitly specifies an array of XYZ points. The parametric
        values provided in this data-object must be consistent with the
        parametric values specified in the referenced parametric line
        array. When constructing a column-layer grid geometry using
        parametric points, the array indexing follows the dimensionality
        of the coordinate lines x NKL, which is either a 2D or 3D array.
    :ivar parametric_line_indices: An optional array of indices that map
        from the array index to the index of the corresponding
        parametric line. If this information is known from context, then
        this array is not needed. For example, in either of these cases:
        (1) If the mapping from array index to parametric line is 1:1.
        (2) If the mapping has already been specified, as with the
        pillar Index from the column-layer geometry of a grid. For
        example, when constructing a column-layer grid geometry using
        parametric lines, the array indexing follows the dimensionality
        of the coordinate lines.
    :ivar truncated_line_indices: A 2D array of line indices for use
        with intersecting parametric lines. Each record consists of a
        single line index, which indicates the array line that uses this
        truncation information, followed by the parametric line indices
        for each of the points on that line. For a non-truncated line,
        the equivalent record repeats the array line index NKL+1 times.
        Size = (NKL+1) x truncatedLineCount
    :ivar parametric_lines:
    """

    class Meta:
        name = "Point3dParametricArray"

    parameters: Optional[AbstractValueArray] = field(
        default=None,
        metadata={
            "name": "Parameters",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parametric_line_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ParametricLineIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    truncated_line_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "TruncatedLineIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    parametric_lines: Optional[AbstractParametricLineArray] = field(
        default=None,
        metadata={
            "name": "ParametricLines",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class Point3DZvalueArray(AbstractPoint3DArray):
    """An array of points defined by applying a Z value on top of an existing array
    of points, XYZ, where Z is ignored. Used in these cases:

    - in 2D for defining geometry of one patch of a 2D grid representation.
    - for extracting nodal geometry from one grid representation for use in another.

    :ivar supporting_geometry: Geometry defining the X and Y
        coordinates.
    :ivar zvalues: The values for Z coordinates
    """

    class Meta:
        name = "Point3dZValueArray"

    supporting_geometry: Optional[AbstractPoint3DArray] = field(
        default=None,
        metadata={
            "name": "SupportingGeometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    zvalues: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "ZValues",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class PointGeometry(AbstractGeometry):
    """
    The geometry of a set of points defined by their location in the local CRS,
    with optional seismic coordinates.
    """

    points: Optional[AbstractPoint3DArray] = field(
        default=None,
        metadata={
            "name": "Points",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    seismic_coordinates: Optional[AbstractSeismicCoordinates] = field(
        default=None,
        metadata={
            "name": "SeismicCoordinates",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ResqmlJaggedArray:
    """Representation for an array of 1D variable length arrays. The representation
    consists of these two arrays:

    - An aggregation of all the variable length arrays into a single dimensional array.
    - The offsets into the other array, given by the sum of all the previous array lengths, including the current array.

    :ivar elements: 1D array of elements containing the aggregation of
        individual array data.
    :ivar cumulative_length: 1D array of cumulative lengths to the end
        of the current array. This is also equal to the index of the
        next element, i.e., the index in the elements array, for which
        the current variable length array begins.
    """

    elements: Optional[AbstractValueArray] = field(
        default=None,
        metadata={
            "name": "Elements",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    cumulative_length: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "CumulativeLength",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class Seismic2DCoordinates(AbstractSeismicCoordinates):
    """A group of 2D seismic coordinates that stores the 1-to-1 mapping between
    geometry patch coordinates (usually X, Y, Z) and trace or inter-trace positions
    on a seismic line.

    BUSINESS RULE: This patch must reference a geometry patch by its UUID.

    :ivar line_abscissa: The sequence of trace or inter-trace positions
        that correspond to the geometry coordinates. BUSINESS RULE: Both
        sequences must be in the same order.
    :ivar vertical_coordinates: The sequence of vertical sample or
        inter-sample positions that correspond to the geometry
        coordinates. BUSINESS RULE: Sequence must be in the same order
        than previous one.
    """

    class Meta:
        name = "Seismic2dCoordinates"

    line_abscissa: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "LineAbscissa",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    vertical_coordinates: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "VerticalCoordinates",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class Seismic3DCoordinates(AbstractSeismicCoordinates):
    """
    The 1-to-1 mapping between geometry coordinates (usually X, Y, Z or X, Y, TWT)
    and trace or inter-trace positions on a seismic lattice.

    :ivar crossline_coordinates: The sequence of trace or inter-trace
        crossline positions that correspond to the geometry coordinates.
        BUSINESS RULE: Both sequences must be in the same order.
    :ivar inline_coordinates: The sequence of trace or inter-trace
        inline positions that correspond to the geometry coordinates.
        BUSINESS RULE: Both sequences must be in the same order.
    :ivar vertical_coordinates: The sequence of vertical sample or
        inter-sample positions that correspond to the geometry
        coordinates. BUSINESS RULE: Sequence must be in the same order
        than two previous ones.
    """

    class Meta:
        name = "Seismic3dCoordinates"

    crossline_coordinates: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "CrosslineCoordinates",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    inline_coordinates: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "InlineCoordinates",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    vertical_coordinates: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "VerticalCoordinates",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class StreamlineWellbores:
    """
    The information that allows you to locate, on one or several grids (existing or
    planned), the intersection of volume (cells) and surface (faces) elements with
    a wellbore trajectory (existing or planned).

    :ivar injector_per_line: Size of array = LineCount. Null values of
        -1 signify that that line does not initiate at a injector, e.g.,
        it may come from fluid expansion or an aquifer.
    :ivar producer_per_line: Size of array = LineCount. Null values of
        -1 signify that that line does not terminate at a producer,
        e.g., it may approach a stagnation area. BUSINESS RULE: The cell
        count must equal the number of non-null entries in this array.
    :ivar wellbore_trajectory_representation:
    """

    injector_per_line: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "InjectorPerLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    producer_per_line: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ProducerPerLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    wellbore_trajectory_representation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "WellboreTrajectoryRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class StringParameter(AbstractActivityParameter):
    """
    Parameter containing a string value.
    """

    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class TimeIndexParameter(AbstractActivityParameter):
    """
    Parameter containing a time index value.
    """

    time_index: Optional[TimeIndex] = field(
        default=None,
        metadata={
            "name": "TimeIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class TimeIndices:
    """Indices into a time series.

    Used to specify time. (Not to be confused with time step.)

    :ivar time_index_count:
    :ivar time_index_start: The index of the start time in the time
        series, if not zero.
    :ivar simulator_time_step: Simulation time step for each time index
    :ivar use_interval: When UseInterval is true, the values are
        associated with each time intervals between two consecutive time
        entries instead of each individual time entry. As a consequence
        the dimension of the value array corresponding to the time
        series is the number of entry in the series minus one.
    :ivar time_series:
    """

    time_index_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "TimeIndexCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    time_index_start: Optional[int] = field(
        default=None,
        metadata={
            "name": "TimeIndexStart",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    simulator_time_step: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "SimulatorTimeStep",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    use_interval: Optional[bool] = field(
        default=None,
        metadata={
            "name": "UseInterval",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    time_series: Optional[str] = field(
        default=None,
        metadata={
            "name": "TimeSeries",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class UniformSubnodePatch(SubnodePatch):
    """
    Use this subnode construction if the number of subnodes is the same for every
    object, e.g., 3 subnodes per edge for all edges.

    :ivar subnode_count_per_object: Number of subnodes per object, with
        the same number for each of this object kind in the grid.
    """

    subnode_count_per_object: Optional[int] = field(
        default=None,
        metadata={
            "name": "SubnodeCountPerObject",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class UnstructuredGridHingeNodeFaces:
    """Hinge nodes define a triangulated interpolation on a cell face.

    In practice, they arise on the K faces of column layer cells and are used to add additional geometric resolution to the shape of the cell. The specification of triangulated interpolation also uniquely defines the interpolation schema on the cell face, and hence the cell volume.
    For an unstructured cell grid, the hinge node faces need to be defined explicitly.
    This hinge node faces object is optional and is only expected to be used if the hinge node faces higher order grid point attachment arises. Hinge node faces are not supported for property attachment. Instead use a subrepresentation or an attachment kind of faces or faces per cell.
    BUSINESS RULE: Each cell must have either 0 or 2 hinge node faces, so that the two hinge nodes for the cell may be used to define a cell center line and a cell thickness.

    :ivar count: Number of K faces. This count must be positive.
    :ivar face_indices: List of faces to be identified as K faces for
        hinge node geometry attachment. BUSINESS RULE: Array length
        equals K face count.
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    face_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "FaceIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class VariableSubnodePatch(SubnodePatch):
    """
    If the number of subnodes per object are variable for each object, use this
    subnode construction.

    :ivar object_indices: Indices of the selected objects
    :ivar subnode_count_per_selected_object: Number of subnodes per
        selected object.
    """

    object_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ObjectIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    subnode_count_per_selected_object: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "SubnodeCountPerSelectedObject",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class VolumeRegion:
    """
    The volume within a shell or envelope.
    """

    patch_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "PatchIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    internal_shells: List[VolumeShell] = field(
        default_factory=list,
        metadata={
            "name": "InternalShells",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    represents: Optional[str] = field(
        default=None,
        metadata={
            "name": "Represents",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    external_shell: Optional[VolumeShell] = field(
        default=None,
        metadata={
            "name": "ExternalShell",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class WellboreMarker(AbstractResqmlDataObject):
    """Representation of a wellbore marker that is located along a wellbore
    trajectory, one for each MD value in the wellbore frame.

    BUSINESS RULE: Ordering of the wellbore markers must match the ordering of the nodes in the wellbore marker frame representation

    :ivar fluid_contact:
    :ivar fluid_marker:
    :ivar geologic_boundary_kind:
    :ivar witsml_formation_marker: Optional WITSML wellbore reference of
        the well marker frame.
    :ivar interpretation:
    """

    fluid_contact: Optional[FluidContact] = field(
        default=None,
        metadata={
            "name": "FluidContact",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    fluid_marker: Optional[FluidMarker] = field(
        default=None,
        metadata={
            "name": "FluidMarker",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    geologic_boundary_kind: Optional[GeologicBoundaryKind] = field(
        default=None,
        metadata={
            "name": "GeologicBoundaryKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    witsml_formation_marker: Optional[str] = field(
        default=None,
        metadata={
            "name": "WitsmlFormationMarker",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    interpretation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Interpretation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjActivity(AbstractResqmlDataObject):
    """
    Instance of a given activity.
    """

    class Meta:
        name = "obj_Activity"

    parent: Optional[str] = field(
        default=None,
        metadata={
            "name": "Parent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    activity_descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "ActivityDescriptor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parameter: List[AbstractActivityParameter] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjGlobalChronostratigraphicColumn(AbstractResqmlDataObject):
    """
    Chronological successions of some chronostratigraphic units organized into 1 to
    n chronological ranks.
    """

    class Meta:
        name = "obj_GlobalChronostratigraphicColumn"

    chronostratigraphic_column_component: List[
        ChronostratigraphicRank
    ] = field(
        default_factory=list,
        metadata={
            "name": "ChronostratigraphicColumnComponent",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjMdDatum(AbstractResqmlDataObject):
    """Specifies the location of the measured depth = 0 reference point.

    The location of this reference point is defined with respect to a
    CRS, which need not be the same as the CRS of a wellbore trajectory
    representation, which may reference this location.

    :ivar location: The location of the md reference point relative to a
        local CRS.
    :ivar md_reference:
    :ivar local_crs:
    """

    class Meta:
        name = "obj_MdDatum"

    location: Optional[Point3D] = field(
        default=None,
        metadata={
            "name": "Location",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    md_reference: Optional[MdReference] = field(
        default=None,
        metadata={
            "name": "MdReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    local_crs: Optional[str] = field(
        default=None,
        metadata={
            "name": "LocalCrs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjPropertyKind(AbstractResqmlDataObject):
    """A description of a property name relative to a standard definition.

    For example, you may specify if the property kind is abstract, the
    dictionary in which the property is unique, and the representative
    unit of measure.

    :ivar naming_system: The name of the dictionary within which the
        property is unique. This also defines the name of the
        controlling authority. Use a URN of the form
        "urn:x-resqml:domainOrEmail:dictionaryName". An example public
        dictionary: "urn:resqml:energistics.org:RESQML" assigned to
        values defined by ResqmlPropertyKind. An example corporate
        dictionary: "urn:resqml:slb.com:product-x". An example personal
        dictionary:
        "urn:resqml:first.last@mycompany.com:my.first.dictionary". The
        purpose of this scheme is to generate a unique name. Parsing for
        semantics is not intended.
    :ivar is_abstract: A value of true indicates that the property kind
        is abstract and an instance of property values must not
        represent this kind. A value of false indicates otherwise (i.e.,
        that an instance of property values may represent this kind).
    :ivar representative_uom: Generally matches the base for conversion,
        except where multiple classes have the same underlying
        dimensional analysis. In this case, the representative unit may
        provide additional information about the underlying concept of
        the class. For example, "area per volume" has the same
        dimensional analysis as "per length", but it specifies a
        representative unit of "m2/m3" instead of "1/m".
    :ivar parent_property_kind:
    """

    class Meta:
        name = "obj_PropertyKind"

    naming_system: Optional[str] = field(
        default=None,
        metadata={
            "name": "NamingSystem",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    is_abstract: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAbstract",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    representative_uom: Optional[ResqmlUom] = field(
        default=None,
        metadata={
            "name": "RepresentativeUom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_property_kind: Optional[AbstractPropertyKind] = field(
        default=None,
        metadata={
            "name": "ParentPropertyKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjPropertySet(AbstractResqmlDataObject):
    """A set of properties collected together for a specific purpose.

    For example, a property set can be used to collect all the
    properties corresponding to the simulation output at a single time,
    or all the values of a single property type for all times.

    :ivar time_set_kind:
    :ivar has_single_property_kind: If true, indicates that the
        collection contains only property values associated with a
        single property kind.
    :ivar has_multiple_realizations: If true, indicates that the
        collection contains properties with defined realization indices.
    :ivar parent_set: A pointer to the parent property group of this
        property group.
    :ivar properties:
    """

    class Meta:
        name = "obj_PropertySet"

    time_set_kind: Optional[TimeSetKind] = field(
        default=None,
        metadata={
            "name": "TimeSetKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    has_single_property_kind: Optional[bool] = field(
        default=None,
        metadata={
            "name": "HasSinglePropertyKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    has_multiple_realizations: Optional[bool] = field(
        default=None,
        metadata={
            "name": "HasMultipleRealizations",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_set: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ParentSet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    properties: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Properties",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjStratigraphicColumn(AbstractResqmlDataObject):
    """A global interpretation of the stratigraphy, which can be made up of several
    ranks of stratigraphic unit interpretations.

    BUSINESS RULE: All stratigraphic column rank interpretations that make up a stratigraphic column must be ordered by age.
    """

    class Meta:
        name = "obj_StratigraphicColumn"

    ranks: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Ranks",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjTimeSeries(AbstractResqmlDataObject):
    """Stores an ordered list of times, for example, for time-dependent properties,
    geometries, or representations.

    It is used in conjunction with the time index to specify times for
    RESQML.

    :ivar time: Individual times composing the series. The list ordering
        is used by the time index.
    :ivar time_series_parentage:
    """

    class Meta:
        name = "obj_TimeSeries"

    time: List[Timestamp] = field(
        default_factory=list,
        metadata={
            "name": "Time",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )
    time_series_parentage: Optional[TimeSeriesParentage] = field(
        default=None,
        metadata={
            "name": "TimeSeriesParentage",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class AbstractGeologicFeature(AbstractFeature):
    """Objects that exist a priori, in the natural world, for example: the rock
    formations and how they are positioned with regard to each other; the fluids
    that are present before production; or the position of the geological intervals
    with respect to each.

    Some of these objects are static—such as geologic intervals---while others are dynamic—such as fluids; their properties, geometries, and quantities may change over time during the course of field production.
    RESQML has these types of features: geologic and technical.
    """


@dataclass
class AbstractGridGeometry(PointGeometry):
    """
    Grid geometry described by means of points attached to nodes and additional
    optional points which may be attached to other indexable elements of the grid
    representation.
    """

    additional_grid_points: List[AdditionalGridPoints] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalGridPoints",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class AbstractOrganizationInterpretation(AbstractFeatureInterpretation):
    """The main class used to group features into meaningful units as a step in
    working towards the goal of building an earth model (the organization of all
    other organizations in RESQML).

    An organization interpretation:
    - Is typically comprised of one stack of its contained elements.
    - May be built on other organization interpretations.
    Typically contains:
    - contacts between the elements of this stack among themselves.
    - contacts between the stack elements and other organization elements.
    """

    contact_interpretation: List[AbstractContactInterpretationPart] = field(
        default_factory=list,
        metadata={
            "name": "ContactInterpretation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class AbstractSurfaceRepresentation(AbstractRepresentation):
    """Parent class of structural surface representations, which can be bounded by
    an outer ring and has inner rings.

    These surfaces may consist of one or more patches.
    """

    surface_role: Optional[SurfaceRole] = field(
        default=None,
        metadata={
            "name": "SurfaceRole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    boundaries: List[PatchBoundaries] = field(
        default_factory=list,
        metadata={
            "name": "Boundaries",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class AbstractTechnicalFeature(AbstractFeature):
    """Objects that exist by the action of humans.

    Examples include: wells and all they may contain, seismic surveys (surface, permanent water bottom), or injected fluid volumes. Because the decision to deploy such equipment is the result of studies or decisions by humans, technical features are usually not subject to the same kind of large changes in interpretation as geologic features. However, they are still subject to measurement error and other sources of uncertainty, and so still can be considered as subject to "interpretation".
    RESQML has these types of features: geologic and technical.
    """


@dataclass
class AbstractValuesProperty(AbstractProperty):
    """Base class for property values.

    Each derived element provides specific property values, including
    point property in support of geometries.
    """

    patch_of_values: List[PatchOfValues] = field(
        default_factory=list,
        metadata={
            "name": "PatchOfValues",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )
    facet: List[PropertyKindFacet] = field(
        default_factory=list,
        metadata={
            "name": "Facet",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class Activity(ObjActivity):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class CellOverlap:
    """Optional cell volume overlap information between the current grid (the
    child) and the parent grid.

    Use this data-object when the child grid has an explicitly defined
    geometry, and these relationships cannot be inferred from the regrid
    descriptions.

    :ivar count: Number of parent-child cell overlaps. Must be positive.
    :ivar parent_child_cell_pairs: (Parent cell index, Child cell index)
        pair for each overlap. BUSINESS RULE: Length of array must equal
        2 x overlapCount.
    :ivar overlap_volume:
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    parent_child_cell_pairs: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ParentChildCellPairs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    overlap_volume: Optional[OverlapVolume] = field(
        default=None,
        metadata={
            "name": "OverlapVolume",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ColumnLayerSplitCoordinateLines:
    """Definition of the indexing for the split coordinate lines.

    When present, this indexing contributes to the coordinate line
    nodes.

    :ivar count: Number of split coordinate lines. The count must be
        positive.
    :ivar pillar_indices: Pillar index for each split coordinate line.
        Length of this array is equal to the number of split coordinate
        lines. For the first pillarCount lines, the index of the
        coordinate line equals the index of the corresponding pillar.
        This array provides the pillar indices for the additional
        (split) coordinate lines. Used to implicitly define column and
        cell geometry.
    :ivar columns_per_split_coordinate_line: Column indices for each of
        the split coordinate lines. Used to implicitly define column and
        cell geometry. List-of-lists construction used to support shared
        coordinate lines.
    :ivar split_column_edges:
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    pillar_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "PillarIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    columns_per_split_coordinate_line: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "ColumnsPerSplitCoordinateLine",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    split_column_edges: Optional[ColumnLayerSplitColumnEdges] = field(
        default=None,
        metadata={
            "name": "SplitColumnEdges",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ConnectionInterpretations:
    """
    :ivar interpretation_indices: Indices for the interpretations for
        each connection, if any. The use of a Resqml jagged array allows
        zero or more than one interpretation to be associated with a
        single connection.
    :ivar feature_interpretation:
    """

    interpretation_indices: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "InterpretationIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    feature_interpretation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "FeatureInterpretation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class DoubleLatticeArray(AbstractDoubleArray):
    """Represents an array of doubles based on an origin and a multi-dimensional
    offset.

    The offset is based on a linearization of a multi-dimensional offset.
    If count(i) is the number of elements in the dimension i and offset(i) is the offset in the dimension i, then:
    globalOffsetInNDimension = startValue+ ni*offset(n) + n_1i*count(n)*offset(n-1) + .... + 0i*count(n)*count(n-1)*....count(1)*offset(0)

    :ivar start_value: Value representing the global start for the
        lattice.
    :ivar offset:
    """

    start_value: Optional[float] = field(
        default=None,
        metadata={
            "name": "StartValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    offset: List[DoubleConstantArray] = field(
        default_factory=list,
        metadata={
            "name": "Offset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class GlobalChronostratigraphicColumn(ObjGlobalChronostratigraphicColumn):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class Grid2DPatch(Patch):
    """Patch representing a single 2D grid and its geometry.

    The FastestAxisCount and the SlowestAxisCount determine the indexing
    of this grid 2D patch, by defining a one dimensional index for the
    2D grid as follows: Index = FastestIndex + FastestAxisCount *
    SlowestIndex This indexing order IS the data order when stored in
    HDF5, in which case, this would be a
    SlowestAxisCount*FastestAxisCount two dimensional array in HDF5.

    :ivar fastest_axis_count: The number of nodes in the fastest
        direction.
    :ivar slowest_axis_count: The number of nodes in the slowest
        direction.
    :ivar geometry:
    """

    class Meta:
        name = "Grid2dPatch"

    fastest_axis_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "FastestAxisCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    slowest_axis_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "SlowestAxisCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    geometry: Optional[PointGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class HorizontalPlaneGeometry(AbstractPlaneGeometry):
    """
    Defines the infinite geometry of a horizontal plane provided by giving its
    unique Z value.
    """

    coordinate: Optional[float] = field(
        default=None,
        metadata={
            "name": "Coordinate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class IjSplitColumnEdges:
    """Used to construct the indices for the cell faces.

    For IJK grids with IJ gaps, the split column edge indices must be
    defined explicitly. Otherwise, column edges are not required to
    describe the lowest order grid geometry, but may be needed for
    higher order geometries or properties.

    :ivar count: Number of IJ split column edges in this grid. Must be
        positive.
    :ivar pillars_per_split_column_edge: Definition of the split column
        edges in terms of the pillars per split column edge. Pillar
        count per edge is usually 2, but the list-of-lists construction
        is used to allow split column edges to be defined by more than 2
        pillars.
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    pillars_per_split_column_edge: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "PillarsPerSplitColumnEdge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class IntegerLatticeArray(AbstractIntegerArray):
    """Represents an array of integers based on an origin and a multi-dimensional
    offset.

    The offset is based on a linearization of a multi-dimensional offset.
    If count(i) is the number of elements in the dimension i and offset(i) is the offset in the dimension i, then:
    globalOffsetInNDimension = startValue+ ni*offset(n) + n_1i*count(n)*offset(n-1) + .... + 0i*count(n)*count(n-1)*....count(1)*offset(0)

    :ivar start_value: Value representing the global start for the
        lattice: i.e., iStart + jStart*ni + kStart*ni*nj
    :ivar offset:
    """

    start_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "StartValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    offset: List[IntegerConstantArray] = field(
        default_factory=list,
        metadata={
            "name": "Offset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class MdDatum(ObjMdDatum):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class NodePatch(Patch1D):
    """
    Patch representing a list of nodes to which geometry may be attached.
    """

    geometry: Optional[PointGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class NodesPerCell:
    """Optional component of Unstructured Cell Finite Elements.

    The choice of node order per cell is important for effective use of the RESQML finite element representations. If you are working with an application with a particular node ordering per cell, be sure to specify the nodes in that order here, for ease of use.
    BUSINESS RULE: If cell subnodes are used for unstructured grids, then nodes per cell must be defined.

    :ivar nodes_per_cell: Defines an ordered list of nodes per cell.
    """

    nodes_per_cell: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "NodesPerCell",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class NonSealedContactRepresentationPart(AbstractContactRepresentationPart):
    """
    Defines a nonsealed contact representation, meaning that this contact
    representation is defined by a geometry.
    """

    contact: List[ContactPatch] = field(
        default_factory=list,
        metadata={
            "name": "Contact",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    geometry: Optional[AbstractGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ParametricLineArray(AbstractParametricLineArray):
    """Defines an array of parametric lines of multiple kinds.

    These are the documented parametric line kinds; see additional information below:
    0 = vertical
    1 = linear spline (piecewise linear)
    2 = natural cubic spline
    3 = cubic spline
    4 = Z linear cubic spline
    5 = minimum-curvature spline
    (-1) = null: no line
    If isBounded=true in the line definition, then any out of range parametric values in the parametric points are truncated to the first or last control point. Otherwise, the interpolant in the first or last interval is used as an extrapolating function.
    Special Cases:
    (1) Natural cubic splines with only two control points reduce to linear interpolation.
    (2) If required but not defined, tangent vectors at a spline knot are calculated from the control point data using a quadratic fit to the control point and the two adjacent control points (if internal) or, if at an edge, by a vanishing second derivative. This calculation reduces locally to a natural spline.
    (3) If not expected but provided, then extraneous information is to be ignored, e.g., tangent vectors for linear splines.
    Vertical:
    (1) Control points are (X,Y,-).
    (2) Parameter values are interpreted as depth =&gt; (X,Y,Z), where the depth to Z conversion depends on the vertical CRS direction.
    Piecewise Linear:
    (1) Control points are (P,X,Y,Z).
    (2) Piecewise interpolation in (X,Y,Z) as a linear function of P.
    Natural Cubic:
    (1) Control points are (P,X,Y,Z).
    (2) First and second derivatives at each knot are inferred from a quadratic fit to the two adjacent control points, if internal, or, if external knots, by specifying a vanishing second derivative.
    (3) Interpolating basis functions are obtained by specifying values and second derivatives at the knots.
    Cubic and Minimum-Curvature.
    (1) Control points are (P,X,Y,Z).
    (2) Tangent vectors are (P,TX,TY,TZ). Tangent vectors are defined as the derivative of position with respect to the parameter. If the parameter is arc-length, then the tangent vectors are unit vectors, but not otherwise.
    (3) Interpolating cubic basis functions obtained by specifying values and first derivatives at the knots.
    (4) Interpolating minimum-curvature basis functions obtained by a circular arc construction that is constrained by the knot data. This differs from the unconstrained "drilling" algorithm in which the knot locations are not independent but for which the parameter must be arc length.
    Z Linear Cubic:
    (1) (X,Y) follow a natural cubic spline and Z follows a linear spline.
    (2) Parametric values cannot be freely chosen but are instead defined to take the values of 0,,,.N for a line with N intervals, N+1 control points.
    (3) On export, to go from Z to P, the RESQML "software writer" first needs to determine the interval and then uses linearity in Z to determine P. For the control points, the P values are 0...N and for values of Z, other than the control points, intermediate values of P arise.
    (4) On import, a RESQML "software reader" converts from P to Z using piecewise linear interpolation, and from P to X and Y using natural cubic spline interpolation. Other than the differing treatment of Z from X and Y, these are completely generic interpolation algorithms.
    (5) The use of P instead of Z for interpolation allows support for over-turned reservoir structures and removes any apparent discontinuities in parametric derivatives at the spline knots.

    :ivar control_point_parameters: An optional array of explicit
        control point parameters for all of the control points on each
        of the parametric lines. Used only if control point parameters
        are present. The number of explicit control point parameters per
        line is given by the count of non-null parameters on each line.
        Described as a 1D array, the control point parameter array is
        divided into segments of length count, with null (NaN) values
        added to each segment to fill it up. Size = count x #Lines,
        e.g., 2D or 3D BUSINESS RULE: This count should be zero for
        vertical and Z linear cubic parametric lines. For all other
        parametric line kinds, there should be one control point
        parameter for each control point. NOTES: (1) Vertical parametric
        lines do not require control point parameters (2) Z linear cubic
        splines have implicitly defined parameters. For a line with N
        intervals (N+1 control points), the parametric values are
        P=0,...,N. BUSINESS RULE: The parametric values must be strictly
        monotonically increasing on each parametric line.
    :ivar control_points: An array of 3D points for all of the control
        points on each of the parametric lines. The number of control
        points per line is given by the count of non-null 3D points on
        each line. Described as a 1D array, the control point array is
        divided into segments of length count, with null (NaN) values
        added to each segment to fill it up. Size = count x #Lines,
        e.g., 2D or 3D
    :ivar knot_count: The first dimension of the control point, control
        point parameter, and tangent vector arrays for the parametric
        splines. The Knot Count is typically chosen to be the maximum
        number of control points, parameters or tangent vectors on any
        parametric line in the array of parametric lines.
    :ivar line_kind_indices: An array of integers indicating the
        parametric line kind. 0 = vertical 1 = linear spline 2 = natural
        cubic spline 3 = cubic spline 4 = Z linear cubic spline 5 =
        minimum-curvature spline (-1) = null: no line Size = #Lines,
        e.g., (1D or 2D)
    :ivar tangent_vectors: An optional array that is of tangent vectors
        for all of the control points on each of the cubic and minimum-
        curvature parametric lines. Used only if tangent vectors are
        present. The number of tangent vectors per line is given by the
        count of non-null tangent vectors on each of these line kinds.
        Described as a 1D array, the tangent vector array is divided
        into segments of length count, with null (NaN) values added to
        each segment to fill it up. Size = count x #Lines, e.g., 2D or
        3D BUSINESS RULE: For all lines other than the cubic and
        minimum-curvature parametric lines, this count is zero. For
        these line kinds, there is one tangent vector for each control
        point. If a tangent vector is missing, then it is computed in
        the same fashion as for a natural cubic spline. Specifically, to
        obtain the tangent at internal knots, the control points are fit
        by a quadratic function with the two adjacent control points. At
        edge knots, the second derivative vanishes.
    :ivar parametric_line_intersections:
    """

    control_point_parameters: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "ControlPointParameters",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    control_points: Optional[AbstractPoint3DArray] = field(
        default=None,
        metadata={
            "name": "ControlPoints",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    knot_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "KnotCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    line_kind_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "LineKindIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    tangent_vectors: Optional[AbstractPoint3DArray] = field(
        default=None,
        metadata={
            "name": "TangentVectors",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    parametric_line_intersections: Optional[
        ParametricLineIntersections
    ] = field(
        default=None,
        metadata={
            "name": "ParametricLineIntersections",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ParametricLineFromRepresentationGeometry(AbstractParametricLineGeometry):
    """The parametric line extracted from an existing representation.

    BUSINESS RULE: The supporting representation must have pillars or lines as indexable elements.

    :ivar line_indiex_on_supporting_representation: The line index of
        the selected line in the supporting representation. For a
        column-layer grid, the parametric lines follow the indexing of
        the pillars.
    :ivar supporting_representation:
    """

    line_indiex_on_supporting_representation: Optional[int] = field(
        default=None,
        metadata={
            "name": "LineIndiexOnSupportingRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    supporting_representation: Optional[str] = field(
        default=None,
        metadata={
            "name": "SupportingRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ParametricLineGeometry(AbstractParametricLineGeometry):
    """Defines a parametric line of any kind.

    For more information on the supported parametric lines, see
    ParametricLineArray.

    :ivar control_point_parameters: An optional array of explicit
        control point parameters for the control points on the
        parametric line. Used only if control point parameters are
        present. NOTES: (1) Vertical parametric lines do not require
        control point parameters. (2) Z linear cubic splines have
        implicitly defined parameters. For a line with N intervals (N+1
        control points), the parametric values are P=0,...,N. BUSINESS
        RULE: If present, the size must match the number of control
        points. BUSINESS RULE: For vertical and Z linear cubic
        parametric lines, this count must be zero. For all other
        parametric line kinds, each control point must have one control
        point parameter. BUSINESS RULE: The parametric values must be
        strictly monotonically increasing on each parametric line. This
        is an optional array which should only be used if control point
        parameters are present. BUSINESS RILE: If present, the size must
        match the number of control points. BUSINESS RULE: This count
        should be zero for vertical and Z linear cubic parametric lines.
        For all other parametric line kinds there should be one control
        point parameter for each control point. Notes: (1) Vertical
        parametric lines do not require control point parameters (2) Z
        linear cubic splines have implicitly defined parameters. For a
        line with N intervals (N+1 control points), the parametric
        values are P=0,...,N. BUSINESS RULE: The parametric values must
        be strictly monotonically increasing on each parametric line.
    :ivar control_points: An array of 3D points for the control points
        on the parametric line.
    :ivar knot_count: Number of spline knots in the parametric line.
    :ivar line_kind_index: Integer indicating the parametric line kind 0
        for vertical 1 for linear spline 2 for natural cubic spline 3
        for cubic spline 4 for z linear cubic spline 5 for minimum-
        curvature spline (-1) for null: no line
    :ivar tangent_vectors: An optional array of tangent vectors for each
        control point on the cubic and minimum-curvature parametric
        lines. Used only if tangent vectors are present. If a tangent
        vector is missing, then it is computed in the same fashion as
        for a natural cubic spline. Specifically, to obtain the tangent
        at internal knots, the control points are fit by a quadratic
        function with the two adjacent control points. At edge knots,
        the second derivative vanishes.
    """

    control_point_parameters: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "ControlPointParameters",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    control_points: Optional[AbstractPoint3DArray] = field(
        default=None,
        metadata={
            "name": "ControlPoints",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    knot_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "KnotCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    line_kind_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "LineKindIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    tangent_vectors: Optional[AbstractPoint3DArray] = field(
        default=None,
        metadata={
            "name": "TangentVectors",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class Point3DLatticeArray(AbstractPoint3DArray):
    """Describes a lattice array of points obtained by sampling from along a multi-
    dimensional lattice.

    Each dimension of the lattice can be uniformly or irregularly
    spaced.

    :ivar all_dimensions_are_orthogonal: The optional element that
        indicates that the offset vectors for each direction are
        mutually orthogonal to each other. This meta-information is
        useful to remove any doubt of orthogonality in case of numerical
        precision issues. BUSINESS RULE: If you don't know it or if only
        one lattice dimension is given, do not provide this element.
    :ivar origin: The origin location of the lattice given as XYZ
        coordinates.
    :ivar offset:
    """

    class Meta:
        name = "Point3dLatticeArray"

    all_dimensions_are_orthogonal: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AllDimensionsAreOrthogonal",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    origin: Optional[Point3D] = field(
        default=None,
        metadata={
            "name": "Origin",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    offset: List[Point3DOffset] = field(
        default_factory=list,
        metadata={
            "name": "Offset",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class PolylineSetPatch(Patch):
    """A patch containing a set of polylines. For performance reasons, the geometry
    of each patch is described in only one 1D array of 3D points, which aggregates
    the nodes of all the polylines together. To be able to separate the polyline
    descriptions, additional information is added about the type of each polyline
    (closed or not) and the number of 3D points (node count) of each polyline.

    This additional information is contained in two arrays which are associated with each polyline set patch. The dimension of these arrays is the number of polylines gathered in one polyline set patch.
    - The first array contains a Boolean for each polyline (closed or not closed)
    - The second array contains the count of nodes for each polyline.

    :ivar closed_polylines:
    :ivar node_count_per_polyline: The first number in the list defines
        the node count for the first polyline in the polyline set patch.
        The second number in the list defines the node count for the
        second polyline in the polyline set patch. etc.
    :ivar geometry:
    """

    closed_polylines: Optional[AbstractBooleanArray] = field(
        default=None,
        metadata={
            "name": "ClosedPolylines",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    node_count_per_polyline: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "NodeCountPerPolyline",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    geometry: Optional[PointGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class PropertyKind(ObjPropertyKind):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class PropertySet(ObjPropertySet):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class Regrid:
    """One-dimensional I, J, or K refinement and coarsening regrid specification.

    The regrid description is organized using intervals. Within each
    interval, the number of parent and child cells is specified. Parent
    and child grid cell faces are aligned at interval boundaries. By
    default, child cells are uniformly sized within an interval unless
    weights are used to modify their size. If the child grid is a root
    grid with an independent geometry, then there will usually be only a
    single interval for a regrid, because internal cell faces are not
    necessarily aligned.

    :ivar initial_index_on_parent_grid: 0-based index for the placement
        of the window on the parent grid.
    :ivar intervals:
    """

    initial_index_on_parent_grid: Optional[int] = field(
        default=None,
        metadata={
            "name": "InitialIndexOnParentGrid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    intervals: Optional[Intervals] = field(
        default=None,
        metadata={
            "name": "Intervals",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class SealedContactRepresentationPart(AbstractContactRepresentationPart):
    """Sealed contact elements that indicate that 2 or more contact patches are
    partially or totally colocated or equivalent.

    For possible types of identity, see IdentityKind.

    :ivar identical_node_indices: Indicate which nodes (identified by
        their common index in all contact patches) of the contact
        patches are identical. If this list is not present, then it
        indicates that all nodes in each representation are identical,
        on an element-by-element level.
    :ivar identity_kind:
    :ivar contact:
    """

    identical_node_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "IdenticalNodeIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    identity_kind: Optional[IdentityKind] = field(
        default=None,
        metadata={
            "name": "IdentityKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    contact: List[ContactPatch] = field(
        default_factory=list,
        metadata={
            "name": "Contact",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 2,
        },
    )


@dataclass
class SplitEdges:
    """If split nodes are used in the construction of a column layer grid and
    indexable elements of kind edges are referenced, then the grid edges need to be
    re-defined.

    Use Case: finite elements, especially for higher order geometry.

    :ivar count: Number of edges. Must be positive.
    :ivar parent_edge_indices: Parent unsplit edge index for each of the
        additional split edges.
    :ivar faces_per_split_edge: Association of faces with the split
        edges, used to infer continuity of property, geometry, or
        interpretation with an attachment kind of edges.
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_edge_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ParentEdgeIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    faces_per_split_edge: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "FacesPerSplitEdge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class StratigraphicColumn(ObjStratigraphicColumn):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class StreamlinePolylineSetPatch(Patch):
    """A patch containing a set of polylines. For performance reasons, the geometry
    of each patch is described in only one 1D array of 3D points, which aggregates
    the nodes of all the polylines together. To be able to separate the polyline
    descriptions, additional information is added about the type of each polyline
    (closed or not) and the number of 3D points (node count) of each polyline.

    This additional information is contained in two arrays which are associated with each polyline set patch. The dimension of these arrays is the number of polylines gathered in one polyline set patch.
    - The first array contains a Boolean for each polyline (closed or not closed)
    - The second array contains the count of nodes for each polyline.

    :ivar node_count: Total number of nodes. BUSINESS RULE: Should be
        equal to the sum of the number of nodes per polyline
    :ivar interval_count: Total number of intervals. BUSINESS RULE:
        Should be equal to the sum of the count of intervals per
        polyline.
    :ivar closed_polylines: Indicates whether a polyline is closed. If
        closed, then the interval count for that polyline is equal to
        the node count. If open, then the interval count for that
        polyline is one less than the node count.
    :ivar node_count_per_polyline: The first number in the list defines
        the node count for the first polyline in the polyline set patch.
        The second number in the list defines the node count for the
        second polyline in the polyline set patch. etc.
    :ivar interval_grid_cells:
    """

    node_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "NodeCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    interval_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "IntervalCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    closed_polylines: Optional[AbstractBooleanArray] = field(
        default=None,
        metadata={
            "name": "ClosedPolylines",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    node_count_per_polyline: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "NodeCountPerPolyline",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    interval_grid_cells: Optional[IntervalGridCells] = field(
        default=None,
        metadata={
            "name": "IntervalGridCells",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class SubRepresentationPatch(Patch1D):
    """Each sub-representation patch has its own list of representation indices,
    drawn from the supporting representation.

    If a list of pairwise elements is required, use two representation
    indices. The count of elements is defined in SubRepresenationPatch.
    Optional additional grid topology is available for grid
    representations.
    """

    element_indices: List[ElementIndices] = field(
        default_factory=list,
        metadata={
            "name": "ElementIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
            "max_occurs": 2,
        },
    )


@dataclass
class SubnodeTopology:
    """
    Finite element subnode topology for an unstructured cell can be either variable
    or uniform, but not columnar.
    """

    variable_subnodes: List[VariableSubnodePatch] = field(
        default_factory=list,
        metadata={
            "name": "VariableSubnodes",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    uniform_subnodes: List[UniformSubnodePatch] = field(
        default_factory=list,
        metadata={
            "name": "UniformSubnodes",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class TiltedPlaneGeometry(AbstractPlaneGeometry):
    """
    Describes the geometry of a tilted (or potentially not tilted) plane from three
    points.
    """

    plane: List[ThreePoint3D] = field(
        default_factory=list,
        metadata={
            "name": "Plane",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class TimeSeries(ObjTimeSeries):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class TrianglePatch(Patch1D):
    """Patch made of triangles, where the number of triangles is given by the patch count.
    BUSINESS RULE: Within a patch, all the triangles must be contiguous.
    The patch contains:
    - Number of nodes within the triangulation and their locations.
    - 2D array describing the topology of the triangles.
    Two triangles that are connected may be in different patches.

    :ivar node_count:
    :ivar triangles: The triangles are a 2D array of non-negative
        integers with the dimensions 3 x numTriangles.
    :ivar geometry:
    :ivar split_edge_patch:
    """

    node_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "NodeCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    triangles: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "Triangles",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    geometry: Optional[PointGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    split_edge_patch: List[EdgePatch] = field(
        default_factory=list,
        metadata={
            "name": "SplitEdgePatch",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class TruncationCellPatch(Patch):
    """Truncation definitions for the truncated and split cells.

    BUSINESS RULE: Patch Index must be positive since a patch index of 0 refers to the fundamental column layer coordinate line nodes and cells.

    :ivar truncation_node_count: Number of additional nodes required for
        the truncation construction. Must be positive. Uses a separate
        enumeration and does not increase the number of nodes, except as
        noted below.
    :ivar truncation_face_count: Number of additional faces required for
        the split and truncation construction. The construction does not
        modify existing face definitions, but instead uses these new
        faces to redefine the truncated cell geometry. Must be positive.
        These faces are added to the enumeration of faces for the grid
    :ivar truncation_cell_count: Number of polyhedral cells created by
        truncation. Must be positive. Note: Parent cells are replace
    :ivar nodes_per_truncation_face: Definition of the truncation faces
        is in terms of an ordered list of nodes. Node indexing is
        EXTENDED, i.e., is based on the list of untruncated grid nodes
        (always first) plus the split nodes (if any) and the truncation
        face nodes. Relative order of split nodes and truncation face
        nodes is set by the pillar indices.
    :ivar parent_cell_indices: Parent cell index for each of the
        truncation cells. BUSINESS RULE: Size must match
        truncationCellCount
    :ivar local_faces_per_cell: Local cell face index for those faces
        which are retained from the parent cell in the definition of the
        truncation cell. The use of a local cell face index, e.g., 0...5
        for an IJK cell, can be used even if the face indices have not
        been defined.
    :ivar truncation_faces_per_cell: Truncation face index for the
        additional cell faces which are required to complete the
        definition of the truncation cell. The resulting local cell face
        index follows the local faces per cell list, followed by the
        truncation faces in the order within the list-of-lists
        constructions.
    :ivar truncation_cell_face_is_right_handed: Boolean mask used to
        indicate which truncation cell faces have an outwardly directed
        normal, following a right hand rule. Data size and order follows
        the truncationFacesPerCell list-of-lists.
    """

    truncation_node_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "TruncationNodeCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    truncation_face_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "TruncationFaceCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    truncation_cell_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "TruncationCellCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    nodes_per_truncation_face: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "NodesPerTruncationFace",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_cell_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ParentCellIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    local_faces_per_cell: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "LocalFacesPerCell",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    truncation_faces_per_cell: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "TruncationFacesPerCell",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    truncation_cell_face_is_right_handed: Optional[
        AbstractBooleanArray
    ] = field(
        default=None,
        metadata={
            "name": "TruncationCellFaceIsRightHanded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class UnstructuredColumnEdges:
    """Column edges are used to construct the index for faces.

    For unstructured column layer grids, the column edge indices must be
    defined explicitly. Column edges are not required to describe lowest
    order grid geometry, but may be needed for higher order geometries
    or properties.

    :ivar count: Number of unstructured column edges in this grid. Must
        be positive.
    :ivar pillars_per_column_edge: Definition of the column edges in
        terms of the pillars per column edge. Pillar count per edge is
        usually 2, but the list-of-lists construction is used to allow
        column edges to be defined by more than 2 pillars.
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    pillars_per_column_edge: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "PillarsPerColumnEdge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjActivityTemplate(AbstractResqmlDataObject):
    """
    Description of one type of activity.
    """

    class Meta:
        name = "obj_ActivityTemplate"

    parameter: List[ParameterTemplate] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjBoundaryFeatureInterpretation(AbstractFeatureInterpretation):
    """The main class for data describing an opinion of a surface feature between
    two volumes.

    BUSINESS RULE: The data-object reference (of type "interprets") must reference only a boundary feature.
    """

    class Meta:
        name = "obj_BoundaryFeatureInterpretation"


@dataclass
class ObjDeviationSurveyRepresentation(AbstractRepresentation):
    """Specifies the station data from a deviation survey.

    The deviation survey does not provide a complete specification of
    the geometry of a wellbore trajectory. Although a minimum-curvature
    algorithm is used in most cases, the implementation varies
    sufficiently that no single algorithmic specification is available
    as a data transfer standard. Instead, the geometry of a RESQML
    wellbore trajectory is represented by a parametric line,
    parameterized by the MD. CRS and units of measure do not need to be
    consistent with the CRS and units of measure for wellbore trajectory
    representation.

    :ivar witsml_deviation_survey:
    :ivar is_final: Used to indicate that this is a final version of the
        deviation survey, as distinct from the interim interpretations.
    :ivar station_count: Number of Stations
    :ivar md_uom: Units of Measure of the measured depths along this
        deviation survey.
    :ivar mds: MD values for the position of the stations BUSINESS RULE:
        Array length equals station count
    :ivar first_station_location: XYZ location of the first station of
        the deviation survey.
    :ivar angle_uom: Defines the units of measure for the azimuth and
        inclination
    :ivar azimuths: An array of azimuth angles, one for each survey
        station. The rotation is relative to the ProjectedCrs north with
        a positive value indication a clockwise rotation as seen from
        above. If the local CRS - whether a LocalTime3dCrs or a
        LocalDepth3dCrs - is rotated relative to the ProjectedCrs, the
        azimuths remain relative to the ProjectedCrs not the local CRS.
        Note that the projection’s north is not the same as true north
        or magnetic north. A good definition of the different kinds of
        "north" can be found in the OGP Surveying &amp; Positioning
        Guidance Note 1 http://www.ogp.org.uk/pubs/373-01.pdf (the
        "True, Grid and Magnetic North bearings" paragraph). BUSINESS
        RULE: Array length equals station count
    :ivar inclinations: Dip (or inclination) angle for each station.
        BUSINESS RULE: Array length equals station count
    :ivar md_datum:
    :ivar time_index:
    """

    class Meta:
        name = "obj_DeviationSurveyRepresentation"

    witsml_deviation_survey: Optional[str] = field(
        default=None,
        metadata={
            "name": "WitsmlDeviationSurvey",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    is_final: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsFinal",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    station_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "StationCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    md_uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdUom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    mds: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "Mds",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    first_station_location: Optional[Point3D] = field(
        default=None,
        metadata={
            "name": "FirstStationLocation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    angle_uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "AngleUom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    azimuths: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "Azimuths",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    inclinations: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "Inclinations",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    md_datum: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdDatum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    time_index: Optional[TimeIndex] = field(
        default=None,
        metadata={
            "name": "TimeIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjDoubleTableLookup(AbstractPropertyLookup):
    """Defines a function for table lookups.

    For example, used for linear interpolation, such as PVT. Used for
    categorical property, which also may use StringTableLookup.
    """

    class Meta:
        name = "obj_DoubleTableLookup"

    value: List[DoubleLookup] = field(
        default_factory=list,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjEarthModelInterpretation(AbstractFeatureInterpretation):
    """An earth model interpretation has a specific role: it gathers a maximum of one of each of these other organization interpretations: structural organization interpretation, stratigraphic organization interpretation, and/or fluid organization interpretation.
    BUSINESS RULE: An earth model Interpretation interprets only an earth model feature."""

    class Meta:
        name = "obj_EarthModelInterpretation"

    stratigraphic_occurrences: List[str] = field(
        default_factory=list,
        metadata={
            "name": "StratigraphicOccurrences",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    stratigraphic_column: Optional[str] = field(
        default=None,
        metadata={
            "name": "StratigraphicColumn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    structure: Optional[str] = field(
        default=None,
        metadata={
            "name": "Structure",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    fluid: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fluid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjGenericFeatureInterpretation(AbstractFeatureInterpretation):
    class Meta:
        name = "obj_GenericFeatureInterpretation"


@dataclass
class ObjGeologicUnitInterpretation(AbstractFeatureInterpretation):
    """
    The main class for data describing an opinion of a volume-based geologic
    feature or unit.
    """

    class Meta:
        name = "obj_GeologicUnitInterpretation"

    geologic_unit_composition: Optional[GeologicUnitComposition] = field(
        default=None,
        metadata={
            "name": "GeologicUnitComposition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    geologic_unit_material_implacement: Optional[
        GeologicUnitMaterialImplacement
    ] = field(
        default=None,
        metadata={
            "name": "GeologicUnitMaterialImplacement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjLocalDepth3DCrs(AbstractLocal3DCrs):
    """Defines a local depth coordinate system, the geometrical origin and location
    is defined by the elements of the base class AbstractLocal3dCRS.

    This CRS uses the units of measure of its projected and vertical
    CRS.
    """

    class Meta:
        name = "obj_LocalDepth3dCrs"


@dataclass
class ObjLocalGridSet(AbstractResqmlDataObject):
    """Used to activate and/or deactivate the specified children grids as local
    grids on their parents.

    Once activated, this object indicates that a child grid replaces
    local portions of the corresponding parent grid. Parentage is
    inferred from the child grid construction. Without a grid set
    activation, the local grids are always active. Otherwise, the grid
    set activation is used to activate and/or deactivate the local grids
    in the set at specific times.
    """

    class Meta:
        name = "obj_LocalGridSet"

    activation: Optional[Activation] = field(
        default=None,
        metadata={
            "name": "Activation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    child_grid: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ChildGrid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjLocalTime3DCrs(AbstractLocal3DCrs):
    """Defines a local time coordinate system, the geometrical origin and location
    is defined by the elements of the base class AbstractLocal3dCRS.

    This CRS defines the time unit that the time-based geometries that
    refers it will use.

    :ivar time_uom: Defines the unit of measure of the third (time)
        coordinates, for the geometries that refers to it.
    """

    class Meta:
        name = "obj_LocalTime3dCrs"

    time_uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "TimeUom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjPointsProperty(AbstractProperty):
    """
    Represents the geometric information that should *not* be used as
    representation geometry, but should be used in another context where the
    location or geometrical vectorial distances are needed.
    """

    class Meta:
        name = "obj_PointsProperty"

    patch_of_points: List[PatchOfPoints] = field(
        default_factory=list,
        metadata={
            "name": "PatchOfPoints",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjRedefinedGeometryRepresentation(AbstractRepresentation):
    """A representation derived from an existing representation by redefining its
    geometry.

    Example use cases include deformation of the geometry of an object,
    change of coordinate system, and change of time &lt;=&gt; depth.
    """

    class Meta:
        name = "obj_RedefinedGeometryRepresentation"

    patch_of_geometry: List[PatchOfGeometry] = field(
        default_factory=list,
        metadata={
            "name": "PatchOfGeometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )
    supporting_representation: Optional[str] = field(
        default=None,
        metadata={
            "name": "SupportingRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjRepresentationSetRepresentation(AbstractRepresentation):
    """The parent class of the framework representations.

    It is used to group together individual representations which may be
    of the same kind to represent a "bag" of representations. If the bag
    is homogeneous, then this may be indicated. These "bags" do not
    imply any geologic consistency. For example, you can define a set of
    wellbore frames, a set of wellbore trajectories, a set of blocked
    wellbores. Because the framework representations inherit from this
    class, they inherit the capability to gather individual
    representations into sealed and non-sealed surface framework
    representations, or sealed volume framework representations.

    :ivar is_homogeneous: Indicates that all of the selected
        representations are of a single kind.
    :ivar representation:
    """

    class Meta:
        name = "obj_RepresentationSetRepresentation"

    is_homogeneous: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsHomogeneous",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    representation: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Representation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjStringTableLookup(AbstractPropertyLookup):
    """Defines an integer-to-string lookup table, for example, stores facies properties, where a facies index is associated with a facies name. .
    Used for categorical properties, which also may use a double table lookup."""

    class Meta:
        name = "obj_StringTableLookup"

    value: List[StringLookup] = field(
        default_factory=list,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjWellboreFrameRepresentation(AbstractRepresentation):
    """Representation of a wellbore that is organized along a wellbore trajectory
    by its MD values.

    RESQML uses MD values to associate properties on points and to
    organize association of properties on intervals between MD points.

    :ivar node_count: Number of nodes. Must be positive.
    :ivar node_md: MD values for each node. BUSINESS RULE: MD values and
        UOM must be consistent with the trajectory representation.
    :ivar witsml_log_reference: The reference to the equivalent WITSML
        well log.
    :ivar interval_stratigraphi_units:
    :ivar cell_fluid_phase_units:
    :ivar trajectory:
    """

    class Meta:
        name = "obj_WellboreFrameRepresentation"

    node_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "NodeCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    node_md: Optional[AbstractDoubleArray] = field(
        default=None,
        metadata={
            "name": "NodeMd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    witsml_log_reference: Optional[str] = field(
        default=None,
        metadata={
            "name": "WitsmlLogReference",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    interval_stratigraphi_units: Optional[IntervalStratigraphicUnits] = field(
        default=None,
        metadata={
            "name": "IntervalStratigraphiUnits",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    cell_fluid_phase_units: Optional[CellFluidPhaseUnits] = field(
        default=None,
        metadata={
            "name": "CellFluidPhaseUnits",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    trajectory: Optional[str] = field(
        default=None,
        metadata={
            "name": "Trajectory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjWellboreInterpretation(AbstractFeatureInterpretation):
    """This class contains the data describing an opinion of a borehole.

    This interpretation is relative to one particular well trajectory.

    :ivar is_drilled: Used to indicate that this wellbore has been, or
        is being, drilled. This distinguishes from planned wells. For
        one wellbore feature we may expect to have multiple wellbore
        interpretations: IsDrilled=TRUE for instance will be used for
        updated drilled trajectories. IsDrilled=FALSE for planned
        trajectories.
    """

    class Meta:
        name = "obj_WellboreInterpretation"

    is_drilled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsDrilled",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjWellboreTrajectoryRepresentation(AbstractRepresentation):
    """
    Representation of a wellbore trajectory.

    :ivar start_md: Specifies the measured depth  for the start of the
        wellbore trajectory. Range may often be from kickoff to TD, but
        this is not necessary. BUSINESS RULE: Start MD is always less
        than the Finish MD.
    :ivar finish_md: Specifies the ending measured depth of the range
        for the wellbore trajectory. Range may often be from kickoff to
        TD, but this is not necessary. BUSINESS RULE: Start MD is always
        less than the Finish MD.
    :ivar md_uom: The unit of measure of the reference MD.
    :ivar md_domain:
    :ivar witsml_trajectory: Pointer to the WITSML trajectory that is
        contained in the referenced wellbore. (For information about
        WITSML well and wellbore references, see the definition for
        RESQML technical feature, WellboreFeature).
    :ivar geometry: Explicit geometry is not required for vertical wells
    :ivar md_datum:
    :ivar deviation_survey:
    :ivar parent_intersection:
    """

    class Meta:
        name = "obj_WellboreTrajectoryRepresentation"

    start_md: Optional[float] = field(
        default=None,
        metadata={
            "name": "StartMd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    finish_md: Optional[float] = field(
        default=None,
        metadata={
            "name": "FinishMd",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    md_uom: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdUom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    md_domain: Optional[MdDomain] = field(
        default=None,
        metadata={
            "name": "MdDomain",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    witsml_trajectory: Optional[str] = field(
        default=None,
        metadata={
            "name": "WitsmlTrajectory",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    geometry: Optional[AbstractParametricLineGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    md_datum: Optional[str] = field(
        default=None,
        metadata={
            "name": "MdDatum",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    deviation_survey: Optional[str] = field(
        default=None,
        metadata={
            "name": "DeviationSurvey",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    parent_intersection: Optional[
        WellboreTrajectoryParentIntersection
    ] = field(
        default=None,
        metadata={
            "name": "ParentIntersection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class AbstractParentWindow:
    """Parent window specification, organized according to the topology of the
    parent grid.

    In addition to a window specification, for grids with I, J, and/or K
    coordinates, the parentage construction includes a regridding
    description that covers grid refinement, coarsening, or any
    combination of the two.
    """

    cell_overlap: Optional[CellOverlap] = field(
        default=None,
        metadata={
            "name": "CellOverlap",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class AbstractSeismicSurveyFeature(AbstractTechnicalFeature):
    """An organization of seismic lines. For the context of RESQML, a seismic
    survey does not refer to any vertical dimension information, but only really at
    shot point locations or common midpoint gathers. The seismic traces, if needed
    by reservoir models, are transferred in an industry standard format such as
    SEGY.

    RESQML supports these basic types of seismic surveys:
    - seismic lattice (organization of the traces for the 3D acquisition and processing phases).
    - seismic line (organization of the traces for the 2D acquisition and processing phases).
    Additionally, these seismic lattices and seismic lines can be aggregated into sets.
    """


@dataclass
class AbstractStratigraphicOrganizationInterpretation(
    AbstractOrganizationInterpretation
):
    """The main class that defines the relationships between the stratigraphic
    units and provides the stratigraphic hierarchy of the Earth.

    BUSINESS RULE: A stratigraphic organization must be in a ranked order from a lower rank to an upper rank. For example, it is possible to find previous unit containment relationships between several ranks.
    """

    ordering_criteria: Optional[OrderingCriteria] = field(
        default=None,
        metadata={
            "name": "OrderingCriteria",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class AbstractSurfaceFrameworkRepresentation(
    ObjRepresentationSetRepresentation
):
    """Parent class for a sealed or non-sealed surface framework representation.

    Each one instantiates a representation set representation. The
    difference between the sealed and non-sealed frameworks is that, in
    the non-sealed case, we do not have all of the contact
    representations, or we have all of the contacts but they are not all
    sealed.
    """

    contact_identity: List[ContactIdentity] = field(
        default_factory=list,
        metadata={
            "name": "ContactIdentity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ActivityTemplate(ObjActivityTemplate):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class BoundaryFeatureInterpretation(ObjBoundaryFeatureInterpretation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class ColumnLayerSubnodeTopology(SubnodeTopology):
    """
    This data-object consists of the Unstructured Cell Finite Elements subnode
    topology plus the column subnodes.
    """

    column_subnodes: List[ColumnSubnodePatch] = field(
        default_factory=list,
        metadata={
            "name": "ColumnSubnodes",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class DeviationSurveyRepresentation(ObjDeviationSurveyRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class DoubleTableLookup(ObjDoubleTableLookup):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class EarthModelInterpretation(ObjEarthModelInterpretation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class GenericFeatureInterpretation(ObjGenericFeatureInterpretation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class GeologicUnitInterpretation(ObjGeologicUnitInterpretation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class IjGaps:
    """
    Optional object used to indicate that adjacent columns of the model are split
    from each other, which is modeled by introducing additional (split) pillars.

    :ivar split_pillar_count: Number of split pillars in the model.
        Count must be positive.
    :ivar parent_pillar_indices: Parent pillar index for each of the
        split pillars. This information is used to infer the grid cell
        geometry. BUSINESS RULE: Array length must match
        splitPillarCount.
    :ivar columns_per_split_pillar: List of columns for each of the
        split pillars. This information is used to infer the grid cell
        geometry. BUSINESS RULE: The length of the first list-of-lists
        array must match the splitPillarCount.
    :ivar ij_split_column_edges:
    """

    split_pillar_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "SplitPillarCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    parent_pillar_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ParentPillarIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    columns_per_split_pillar: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "ColumnsPerSplitPillar",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    ij_split_column_edges: Optional[IjSplitColumnEdges] = field(
        default=None,
        metadata={
            "name": "IjSplitColumnEdges",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class LocalDepth3DCrs(ObjLocalDepth3DCrs):
    class Meta:
        name = "LocalDepth3dCrs"
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class LocalGridSet(ObjLocalGridSet):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class LocalTime3DCrs(ObjLocalTime3DCrs):
    class Meta:
        name = "LocalTime3dCrs"
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class ParametricLineFromRepresentationLatticeArray(
    AbstractParametricLineArray
):
    """The lattice array of parametric lines extracted from an existing
    representation.

    BUSINESS RULE: The supporting representation must have pillars or lines as indexable elements.

    :ivar line_indices_on_supporting_representation: The line indices of
        the selected lines in the supporting representation. The index
        selection is regularly incremented from one node to the next
        node. BUSINESS RULE: The dimensions of the integer lattice array
        must be consistent with the dimensions of the supporting
        representation. For a column-layer grid, the parametric lines
        follow the indexing of the pillars. BUSINESS RULE: The start
        value of the integer lattice array must be the linearized index
        of the starting line. Example: iStart + ni * jStart in case of a
        supporting 2D grid.
    :ivar supporting_representation:
    """

    line_indices_on_supporting_representation: Optional[
        IntegerLatticeArray
    ] = field(
        default=None,
        metadata={
            "name": "LineIndicesOnSupportingRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    supporting_representation: Optional[str] = field(
        default=None,
        metadata={
            "name": "SupportingRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class Point3DFromRepresentationLatticeArray(AbstractPoint3DArray):
    """A lattice array of points extracted from an existing representation.

    BUSINESS RULE: The supporting representation must have nodes as indexable elements

    :ivar node_indices_on_supporting_representation: The node indices of
        the selected nodes in the supporting representation. The index
        selection is regularly incremented from one node to the next
        node. BUSINESS RULE: The node indices must be consistent with
        the size of supporting representation.
    :ivar supporting_representation:
    """

    class Meta:
        name = "Point3dFromRepresentationLatticeArray"

    node_indices_on_supporting_representation: Optional[
        IntegerLatticeArray
    ] = field(
        default=None,
        metadata={
            "name": "NodeIndicesOnSupportingRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    supporting_representation: Optional[str] = field(
        default=None,
        metadata={
            "name": "SupportingRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class PointsProperty(ObjPointsProperty):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class RedefinedGeometryRepresentation(ObjRedefinedGeometryRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class RepresentationSetRepresentation(ObjRepresentationSetRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class SplitFaces:
    """Optional construction used to introduce additional faces created by split
    nodes.

    Used to represent complex geometries, e.g., for stair-step grids and
    reverse faults.

    :ivar count: Number of additional split faces. Count must be
        positive.
    :ivar parent_face_indices: Parent unsplit face index for each of the
        additional split faces.
    :ivar cell_indices: Cell index for each split face. Used to
        implicitly define cell geometry.
    :ivar split_edges:
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_face_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ParentFaceIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    cell_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "CellIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    split_edges: Optional[SplitEdges] = field(
        default=None,
        metadata={
            "name": "SplitEdges",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class StringTableLookup(ObjStringTableLookup):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class UnstructuredSubnodeTopology(SubnodeTopology):
    """If edge subnodes are used, then edges must be defined.

    If cell subnodes are used, nodes per cell must be defined.
    """

    edges: Optional[Edges] = field(
        default=None,
        metadata={
            "name": "Edges",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    nodes_per_cell: Optional[NodesPerCell] = field(
        default=None,
        metadata={
            "name": "NodesPerCell",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class WellboreFrameRepresentation(ObjWellboreFrameRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class WellboreInterpretation(ObjWellboreInterpretation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class WellboreTrajectoryRepresentation(ObjWellboreTrajectoryRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class ObjBlockedWellboreRepresentation(ObjWellboreFrameRepresentation):
    """
    The information that allows you to locate, on one or several grids (existing or
    planned), the intersection of volume (cells) and surface (faces) elements with
    a wellbore trajectory (existing or planned).

    :ivar cell_count: The number of non-null entries in the grid indices
        array.
    :ivar cell_indices: The grid cell index for each blocked well cell.
        BUSINESS RULE: Array length must equal cell count.
    :ivar grid_indices: Size of array = IntervalCount. Null values of -1
        signify that that interval is not within a grid. BUSINESS RULE:
        The cell count must equal the number of non-null entries in this
        array.
    :ivar local_face_pair_per_cell_indices: For each cell, these are the
        entry and exit faces of the trajectory. Use null (-1), for
        instance, at TD when there only one intersection. The local
        face-per-cell index is used because a global face index need not
        have been defined on the grid. BUSINESS RULE: The array
        dimensions must equal 2 x CellCount.
    :ivar grid:
    """

    class Meta:
        name = "obj_BlockedWellboreRepresentation"

    cell_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "CellCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    cell_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "CellIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    grid_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "GridIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    local_face_pair_per_cell_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "LocalFacePairPerCellIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    grid: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Grid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjBoundaryFeature(AbstractGeologicFeature):
    """An interface between two geological objects, such as horizons and faults.

    It is a surface object.
    """

    class Meta:
        name = "obj_BoundaryFeature"


@dataclass
class ObjCategoricalProperty(AbstractValuesProperty):
    """Information specific to one categorical property. Contains discrete integer.

    This type of property is associated either as:
    - an internally stored index to a string through a lookup mapping.
    - an internally stored double to another double value through an explicitly provided table.
    """

    class Meta:
        name = "obj_CategoricalProperty"

    lookup: Optional[str] = field(
        default=None,
        metadata={
            "name": "Lookup",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjCommentProperty(AbstractValuesProperty):
    """Information specific to one comment property.

    Used to capture comments or annotations associated with a given
    element type in a data-object, for example, associating comments on
    the specific location of a well path.

    :ivar language: Identify the language (e.g., US English or French)
        of the string. It is recommended that language names conform to
        ISO 639.
    """

    class Meta:
        name = "obj_CommentProperty"

    language: Optional[str] = field(
        default=None,
        metadata={
            "name": "Language",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjContinuousProperty(AbstractValuesProperty):
    """Most common type of property used for storing rock or fluid attributes; all
    are represented as doubles.

    So that the value range can be known before accessing all values, the min and max values of the range are also stored.
    BUSINESS RULE: It also contains a unit of measure that can be different from the unit of measure of its property type, but it must be convertible into this unit.

    :ivar minimum_value: The minimum of the associated property values.
        BUSINESS RULE: There can be only one value per number of
        elements.
    :ivar maximum_value: The maximum of the associated property values.
        BUSINESS RULE: There can be only one value per number of
        elements.
    :ivar uom: Unit of measure for the property.
    """

    class Meta:
        name = "obj_ContinuousProperty"

    minimum_value: List[float] = field(
        default_factory=list,
        metadata={
            "name": "MinimumValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    maximum_value: List[float] = field(
        default_factory=list,
        metadata={
            "name": "MaximumValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    uom: Optional[ResqmlUom] = field(
        default=None,
        metadata={
            "name": "UOM",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjDiscreteProperty(AbstractValuesProperty):
    """Contains discrete integer values; typically used to store any type of index.

    So that the value range can be known before accessing all values, it
    also stores the minimum and maximum value in the range.

    :ivar minimum_value: The minimum of the associated property values.
        BUSINESS RULE: There can only be one value per number of
        elements.
    :ivar maximum_value: The maximum of the associated property values.
        BUSINESS RULE: There can only be one value per number of
        elements.
    """

    class Meta:
        name = "obj_DiscreteProperty"

    minimum_value: List[int] = field(
        default_factory=list,
        metadata={
            "name": "MinimumValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    maximum_value: List[int] = field(
        default_factory=list,
        metadata={
            "name": "MaximumValue",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjFaultInterpretation(ObjBoundaryFeatureInterpretation):
    """
    A type of boundary feature, this class contains the data describing an opinion
    about the characterization of the fault, which includes the attributes listed
    below.

    :ivar is_listric: Indicates if the normal fault is listric or not.
        BUSINESS RULE: Must be present if the fault is normal. Must not
        be present if the fault is not normal.
    :ivar maximum_throw:
    :ivar mean_azimuth:
    :ivar mean_dip:
    :ivar throw_interpretation:
    """

    class Meta:
        name = "obj_FaultInterpretation"

    is_listric: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsListric",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    maximum_throw: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaximumThrow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    mean_azimuth: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeanAzimuth",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    mean_dip: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeanDip",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    throw_interpretation: List[FaultThrow] = field(
        default_factory=list,
        metadata={
            "name": "ThrowInterpretation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjFrontierFeature(AbstractTechnicalFeature):
    """
    Identifies a frontier or boundary in the earth model that is not a geological
    feature but an arbitrary geographic/geometric surface used to delineate the
    boundary of the model.
    """

    class Meta:
        name = "obj_FrontierFeature"


@dataclass
class ObjGeobodyBoundaryInterpretation(ObjBoundaryFeatureInterpretation):
    """
    A type of boundary feature, this class identifies if the boundary is a geobody
    and the type of the boundary.
    """

    class Meta:
        name = "obj_GeobodyBoundaryInterpretation"

    boundary_relation: List[BoundaryRelation] = field(
        default_factory=list,
        metadata={
            "name": "BoundaryRelation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjGeobodyInterpretation(ObjGeologicUnitInterpretation):
    """
    A type of rock feature, this class identifies if a rock feature is a geobody
    with any qualifications on the interpretation of the geobody.
    """

    class Meta:
        name = "obj_GeobodyInterpretation"

    geobody3d_shape: Optional[Geobody3DShape] = field(
        default=None,
        metadata={
            "name": "Geobody3dShape",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjGeologicUnitFeature(AbstractGeologicFeature):
    """A volume of rock located between one or more boundary features.

    The limiting boundary features should be genetic boundary features
    (i.e. should not be faults).
    """

    class Meta:
        name = "obj_GeologicUnitFeature"


@dataclass
class ObjGrid2DRepresentation(AbstractSurfaceRepresentation):
    """Representation based on a 2D grid.

    For definitions of slowest and fastest axes of the array, see
    Grid2dPatch.
    """

    class Meta:
        name = "obj_Grid2dRepresentation"

    grid2d_patch: Optional[Grid2DPatch] = field(
        default=None,
        metadata={
            "name": "Grid2dPatch",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjGrid2DSetRepresentation(AbstractSurfaceRepresentation):
    """Set of representations based on a 2D grid.

    Each 2D grid representation corresponds to one patch of the set.
    """

    class Meta:
        name = "obj_Grid2dSetRepresentation"

    grid2d_patch: List[Grid2DPatch] = field(
        default_factory=list,
        metadata={
            "name": "Grid2dPatch",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 2,
        },
    )


@dataclass
class ObjGridConnectionSetRepresentation(AbstractRepresentation):
    """Representation which consists of a list of connections between grid cells,
    potentially on different grids.

    Connections are in the form of (Grid,Cell,Face)1&lt;=&gt;(Grid,Cell,Face)2 and are stored as three integer pair arrays corresponding to these six elements.
    Grid connection sets are the preferred means of representing faults on a grid. The use of cell-face-pairs is more complete than single cell-faces, which are missing a corresponding cell face entry, and only provide an incomplete representation of the topology of a fault.
    Unlike what is sometimes the case in reservoir simulation software, RESQML does not distinguish between standard and non-standard connections.
    Within RESQML if a grid connection corresponds to a "nearest neighbor" as defined by the cell indices, then it is never additive to the implicit nearest neighbor connection.
    BUSINESS RULE: A single cell-face-pair should not appear within more than a single grid connection set. This rule is designed to simplify the interpretation of properties assigned to multiple grid connection sets, which might otherwise have the same property defined more than once on a single connection, with no clear means of resolving the multiple values.

    :ivar count: count of connections. Must be positive.
    :ivar cell_index_pairs: 2 x #Connections array of cell indices for
        (Cell1,Cell2) for each connection.
    :ivar grid_index_pairs: 2 x #Connections array of grid indices for
        (Cell1,Cell2) for each connection. The grid indices are obtained
        from the grid index pairs. If only a single grid is referenced
        from the grid index, then this array need not be used. BUSINESS
        RULE: This array should appear if more than one grid index pair
        is referenced.
    :ivar local_face_per_cell_index_pairs: Optional 2 x #Connections
        array of local face per cell indices for (Cell1,Cell2) for each
        connection. Local face per cell indices are used because global
        face indices need not have been defined. Null value = -1. If no
        face per cell definition occur as part of the grid
        representation, e.g., for a block centered grid, then this array
        need not appear.
    :ivar connection_interpretations:
    :ivar grid:
    """

    class Meta:
        name = "obj_GridConnectionSetRepresentation"

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    cell_index_pairs: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "CellIndexPairs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    grid_index_pairs: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "GridIndexPairs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    local_face_per_cell_index_pairs: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "LocalFacePerCellIndexPairs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    connection_interpretations: Optional[ConnectionInterpretations] = field(
        default=None,
        metadata={
            "name": "ConnectionInterpretations",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    grid: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Grid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjHorizonInterpretation(ObjBoundaryFeatureInterpretation):
    """A type of boundary feature, the class specifies if the boundary feature is a
    horizon.

    Maximum Flooding Surface
    - Transgressive Surface ( for erosion or intrusion ?)
    - Sequence Boundary
    - Stratigraphic Limit
    """

    class Meta:
        name = "obj_HorizonInterpretation"

    boundary_relation: List[BoundaryRelation] = field(
        default_factory=list,
        metadata={
            "name": "BoundaryRelation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    sequence_stratigraphy_surface: Optional[
        SequenceStratigraphySurface
    ] = field(
        default=None,
        metadata={
            "name": "SequenceStratigraphySurface",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjOrganizationFeature(AbstractGeologicFeature):
    """The explicit description of the relationships between geologic features,
    such as rock features (e.g., stratigraphic units, geobodies, phase unit) and
    boundary features (e.g., genetic, tectonic, and fluid boundaries).

    For types of organizations, see OrganizationKind.
    """

    class Meta:
        name = "obj_OrganizationFeature"

    organization_kind: Optional[OrganizationKind] = field(
        default=None,
        metadata={
            "name": "OrganizationKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjPlaneSetRepresentation(AbstractSurfaceRepresentation):
    """Defines a plane representation, which can be made up of multiple patches.

    Commonly represented features are fluid contacts or frontiers. Common geometries of this representation are titled or horizontal planes.
    BUSINESS RULE: If the plane representation is made up of multiple patches, then you must specify the outer rings for each plane patch.
    """

    class Meta:
        name = "obj_PlaneSetRepresentation"

    planes: List[AbstractPlaneGeometry] = field(
        default_factory=list,
        metadata={
            "name": "Planes",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjPointSetRepresentation(AbstractRepresentation):
    """A representation that consists of one or more node patches.

    Each node patch is an array of XYZ coordinates for the 3D points.
    There is no implied linkage between the multiple patches.
    """

    class Meta:
        name = "obj_PointSetRepresentation"

    node_patch: List[NodePatch] = field(
        default_factory=list,
        metadata={
            "name": "NodePatch",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjPolylineRepresentation(AbstractRepresentation):
    """A representation made up of a single polyline or "polygonal chain", which
    may be closed or not.

    Definition from Wikipedia (http://en.wikipedia.org/wiki/Piecewise_linear_curve):
    A polygonal chain, polygonal curve, polygonal path, or piecewise linear curve, is a connected series of line segments. More formally, a polygonal chain P is a curve specified by a sequence of points \\scriptstyle(A_1, A_2, \\dots, A_n) called its vertices so that the curve consists of the line segments connecting the consecutive vertices.
    In computer graphics a polygonal chain is called a polyline and is often used to approximate curved paths.
    BUSINESS RULE: To record a polyline the writer software must give the values of the geometry of each node in an order corresponding to the logical series of segments (edges). The geometry of a polyline must be a 1D array of points.
    A simple polygonal chain is one in which only consecutive (or the first and the last) segments intersect and only at their endpoints.
    A closed polygonal chain (isClosed=True) is one in which the first vertex coincides with the last one, or the first and the last vertices are connected by a line segment.
    """

    class Meta:
        name = "obj_PolylineRepresentation"

    line_role: Optional[LineRole] = field(
        default=None,
        metadata={
            "name": "LineRole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    is_closed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsClosed",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    node_patch: Optional[NodePatch] = field(
        default=None,
        metadata={
            "name": "NodePatch",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjPolylineSetRepresentation(AbstractRepresentation):
    """A representation made up of a set of polylines or a set of polygonal chains
    (for more information, see PolylineRepresentation).

    For compactness, it is organized by line patch as a unique polyline
    set patch. if allPolylineClosed = True, all the polylines are
    connected between the first and the last point. Its geometry is a 1D
    array of points, corresponding to the concatenation of the points of
    all polyline points.
    """

    class Meta:
        name = "obj_PolylineSetRepresentation"

    line_role: Optional[LineRole] = field(
        default=None,
        metadata={
            "name": "LineRole",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    line_patch: List[PolylineSetPatch] = field(
        default_factory=list,
        metadata={
            "name": "LinePatch",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjRockFluidOrganizationInterpretation(
    AbstractOrganizationInterpretation
):
    """
    Interpretation of the fluid organization units.
    """

    class Meta:
        name = "obj_RockFluidOrganizationInterpretation"

    rock_fluid_unit_index: Optional[RockFluidUnitInterpretationIndex] = field(
        default=None,
        metadata={
            "name": "RockFluidUnitIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjRockFluidUnitInterpretation(ObjGeologicUnitInterpretation):
    """
    A type of rock fluid feature interpretation , this class identifies if a rock
    fluid feature by its phase.
    """

    class Meta:
        name = "obj_RockFluidUnitInterpretation"

    phase: Optional[Phase] = field(
        default=None,
        metadata={
            "name": "Phase",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjSealedVolumeFrameworkRepresentation(
    ObjRepresentationSetRepresentation
):
    """A strict boundary representation (BREP), which represents the volume region
    by assembling together shells.

    BUSINESS RULE: The sealed structural framework must be part of the same earth model as this sealed volume framework.
    """

    class Meta:
        name = "obj_SealedVolumeFrameworkRepresentation"

    based_on: Optional[str] = field(
        default=None,
        metadata={
            "name": "BasedOn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    shells: List[VolumeShell] = field(
        default_factory=list,
        metadata={
            "name": "Shells",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )
    regions: List[VolumeRegion] = field(
        default_factory=list,
        metadata={
            "name": "Regions",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjStratigraphicUnitInterpretation(ObjGeologicUnitInterpretation):
    """
    Interpretation of a stratigraphic unit which includes the knowledge of the top,
    the bottom, the deposition mode.

    :ivar deposition_mode: BUSINESS RULE / The Deposition mode for a
        Geological Unit MUST be conssitent with the Boundary Relations
        of A Genetic Boundary. If it is not the case the Boundary
        Relation declaration is retained.
    :ivar max_thickness:
    :ivar min_thickness:
    """

    class Meta:
        name = "obj_StratigraphicUnitInterpretation"

    deposition_mode: Optional[DepositionMode] = field(
        default=None,
        metadata={
            "name": "DepositionMode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    max_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "MaxThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    min_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "MinThickness",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjStreamlinesFeature(AbstractTechnicalFeature):
    """Specification of the vector field upon which the streamlines are based.

    Streamlines are commonly used to trace the flow of phases (water /
    oil / gas / total) based upon their flux at a specified time. They
    may also be used for trace components for compositional simulation,
    e.g., CO2, or temperatures for thermal simulation. The flux
    enumeration provides support for the most usual cases with provision
    for extensions to other fluxes.

    :ivar flux: Specification of the streamline flux, drawn from the
        enumeration.
    :ivar other_flux: Optional specification of the streamline flux, if
        an extension is required beyond the enumeration. BUSINESS RULE:
        OtherFlux should appear if Flux has the value of other.
    :ivar time_index:
    """

    class Meta:
        name = "obj_StreamlinesFeature"

    flux: Optional[StreamlineFlux] = field(
        default=None,
        metadata={
            "name": "Flux",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    other_flux: Optional[str] = field(
        default=None,
        metadata={
            "name": "OtherFlux",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    time_index: Optional[TimeIndex] = field(
        default=None,
        metadata={
            "name": "TimeIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjStreamlinesRepresentation(AbstractRepresentation):
    """Representation of streamlines associated with a streamline feature and
    interpretation.

    Use StreamlinesFeature to define the vector field that supports the streamlines, i.e., describes what flux is being traced.
    Use Interpretation to distinguish between shared and differing interpretations.
    Usage Note: When defining streamline geometry, the PatchIndex will not be referenced, and may be set to a value of 0.

    :ivar line_count: Number of streamlines.
    :ivar streamline_wellbores:
    :ivar geometry:
    """

    class Meta:
        name = "obj_StreamlinesRepresentation"

    line_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "LineCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    streamline_wellbores: Optional[StreamlineWellbores] = field(
        default=None,
        metadata={
            "name": "StreamlineWellbores",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    geometry: Optional[StreamlinePolylineSetPatch] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjStructuralOrganizationInterpretation(
    AbstractOrganizationInterpretation
):
    """
    One of the main types of RESQML organizations, this class gathers boundary
    interpretations (e.g., horizons and faults) plus frontier features and their
    relationships (contacts interpretations), which when taken together define the
    structure of a part of the earth.
    """

    class Meta:
        name = "obj_StructuralOrganizationInterpretation"

    ordering_criteria: Optional[OrderingCriteria] = field(
        default=None,
        metadata={
            "name": "OrderingCriteria",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    faults: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Faults",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    horizons: List[HorizonInterpretationIndex] = field(
        default_factory=list,
        metadata={
            "name": "Horizons",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    sides: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Sides",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    top_frontier: List[str] = field(
        default_factory=list,
        metadata={
            "name": "TopFrontier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    bottom_frontier: List[str] = field(
        default_factory=list,
        metadata={
            "name": "BottomFrontier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjTriangulatedSetRepresentation(AbstractSurfaceRepresentation):
    """A representation based on set of triangulated mesh patches, which gets its
    geometry from a 1D array of points.

    BUSINESS RULE: The orientation of all the triangles of this representation must be consistent.
    """

    class Meta:
        name = "obj_TriangulatedSetRepresentation"

    triangle_patch: List[TrianglePatch] = field(
        default_factory=list,
        metadata={
            "name": "TrianglePatch",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjWellboreFeature(AbstractTechnicalFeature):
    """May refer to one of these:
    wellbore. A unique, oriented path from the bottom of a drilled borehole to the surface of the earth. The path must not overlap or cross itself.
    borehole. A hole excavated in the earth as a result of drilling or boring operations. The borehole may represent the hole of an entire wellbore (when no sidetracks are present), or a sidetrack extension. A borehole extends from an originating point (the surface location for the initial borehole or kickoff point for sidetracks) to a terminating (bottomhole) point.
    sidetrack. A borehole that originates in another borehole as opposed to originating at the surface."""

    class Meta:
        name = "obj_WellboreFeature"

    witsml_wellbore: Optional[WitsmlWellboreReference] = field(
        default=None,
        metadata={
            "name": "WitsmlWellbore",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjWellboreMarkerFrameRepresentation(ObjWellboreFrameRepresentation):
    """
    A well log frame where each entry represents a well marker.
    """

    class Meta:
        name = "obj_WellboreMarkerFrameRepresentation"

    wellbore_marker: List[WellboreMarker] = field(
        default_factory=list,
        metadata={
            "name": "WellboreMarker",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class AbstractGridRepresentation(AbstractRepresentation):
    """
    Abstract class for all grid representations.
    """

    cell_fluid_phase_units: Optional[CellFluidPhaseUnits] = field(
        default=None,
        metadata={
            "name": "CellFluidPhaseUnits",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    parent_window: Optional[AbstractParentWindow] = field(
        default=None,
        metadata={
            "name": "ParentWindow",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    cell_stratigraphic_units: Optional[CellStratigraphicUnits] = field(
        default=None,
        metadata={
            "name": "CellStratigraphicUnits",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class BlockedWellboreRepresentation(ObjBlockedWellboreRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class BoundaryFeature(ObjBoundaryFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class CategoricalProperty(ObjCategoricalProperty):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class CellParentWindow(AbstractParentWindow):
    """
    Parent window for ANY grid indexed as if it were an unstructured cell grid,
    i.e., using a 1D index.

    :ivar cell_indices: Cell indices which list the cells in the parent
        window. BUSINESS RULE: Number of cells must be consistent with
        the child grid cell count.
    :ivar parent_grid:
    """

    cell_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "CellIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_grid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ParentGrid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ColumnLayerParentWindow(AbstractParentWindow):
    """
    Parent window for any column layer grid indexed as if it were an unstructured
    column layer grid, i.e., IJ columns are replaced by a column index.

    :ivar column_indices: Column indices that list the columns in the
        parent window. BUSINESS RULE: Number of columns must be
        consistent with the child grid column count.
    :ivar omit_parent_cells: List of parent cells that are to be
        retained at their original resolution and are not to be included
        within a local grid. The omit allows non-rectangular local grids
        to be specified. 0-based indexing follows #Columns x #Layers
        relative to the parent window cell count, not to the parent
        grid.
    :ivar kregrid:
    :ivar parent_grid:
    """

    column_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ColumnIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    omit_parent_cells: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "OmitParentCells",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    kregrid: Optional[Regrid] = field(
        default=None,
        metadata={
            "name": "KRegrid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_grid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ParentGrid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class CommentProperty(ObjCommentProperty):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class ContinuousProperty(ObjContinuousProperty):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class DiscreteProperty(ObjDiscreteProperty):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class FaultInterpretation(ObjFaultInterpretation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class FrontierFeature(ObjFrontierFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class GeobodyBoundaryInterpretation(ObjGeobodyBoundaryInterpretation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class GeobodyInterpretation(ObjGeobodyInterpretation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class GeologicUnitFeature(ObjGeologicUnitFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class Grid2DRepresentation(ObjGrid2DRepresentation):
    class Meta:
        name = "Grid2dRepresentation"
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class Grid2DSetRepresentation(ObjGrid2DSetRepresentation):
    class Meta:
        name = "Grid2dSetRepresentation"
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class GridConnectionSetRepresentation(ObjGridConnectionSetRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class HorizonInterpretation(ObjHorizonInterpretation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class IjkParentWindow(AbstractParentWindow):
    """
    Parent window for any IJK grid.

    :ivar omit_parent_cells: List of parent cells that are to be
        retained at their original resolution and are not to be included
        within a local grid. The "omit" allows non-rectangular local
        grids to be specified. 0-based indexing follows NI x NJ x NK
        relative to the parent window cell count—not to the parent grid.
    :ivar jregrid:
    :ivar parent_grid:
    :ivar kregrid:
    :ivar iregrid:
    """

    omit_parent_cells: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "OmitParentCells",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    jregrid: Optional[Regrid] = field(
        default=None,
        metadata={
            "name": "JRegrid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_grid: Optional[str] = field(
        default=None,
        metadata={
            "name": "ParentGrid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    kregrid: Optional[Regrid] = field(
        default=None,
        metadata={
            "name": "KRegrid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    iregrid: Optional[Regrid] = field(
        default=None,
        metadata={
            "name": "IRegrid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class OrganizationFeature(ObjOrganizationFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class PlaneSetRepresentation(ObjPlaneSetRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class PointSetRepresentation(ObjPointSetRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class PolylineRepresentation(ObjPolylineRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class PolylineSetRepresentation(ObjPolylineSetRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class RockFluidOrganizationInterpretation(
    ObjRockFluidOrganizationInterpretation
):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class RockFluidUnitInterpretation(ObjRockFluidUnitInterpretation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class SealedVolumeFrameworkRepresentation(
    ObjSealedVolumeFrameworkRepresentation
):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class SeismicLatticeSetFeature(AbstractSeismicSurveyFeature):
    """An unordered set of several seismic lattices.

    Generally, it has no direct interpretation or representation.
    """


@dataclass
class SplitNodePatch(Patch):
    """Optional construction used to introduce additional nodes on coordinate
    lines.

    Used to represent complex geometries, e.g., for stair-step grids and reverse faults.
    BUSINESS RULE: Patch Index must be positive since a patch index of 0 refers to the fundamental column layer coordinate line nodes.

    :ivar count: Number of additional split nodes. Count must be
        positive.
    :ivar parent_node_indices: Parent coordinate line node index for
        each of the split nodes. Used to implicitly define cell
        geometry.
    :ivar cells_per_split_node: Cell indices for each of the split
        nodes. Used to implicitly define cell geometry. List-of-lists
        construction used to support split nodes shared between multiple
        cells.
    :ivar split_faces:
    """

    count: Optional[int] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    parent_node_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "ParentNodeIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    cells_per_split_node: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "CellsPerSplitNode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    split_faces: Optional[SplitFaces] = field(
        default=None,
        metadata={
            "name": "SplitFaces",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class StratigraphicUnitInterpretation(ObjStratigraphicUnitInterpretation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class StreamlinesFeature(ObjStreamlinesFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class StreamlinesRepresentation(ObjStreamlinesRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class StructuralOrganizationInterpretation(
    ObjStructuralOrganizationInterpretation
):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class TriangulatedSetRepresentation(ObjTriangulatedSetRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class UnstructuredGridGeometry(AbstractGridGeometry):
    """Description of the geometry of an unstructured cell grid, which includes
    geometric characteristics, e.g., cell face parity, and supporting topology.

    Each grid cell is defined by a (signed) list of cell faces. Each
    cell face is defined by a list of nodes.

    :ivar cell_shape:
    :ivar node_count: Total number of nodes in the grid. Must be
        positive.
    :ivar face_count: Total number of faces in the grid. Must be
        positive.
    :ivar nodes_per_face: List of nodes per face. node count per face
        can be obtained from the offsets in the first list of list
        array. BUSINESS RULE: faceCount must match the length of the
        first list of list array.
    :ivar faces_per_cell: List of faces per cell. face count per cell
        can be obtained from the offsets in the first list of list
        array. BUSINESS RULE: cellCount must match the length of the
        first list of list array.
    :ivar cell_face_is_right_handed: Boolean mask used to indicate which
        cell faces have an outwardly directed normal following a right
        hand rule. Array length is the sum of the cell face count per
        cell, and the data follows the order of the faces per cell
        resqml list-of-lists.
    :ivar hinge_node_faces:
    :ivar subnode_topology:
    """

    cell_shape: Optional[CellShape] = field(
        default=None,
        metadata={
            "name": "CellShape",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    node_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "NodeCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    face_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "FaceCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    nodes_per_face: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "NodesPerFace",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    faces_per_cell: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "FacesPerCell",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    cell_face_is_right_handed: Optional[AbstractBooleanArray] = field(
        default=None,
        metadata={
            "name": "CellFaceIsRightHanded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    hinge_node_faces: Optional[UnstructuredGridHingeNodeFaces] = field(
        default=None,
        metadata={
            "name": "HingeNodeFaces",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    subnode_topology: Optional[UnstructuredSubnodeTopology] = field(
        default=None,
        metadata={
            "name": "SubnodeTopology",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class WellboreFeature(ObjWellboreFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class WellboreMarkerFrameRepresentation(ObjWellboreMarkerFrameRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class ObjCategoricalPropertySeries(ObjCategoricalProperty):
    """Information specific to one comment property.

    Used to capture comments or annotations associated with a given
    element type in a data-object, for example, associating comments on
    the specific location of a well path.

    :ivar realization_indices: Provide the list of indices corresponding
        to realizations number. For example, if a user wants to send the
        realization corresponding to p10, p20, ... he would write the
        array 10, 20, ... If not provided, then the realization count
        (which could be 1) does not introduce a dimension to the multi-
        dimensional array storage.
    :ivar series_time_indices:
    """

    class Meta:
        name = "obj_CategoricalPropertySeries"

    realization_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "RealizationIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    series_time_indices: Optional[TimeIndices] = field(
        default=None,
        metadata={
            "name": "SeriesTimeIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjCommentPropertySeries(ObjCommentProperty):
    """Information specific to one comment property.

    Used to capture comments or annotations associated with a given
    element type in a data-object, for example, associating comments on
    the specific location of a well path.

    :ivar realization_indices: Provide the list of indices corresponding
        to realizations number. For example, if a user wants to send the
        realization corresponding to p10, p20, ... he would write the
        array 10, 20, ... If not provided, then the realization count
        (which could be 1) does not introduce a dimension to the multi-
        dimensional array storage.
    :ivar series_time_indices:
    """

    class Meta:
        name = "obj_CommentPropertySeries"

    realization_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "RealizationIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    series_time_indices: Optional[TimeIndices] = field(
        default=None,
        metadata={
            "name": "SeriesTimeIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjContinuousPropertySeries(ObjContinuousProperty):
    """Information specific to one comment property.

    Used to capture comments or annotations associated with a given
    element type in a data-object, for example, associating comments on
    the specific location of a well path.

    :ivar realization_indices: Provide the list of indices corresponding
        to realizations number. For example, if a user wants to send the
        realization corresponding to p10, p20, ... he would write the
        array 10, 20, ... If not provided, then the realization count
        (which could be 1) does not introduce a dimension to the multi-
        dimensional array storage.
    :ivar series_time_indices:
    """

    class Meta:
        name = "obj_ContinuousPropertySeries"

    realization_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "RealizationIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    series_time_indices: Optional[TimeIndices] = field(
        default=None,
        metadata={
            "name": "SeriesTimeIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjDiscretePropertySeries(ObjDiscreteProperty):
    """Information specific to one comment property.

    Used to capture comments or annotations associated with a given
    element type in a data-object, for example, associating comments on
    the specific location of a well path.

    :ivar realization_indices: Provide the list of indices corresponding
        to realizations number. For example, if a user wants to send the
        realization corresponding to p10, p20, ... he would write the
        array 10, 20, ... If not provided, then the realization count
        (which could be 1) does not introduce a dimension to the multi-
        dimensional array storage.
    :ivar series_time_indices:
    """

    class Meta:
        name = "obj_DiscretePropertySeries"

    realization_indices: Optional[AbstractIntegerArray] = field(
        default=None,
        metadata={
            "name": "RealizationIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    series_time_indices: Optional[TimeIndices] = field(
        default=None,
        metadata={
            "name": "SeriesTimeIndices",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjFluidBoundaryFeature(ObjBoundaryFeature):
    """A boundary (usually a plane) separating two fluid phases, such as a gas-oil
    contact (GOC), a water-oil contact (WOC), a gas-oil contact (GOC), or others.

    For types, see FluidContact.
    """

    class Meta:
        name = "obj_FluidBoundaryFeature"

    fluid_contact: Optional[FluidContact] = field(
        default=None,
        metadata={
            "name": "FluidContact",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjGeneticBoundaryFeature(ObjBoundaryFeature):
    """A boundary between two units produced by a contrast between two deposits
    that occurred at two different geologic time periods.

    For types, see GeneticBoundaryKind.
    """

    class Meta:
        name = "obj_GeneticBoundaryFeature"

    genetic_boundary_kind: Optional[GeneticBoundaryKind] = field(
        default=None,
        metadata={
            "name": "GeneticBoundaryKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    absolute_age: Optional[Timestamp] = field(
        default=None,
        metadata={
            "name": "AbsoluteAge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjGeobodyFeature(ObjGeologicUnitFeature):
    """A volume of rock that is identified based on some specific attribute, like
    its mineral content or other physical characteristic.

    Unlike stratigraphic or phase units, there is no associated time or
    fluid content semantic. For types, see GeobodyKind.
    """

    class Meta:
        name = "obj_GeobodyFeature"


@dataclass
class ObjNonSealedSurfaceFrameworkRepresentation(
    AbstractSurfaceFrameworkRepresentation
):
    """A collection of contact representations parts, which are a list of contact
    patches with no identity.

    This collection of contact representations is completed by a set of
    representations gathered at the representation set representation
    level.
    """

    class Meta:
        name = "obj_NonSealedSurfaceFrameworkRepresentation"

    non_sealed_contact_representation: List[
        AbstractContactRepresentationPart
    ] = field(
        default_factory=list,
        metadata={
            "name": "NonSealedContactRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjRockFluidUnitFeature(ObjGeologicUnitFeature):
    """A fluid phase plus one or more stratigraphic units.

    A unit may correspond to a pair of horizons that are not adjacent
    stratigraphically, e.g., a coarse zonation, and is often used to
    define the reservoir. For types, see Phase.
    """

    class Meta:
        name = "obj_RockFluidUnitFeature"

    phase: Optional[Phase] = field(
        default=None,
        metadata={
            "name": "Phase",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    fluid_boundary_bottom: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidBoundaryBottom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    fluid_boundary_top: Optional[str] = field(
        default=None,
        metadata={
            "name": "FluidBoundaryTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjSealedSurfaceFrameworkRepresentation(
    AbstractSurfaceFrameworkRepresentation
):
    """A collection of contact representations parts, which are a list of contact
    patches and their identities.

    This collection of contact representations is completed by a set of
    representations gathered at the representation set representation
    level.
    """

    class Meta:
        name = "obj_SealedSurfaceFrameworkRepresentation"

    sealed_contact_representation: List[
        SealedContactRepresentationPart
    ] = field(
        default_factory=list,
        metadata={
            "name": "SealedContactRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjSeismicLineFeature(AbstractSeismicSurveyFeature):
    """Defined by one lateral dimension: trace (lateral). Seismic trace of the 3D seismic survey.
    To specify its location, the seismic feature can be associated with the seismic coordinates of the points of a representation.

    :ivar first_trace_index: The index of the first trace of the seismic
        line.
    :ivar trace_count: The count of traces in the seismic line.
    :ivar trace_index_increment: The constant index increment between
        two consecutive traces.
    :ivar is_part_of:
    """

    class Meta:
        name = "obj_SeismicLineFeature"

    first_trace_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "FirstTraceIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    trace_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "TraceCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    trace_index_increment: Optional[int] = field(
        default=None,
        metadata={
            "name": "TraceIndexIncrement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    is_part_of: Optional[str] = field(
        default=None,
        metadata={
            "name": "IsPartOf",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjSeismicLineSetFeature(AbstractSeismicSurveyFeature):
    """An unordered set of several seismic lines.

    Generally, it has no direct interpretation or representation.
    """

    class Meta:
        name = "obj_SeismicLineSetFeature"


@dataclass
class ObjStratigraphicColumnRankInterpretation(
    AbstractStratigraphicOrganizationInterpretation
):
    """
    A global hierarchy containing an ordered list of stratigraphic unit
    interpretations.
    """

    class Meta:
        name = "obj_StratigraphicColumnRankInterpretation"

    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    stratigraphic_units: List[StratigraphicUnitInterpretationIndex] = field(
        default_factory=list,
        metadata={
            "name": "StratigraphicUnits",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjStratigraphicOccurrenceInterpretation(
    AbstractStratigraphicOrganizationInterpretation
):
    """A local Interpretation—it could be along a well, on a 2D map, or on a 2D
    section or on a part of the global volume of an earth model—of a succession of
    rock feature elements.

    The stratigraphic column rank interpretation composing a stratigraphic occurrence can be ordered by the criteria listed in OrderingCriteria.
    BUSINESS RULE: A representation of a stratigraphic occurrence interpretation can be a wellbore marker or a wellbore frame.
    """

    class Meta:
        name = "obj_StratigraphicOccurrenceInterpretation"

    is_occurrence_of: Optional[str] = field(
        default=None,
        metadata={
            "name": "IsOccurrenceOf",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    geologic_unit_index: List[GeologicUnitInterpretationIndex] = field(
        default_factory=list,
        metadata={
            "name": "GeologicUnitIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjStratigraphicUnitFeature(ObjGeologicUnitFeature):
    """A stratigraphic unit that can have a well-known (e.g., "Jurassic")
    chronostratigraphic top and chronostratigraphic bottom.

    These chronostratigraphic units have no associated interpretations or representations.
    BUSINESS RULE: The name must reference a well-known chronostratigraphic unit (such as "Jurassic"), for example, from the International Commission on Stratigraphy (http://www.stratigraphy.org).
    """

    class Meta:
        name = "obj_StratigraphicUnitFeature"

    chronostratigraphic_bottom: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChronostratigraphicBottom",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    chronostratigraphic_top: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChronostratigraphicTop",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjTectonicBoundaryFeature(ObjBoundaryFeature):
    """A boundary caused by tectonic movement or metamorphism, such as a fault or a
    fracture.

    For types, see TectonicBoundaryKind.
    """

    class Meta:
        name = "obj_TectonicBoundaryFeature"

    tectonic_boundary_kind: Optional[TectonicBoundaryKind] = field(
        default=None,
        metadata={
            "name": "TectonicBoundaryKind",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class AbstractColumnLayerGridGeometry(AbstractGridGeometry):
    """Description of the geometry of a column layer grid, e.g., parity and pinch,
    together with its supporting topology.

    Column layer grid cell geometry is based upon nodes on coordinate
    lines. Geometry is contained within the representation of a grid.
    Point Geometry is that of the column layer coordinate line nodes.
    Coordinate line nodes for all of the coordinate lines, with NKL
    nodes per line. The numbering of these lines follow the pillar
    numbering if no split coordinate lines are present. The unsplit
    coordinate lines share an indexing with the pillars. The numbering
    of the remaining lines are defined in the
    columnsPerSplitCoordinateLine list-of-lists if split coordinate
    lines are present. Pillar numbering is either 1D or 2D, so for
    unfaulted grids, the node dimensions may follow either a 2D or 3D
    array. Otherwise the nodes will be 2D. In HDF5 nodes are stored as
    separate X, Y, Z, values, so add another dimension (size=3) which is
    fastest in HDF5.

    :ivar kdirection:
    :ivar pillar_geometry_is_defined: Indicator that a pillar has at
        least one node with a defined cell geometry. This is considered
        grid meta-data. If the indicator does not indicate that the
        pillar geometry is defined, then this over-rides any other node
        geometry specification. Array index follows #Pillars and so may
        be either 2d or 1d.
    :ivar pillar_shape:
    :ivar cell_geometry_is_defined: Indicator that a cell has a defined
        geometry. This attribute is grid metadata. If the indicator
        shows that the cell geometry is NOT defined, then this attribute
        overrides any other node geometry specification. Array index is
        2D/3D.
    :ivar node_is_colocated_in_kdirection: Optional indicator that two
        adjacent nodes on a coordinate line are colocated. This is
        considered grid meta-data, and is intended to over-ride any
        geometric comparison of node locations. Array index follows
        #CoordinateLines x (NKL-1).
    :ivar node_is_colocated_on_kedge: Optional indicator that two
        adjacent nodes on the KEDGE of a cell are colocated. This is
        considered grid meta-data, and is intended to over-ride any
        geometric comparison of node locations. Array index follows
        #EdgesPerColumn x NKL for unstructured column layer grids and 4
        x NI x NJ x NKL for IJK grids.
    :ivar subnode_topology:
    :ivar split_coordinate_lines:
    :ivar split_nodes:
    """

    kdirection: Optional[Kdirection] = field(
        default=None,
        metadata={
            "name": "KDirection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    pillar_geometry_is_defined: Optional[AbstractBooleanArray] = field(
        default=None,
        metadata={
            "name": "PillarGeometryIsDefined",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    pillar_shape: Optional[PillarShape] = field(
        default=None,
        metadata={
            "name": "PillarShape",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    cell_geometry_is_defined: Optional[AbstractBooleanArray] = field(
        default=None,
        metadata={
            "name": "CellGeometryIsDefined",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    node_is_colocated_in_kdirection: Optional[AbstractBooleanArray] = field(
        default=None,
        metadata={
            "name": "NodeIsColocatedInKDirection",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    node_is_colocated_on_kedge: Optional[AbstractBooleanArray] = field(
        default=None,
        metadata={
            "name": "NodeIsColocatedOnKEdge",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    subnode_topology: Optional[ColumnLayerSubnodeTopology] = field(
        default=None,
        metadata={
            "name": "SubnodeTopology",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    split_coordinate_lines: Optional[ColumnLayerSplitCoordinateLines] = field(
        default=None,
        metadata={
            "name": "SplitCoordinateLines",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    split_nodes: Optional[SplitNodePatch] = field(
        default=None,
        metadata={
            "name": "SplitNodes",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class AbstractColumnLayerGridRepresentation(AbstractGridRepresentation):
    """Abstract class that includes IJK grids and unstructured column layer grids.

    All column layer grids have a layer index K=1,...,NK or K0=0,...,NK-1.
    Cell geometry is characterized by nodes on coordinate lines.

    :ivar nk: Number of layers in the grid. Must be positive.
    :ivar interval_stratigraphic_units:
    """

    nk: Optional[int] = field(
        default=None,
        metadata={
            "name": "Nk",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    interval_stratigraphic_units: Optional[IntervalStratigraphicUnits] = field(
        default=None,
        metadata={
            "name": "IntervalStratigraphicUnits",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class AbstractTruncatedColumnLayerGridRepresentation(
    AbstractGridRepresentation
):
    """Abstract class for truncated IJK grids and truncated unstructured column
    layer grids.

    Each column layer grid class must have a defined geometry in which
    cells are truncated and additional split cells are defined.

    :ivar nk: Number of layers in the grid. Must be positive.
    :ivar truncation_cells:
    """

    nk: Optional[int] = field(
        default=None,
        metadata={
            "name": "Nk",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    truncation_cells: Optional[TruncationCellPatch] = field(
        default=None,
        metadata={
            "name": "TruncationCells",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class AdditionalGridTopology:
    """Additional grid topology and/or patches, if required, for indexable elements
    that otherwise do not have their topology defined within the grid
    representation.

    For example, column edges need to be defined if we wish to have an
    enumeration for the faces of a column layer grid, but not otherwise.
    """

    split_edges: Optional[SplitEdges] = field(
        default=None,
        metadata={
            "name": "SplitEdges",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    split_nodes: Optional[SplitNodePatch] = field(
        default=None,
        metadata={
            "name": "SplitNodes",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    split_column_edges: Optional[ColumnLayerSplitColumnEdges] = field(
        default=None,
        metadata={
            "name": "SplitColumnEdges",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    unstructured_column_edges: Optional[UnstructuredColumnEdges] = field(
        default=None,
        metadata={
            "name": "UnstructuredColumnEdges",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    split_faces: Optional[SplitFaces] = field(
        default=None,
        metadata={
            "name": "SplitFaces",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    ij_split_column_edges: Optional[IjSplitColumnEdges] = field(
        default=None,
        metadata={
            "name": "IjSplitColumnEdges",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    unstructured_subnode_topology: Optional[
        UnstructuredSubnodeTopology
    ] = field(
        default=None,
        metadata={
            "name": "UnstructuredSubnodeTopology",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    column_layer_subnode_topology: Optional[
        ColumnLayerSubnodeTopology
    ] = field(
        default=None,
        metadata={
            "name": "ColumnLayerSubnodeTopology",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class CategoricalPropertySeries(ObjCategoricalPropertySeries):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class CommentPropertySeries(ObjCommentPropertySeries):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class ContinuousPropertySeries(ObjContinuousPropertySeries):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class DiscretePropertySeries(ObjDiscretePropertySeries):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class FluidBoundaryFeature(ObjFluidBoundaryFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class GeneticBoundaryFeature(ObjGeneticBoundaryFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class GeobodyFeature(ObjGeobodyFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class GpGridUnstructuredGridPatch(Patch):
    """Used to specify unstructured cell grid patch(es) within a general purpose
    grid.

    Multiple patches are supported.

    :ivar unstructured_cell_count: Number of unstructured cells.
        Degenerate case (count=0) is allowed for GPGrid.
    :ivar geometry:
    """

    unstructured_cell_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "UnstructuredCellCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    geometry: Optional[UnstructuredGridGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class NonSealedSurfaceFrameworkRepresentation(
    ObjNonSealedSurfaceFrameworkRepresentation
):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class RockFluidUnitFeature(ObjRockFluidUnitFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class SealedSurfaceFrameworkRepresentation(
    ObjSealedSurfaceFrameworkRepresentation
):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class SeismicLineFeature(ObjSeismicLineFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class SeismicLineSetFeature(ObjSeismicLineSetFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class StratigraphicColumnRankInterpretation(
    ObjStratigraphicColumnRankInterpretation
):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class StratigraphicOccurrenceInterpretation(
    ObjStratigraphicOccurrenceInterpretation
):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class StratigraphicUnitFeature(ObjStratigraphicUnitFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class TectonicBoundaryFeature(ObjTectonicBoundaryFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class ObjSeismicLatticeFeature(AbstractSeismicSurveyFeature):
    """Defined by two lateral ordered dimensions: inline (lateral), crossline (lateral and orthogonal to the inline dimension), which are fixed.
    To specify its location, a seismic feature can be associated with the seismic coordinates of the points of a representation.

    :ivar crossline_count: The count of crosslines in the 3D seismic
        survey.
    :ivar crossline_index_increment: The constant index increment
        between two consecutive crosslines of the 3D seismic survey.
    :ivar first_crossline_index: The index of the first crossline of the
        3D seismic survey.
    :ivar first_inline_index: The index of the first inline of the 3D
        seismic survey.
    :ivar inline_count: The count of inlines in the 3D seismic survey.
    :ivar inline_index_increment: The constant index increment between
        two consecutive inlines of the 3D seismic survey.
    :ivar is_part_of:
    """

    class Meta:
        name = "obj_SeismicLatticeFeature"

    crossline_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "CrosslineCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    crossline_index_increment: Optional[int] = field(
        default=None,
        metadata={
            "name": "CrosslineIndexIncrement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    first_crossline_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "FirstCrosslineIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    first_inline_index: Optional[int] = field(
        default=None,
        metadata={
            "name": "FirstInlineIndex",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    inline_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "InlineCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    inline_index_increment: Optional[int] = field(
        default=None,
        metadata={
            "name": "InlineIndexIncrement",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    is_part_of: Optional[SeismicLatticeSetFeature] = field(
        default=None,
        metadata={
            "name": "IsPartOf",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjUnstructuredGridRepresentation(AbstractGridRepresentation):
    """Unstructured grid representation characterized by a cell count, and
    potentially nothing else.

    Both the oldest and newest simulation formats are based on this
    format.

    :ivar cell_count: Number of cells in the grid. Must be positive.
    :ivar geometry:
    """

    class Meta:
        name = "obj_UnstructuredGridRepresentation"

    cell_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "CellCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    geometry: Optional[UnstructuredGridGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class IjkGridGeometry(AbstractColumnLayerGridGeometry):
    """Explicit geometry definition for the cells of the IJK grid.

    Grid options are also defined through this object.

    :ivar grid_is_righthanded: Indicates that the IJK grid is right
        handed, as determined by the triple product of tangent vectors
        in the I, J, and K directions.
    :ivar ij_gaps:
    """

    grid_is_righthanded: Optional[bool] = field(
        default=None,
        metadata={
            "name": "GridIsRighthanded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    ij_gaps: Optional[IjGaps] = field(
        default=None,
        metadata={
            "name": "IjGaps",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class RepresentationIdentity:
    """Indicates the nature of the relationship between 2 or more representations,
    specifically if they are partially or totally identical.

    For possible types of relationships, see IdentityKind.

    :ivar identical_element_count: Number of elements within each
        representation for which a representation identity is specified.
    :ivar element_identity:
    :ivar additional_grid_topology:
    """

    identical_element_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "IdenticalElementCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    element_identity: List[ElementIdentity] = field(
        default_factory=list,
        metadata={
            "name": "ElementIdentity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 2,
        },
    )
    additional_grid_topology: Optional[AdditionalGridTopology] = field(
        default=None,
        metadata={
            "name": "AdditionalGridTopology",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class SeismicLatticeFeature(ObjSeismicLatticeFeature):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class UnstructuredColumnLayerGridGeometry(AbstractColumnLayerGridGeometry):
    """Description of the geometry of an unstructured column layer grid, e.g.,
    parity and pinch, together with its supporting topology.

    Unstructured column layer cell geometry is derived from column layer
    cell geometry and hence is based upon nodes on coordinate lines.
    Geometry is contained within the representation of a grid.

    :ivar column_shape:
    :ivar pillar_count: Number of pillars in the grid. Must be positive.
        Pillars are used to describe the shape of the columns in the
        grid.
    :ivar pillars_per_column: List of pillars for each column. The
        pillars define the corners of each column. The number of pillars
        per column can be obtained from the offsets in the first list of
        list array. BUSINESS RULE: The length of the first array in the
        list of list construction should equal the columnCount.
    :ivar column_is_right_handed: List of columns which are right
        handed. Right handedness is evaluated following the pillar order
        and the K-direction tangent vector for each column.
    :ivar column_edges:
    """

    column_shape: Optional[ColumnShape] = field(
        default=None,
        metadata={
            "name": "ColumnShape",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    pillar_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "PillarCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    pillars_per_column: Optional[ResqmlJaggedArray] = field(
        default=None,
        metadata={
            "name": "PillarsPerColumn",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    column_is_right_handed: Optional[AbstractBooleanArray] = field(
        default=None,
        metadata={
            "name": "ColumnIsRightHanded",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    column_edges: Optional[UnstructuredColumnEdges] = field(
        default=None,
        metadata={
            "name": "ColumnEdges",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class UnstructuredGridRepresentation(ObjUnstructuredGridRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class ObjSubRepresentation(AbstractRepresentation):
    """An ordered list of indexable elements and/or indexable element pairs of an
    existing representation.

    Because the representation concepts of topology, geometry, and
    property values are separate in RESQML, it is now possible to select
    a range of nodes, edges, faces, or volumes (cell) indices from the
    topological support of an existing representation to define a sub-
    representation. A sub-representation may describe a different
    feature interpretation using the same geometry or property as the
    "parent" representation. In this case, the only information
    exchanged is a set of potentially non-consecutive indices of the
    topological support of the representation.
    """

    class Meta:
        name = "obj_SubRepresentation"

    additional_grid_topology: Optional[AdditionalGridTopology] = field(
        default=None,
        metadata={
            "name": "AdditionalGridTopology",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    supporting_representation: Optional[str] = field(
        default=None,
        metadata={
            "name": "SupportingRepresentation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    sub_representation_patch: List[SubRepresentationPatch] = field(
        default_factory=list,
        metadata={
            "name": "SubRepresentationPatch",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class GpGridIjkGridPatch(Patch):
    """Used to specify IJK grid patch(es) within a general purpose grid.

    Multiple patches are supported.

    :ivar ni: Count of I indices. Degenerate case (ni=0) is allowed for
        GPGrid representations.
    :ivar nj: Count of J indices. Degenerate case (nj=0) is allowed for
        GPGrid representations.
    :ivar radial_grid_is_complete: TRUE if the grid is periodic in J,
        i.e., has the topology of a complete 360 degree circle. If TRUE,
        then NJL=NJ. Otherwise, NJL=NJ+1
    :ivar geometry:
    :ivar truncation_cells:
    """

    ni: Optional[int] = field(
        default=None,
        metadata={
            "name": "Ni",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    nj: Optional[int] = field(
        default=None,
        metadata={
            "name": "Nj",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    radial_grid_is_complete: Optional[bool] = field(
        default=None,
        metadata={
            "name": "RadialGridIsComplete",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    geometry: Optional[IjkGridGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    truncation_cells: Optional[TruncationCellPatch] = field(
        default=None,
        metadata={
            "name": "TruncationCells",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class GpGridUnstructuredColumnLayerGridPatch(Patch):
    """Used to specify unstructured column layer grid patch(es) within a general
    purpose grid.

    Multiple patches are supported.

    :ivar unstructured_column_count: Number of unstructured columns.
        Degenerate case (count=0) is allowed for GPGrid.
    :ivar geometry:
    :ivar truncation_cells:
    """

    unstructured_column_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "UnstructuredColumnCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    geometry: Optional[UnstructuredColumnLayerGridGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    truncation_cells: Optional[TruncationCellPatch] = field(
        default=None,
        metadata={
            "name": "TruncationCells",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class SubRepresentation(ObjSubRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class ObjIjkGridRepresentation(AbstractColumnLayerGridRepresentation):
    """Grid whose topology is characterized by structured column indices (I,J) and
    a layer index, K.

    Cell geometry is characterized by nodes on coordinate lines, where each column of the model has 4 sides. Geometric degeneracy is permitted.
    IJK grids support the following specific extensions:
    IJK radial grids
    K-Layer gaps
    IJ-Column gaps

    :ivar ni: Count of cells in the I-direction in the grid. Must be
        positive. I=1,...,NI, I0=0,...,NI-1.
    :ivar nj: Count of cells in the J-direction in the grid. Must be
        positive. J=1,...,NJ, J0=0,...,NJ-1.
    :ivar radial_grid_is_complete: TRUE if the grid is periodic in J,
        i.e., has the topology of a complete 360 degree circle. If TRUE,
        then NJL=NJ. Otherwise, NJL=NJ+1 May be used to change the grid
        topology for either a cartesian or a radial grid, although
        radial grid usage is by far the more common.
    :ivar kgaps:
    :ivar geometry:
    """

    class Meta:
        name = "obj_IjkGridRepresentation"

    ni: Optional[int] = field(
        default=None,
        metadata={
            "name": "Ni",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    nj: Optional[int] = field(
        default=None,
        metadata={
            "name": "Nj",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    radial_grid_is_complete: Optional[bool] = field(
        default=None,
        metadata={
            "name": "RadialGridIsComplete",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    kgaps: Optional[Kgaps] = field(
        default=None,
        metadata={
            "name": "KGaps",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    geometry: Optional[IjkGridGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class ObjRepresentationIdentitySet(AbstractResqmlDataObject):
    """
    A collection of representation identities.
    """

    class Meta:
        name = "obj_RepresentationIdentitySet"

    representation_identity: List[RepresentationIdentity] = field(
        default_factory=list,
        metadata={
            "name": "RepresentationIdentity",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "min_occurs": 1,
        },
    )


@dataclass
class ObjTruncatedIjkGridRepresentation(
    AbstractTruncatedColumnLayerGridRepresentation
):
    """Grid class with an underlying IJK topology, together with a 1D split cell
    list.

    The truncated IJK cells have more than the usual 6 faces. The split
    cells are arbitrary polyhedra, identical to those of an unstructured
    cell grid.

    :ivar ni: Count of I-indices in the grid. Must be positive.
    :ivar nj: Count of J-indices in the grid. Must be positive.
    :ivar geometry:
    """

    class Meta:
        name = "obj_TruncatedIjkGridRepresentation"

    ni: Optional[int] = field(
        default=None,
        metadata={
            "name": "Ni",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    nj: Optional[int] = field(
        default=None,
        metadata={
            "name": "Nj",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    geometry: Optional[IjkGridGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjTruncatedUnstructuredColumnLayerGridRepresentation(
    AbstractTruncatedColumnLayerGridRepresentation
):
    """Grid class with an underlying unstructured column layer topology, together
    with a 1D split cell list.

    The truncated cells have more than the usual number of faces within
    each column. The split cells are arbitrary polyhedra, identical to
    those of an unstructured cell grid.

    :ivar column_count: Number of unstructured columns in the grid. Must
        be positive.
    :ivar geometry:
    """

    class Meta:
        name = "obj_TruncatedUnstructuredColumnLayerGridRepresentation"

    column_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "ColumnCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    geometry: Optional[UnstructuredColumnLayerGridGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )


@dataclass
class ObjUnstructuredColumnLayerGridRepresentation(
    AbstractColumnLayerGridRepresentation
):
    """Grid whose topology is characterized by an unstructured column index and a
    layer index, K.

    Cell geometry is characterized by nodes on coordinate lines, where
    each column of the model may have an arbitrary number of sides.

    :ivar column_count: Number of unstructured columns in the grid. Must
        be positive.
    :ivar geometry:
    """

    class Meta:
        name = "obj_UnstructuredColumnLayerGridRepresentation"

    column_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "ColumnCount",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    geometry: Optional[UnstructuredColumnLayerGridGeometry] = field(
        default=None,
        metadata={
            "name": "Geometry",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class GpGridColumnLayerGrid:
    """Used to construct a column layer grid patch based upon multiple unstructured
    column layer and IJK grids which share a layering scheme.

    Multiple patches are supported.

    :ivar nk: Number of layers. Degenerate case (nk=0) is allowed for
        GPGrid.
    :ivar kgaps:
    :ivar ijk_grid_patch:
    :ivar unstructured_column_layer_grid_patch:
    """

    nk: Optional[int] = field(
        default=None,
        metadata={
            "name": "Nk",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
            "required": True,
        },
    )
    kgaps: Optional[Kgaps] = field(
        default=None,
        metadata={
            "name": "KGaps",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    ijk_grid_patch: List[GpGridIjkGridPatch] = field(
        default_factory=list,
        metadata={
            "name": "IjkGridPatch",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    unstructured_column_layer_grid_patch: List[
        GpGridUnstructuredColumnLayerGridPatch
    ] = field(
        default_factory=list,
        metadata={
            "name": "UnstructuredColumnLayerGridPatch",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class IjkGridRepresentation(ObjIjkGridRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class RepresentationIdentitySet(ObjRepresentationIdentitySet):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class TruncatedIjkGridRepresentation(ObjTruncatedIjkGridRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class TruncatedUnstructuredColumnLayerGridRepresentation(
    ObjTruncatedUnstructuredColumnLayerGridRepresentation
):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class UnstructuredColumnLayerGridRepresentation(
    ObjUnstructuredColumnLayerGridRepresentation
):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"


@dataclass
class ObjGpGridRepresentation(AbstractGridRepresentation):
    """General purpose (GP) grid representation, which includes and/or extends the
    features from all other grid representations.

    This general purpose representation is included in the schema for
    research and/or advanced modeling purposes, but is not expected to
    be used for routine data transfer.
    """

    class Meta:
        name = "obj_GpGridRepresentation"

    column_layer_grid: List[GpGridColumnLayerGrid] = field(
        default_factory=list,
        metadata={
            "name": "ColumnLayerGrid",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )
    unstructured_grid_patch: List[GpGridUnstructuredGridPatch] = field(
        default_factory=list,
        metadata={
            "name": "UnstructuredGridPatch",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/resqmlv2",
        },
    )


@dataclass
class GpGridRepresentation(ObjGpGridRepresentation):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/resqmlv2"
