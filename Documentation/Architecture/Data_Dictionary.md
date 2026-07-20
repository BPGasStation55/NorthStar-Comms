# NorthStar-Comms Data Dictionary

**Document Status:** Initial Data Standard
**Target Release:** v0.2.0
**Milestone:** Milestone 1 - Master Database Foundation
**Depends On:** `Canonical_Data_Schema.md`

---

# 1. Purpose

This document defines the official field-level data standards used by NorthStar-Comms.

The Data Dictionary establishes:

* Field names
* Field definitions
* Data types
* Required and optional status
* Allowed values
* Validation requirements
* Relationships between entities
* Example values
* Export behavior
* Data ownership

This document is the authoritative reference for interpreting fields within:

* `Master_Radio_Database.xlsx`
* Future SQLite or PostgreSQL databases
* Python automation
* CSV exporters
* Radio programming adapters
* Reference-card generators
* Mission-planning tools
* GIS integrations
* Future APIs

The guiding principle remains:

> **One Database. Every Radio. Every Mission.**

---

# 2. General Data Standards

## 2.1 Field Naming

Canonical field names use:

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

Field names should remain stable after release unless a documented schema migration is performed.

---

## 2.2 Identifier Data Type

All identifiers are stored as text.

Examples:

```text
NSC-001
RPT-001
RMD-001
LOC-001
SRC-001
EXP-001
VER-001
```

Identifiers must never be interpreted as integers.

---

## 2.3 Null Values

A blank value represents:

* Unknown
* Not yet entered
* Not applicable

depending on field context.

Do not use arbitrary placeholders such as:

```text
N/A
?
-
TBD
UNKNOWN
```

unless the field explicitly defines one of those values as part of its controlled vocabulary.

---

## 2.4 Boolean Values

Canonical boolean values are:

```text
TRUE
FALSE
```

Export adapters may translate these values into radio-specific terminology such as:

```text
Yes / No
On / Off
1 / 0
```

---

## 2.5 Date Format

Canonical dates use:

```text
YYYY-MM-DD
```

Example:

```text
2026-07-19
```

---

## 2.6 Frequency Format

All canonical radio frequencies are stored numerically in MHz.

Examples:

```text
462.562500
146.520000
121.500000
```

The database should preserve at least six decimal places of precision.

Do not include units in frequency cells.

Correct:

```text
462.562500
```

Incorrect:

```text
462.562500 MHz
```

---

## 2.7 Geographic Coordinates

Latitude and longitude are stored as decimal degrees.

Example:

```text
Latitude: 44.854700
Longitude: -93.470800
```

The initial geographic reference standard is WGS84.

---

# 3. Identifier Standards

## 3.1 Canonical Channel Identifier

### Field

```text
NSC_ID
```

### Format

```text
NSC-###
```

Examples:

```text
NSC-001
NSC-043
NSC-128
NSC-999
NSC-1000
```

### Rules

* Required
* Unique
* Immutable
* Never reused
* Never renumbered
* Must not encode service or geography
* Retained after deprecation

---

## 3.2 Other Identifier Namespaces

| Entity          | Field                | Format    |
| --------------- | --------------------  | --------- |
| Repeater        | `Repeater_ID`        | `RPT-###` |
| Radio Model     | `Radio_Model_ID`     | `RMD-###` |
| Radio Instance  | `Radio_Instance_ID`  | `RDI-###` |
| Radio Capability| `Radio_Capability_ID`| `RDI-###` |
| Location        | `Location_ID`        | `LOC-###` |
| Source          | `Source_ID`          | `SRC-###` |
| Export Profile  | `Export_Profile_ID`  | `EXP-###` |
| Verification    | `Verification_ID`    | `VER-###` |
| Mission Profile | `Mission_ID`         | `MIS-###` |
| Field Test      | `Test_ID`            | `TST-###` |
| Data Change     | `Change_ID`          | `CHG-###` |

---

# 4. Entity: CHANNELS

## 4.1 Purpose

The `CHANNELS` entity is the canonical source for communications channel configuration.

One row represents one logically distinct communications resource.

---

## 4.2 Field Definitions

### `NSC_ID`

**Type:** TEXT
**Required:** Yes
**Unique:** Yes
**Primary Key:** Yes

Permanent NorthStar-Comms channel identifier.

Example:

```text
NSC-001
```

Validation:

* Must match `NSC-[0-9]+`
* Must not duplicate another record
* Must never be reused

Export behavior:

Not normally exported directly to consumer radio CPS files unless a supported format provides a metadata field.

---

### `Master_Channel_Number`

**Type:** INTEGER
**Required:** Yes
**Unique:** Normally

Preferred human-facing fleet channel number.

Example:

```text
1
43
128
```

Validation:

