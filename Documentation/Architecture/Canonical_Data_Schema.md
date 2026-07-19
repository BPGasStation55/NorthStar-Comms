# NorthStar-Comms Canonical Data Schema

**Document Status:** Initial Architecture
**Target Release:** v0.2.0
**Milestone:** Milestone 1 - Master Database Foundation

---

# 1. Purpose

This document defines the canonical data architecture for NorthStar-Comms.

The schema establishes the structure used to manage:

* Communications channels
* Frequencies
* Repeaters
* Locations
* Radio models
* Radio capabilities
* Export profiles
* Radio-specific channel assignments
* Source provenance
* Verification history
* Validation rules
* Future mission-planning integrations

The schema is designed around the NorthStar-Comms guiding principle:

> **One Database. Every Radio. Every Mission.**

The initial implementation will use Microsoft Excel as the primary data-management interface.

The architecture must remain sufficiently structured to allow future migration to:

* SQLite
* PostgreSQL
* Desktop applications
* APIs
* Automated build systems

without fundamentally redesigning the canonical data model.

---

# 2. Core Architecture Principles

## 2.1 Single Source of Truth

Canonical communications data should be stored once.

Generated outputs such as:

* CSV files
* Radio codeplugs
* Channel cards
* ICS communications plans
* Reference sheets
* Mission packages

must derive from canonical source data whenever practical.

Generated files must not become independent sources of truth.

---

## 2.2 Stable Canonical Identifiers

Every canonical communications channel receives an immutable NorthStar-Comms identifier.

Format:

```text
NSC-XXX
```

Examples:

```text
NSC-001
NSC-002
NSC-043
NSC-128
```

The numeric component uses a minimum width of three digits.

If the database exceeds 999 records, identifiers continue naturally:

```text
NSC-999
NSC-1000
NSC-1001
```

Existing identifiers must never be renumbered to maintain formatting width.

Canonical IDs:

* Never change after assignment
* Are never reused
* Do not encode service, geography, or radio model
* Remain valid if channel numbers change
* Remain valid if a channel is deprecated
* Remain valid across all radio platforms

---

## 2.3 Identity Is Separate From Memory Position

The canonical identifier is not the same as a programmed radio memory number.

Example:

```text
Canonical ID:
NSC-043

Master Channel Number:
43

UV-5R Memory:
43

GM25 Memory:
43

UV32 Memory:
43

Future Mission Profile:
Memory 12
```

`NSC-043` identifies the communications resource permanently.

The memory number determines where that resource appears in a specific radio or export profile.

---

## 2.4 IDs Must Be Non-Semantic

Canonical IDs must not encode:

* Radio service
* Geographic region
* Channel bank
* Radio manufacturer
* Mission
* Frequency

For example, `NSC-043` should not mean "GMRS repeater number 43."

This prevents identifier instability when records are reorganized.

---

## 2.5 No Comma-Separated Relationships

Relational information must not be stored as comma-separated lists.

Do not store:

```text
Compatible_Radios:
UV5R, GM25, UV32
```

Instead, radio compatibility will be determined through:

* Radio model capabilities
* Export profiles
* Profile-to-channel mappings

This allows the same architecture to migrate to a relational database later.

---

# 3. Identifier Namespaces

The following identifier namespaces are established.

| Entity              | Format    | Example   |
| ------------------- | --------- | --------- |
| Canonical Channel   | `NSC-###` | `NSC-001` |
| Repeater            | `RPT-###` | `RPT-001` |
| Radio Model         | `RMD-###` | `RMD-001` |
| Radio Instance      | `RDI-###` | `RDI-001` |
| Location            | `LOC-###` | `LOC-001` |
| Source              | `SRC-###` | `SRC-001` |
| Export Profile      | `EXP-###` | `EXP-001` |
| Verification Record | `VER-###` | `VER-001` |
| Mission Profile     | `MIS-###` | `MIS-001` |
| Field Test          | `TST-###` | `TST-001` |

