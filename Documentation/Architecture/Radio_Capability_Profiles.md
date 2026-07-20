# NorthStar-Comms Radio Capability Profiles

**Document Status:** Initial Hardware Capability Baseline  
**Target Release:** v0.2.0  
**Milestone:** Milestone 1 - Master Database Foundation  
**Depends On:** `Canonical_Data_Schema.md`, `Data_Dictionary.md`

---

# 1. Purpose

This document defines the initial technical capability profiles for the three radio families currently targeted by NorthStar-Comms:

- Baofeng UV-5R
- Baofeng GM-15 Pro / project GM25 CPS family
- Baofeng DM-32UV

These profiles describe hardware and programming capabilities. They do **not** independently grant authorization to transmit.

Regulatory authorization, service rules, equipment authorization, and project-level transmit restrictions are evaluated separately.

---

# 2. Required Schema Amendment

Before this capability profile is considered final, add a stable primary key to `RADIO_CAPABILITIES`.

## New Identifier Namespace

| Entity | Field | Format |
|---|---|---|
| Radio Capability | `Radio_Capability_ID` | `RCP-###` |

Examples:

```text
RCP-001
RCP-002
RCP-022
```

## Required Field

### `Radio_Capability_ID`

**Type:** TEXT  
**Required:** Yes  
**Unique:** Yes  
**Primary Key:** Yes

Permanent identifier for one radio-capability record.

Validation:

- Must match `RCP-[0-9]+`
- Must not duplicate another capability record
- Must never be reused

Reason:

`Verification_Log.Entity_Type` supports `RADIO_CAPABILITY`, so individual capability records require a stable entity identifier for verification history and change tracking.

---

# 3. Baofeng UV-5R

## Canonical Model

```text
Radio_Model_ID: RMD-001
Manufacturer: Baofeng
Model: UV-5R
Max_Memories: 128
Channel_Name_Max_Length: 15
Power Classes: LOW / HIGH
```

## Capability Summary

| Capability ID | Type | Min MHz | Max MHz | Mode | TX | RX |
|---|---|---:|---:|---|---|---|
| RCP-001 | RECEIVE | 65.000000 | 108.000000 | FM | No | Yes |
| RCP-002 | RECEIVE_TRANSMIT | 136.000000 | 174.000000 | FM | Yes | Yes |
| RCP-003 | RECEIVE_TRANSMIT | 136.000000 | 174.000000 | NFM | Yes | Yes |
| RCP-004 | RECEIVE_TRANSMIT | 400.000000 | 480.000000 | FM | Yes | Yes |
| RCP-005 | RECEIVE_TRANSMIT | 400.000000 | 480.000000 | NFM | Yes | Yes |
| RCP-006 | RECEIVE | 480.000001 | 520.000000 | FM | No | Yes |
| RCP-007 | RECEIVE | 480.000001 | 520.000000 | NFM | No | Yes |

## Notes

The current manufacturer product information lists:

- 128 channels
- High/Low power
- Wide/Narrow operation
- VHF 136-174 MHz
- UHF receive extending to 520 MHz
- Manufacturer comparison data indicating UHF transmit through 480 MHz
- Broadcast FM reception

Hardware and firmware variants exist within the broader UV-5R family. Unit-specific behavior should therefore be field validated before NorthStar-Comms treats edge-of-range behavior as hardware verified.

The UV-5R does not have documented AM aviation-band reception in this profile.

---

# 4. Baofeng GM-15 Pro / GM25 CPS Family

## Canonical Model

```text
Radio_Model_ID: RMD-002
Manufacturer: Baofeng
Model: GM-15 Pro
Max_Memories: 250
Channel_Name_Max_Length: 6
Power Classes: LOW / HIGH
```

## Capability Summary

| Capability ID | Type | Min MHz | Max MHz | Mode | TX | RX |
|---|---|---:|---:|---|---|---|
| RCP-008 | RECEIVE | 136.000000 | 174.000000 | FM | No | Yes |
| RCP-009 | RECEIVE | 136.000000 | 174.000000 | NFM | No | Yes |
| RCP-010 | RECEIVE | 400.000000 | 512.000000 | FM | No | Yes |
| RCP-011 | RECEIVE | 400.000000 | 512.000000 | NFM | No | Yes |
| RCP-012 | TRANSMIT | 462.550000 | 467.725000 | FM | Yes | No |

## Notes

The current manufacturer specifications list:

- 22 GMRS channels
- 8 default GMRS repeater channels
- 24 customizable GMRS repeater memories in the extended channel area
- 220 programmable receive-only scanner channels
- 11 NOAA weather memories
- 136-174 MHz scanning receive
- 400-512 MHz scanning receive
- 0.5 W / 5 W power levels

`RCP-012` is a **frequency envelope**, not a statement that every frequency between 462.550000 and 467.725000 MHz is independently programmable or authorized for transmission.

NorthStar-Comms must enforce actual GMRS channelization, service rules, radio firmware restrictions, and certified operating behavior at the canonical channel/export-validation level.

The project-provided programming template uses the filename:

```text
GM25 - Template - Modified from base config.data
```

This filename is retained as a project artifact, but the physical radio target remains the GM-15 Pro unless later hardware validation establishes a separate model relationship.

---

# 5. Baofeng DM-32UV

## Canonical Model