* Must be positive integer
* Should be unique among active master-plan channels
* May differ from radio-specific `Memory_Number`

Export behavior:

Used as the default memory position when a profile does not define an alternative assignment.

---

### `Canonical_Name`

**Type:** TEXT
**Required:** Yes

Full descriptive name for the communications resource.

Examples:

```text
FAMILY PRIMARY
GMRS 01
NOAA WEATHER 1
NATIONAL SIMPLEX
```

Validation:

* Cannot be blank
* Should be concise
* Must not be limited by a specific radio display length

Export behavior:

Used as the source for radio-specific channel-name rendering.

---

### `Service`

**Type:** ENUM
**Required:** Yes

Identifies the radio service or frequency category.

Initial allowed values:

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

Export behavior:

Used for:

* Radio compatibility validation
* Regulatory warnings
* Filtering
* Mission planning
* Documentation

---

### `Channel_Type`

**Type:** ENUM
**Required:** Yes

Functional type of channel.

Allowed values:

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

---

### `RX_Frequency_MHz`

**Type:** DECIMAL
**Required:** Yes

Receive frequency in MHz.

Example:

```text
462.562500
```

Validation:

* Must be numeric
* Must be greater than zero
* Must fall within configured validation boundaries
* Must be supported by target radio for export

---

### `TX_Frequency_MHz`

**Type:** DECIMAL
**Required:** Conditional

Transmit frequency in MHz.

Required when:

```text
Project_TX_Mode = TX_ENABLED
```

May be blank when:

```text
Project_TX_Mode = RX_ONLY
```

Validation:

* Numeric when populated
* Must be supported by radio hardware for transmission
* Does not itself imply legal authorization

---

### `Modulation`

**Type:** ENUM
**Required:** Yes

Initial allowed values:

```text
FM
NFM
AM
DMR
OTHER
```

Additional modulation modes may be added through controlled validation lists.

---

### `Bandwidth`

**Type:** ENUM
**Required:** Yes

Canonical bandwidth designation.

Initial values:

```text
WIDE
NARROW
RADIO_DEFAULT
NOT_APPLICABLE
```

Export mappings may translate:

```text
WIDE → Wide
NARROW → Narrow
```

---

### `TX_Tone_Type`

**Type:** ENUM
**Required:** Yes

Transmit encode tone type.

Allowed values:

```text
NONE
CTCSS
DCS
```

Future digital access methods may extend this list.

---

### `TX_Tone_Value`

**Type:** TEXT or DECIMAL
**Required:** Conditional

Encode tone or code.

Examples:

```text
141.3
100.0
431
```

Required when:

```text
TX_Tone_Type != NONE
```

Must be blank when:

```text
TX_Tone_Type = NONE
```

---

### `TX_Tone_Polarity`

**Type:** ENUM
**Required:** Conditional

DCS polarity.

Allowed values:

```text
NONE
NORMAL
INVERTED
```

Required only when:

```text
TX_Tone_Type = DCS
```

---

### `RX_Tone_Type`

**Type:** ENUM
**Required:** Yes

Receive decode tone type.

Allowed values:

```text
NONE
CTCSS
DCS
```

---

### `RX_Tone_Value`

**Type:** TEXT or DECIMAL
**Required:** Conditional

Receive tone/code.

Required when:

```text
RX_Tone_Type != NONE
```

---

### `RX_Tone_Polarity`

**Type:** ENUM
**Required:** Conditional

Allowed values:

```text
NONE
NORMAL
INVERTED
```

Used primarily with DCS.

---

### `Default_Power_Class`

**Type:** ENUM
**Required:** Yes

Preferred power-setting class.

Allowed values:

```text
LOW
MID
HIGH
RADIO_DEFAULT
```

This value describes programming intent rather than a fixed wattage.

A radio export adapter converts the canonical value to a supported radio-specific setting.

---

### `Project_TX_Mode`

**Type:** ENUM
**Required:** Yes

Controls whether NorthStar-Comms intends the channel to permit transmission.

Allowed values:

```text
TX_ENABLED
RX_ONLY
```

This field is independent of legal authorization.

Export behavior:

For `RX_ONLY` channels:

* Exporter should enable transmit inhibit when supported
* If transmit inhibit is unavailable, exporter should use the safest supported configuration
* Validation should generate a warning when hardware cannot enforce receive-only operation

---

### `Required_License_Class`

**Type:** ENUM
**Required:** Yes

Identifies the general authorization category associated with transmission.

Allowed values:

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

This field is informational and validation-oriented.

It does not constitute legal authorization.

---

### `Equipment_Authorization_Required`

**Type:** BOOLEAN
**Required:** Yes

Indicates whether equipment authorization/certification is relevant to lawful transmission in the service.

Allowed values:

```text
TRUE
FALSE
```

---

### `Scan_Default`