All identifier namespaces follow the same rules:

* Stable
* Immutable
* Never reused
* Minimum numeric width of three digits
* Expand naturally beyond 999

Not all namespaces must be implemented in v0.2.0.

---

# 4. Canonical Data Entities

The initial architecture contains the following primary entities.

```text
CHANNELS
    │
    ├──── REPEATERS
    │        │
    │        └──── LOCATIONS
    │
    ├──── CHANNEL_SOURCES ──── SOURCES
    │
    └──── PROFILE_CHANNELS
                │
                └──── EXPORT_PROFILES
                           │
                           └──── RADIO_MODELS
                                      │
                                      └──── RADIO_CAPABILITIES

ALL ENTITIES
    │
    └──── VERIFICATION_LOG
```

Future entities include:

```text
RADIO_INSTANCES
MISSION_PROFILES
MISSION_CHANNELS
FIELD_TESTS
EQUIPMENT
DEPLOYMENTS
```

---

# 5. Entity: CHANNELS

## Purpose

`CHANNELS` is the canonical source for communications channel configuration.

Each row represents one distinct communications resource.

Examples:

* GMRS simplex channel
* GMRS repeater
* Amateur simplex channel
* Amateur repeater
* NOAA receive channel
* Aviation receive channel
* MURS channel
* Railroad receive channel

---

## Required Fields

| Field                              | Type         |    Required | Description                                        |
| ---------------------------------- | ------------ | ----------: | -------------------------------------------------- |
| `NSC_ID`                           | Text         |         Yes | Immutable canonical identifier                     |
| `Master_Channel_Number`            | Integer      |         Yes | Default fleet-wide channel number                  |
| `Canonical_Name`                   | Text         |         Yes | Human-readable canonical name                      |
| `Service`                          | Enum         |         Yes | Radio service or frequency category                |
| `Channel_Type`                     | Enum         |         Yes | Functional channel type                            |
| `RX_Frequency_MHz`                 | Decimal      |         Yes | Receive frequency in MHz                           |
| `TX_Frequency_MHz`                 | Decimal      | Conditional | Transmit frequency in MHz                          |
| `Modulation`                       | Enum         |         Yes | FM, NFM, AM, DMR, etc.                             |
| `Bandwidth`                        | Enum         |         Yes | Canonical bandwidth designation                    |
| `TX_Tone_Type`                     | Enum         |         Yes | None, CTCSS, DCS, etc.                             |
| `TX_Tone_Value`                    | Text/Decimal | Conditional | Encode tone/code                                   |
| `TX_Tone_Polarity`                 | Enum         | Conditional | DCS polarity if applicable                         |
| `RX_Tone_Type`                     | Enum         |         Yes | None, CTCSS, DCS, etc.                             |
| `RX_Tone_Value`                    | Text/Decimal | Conditional | Decode tone/code                                   |
| `RX_Tone_Polarity`                 | Enum         | Conditional | DCS polarity if applicable                         |
| `Default_Power_Class`              | Enum         |         Yes | Low, Mid, High, or Radio Default                   |
| `Project_TX_Mode`                  | Enum         |         Yes | TX Enabled or RX Only                              |
| `Required_License_Class`           | Enum         |         Yes | Required authorization category                    |
| `Equipment_Authorization_Required` | Boolean      |         Yes | Whether authorized/certified equipment is required |
| `Scan_Default`                     | Boolean      |         Yes | Default scan inclusion                             |
| `Busy_Lock_Default`                | Boolean      |         Yes | Default busy-channel lockout                       |
| `Operational_Category`             | Enum/Text    |         Yes | Family, GMRS, Weather, Ham, etc.                   |
| `Lifecycle_Status`                 | Enum         |         Yes | Active, Reserved, Deprecated, Disabled             |
| `Notes`                            | Text         |          No | Administrative or operational notes                |

---

## Example

