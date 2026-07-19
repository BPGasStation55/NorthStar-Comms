# Changelog

All notable changes to the NorthStar-Comms project will be documented in this file.

The project follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes or major architecture changes
- **MINOR**: New features or expanded capabilities
- **PATCH**: Bug fixes and minor improvements

---

# [Unreleased]

## Planned

- Master communications database
- Radio export templates
- CSV generation tools
- Initial Baofeng codeplugs
- Communications SOP documentation

---

# [0.1.0] - 2026-07-19

## Added

* Initial public NorthStar-Comms GitHub repository
* MIT License
* Project README
* Project Charter
* Development Roadmap
* Contribution guidelines
* Changelog and semantic versioning structure
* Project `.gitignore`
* Initial repository directory architecture
* GitHub Project development board
* Initial project labels and workflow structure
* Initial Milestone 1 development Issues

## Architecture

Established the initial NorthStar-Comms architectural principles:

* Database-driven design
* Single source of truth for communications data
* Radio-agnostic architecture
* Offline-first core functionality
* Modular and extensible design
* Validation before export
* Reproducible generated outputs

Established the canonical NorthStar-Comms identifier convention:

```text
NSC-XXX
```

Canonical identifiers will provide stable internal references independent of individual radio memory positions.

## Project Management

Established:

* Semantic versioning
* Milestone-based development
* Definition of Done criteria
* GitHub Issues workflow
* GitHub Projects workflow
* Contribution standards
* Data verification philosophy

## Initial Supported Radio Targets

Development targets established for:

* Baofeng UV-5R
* Baofeng GM25 / GM15 Pro
* Baofeng UV32 / DM32

## Next Milestone

**Milestone 1 - Master Database Foundation**

Primary objectives:

* Define the canonical NorthStar-Comms data schema
* Create the NorthStar-Comms Data Dictionary
* Build `Master_Radio_Database.xlsx`
* Define radio capability profiles
* Establish the initial standardized 128-channel plan


# Future Releases

## 0.2.0 - Database Foundation

Planned:

- Master Radio Database workbook
- Frequency database structure
- Validation tables
- Radio compatibility tracking
- Export templates

---

## 0.3.0 - Initial Radio Support

Planned:

- Baofeng UV-5R support
- Baofeng GM25/GM15 Pro support
- Baofeng UV32/DM32 support
- Initial CSV generation

---

## 0.4.0 - Communications Database Expansion

Planned:

- GMRS repeater database
- Amateur repeater database
- NOAA weather channels
- MURS channels
- FRS receive channels
- Regional travel frequencies

---

## 0.5.0 - Documentation and Field Tools

Planned:

- Channel reference cards
- Vehicle reference sheets
- Programming guides
- Communications SOP
- ICS communications templates

---

## 1.0.0 - Initial Stable Release

Target capabilities:

- Master database
- Automated exports
- Verified codeplugs
- Documentation package
- Reference materials
- Release management process

---

# Release Notes Format

Future releases should document:

## Added

New features.

## Changed

Updates to existing features.

## Fixed

Bug fixes.

## Removed

Deprecated functionality.

## Security

Security-related changes.