**Type:** BOOLEAN
**Required:** Yes

Default inclusion in radio scan behavior.

Allowed values:

```text
TRUE
FALSE
```

Radio exporters may translate to:

```text
Yes
No
```

---

### `Busy_Lock_Default`

**Type:** BOOLEAN
**Required:** Yes

Default busy-channel lockout setting.

Allowed values:

```text
TRUE
FALSE
```

---

### `Operational_Category`

**Type:** ENUM/TEXT
**Required:** Yes

High-level functional grouping.

Initial values:

```text
FAMILY
CONVOY
CAMP
GMRS_STANDARD
GMRS_REPEATER
WEATHER
MURS
AMATEUR
AIRBAND
MARINE
RAILROAD
INTEROP
MONITORING
TRAVEL
EMERGENCY
RESERVED
```

Additional values may be introduced through controlled validation.

---

### `Lifecycle_Status`

**Type:** ENUM
**Required:** Yes

Allowed values:

```text
ACTIVE
RESERVED
DEPRECATED
DISABLED
```

Definitions:

**ACTIVE**
Current and available for project use.

**RESERVED**
Held for planned future use.

**DEPRECATED**
Retained for historical integrity but no longer recommended.

**DISABLED**
Temporarily excluded from normal use or export.

---

### `Notes`

**Type:** TEXT
**Required:** No

Free-text administrative or operational notes.

Notes must not be used as a substitute for structured fields.

---

# 5. Entity: REPEATERS

## 5.1 Purpose

Stores physical repeater-system metadata.

Frequency and programming parameters remain canonical in `CHANNELS`.

---

### `Repeater_ID`

**Type:** TEXT
**Required:** Yes
**Primary Key:** Yes

Format:

```text
RPT-###
```

---

### `NSC_ID`

**Type:** FOREIGN KEY
**Required:** Yes

References:

```text
CHANNELS.NSC_ID
```

The referenced channel should normally use:

```text
Channel_Type = REPEATER
```

---

### `Repeater_Name`

**Type:** TEXT
**Required:** Yes

Human-readable repeater name.

Example:

```text
MINNEAPOLIS 675
```

---

### `Callsign`

**Type:** TEXT
**Required:** No

Repeater or trustee callsign where applicable.

---

### `Owner_Organization`

**Type:** TEXT
**Required:** No

Owner, trustee, club, or managing organization.

---

### `Access_Type`

**Type:** ENUM
**Required:** Yes

Allowed values:

```text
OPEN
PERMISSION_REQUIRED
PRIVATE
UNKNOWN
```

---

### `Network`

**Type:** TEXT
**Required:** No

Linked network or repeater system name.

---

### `Location_ID`

**Type:** FOREIGN KEY
**Required:** No

References:

```text
LOCATIONS.Location_ID
```

---

### `Coverage_Notes`

**Type:** TEXT
**Required:** No

Descriptive coverage information.

Do not treat coverage notes as guaranteed service areas.

---

### `Access_Notes`

**Type:** TEXT
**Required:** No

Access requirements, usage restrictions, or owner instructions.

---

### `Operational_Status`

**Type:** ENUM
**Required:** Yes

Allowed values:

```text
ACTIVE
UNKNOWN
OFFLINE
DEPRECATED
```

---

### `Last_Confirmed_On_Air`

**Type:** DATE
**Required:** No

Most recent known operational confirmation.

---

### `Notes`

**Type:** TEXT
**Required:** No

Additional repeater-specific information.

---

# 6. Entity: LOCATIONS

### `Location_ID`

**Type:** TEXT
**Required:** Yes
**Primary Key:** Yes

Format:

```text
LOC-###
```

---

### `Location_Name`

**Type:** TEXT
**Required:** Yes

Human-readable location description.

---

### `City`

**Type:** TEXT
**Required:** No

---

### `County`

**Type:** TEXT
**Required:** No

---

### `State_Province`

**Type:** TEXT
**Required:** No

Recommended U.S. format:

```text
MN
WI
IA
```

---

### `Country`

**Type:** TEXT
**Required:** Yes

Recommended value:

```text
US
```

for United States records.

---

### `Latitude`

**Type:** DECIMAL
**Required:** No

Decimal degrees.

Valid range:

```text
-90 through +90
```

---

### `Longitude`

**Type:** DECIMAL
**Required:** No

Decimal degrees.

Valid range:

```text
-180 through +180
```

---

### `Elevation_m`

**Type:** DECIMAL
**Required:** No

Elevation in meters.

Unit is encoded in the field name and must not be entered in the cell.

---

### `Location_Precision`

**Type:** ENUM
**Required:** Yes

Allowed values:

```text
EXACT
APPROXIMATE
CITY_CENTER
COUNTY_ONLY
UNKNOWN
```

---

### `Notes`

