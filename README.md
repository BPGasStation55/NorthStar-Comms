# NorthStar-Comms

> **NorthStar-Comms** is a comprehensive communications planning toolkit for amateur radio, GMRS, overlanding, emergency preparedness, volunteer response, and disaster communications.

---

## Project Overview

NorthStar-Comms is designed to provide a **single source of truth** for managing radio fleets, channel plans, repeaters, documentation, and communications planning.

Unlike traditional radio codeplugs that are maintained separately for each radio, NorthStar-Comms uses a centralized database to automatically generate programming files, documentation, reference cards, and future mission plans.

The long-term goal is to build a scalable communications platform suitable for:

- Amateur Radio Operators
- GMRS Users
- Overlanding Groups
- Search & Rescue Teams
- CERT Organizations
- Volunteer Emergency Communications
- Homesteads
- Family Emergency Planning
- Off-Road Recovery Teams
- Incident Command System (ICS) Operations

---

# Project Goals

- Maintain one master communications database
- Automatically generate codeplugs for multiple radio models
- Standardize channel numbering across every radio
- Generate printable reference materials
- Maintain verified repeater databases
- Document communications procedures
- Support future desktop and mobile applications
- Build a long-term communications planning platform

---

# Current Supported Radios

| Manufacturer | Model | Status |
|--------------|-------|--------|
| Baofeng | UV-5R | Planned |
| Baofeng | GM25 / GM15 Pro | Planned |
| Baofeng | UV32 / DM32 | Planned |

Future planned support:

- Yaesu
- Icom
- Kenwood
- Motorola
- BTECH
- AnyTone
- Midland
- Retevis

---

# Repository Structure

```
NorthStar-Comms/

Database/
CSV/
Codeplugs/
Documentation/
Maps/
Reference Cards/
Vehicle/
Base Station/
Field Testing/
Scripts/
Releases/
```

---

# Development Roadmap

## Version 0.1

- Repository initialization
- Documentation
- Folder structure
- Development standards

---

## Version 0.2

- Master communications database
- Export templates
- CSV generation
- Validation engine

---

## Version 0.3

- Initial codeplugs
- UV-5R
- GM25
- UV32

---

## Version 0.4

- Minnesota GMRS repeaters
- Minnesota amateur repeaters
- NOAA
- MURS
- FRS
- National interoperability channels

---

## Version 0.5

- Reference cards
- Programming guides
- Communications SOP
- Vehicle communications

---

## Version 1.0

Initial Stable Release

Includes:

- Master Database
- CSV Generator
- Verified Repeaters
- Documentation
- Reference Cards
- Import Validation

---

# Long-Term Vision

NorthStar-Comms is intended to evolve into a complete communications management system.

Future development includes:

- Desktop application
- Interactive repeater maps
- Automatic CSV generation
- PDF generation
- ICS-205 Communications Plans
- Vehicle communications planning
- Portable repeater planning
- Antenna planning
- Equipment inventory
- Battery runtime calculators
- Field testing logs
- GIS integration

---

# Development Philosophy

Everything starts with a single database.

```
Master Database

        ↓

Validation

        ↓

CSV Generator

        ↓

Radio Programming

        ↓

Reference Cards

        ↓

Documentation

        ↓

Release Package
```

No duplicate data.

No manually maintaining multiple spreadsheets.

One source of truth.

---

# Versioning

NorthStar-Comms follows Semantic Versioning.

Examples:

- v0.1.0
- v0.2.0
- v1.0.0

---

# Contributing

Contributions are welcome.

Current priorities include:

- Additional radio support
- Repeater verification
- Documentation improvements
- Export templates
- Testing
- Bug reports
- Feature requests

---

# Disclaimer

This project is intended to assist users in organizing and documenting radio communications.

Users are responsible for complying with all applicable local, state, and federal regulations, including FCC rules governing the Amateur Radio Service, GMRS, MURS, FRS, aviation, marine, and other radio services.

This repository does **not** encourage or endorse operation outside the privileges granted by the user's license or equipment certification.

Always verify frequencies, repeater access requirements, and licensing before transmitting.

---

# License

This project is licensed under the MIT License.