```text
NSC_ID: NSC-001
Master_Channel_Number: 1
Canonical_Name: FAMILY PRIMARY
Service: GMRS
Channel_Type: SIMPLEX
RX_Frequency_MHz: 462.XXXXXX
TX_Frequency_MHz: 462.XXXXXX
Modulation: FM
Bandwidth: WIDE
TX_Tone_Type: NONE
RX_Tone_Type: NONE
Default_Power_Class: HIGH
Project_TX_Mode: TX_ENABLED
Required_License_Class: GMRS
Equipment_Authorization_Required: TRUE
Scan_Default: TRUE
Busy_Lock_Default: TRUE
Operational_Category: FAMILY
Lifecycle_Status: ACTIVE
```

Actual production frequency data will be populated only after verification.

---

# 6. Master Channel Number

`Master_Channel_Number` represents the preferred fleet-wide human channel number.

It is distinct from `NSC_ID`.

Example:

```text
NSC_ID                  NSC-043
Master_Channel_Number   43
```

Unlike `NSC_ID`, the master channel number may change during a future channel-plan revision.

The goal is to keep master channel numbers consistent across radios whenever hardware capacity permits.

Radio-specific memory assignments are stored separately.

---

# 7. Frequency Storage Standard

All canonical frequencies will be stored in:

```text
MHz
```

using numeric values with sufficient precision for at least six decimal places.

Example:

```text
462.562500
146.520000
121.500000
```

Frequency fields must remain numeric rather than formatted text whenever practical.

Do not store units inside frequency cells.

Correct:

```text
462.562500
```

Incorrect:

```text
462.5625 MHz
```

---

# 8. Channel Type Controlled Vocabulary

Initial permitted values:

```text
SIMPLEX
REPEATER
CALLING
WEATHER
INTEROP
RECEIVE_ONLY
DATA
SPECIAL
```

Additional values may be added through the validation system.

---

# 9. Service Controlled Vocabulary

Initial values may include:

```text
GMRS
FRS
MURS
AMATEUR
NOAA
AIRBAND
MARINE
RAILROAD
PUBLIC_SAFETY_RX
BUSINESS_RX
INTEROP
OTHER_RX
```

The Data Dictionary will define each value precisely.

Service values must not be invented independently inside data rows.

---

# 10. Project TX Mode

`Project_TX_Mode` controls whether NorthStar-Comms intends an exported channel to permit transmission.

Initial values:

```text
TX_ENABLED
RX_ONLY
```

This field is independent from whether a frequency could theoretically be transmitted on under some authorization.

Examples:

Aviation monitoring channel:

```text
Project_TX_Mode:
RX_ONLY
```

Amateur simplex channel:

```text
Project_TX_Mode:
TX_ENABLED
```

with appropriate license metadata.

Exporters should enforce receive-only behavior whenever supported by the target radio.

If a radio cannot reliably enforce receive-only behavior, the exporter or documentation should generate a warning.

---

# 11. Authorization Metadata

NorthStar-Comms should distinguish programming intent from regulatory authorization.

## Required_License_Class

Initial values:

```text
NONE
GMRS
AMATEUR
AVIATION
MARINE
COMMERCIAL
SPECIAL_AUTHORIZATION
UNKNOWN
```

## Equipment_Authorization_Required

Boolean:

```text
TRUE
FALSE
```

These fields are informational and validation-oriented.

They do not constitute legal advice or automatically determine whether a specific user may transmit.

---

# 12. Tone Architecture

Encode and decode tones must be stored separately.

Do not use one combined field in the canonical database.

## Tone Type

Initial values:

```text
NONE
CTCSS
DCS
```

Future expansion may include digital access methods.

## Tone Value

Examples:

```text
141.3
100.0
431
```

## DCS Polarity

Initial values:

```text
NORMAL
INVERTED
NONE
```

Radio exporters are responsible for converting canonical tone representation into each manufacturer's required format.

---

# 13. Entity: REPEATERS