**Type:** TEXT
**Required:** No

Sensitive private residential coordinates should not be committed to the public database.

---

# 7. Entity: RADIO_MODELS

### `Radio_Model_ID`

**Type:** TEXT
**Required:** Yes
**Primary Key:** Yes

Format:

```text
RMD-###
```

---

### `Manufacturer`

**Type:** TEXT
**Required:** Yes

Example:

```text
Baofeng
```

---

### `Model`

**Type:** TEXT
**Required:** Yes

Examples:

```text
UV-5R
GM25
UV32
```

---

### `Model_Family`

**Type:** TEXT
**Required:** No

Used when multiple branded or closely related variants share an architecture.

Examples may include:

```text
GM15 Pro / GM25 Family
UV32 / DM32 Family
```

---

### `Max_Memories`

**Type:** INTEGER
**Required:** Yes

Maximum supported programmable memory count.

Must be validated against actual programming software and hardware.

---

### `Channel_Name_Max_Length`

**Type:** INTEGER
**Required:** Yes

Maximum supported channel-name length.

Initial known project values:

```text
GM25 / GM15 Pro: 6
UV32 / DM32: 15
UV-5R: 15
```

These values should carry an appropriate verification status until confirmed against hardware/software.

---

### `Supported_Power_Labels`

**Type:** RELATIONAL / CONTROLLED TEXT
**Required:** Yes

Canonical initial power labels:

```text
LOW
MID
HIGH
```

Radio export adapters translate these into manufacturer terminology.

---

### `Programming_Software`

**Type:** TEXT
**Required:** No

Name of supported CPS or programming application.

---

### `Import_Format`

**Type:** TEXT
**Required:** No

Examples:

```text
CSV
DATA
PROPRIETARY
```

---

### `Export_Format`

**Type:** TEXT
**Required:** No

Output format supported by NorthStar-Comms.

---

### `Template_File`

**Type:** TEXT
**Required:** No

Relative repository path to a sanitized programming template where applicable.

---

### `Active_Support`

**Type:** BOOLEAN
**Required:** Yes

Values:

```text
TRUE
FALSE
```

---

### `Notes`

**Type:** TEXT
**Required:** No

Firmware limitations, hardware variants, or implementation notes.

---

# 8. Entity: RADIO_CAPABILITIES

### `Radio_Model_ID`

**Type:** FOREIGN KEY
**Required:** Yes

References:

```text
RADIO_MODELS.Radio_Model_ID

```

### `Radio_Capability_ID`

**Type:** TEXT  
**Required:** Yes  
**Unique:** Yes  
**Primary Key:** Yes

Permanent identifier for an individual radio capability record.

Format:

```text
RCP-###
### `Capability_Type`

**Type:** ENUM
**Required:** Yes

Allowed values:

```text
RECEIVE
TRANSMIT
RECEIVE_TRANSMIT
```

---

### `Frequency_Min_MHz`

**Type:** DECIMAL
**Required:** Yes

Lower boundary of capability range.

---

### `Frequency_Max_MHz`

**Type:** DECIMAL
**Required:** Yes

Upper boundary of capability range.

Validation:

```text
Frequency_Max_MHz >= Frequency_Min_MHz
```

---

### `Modulation`

**Type:** ENUM
**Required:** Yes

Examples:

```text
FM
NFM
AM
DMR
```

---

### `Transmit_Capable`

**Type:** BOOLEAN
**Required:** Yes

Technical hardware capability only.

Does not imply authorization.

---

### `Receive_Capable`

**Type:** BOOLEAN
**Required:** Yes

---

### `Notes`

**Type:** TEXT
**Required:** No

Used for firmware-dependent or hardware-dependent limitations.

---

# 9. Entity: EXPORT_PROFILES

### `Export_Profile_ID`

**Type:** TEXT
**Required:** Yes
**Primary Key:** Yes

Format:

```text
EXP-###
```

---

### `Profile_Name`

**Type:** TEXT
**Required:** Yes

Examples:

```text
UV5R MASTER 128
GM25 MASTER
UV32 FULL MASTER
```

---

### `Radio_Model_ID`

**Type:** FOREIGN KEY
**Required:** Yes

References:

```text
RADIO_MODELS.Radio_Model_ID
```

---

### `Profile_Purpose`

**Type:** TEXT
**Required:** Yes

Examples:

```text
MASTER
FAMILY
OVERLAND
TRAVEL
MISSION
TEST
```

---

### `Profile_Version`

**Type:** TEXT
**Required:** Yes

Recommended format:

```text
v0.2.0
```

---

### `Max_Memory_Count`

**Type:** INTEGER
**Required:** Yes

Must not exceed:

```text
RADIO_MODELS.Max_Memories
```

---

### `Active`

**Type:** BOOLEAN
**Required:** Yes

---

### `Notes`

**Type:** TEXT
**Required:** No

---

# 10. Entity: PROFILE_CHANNELS

## 10.1 Purpose

Maps canonical channels into specific radio programming profiles.

Composite uniqueness requirement:

```text
Export_Profile_ID + Memory_Number
```

must be unique.

---

### `Export_Profile_ID`

**Type:** FOREIGN KEY
**Required:** Yes

References:

```text
EXPORT_PROFILES.Export_Profile_ID
```

---

### `NSC_ID`

**Type:** FOREIGN KEY
**Required:** Yes

References:

```text
CHANNELS.NSC_ID
```

---

### `Memory_Number`

**Type:** INTEGER
**Required:** Yes

Radio-specific memory position.

Validation:

```text
1 <= Memory_Number <= Export_Profile.Max_Memory_Count
```

---

### `Enabled`

**Type:** BOOLEAN
**Required:** Yes

Determines whether record is included in generated export.

---

### `Display_Name_Override`

**Type:** TEXT
**Required:** No

Optional explicit radio-specific channel name.

Must not exceed:

```text
RADIO_MODELS.Channel_Name_Max_Length
```

---

### `Power_Override`

**Type:** ENUM
**Required:** No

Allowed values:

```text
LOW
MID
HIGH
RADIO_DEFAULT
```

Blank means:

```text
Use CHANNELS.Default_Power_Class
```

---

### `Bandwidth_Override`

**Type:** ENUM
**Required:** No

Allowed values:

```text
WIDE
NARROW
RADIO_DEFAULT
```

Blank means use canonical value.

---

### `Scan_Add_Override`

**Type:** BOOLEAN
**Required:** No

Blank means:

```text
Use CHANNELS.Scan_Default
```

---

### `Busy_Lock_Override`

**Type:** BOOLEAN
**Required:** No

Blank means:

```text
Use CHANNELS.Busy_Lock_Default
```

---

### `TX_Inhibit_Override`

**Type:** BOOLEAN
**Required:** No

Used to force transmit inhibition on a specific export.

Must not be used to override a canonical `RX_ONLY` channel into transmitting.

---

### `PTT_ID`

**Type:** TEXT
**Required:** No

Radio-specific setting.

Canonical default:

```text
NONE
```

when supported by target CPS.

---

### `SigCode`

**Type:** TEXT
**Required:** No

Radio-specific signaling code field.

Used only where required by target programming software.

---

### `Notes`

**Type:** TEXT
**Required:** No

---

# 11. Entity: SOURCES

### `Source_ID`

**Type:** TEXT
**Required:** Yes
**Primary Key:** Yes

Format:

```text
SRC-###
```

---

### `Source_Type`

**Type:** ENUM
**Required:** Yes

Allowed values:

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

### `Source_Name`

**Type:** TEXT
**Required:** Yes

Human-readable source title.

---

### `Publisher_Organization`

**Type:** TEXT
**Required:** No

---

### `Source_URL`

**Type:** TEXT
**Required:** No

URL to source where applicable.

---

### `Published_Date`

**Type:** DATE
**Required:** No

Original source publication/update date if known.

---

### `Accessed_Date`

**Type:** DATE
**Required:** Yes for online sources

Date source was reviewed.

---

### `Notes`

**Type:** TEXT
**Required:** No

---

# 12. Entity: CHANNEL_SOURCES

### `NSC_ID`

**Type:** FOREIGN KEY
**Required:** Yes

References:

```text
CHANNELS.NSC_ID
```

---

### `Source_ID`

**Type:** FOREIGN KEY
**Required:** Yes

References:

```text
SOURCES.Source_ID
```

---

### `Relationship_Type`

**Type:** ENUM
**Required:** Yes

Initial values:

```text
REGULATORY
FREQUENCY_REFERENCE
REPEATER_DIRECTORY
OWNER_CONFIRMATION
MANUFACTURER_REFERENCE
FIELD_CONFIRMATION
OTHER
```

---

### `Primary_Source`

**Type:** BOOLEAN
**Required:** Yes

Indicates preferred source for the linked relationship.

---

### `Notes`

**Type:** TEXT
**Required:** No

---

# 13. Entity: VERIFICATION_LOG

### `Verification_ID`

**Type:** TEXT
**Required:** Yes
**Primary Key:** Yes

Format:

```text
VER-###
```

---

### `Entity_Type`

**Type:** ENUM
**Required:** Yes

Initial values:

```text
CHANNEL
REPEATER
LOCATION
RADIO_MODEL
RADIO_CAPABILITY
EXPORT_PROFILE
EXPORT_FILE
OTHER
```

---

### `Entity_ID`

**Type:** TEXT
**Required:** Yes

Identifier of the record being verified.

---

### `Verification_Status`

**Type:** ENUM
**Required:** Yes

Allowed values:

```text
UNVERIFIED
COMMUNITY_REPORTED
SOURCE_VERIFIED
FIELD_VERIFIED
DEPRECATED
```

---

### `Verification_Method`

**Type:** ENUM
**Required:** Yes

Allowed values:

```text
SOURCE_REVIEW
OWNER_CONFIRMATION
CPS_IMPORT
RADIO_PROGRAMMING
ON_AIR_TEST
FIELD_RANGE_TEST
OTHER
```

---

### `Verified_Date`

**Type:** DATE
**Required:** Yes

---

### `Verified_By`

**Type:** TEXT
**Required:** Yes

Person, project contributor, or verification source.

Public repositories should avoid unnecessary sensitive personal information.

---

### `Source_ID`

**Type:** FOREIGN KEY
**Required:** No

References:

```text
SOURCES.Source_ID
```

---

### `Result`

**Type:** ENUM
**Required:** Yes

Allowed values:

```text
PASS
FAIL
PARTIAL
INCONCLUSIVE
```

---

### `Notes`

**Type:** TEXT
**Required:** No

---

# 14. Entity: VALIDATION_LISTS

### `Validation_Group`

**Type:** TEXT
**Required:** Yes

Identifies controlled-value category.

Examples:

```text
Service
Channel_Type
Tone_Type
Power_Class
Lifecycle_Status
```

---

### `Allowed_Value`

**Type:** TEXT
**Required:** Yes

Machine-readable canonical value.

Example:

```text
GMRS
```

---

### `Display_Label`

**Type:** TEXT
**Required:** Yes

Human-readable display value.

Example:

```text
GMRS
```

or:

```text
Permission Required
```

---

### `Description`

**Type:** TEXT
**Required:** Yes

Defines meaning of value.

---

### `Sort_Order`

**Type:** INTEGER
**Required:** Yes

Controls dropdown/display ordering.

---

### `Active`

**Type:** BOOLEAN
**Required:** Yes

Allows controlled values to be retired without deleting historical references.

---

# 15. Entity: DATA_CHANGE_LOG

### `Change_ID`

**Type:** TEXT
**Required:** Yes
**Primary Key:** Yes

Format:

```text
CHG-###
```

---

### `Entity_Type`

**Type:** ENUM
**Required:** Yes

Type of record changed.

---

### `Entity_ID`

**Type:** TEXT
**Required:** Yes

Affected record identifier.

---

### `Change_Date`

**Type:** DATE
**Required:** Yes

---

### `Changed_By`

**Type:** TEXT
**Required:** Yes

---

### `Change_Type`

**Type:** ENUM
**Required:** Yes

Initial values:

```text
CREATE
UPDATE
DEPRECATE
RESTORE
CORRECT
VERIFY
MIGRATE
OTHER
```

---

### `Field_Name`

**Type:** TEXT
**Required:** Conditional

Specific field changed where applicable.

---

### `Previous_Value`

**Type:** TEXT
**Required:** No

---

### `New_Value`

**Type:** TEXT
**Required:** No

---

### `Reason`

**Type:** TEXT
**Required:** Yes

Reason for change.

---

### `Source_ID`

**Type:** FOREIGN KEY
**Required:** No

---

### `Release_Version`

**Type:** TEXT
**Required:** No

Example:

```text
v0.2.1
```

---

### `Notes`

**Type:** TEXT
**Required:** No

---

# 16. Controlled Vocabulary Definitions

## 16.1 Service

| Value              | Definition                                      |
| ------------------ | ----------------------------------------------- |
| `GMRS`             | General Mobile Radio Service                    |
| `FRS`              | Family Radio Service                            |
| `MURS`             | Multi-Use Radio Service                         |
| `AMATEUR`          | Amateur Radio Service                           |
| `NOAA`             | NOAA Weather Radio monitoring                   |
| `AIRBAND`          | Civil aviation band monitoring                  |
| `MARINE`           | Marine communications monitoring                |
| `RAILROAD`         | Railroad communications monitoring              |
| `PUBLIC_SAFETY_RX` | Receive-only public safety monitoring           |
| `BUSINESS_RX`      | Receive-only business communications monitoring |
| `INTEROP`          | Interoperability resource                       |
| `OTHER_RX`         | Other receive-only resource                     |

---

## 16.2 Channel Type

| Value          | Definition                                                      |
| -------------- | --------------------------------------------------------------- |
| `SIMPLEX`      | Same or direct paired operation without repeater infrastructure |
| `REPEATER`     | Uses repeater infrastructure                                    |
| `CALLING`      | Calling or commonly recognized contact channel                  |
| `WEATHER`      | Weather information resource                                    |
| `INTEROP`      | Interoperability channel                                        |
| `RECEIVE_ONLY` | Monitoring-only channel                                         |
| `DATA`         | Data-focused communication                                      |
| `SPECIAL`      | Special-purpose resource                                        |

---

## 16.3 Tone Type

```text
NONE
CTCSS
DCS
```

---

## 16.4 DCS Polarity

```text
NONE
NORMAL
INVERTED
```

---

## 16.5 Power Class

```text
LOW
MID
HIGH
RADIO_DEFAULT
```

Power classes intentionally do not specify wattage.

Actual output power varies by radio model and hardware.

---

## 16.6 Project TX Mode

```text
TX_ENABLED
RX_ONLY
```

---

## 16.7 Lifecycle Status

```text
ACTIVE
RESERVED
DEPRECATED
DISABLED
```

---

## 16.8 Verification Status

```text
UNVERIFIED
COMMUNITY_REPORTED
SOURCE_VERIFIED
FIELD_VERIFIED
DEPRECATED
```

---

## 16.9 Verification Result

```text
PASS
FAIL
PARTIAL
INCONCLUSIVE
```

---

# 17. Validation Severity Levels

NorthStar-Comms validation should distinguish severity.

## ERROR

Export or release should normally be blocked.

Examples:

* Duplicate `NSC_ID`
* Duplicate memory number within one profile
* Required field missing
* Invalid foreign key
* Memory exceeds radio capacity
* Invalid frequency format

---

## WARNING

Requires review but may not block export.

Examples:

* Receive-only channel cannot be hardware TX-inhibited
* Frequency duplicated across different canonical channels
* Source verification is stale
* Radio capability uncertain
* Channel name requires truncation

---

## INFO

Informational notice.

Examples:

* Radio-specific override applied
* Channel omitted from a profile
* Deprecated record retained
* Default value inherited

---

# 18. Export Precedence Rules

When generating a radio programming file, settings should be resolved in this order:

```text
1. Safety / TX Restrictions
        ↓