```text
Radio_Model_ID: RMD-003
Manufacturer: Baofeng
Model: DM-32UV
Max_Memories: 4000
Channel_Name_Max_Length: 15
Power Classes: LOW / MID / HIGH
```

## Capability Summary

| Capability ID | Type | Min MHz | Max MHz | Mode | TX | RX |
|---|---|---:|---:|---|---|---|
| RCP-013 | RECEIVE | 65.000000 | 108.000000 | FM | No | Yes |
| RCP-014 | RECEIVE | 108.000000 | 136.000000 | AM | No | Yes |
| RCP-015 | RECEIVE_TRANSMIT | 136.000000 | 174.000000 | FM | Yes | Yes |
| RCP-016 | RECEIVE_TRANSMIT | 136.000000 | 174.000000 | NFM | Yes | Yes |
| RCP-017 | RECEIVE_TRANSMIT | 136.000000 | 174.000000 | DMR | Yes | Yes |
| RCP-018 | RECEIVE_TRANSMIT | 400.000000 | 470.000000 | FM | Yes | Yes |
| RCP-019 | RECEIVE_TRANSMIT | 400.000000 | 470.000000 | NFM | Yes | Yes |
| RCP-020 | RECEIVE_TRANSMIT | 400.000000 | 470.000000 | DMR | Yes | Yes |
| RCP-021 | RECEIVE | 470.000001 | 480.000000 | FM | No | Yes |
| RCP-022 | RECEIVE | 470.000001 | 480.000000 | NFM | No | Yes |

## Notes

The current manufacturer specifications list:

- 4,000 programmable channels
- 250 zones
- Analog and DMR Tier II operation
- High / Mid / Low power
- 10 W / 4 W / 1 W nominal output levels
- 65-108 MHz FM reception
- 108-136 MHz AM aviation reception
- 136-174 MHz receive/transmit
- 400-480 MHz receive
- 400-470 MHz transmit
- 25 kHz and 12.5 kHz channel spacing
- NOAA reception and alerts
- GPS and Digital APRS

Aviation-band channels must remain receive-only in NorthStar-Comms profiles.

Digital voice capabilities do not imply that encryption or obscured communications are lawful on every radio service. Service-specific rules remain authoritative.

---

# 6. DM-32UV Is Not the Same Radio as UV-32

The project currently contains a programming-template file named:

```text
UV32 - Template.data
```

That filename must not be used as evidence that the user's DM-32UV has the same capabilities as Baofeng's separate `UV-32` radio.

Current manufacturer specifications show material differences:

| Feature | DM-32UV | UV-32 |
|---|---|---|
| Primary mode | Analog + DMR | Analog |
| Channel capacity | 4,000 | 1,000 |
| 220-260 MHz TX | Not listed | Listed |
| UHF TX | 400-470 MHz | 400-520 MHz |
| DMR Tier II | Yes | No / not listed as DMR |

NorthStar-Comms should therefore maintain separate hardware model records if UV-32 support is added later.

The current `RMD-003` record represents **DM-32UV only**.

---

# 7. Compatibility Principles

Radio compatibility is derived rather than manually assigned.

A channel is evaluated against:

```text
CHANNELS
    +
RADIO_CAPABILITIES
    +
Project_TX_Mode
    +
Service / authorization constraints
    +
Export adapter capabilities
```

Possible derived results:

```text
FULL
RX_ONLY
UNSUPPORTED
REQUIRES_REVIEW
```

Examples:

- AM aviation channel + DM-32UV → `RX_ONLY`
- AM aviation channel + UV-5R → `UNSUPPORTED`
- GMRS scanner channel + GM-15 Pro → `RX_ONLY` unless it is a certified GMRS transmit channel
- Amateur VHF simplex + UV-5R → technically `FULL`, subject to operator licensing and lawful frequency selection

---

# 8. Verification Status

Initial capability rows are:

```text
SOURCE_VERIFIED
```

because they are based on current manufacturer specifications.

They are not yet:

```text
FIELD_VERIFIED
```

Field verification should include, where practical:

- CPS import
- Successful programming
- Channel display verification
- Receive test
- Transmit test where lawful and appropriate
- Power-setting behavior
- Wide/Narrow behavior
- TX-inhibit behavior
- Boundary-frequency behavior where relevant

---

# 9. Definition of Done - Radio Capability Profiles

This task is complete when:

- [ ] `Radio_Capability_ID` schema amendment documented
- [ ] Canonical Data Schema updated with `RCP-###`
- [ ] Data Dictionary updated with `Radio_Capability_ID`
- [ ] UV-5R capabilities documented
- [ ] GM-15 Pro capabilities documented
- [ ] DM-32UV capabilities documented
- [ ] DM-32UV and UV-32 distinction documented
- [ ] `Radio_Capabilities` workbook table populated
- [ ] Source records linked
- [ ] Verification records created
- [ ] Validation report passes capability-profile checks
- [ ] Updated workbook committed
- [ ] Capability-profile document committed

---

# 10. Next Development Step

After this task is complete:

```text
Canonical Schema ✅
        ↓
Data Dictionary ✅
        ↓
Master Database ✅
        ↓
Radio Capability Profiles ✅
        ↓
Initial 128-Channel Master Plan
        ↓
CSV / CPS Export Validation
```

The next issue should be:

```text
Define initial 128-channel master plan
```

---

## Guiding Principle

> **One Database. Every Radio. Every Mission.**