## Purpose

`REPEATERS` stores metadata specific to physical repeater systems.

Radio programming parameters remain in `CHANNELS`.

This prevents duplicating:

* RX frequency
* TX frequency
* Tones
* Bandwidth

between tables.

Each repeater record references its canonical channel using `NSC_ID`.

---

## Fields

| Field                   | Type | Required | Description                          |
| ----------------------- | ---- | -------: | ------------------------------------ |
| `Repeater_ID`           | Text |      Yes | Stable `RPT-###` identifier          |
| `NSC_ID`                | FK   |      Yes | Associated canonical channel         |
| `Repeater_Name`         | Text |      Yes | Human-readable repeater name         |
| `Callsign`              | Text |       No | Callsign where applicable            |
| `Owner_Organization`    | Text |       No | Owner or managing organization       |
| `Access_Type`           | Enum |      Yes | Open, Permission, Private, Unknown   |
| `Network`               | Text |       No | Linked network or system             |
| `Location_ID`           | FK   |       No | Geographic location                  |
| `Coverage_Notes`        | Text |       No | Descriptive coverage information     |
| `Access_Notes`          | Text |       No | Permission or usage requirements     |
| `Operational_Status`    | Enum |      Yes | Active, Unknown, Offline, Deprecated |
| `Last_Confirmed_On_Air` | Date |       No | Most recent field confirmation       |
| `Notes`                 | Text |       No | Additional information               |

---

# 14. Entity: LOCATIONS

## Purpose

Stores reusable geographic information.

---

## Fields

| Field                | Type    |
| -------------------- | ------- |
| `Location_ID`        | Text    |
| `Location_Name`      | Text    |
| `City`               | Text    |
| `County`             | Text    |
| `State_Province`     | Text    |
| `Country`            | Text    |
| `Latitude`           | Decimal |
| `Longitude`          | Decimal |
| `Elevation_m`        | Decimal |
| `Location_Precision` | Enum    |
| `Notes`              | Text    |

Coordinates should use decimal degrees.

The initial geographic reference standard should be WGS84 unless a future GIS architecture explicitly requires otherwise.

Sensitive private residential coordinates should not be included in the public repository.

---

# 15. Entity: RADIO_MODELS

## Purpose

Defines radio hardware models supported by NorthStar-Comms.

A radio model is different from an individual physical radio.

Example:

```text
Radio Model:
Baofeng UV-5R

Physical Radios:
UV5R-Unit-01
UV5R-Unit-02
```

---

## Fields

| Field                     | Type          | Required |
| ------------------------- | ------------- | -------: |
| `Radio_Model_ID`          | Text          |      Yes |
| `Manufacturer`            | Text          |      Yes |
| `Model`                   | Text          |      Yes |
| `Model_Family`            | Text          |       No |
| `Max_Memories`            | Integer       |      Yes |
| `Channel_Name_Max_Length` | Integer       |      Yes |
| `Supported_Power_Labels`  | Text/Relation |      Yes |
| `Programming_Software`    | Text          |       No |
| `Import_Format`           | Text          |       No |
| `Export_Format`           | Text          |       No |
| `Template_File`           | Text          |       No |
| `Active_Support`          | Boolean       |      Yes |
| `Notes`                   | Text          |       No |

Initial radio models:

```text
Baofeng UV-5R
Baofeng GM25 / GM15 Pro
Baofeng UV32 / DM32
```

Exact model naming and capability distinctions will be validated before production use.

---

# 16. Entity: RADIO_CAPABILITIES

## Purpose

Stores radio capability ranges without placing multiple frequency ranges into one text field.

A radio can have multiple capability rows.

Example:

```text
Radio_Model_ID: RMD-001
Capability_Type: RECEIVE
Frequency_Min_MHz: 136.000000
Frequency_Max_MHz: 174.000000
```

Another row may define a separate UHF range.

---

## Fields