2. Profile-Specific Override
        ↓
3. Canonical Channel Value
        ↓
4. Radio Export Default
```

A lower-priority setting must never override a higher-priority safety restriction.

Example:

```text
Canonical:
Project_TX_Mode = RX_ONLY

Profile:
TX_Inhibit_Override = FALSE
```

Result:

```text
RX_ONLY remains authoritative
```

A profile cannot enable transmission on a canonical receive-only channel.

---

# 19. Display Name Precedence

Radio display names should resolve as:

```text
1. Display_Name_Override
        ↓
2. Radio-specific deterministic abbreviation
        ↓
3. Canonical_Name truncated only as last resort
```

Name generation must be deterministic.

The same canonical record exported twice for the same radio/profile should produce the same display name.

---

# 20. Initial Radio Export Terminology

## UV-5R CPS

Known field headers:

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

Known value conventions:

```text
TX Power:
Low / Mid / High

BusyLock:
Yes / No

Scan_Add:
Yes / No

Disabled / Off value:
None

Maximum channel name:
15 characters
```

---

## GM25 / GM15 Pro

Known project constraint:

```text
Maximum channel name:
6 characters
```

Detailed import-field mapping must be validated from an actual CPS export template before production generation.

---

## UV32 / DM32

Known project constraint:

```text
Maximum channel name:
15 characters
```

Detailed import-field mapping must be validated from an actual CPS export template before production generation.

---

# 21. Canonical-to-UV5R Export Mapping

| Canonical Source             | UV-5R CPS Field |
| ---------------------------- | --------------- |
| `Memory_Number`              | `Channel`       |
| Radio capability calculation | `Band`          |
| `RX_Frequency_MHz`           | `RX Frequency`  |
| Effective TX frequency       | `TX Frequency`  |
| Effective RX tone            | `CTCSS/DCS Dec` |
| Effective TX tone            | `CTCSS/DCS Enc` |
| Effective power              | `TX Power`      |
| Effective bandwidth          | `W/N`           |
| `PTT_ID`                     | `PTT-ID`        |
| Effective busy lock          | `BusyLock`      |
| Effective scan add           | `Scan_Add`      |
| `SigCode`                    | `SigCode`       |
| Rendered display name        | `CH-Name`       |

The exporter is responsible for converting canonical values into exact CPS terminology.

---

# 22. Radio Compatibility Logic

Radio compatibility should not be manually stored as comma-separated text.

Compatibility is derived from:

```text
CHANNEL
   +
