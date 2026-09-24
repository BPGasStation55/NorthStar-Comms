# TAK and Situational-Awareness Scope

**Status:** Accepted long-term milestone; implementation architecture deferred

## Intended scope

- ATAK-CIV and WinTAK
- Offline maps and GIS data
- Team and vehicle tracking
- Shared markers, routes and mission data
- Optional TAK Server
- Resilient local networking
- Possible satellite/IP, sensor and compatible-drone integration

## Required boundary

TAK Cursor-on-Target data is not interchangeable with radio-native APRS or DMR GPS merely because all three can represent positions.

APRS, DMR GPS and other radio data remain separate until a specific interface or gateway is:

1. Defined.
2. Tested with representative data.
3. Checked for identity, timestamp and coordinate handling.
4. Tested for duplicate, delayed and disconnected states.
5. Documented with its failure behavior.

No repository component should imply an operational TAK/APRS/DMR bridge before that validation exists.