| Field               | Type    |
| ------------------- | ------- |
| `Radio_Model_ID`    | FK      |
| `Capability_Type`   | Enum    |
| `Frequency_Min_MHz` | Decimal |
| `Frequency_Max_MHz` | Decimal |
| `Modulation`        | Enum    |
| `Transmit_Capable`  | Boolean |
| `Receive_Capable`   | Boolean |
| `Notes`             | Text    |

This table describes technical capability.

It does not imply regulatory authorization to transmit.

---

# 17. Entity: EXPORT_PROFILES

## Purpose

Defines a specific programming configuration for a radio model.

This separation is critical because one radio model may eventually have multiple codeplugs.

Examples:

```text
UV5R - MASTER 128
UV5R - OVERLAND
UV5R - FAMILY
UV32 - FULL MASTER
GM25 - FAMILY GMRS
```

---

## Fields

| Field               | Type    |
| ------------------- | ------- |
| `Export_Profile_ID` | Text    |
| `Profile_Name`      | Text    |
| `Radio_Model_ID`    | FK      |
| `Profile_Purpose`   | Text    |
| `Profile_Version`   | Text    |
| `Max_Memory_Count`  | Integer |
| `Active`            | Boolean |
| `Notes`             | Text    |

---

# 18. Entity: PROFILE_CHANNELS

## Purpose

Maps canonical channels to radio memory positions.

This is where the distinction between canonical identity and radio programming becomes operational.

---

## Fields

| Field                   | Type    | Description                  |
| ----------------------- | ------- | ---------------------------- |
| `Export_Profile_ID`     | FK      | Target programming profile   |
| `NSC_ID`                | FK      | Canonical channel            |
| `Memory_Number`         | Integer | Radio memory position        |
| `Enabled`               | Boolean | Include in export            |
| `Display_Name_Override` | Text    | Optional radio-specific name |
| `Power_Override`        | Enum    | Optional                     |
| `Bandwidth_Override`    | Enum    | Optional                     |
| `Scan_Add_Override`     | Boolean | Optional                     |
| `Busy_Lock_Override`    | Boolean | Optional                     |
| `TX_Inhibit_Override`   | Boolean | Optional                     |
| `PTT_ID`                | Text    | Radio-specific if applicable |
| `SigCode`               | Text    | Radio-specific if applicable |
| `Notes`                 | Text    | Export-specific notes        |

Frequency values should not normally be overridden here.

A different operating frequency should generally represent a different canonical channel.

---

# 19. Radio-Specific Display Names

The canonical channel name must remain independent from hardware display limitations.

Example:

```text
Canonical_Name:
FAMILY PRIMARY
```

Radio-specific rendering may be:

```text
UV32:
FAMILY PRIMARY

UV-5R:
FAMILY PRIMARY

GM25:
FAMPRI
```

The exporter may use:

1. An explicit `Display_Name_Override`, or
2. A deterministic naming rule.

For the initial supported radios:

```text
GM25 / GM15 Pro:
Maximum 6 characters

UV32 / DM32:
Maximum 15 characters

UV-5R:
Maximum 15 characters
```

These limits should be validated against actual programming software and hardware before being marked field verified.

---

# 20. Entity: SOURCES

## Purpose

Tracks where communications data originated.

---

## Fields

| Field                    | Type |
| ------------------------ | ---- |
| `Source_ID`              | Text |
| `Source_Type`            | Enum |
| `Source_Name`            | Text |
| `Publisher_Organization` | Text |
| `Source_URL`             | Text |
| `Published_Date`         | Date |
| `Accessed_Date`          | Date |
| `Notes`                  | Text |

Initial source types:

```text
OFFICIAL
REPEATER_OWNER
MANUFACTURER
DIRECTORY
FIELD_TEST
COMMUNITY
OTHER
```

---

# 21. Entity: CHANNEL_SOURCES

## Purpose

Allows one channel to reference multiple sources without duplicating source information.

---

## Fields