RADIO_CAPABILITIES
   +
Project_TX_Mode
   +
Service constraints
   +
Export adapter capabilities
```

Possible derived compatibility states:

```text
FULL
RX_ONLY
UNSUPPORTED
REQUIRES_REVIEW
```

These states may later be generated dynamically.

---

# 23. Verification Freshness

Verification records should preserve history.

A newer verification does not delete an older verification.

Current status may be calculated from the most recent valid verification event.

Potential future freshness indicators:

```text
CURRENT
AGING
STALE
UNKNOWN
```

Thresholds will be defined separately by data category.

Repeater data may require more frequent review than static national calling frequencies.

---

# 24. Derived Fields

Derived values should not normally be manually maintained when they can be calculated.

Potential derived fields include:

```text
Frequency_Offset_MHz
Compatibility_Status
Rendered_Channel_Name
Verification_Age_Days
Distance_From_Home_Miles
Effective_TX_Power
Effective_Bandwidth
Effective_Scan_Add
```

Derived fields may appear in reporting or export sheets but should not duplicate canonical source data unnecessarily.

---

# 25. Offset Calculation

Repeater offset may be derived as:

```text
TX_Frequency_MHz - RX_Frequency_MHz
```

Examples:

```text
+5.000000
-0.600000
```

The canonical database should store explicit RX and TX frequencies.

Offset should normally be calculated rather than used as the only representation of repeater transmit configuration.

---

# 26. Data Ownership Rules

## Canonical Tables

Manually maintained:

```text
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
```

## Generated Tables

Automatically derived whenever practical:

```text
Export_UV5R
Export_GM25
Export_UV32
Validation_Report
Channel_Cards
Release_Manifest
```

Users should not manually edit generated tables unless performing explicit troubleshooting.

---

# 27. Excel Table Names

Recommended structured-table names:

```text
tblChannels
tblRepeaters
tblLocations
tblRadioModels
tblRadioCapabilities
tblExportProfiles
tblProfileChannels
tblSources
tblChannelSources
tblVerificationLog
tblValidationLists
tblDataChangeLog
```

Generated tables:

```text
tblExportUV5R
tblExportGM25
tblExportUV32
```

These names should remain stable so future Python scripts can reference them reliably.

---

# 28. Workbook Worksheet Names

Recommended worksheet names:

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
Validation_Report
```

Avoid spaces in worksheet names where practical.

---

# 29. Required Field Summary

## CHANNELS

Required:

```text
NSC_ID
Master_Channel_Number
Canonical_Name
Service
Channel_Type
RX_Frequency_MHz
Modulation
Bandwidth
TX_Tone_Type
RX_Tone_Type
Default_Power_Class
Project_TX_Mode
Required_License_Class
Equipment_Authorization_Required
Scan_Default
Busy_Lock_Default
Operational_Category
Lifecycle_Status
```

Conditional:

```text
TX_Frequency_MHz
TX_Tone_Value
TX_Tone_Polarity
RX_Tone_Value
RX_Tone_Polarity
```

Optional:

```text
Notes
```

---

# 30. Data Dictionary Governance

This Data Dictionary is authoritative for canonical field meaning.

Whenever a schema field is:

* Added
* Renamed
* Removed
* Reinterpreted
* Given new allowed values

the following must be reviewed:

```text
Canonical_Data_Schema.md
Data_Dictionary.md
Master_Radio_Database.xlsx
Validation rules
Export adapters
Tests
CHANGELOG.md
```

Breaking changes require documented migration instructions.

---

# 31. Definition of Done - Data Dictionary

The Data Dictionary is complete for Milestone 1 when:

* [ ] General data standards documented
* [ ] Identifier formats documented
* [ ] All required v0.2.0 entities documented
* [ ] All CHANNELS fields defined
* [ ] All REPEATERS fields defined
* [ ] All LOCATIONS fields defined
* [ ] All RADIO_MODELS fields defined
* [ ] All RADIO_CAPABILITIES fields defined
* [ ] All EXPORT_PROFILES fields defined
* [ ] All PROFILE_CHANNELS fields defined
* [ ] All SOURCES fields defined
* [ ] All CHANNEL_SOURCES fields defined
* [ ] All VERIFICATION_LOG fields defined
* [ ] All VALIDATION_LISTS fields defined
* [ ] All DATA_CHANGE_LOG fields defined
* [ ] Controlled vocabularies documented
* [ ] Validation severity levels documented
* [ ] Export precedence rules documented
* [ ] Initial UV-5R export mapping documented
* [ ] Excel worksheet naming defined
* [ ] Excel table naming defined
* [ ] Data ownership rules documented
* [ ] Schema governance process documented
* [ ] Data Dictionary committed to repository

---

# 32. Next Development Step

After approval of the Data Dictionary:

```text
Canonical Schema ✅
        ↓
Data Dictionary ✅
        ↓
Master_Radio_Database.xlsx
        ↓
Radio Capability Profiles
        ↓
Initial 128-Channel Master Plan
        ↓
Export Validation
```

The Excel workbook must implement this Data Dictionary rather than introducing undocumented fields independently.

---

## Guiding Principle

> **One Database. Every Radio. Every Mission.**