| Field               | Type    |
| ------------------- | ------- |
| `NSC_ID`            | FK      |
| `Source_ID`         | FK      |
| `Relationship_Type` | Enum    |
| `Primary_Source`    | Boolean |
| `Notes`             | Text    |

A channel may have:

* One authoritative regulatory source
* One repeater-directory source
* One owner confirmation
* One field-verification record

without placing multiple URLs into the channel row.

---

# 22. Entity: VERIFICATION_LOG

## Purpose

Tracks verification events over time.

Verification history should be preserved rather than overwritten.

---

## Fields

| Field                 | Type        |
| --------------------- | ----------- |
| `Verification_ID`     | Text        |
| `Entity_Type`         | Enum        |
| `Entity_ID`           | Text        |
| `Verification_Status` | Enum        |
| `Verification_Method` | Enum        |
| `Verified_Date`       | Date        |
| `Verified_By`         | Text        |
| `Source_ID`           | FK/Optional |
| `Result`              | Enum        |
| `Notes`               | Text        |

---

## Verification Status Values

```text
UNVERIFIED
COMMUNITY_REPORTED
SOURCE_VERIFIED
FIELD_VERIFIED
DEPRECATED
```

## Verification Method Examples

```text
SOURCE_REVIEW
OWNER_CONFIRMATION
CPS_IMPORT
RADIO_PROGRAMMING
ON_AIR_TEST
FIELD_RANGE_TEST
OTHER
```

Verification is an event history.

A record should not lose previous verification history when rechecked.

---

# 23. Entity: VALIDATION_LISTS

## Purpose

Defines controlled vocabulary used by the workbook and future software.

---

## Fields

```text
Validation_Group
Allowed_Value
Display_Label
Description
Sort_Order
Active
```

Examples:

```text
Service | GMRS
Service | AMATEUR
Tone_Type | NONE
Tone_Type | CTCSS
Power_Class | LOW
Power_Class | MID
Power_Class | HIGH
```

Excel dropdown lists should derive from this table.

Future software should use the same canonical values.

---

# 24. Entity: DATA_CHANGE_LOG

This is distinct from the repository-level `CHANGELOG.md`.

## Purpose

Tracks significant changes to canonical data records.

---

## Fields

```text
Change_ID
Entity_Type
Entity_ID
Change_Date
Changed_By
Change_Type
Previous_Value
New_Value
Reason
Source_ID
Release_Version
Notes
```

This supports future auditing of changes such as:

```text
Repeater tone changed
Repeater deprecated
Frequency corrected
Channel renamed
Verification status updated
```

---

# 25. Future Entity: RADIO_INSTANCES

Not required for initial v0.2.0 implementation.

This entity will represent individual physical radios.

Example:

```text
RDI-001
Baofeng UV-5R
Family Unit 1
```

Future fields may include:

* Asset name
* Serial number
* Firmware
* Assigned user
* Battery inventory
* Programming version
* Last programmed date
* Maintenance status

Sensitive identifiers should be handled carefully in public repositories.

---

# 26. Future Entity: MISSION_PROFILES

Not required for initial v0.2.0 implementation.

Mission profiles will eventually support:

```text
Family Convoy
Overlanding
Base Camp
Search and Rescue
Winter Storm
Tornado Response
Homestead Operations
Off-Road Recovery
```

Mission profiles will reference canonical `NSC_ID` values rather than duplicate frequency information.

---

# 27. Future Entity: FIELD_TESTS

Not required for initial v0.2.0 implementation.

Field testing may eventually record:

```text
TST_ID
Date
Location
Radio
Antenna
Power
NSC_ID
Distance
Signal Report
GPS Data
Environmental Conditions
Result
Notes
```

This data may later support empirical coverage mapping.

---

# 28. Canonical Data Formatting Rules

## Text

Use plain text without unnecessary formatting characters.

## Dates

Use ISO-style dates:

```text
YYYY-MM-DD
```

Example:

```text
2026-07-19
```

## Booleans

Canonical values:

```text
TRUE
FALSE
```

Radio exporters may translate these into:

```text
Yes
No
On
Off
1
0
```

as required by programming software.

## Null Values

Blank/null values should represent unknown or not applicable data.

Do not substitute ambiguous strings such as:

```text
N/A
-
?
NONE
```

unless `NONE` is a defined controlled vocabulary value for that specific field.

## Frequencies

Store in MHz as numeric values.

## Coordinates

Store latitude and longitude as decimal degrees.

## IDs

Store identifiers as text.

---

# 29. Canonical vs Export Values

The master database stores canonical values.

Radio exporters translate them into manufacturer-specific terminology.

Example:

```text
Canonical:
Power = HIGH

UV-5R CPS:
High

Canonical:
Tone Type = NONE

UV-5R CPS:
None

Canonical:
Scan = TRUE

UV-5R CPS:
Yes
```

The canonical schema must not be distorted solely to match one manufacturer's CSV terminology.

Translation belongs in the export layer.

---

# 30. Radio Export Architecture

The target architecture is:

```text
CHANNELS
      +
RADIO_MODELS
      +
RADIO_CAPABILITIES
      +
EXPORT_PROFILES
      +
PROFILE_CHANNELS
      ↓
VALIDATION ENGINE
      ↓
RADIO EXPORT ADAPTER
      ↓
Manufacturer CSV / Codeplug
```

Each radio model will eventually have an export adapter.

Examples:

```text
UV5R Adapter
GM25 Adapter
UV32 Adapter
```

The adapter converts canonical data into the exact column names and values expected by the relevant programming software.

---

# 31. Initial UV-5R Export Mapping

The currently identified UV-5R programming software fields are:

```text
Channel
Band
RX Frequency
TX Frequency
CTCSS/DCS Dec
CTCSS/DCS Enc
TX Power
W/N
PTT-ID
BusyLock
Scan_Add
SigCode
CH-Name
```

These fields are export-layer fields.

They are not the canonical database schema.

Example mapping:

```text
Master_Channel_Number
        ↓
Channel

RX_Frequency_MHz
        ↓
RX Frequency

TX_Frequency_MHz
        ↓
TX Frequency

RX_Tone
        ↓
CTCSS/DCS Dec

TX_Tone
        ↓
CTCSS/DCS Enc

Default_Power_Class
        ↓
TX Power

Bandwidth
        ↓
W/N

Busy_Lock_Default
        ↓
BusyLock

Scan_Default
        ↓
Scan_Add

Rendered Display Name
        ↓
CH-Name
```

Manufacturer-specific translations will be documented in the Data Dictionary and export specifications.

---

# 32. Referential Integrity Rules

The following rules apply.

## Rule 1

Every `NSC_ID` must be unique.

## Rule 2

An `NSC_ID` may never be reused.

## Rule 3

Every foreign key must reference an existing parent record.

## Rule 4

Every active profile memory number must be unique within that export profile.

## Rule 5

A radio profile cannot exceed the target radio's maximum memory count.

## Rule 6

A rendered channel name cannot exceed the target radio's supported display length.

## Rule 7

Channels marked `RX_ONLY` must not intentionally export a usable transmit configuration when the target radio supports transmit inhibition.

## Rule 8

Required canonical fields cannot be blank.

## Rule 9

Controlled vocabulary fields must use values defined in `VALIDATION_LISTS`.

## Rule 10

Deprecated records remain in the database and retain their identifiers.

---

# 33. Duplicate Detection

Not all duplicate frequencies are errors.

Multiple valid records may share the same frequency.

Examples:

* Different repeaters using the same pair in different locations
* Different operational uses of the same simplex frequency
* Different tone configurations

Validation should distinguish:

```text
Duplicate ID
    = ERROR

Duplicate memory number within one export profile
    = ERROR

Identical canonical record
    = WARNING / REVIEW

Same frequency with different purpose or geography
    = ALLOWED WITH REVIEW
```

Frequency duplication alone must not automatically invalidate a record.

---

# 34. Lifecycle Status

Initial values:

```text
ACTIVE
RESERVED
DEPRECATED
DISABLED
```

## ACTIVE

Current and available for normal project use.

## RESERVED

Identifier or channel position intentionally held for future use.

## DEPRECATED

Historical record retained but no longer recommended.

## DISABLED

Temporarily excluded from active use or exports.

Deprecated IDs are never reused.

---

# 35. Excel Implementation

The initial `Master_Radio_Database.xlsx` should contain separate structured Excel Tables.

Recommended worksheets:

```text
README
Channels
Repeaters
Locations
Radio_Models
Radio_Capabilities
Export_Profiles
Profile_Channels
Sources
Channel_Sources
Verification_Log
Validation_Lists
Data_Change_Log
Export_UV5R
Export_GM25
Export_UV32
```

Generated export sheets must derive from canonical tables whenever practical.

They must not become independent manually maintained databases.

---

# 36. Workbook Design Rules

The workbook should:

* Use Excel Tables rather than unstructured cell ranges
* Use stable machine-readable column headers
* Use data validation dropdowns
* Freeze headers
* Enable filters
* Avoid merged cells in data tables
* Avoid hidden business logic whenever possible
* Document formulas
* Separate canonical data from generated output
* Preserve numeric frequency precision
* Use conditional formatting for validation results
* Support future Python ingestion

Column headers should use:

```text
Upper_Snake_Case
```

Examples:

```text
NSC_ID
Master_Channel_Number
RX_Frequency_MHz
Verification_Status
```

This convention should remain stable after v0.2.0 unless a schema migration is documented.

---

# 37. Required v0.2.0 Entities

The following must be implemented for Milestone 1:

```text
CHANNELS
REPEATERS
LOCATIONS
RADIO_MODELS
RADIO_CAPABILITIES
EXPORT_PROFILES
PROFILE_CHANNELS
SOURCES
CHANNEL_SOURCES
VERIFICATION_LOG
VALIDATION_LISTS
DATA_CHANGE_LOG
```

Future entities should not block v0.2.0.

---

# 38. Schema Change Policy

After the canonical schema is released in v0.2.0:

Any structural change must document:

* Field added, removed, or modified
* Reason
* Data type
* Allowed values
* Required/null behavior
* Impact on existing records
* Impact on exporters
* Migration requirements
* Release version

Breaking schema changes should not be made casually.

---

# 39. Definition of Done - Canonical Schema

The canonical schema is considered complete for Milestone 1 when:

* [ ] Canonical identifier rules are documented
* [ ] `NSC-XXX` identity rules are approved
* [ ] Core entities are defined
* [ ] Entity relationships are defined
* [ ] Canonical channel fields are defined
* [ ] Repeater data structure is defined
* [ ] Radio model structure is defined
* [ ] Radio capability structure is defined
* [ ] Export profile architecture is defined
* [ ] Source provenance structure is defined
* [ ] Verification architecture is defined
* [ ] Validation architecture is defined
* [ ] Data formatting standards are defined
* [ ] Referential integrity rules are defined
* [ ] Excel implementation structure is defined
* [ ] Future database migration is supported by the architecture
* [ ] Schema document committed to the repository

---

# 40. Next Step

After approval of this schema:

```text
Canonical Data Schema
        ↓
Data Dictionary
        ↓
Master_Radio_Database.xlsx
        ↓
Radio Capability Profiles
        ↓
Initial 128-Channel Master Plan
        ↓
CSV Export Validation
```

The Data Dictionary will define each field in detail, including:

* Field name
* Definition
* Data type
* Required status
* Allowed values
* Validation rule
* Example
* Source table
* Export behavior
* Notes

---

## Guiding Principle

> **One Database. Every Radio. Every Mission.**
