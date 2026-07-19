# NorthStar-Comms Development Roadmap

## Current Development Status

| Item | Status |
|------|--------|
| Current Version | v0.1.0 Development |
| Current Milestone | Milestone 0 |
| Current Focus | Repository Foundation |
| Next Milestone | Master Communications Database |
| Repository Status | Active Development |
| Last Updated | July 2026 |


### Overview

This roadmap defines the planned development path for the NorthStar-Comms project.

NorthStar-Comms is being developed as a modular communications planning toolkit with the goal of creating a unified system for:

- Radio programming management
- Frequency database management
- Communications planning
- Emergency preparedness
- Overlanding operations
- Volunteer response support
- Field communications documentation

The project follows a database-first design philosophy:

Master Database
    ↓
Validation
    ↓
Export Engine
    ↓
Radio Codeplug
    ↓
Reference Materials
    ↓
Documentation
    ↓
Release Package


The master database is the single source of truth. All outputs should be generated from validated source data.

# Release Philosophy

Every release should satisfy the following criteria:

- Stable
- Reproducible
- Fully documented
- Tested on supported hardware
- Version controlled
- Backward compatible whenever practical

Major releases should include release notes summarizing new capabilities, known limitations, and migration guidance.

# Planned Release Timeline

| Version | Goal |
|---------|------|
| v0.1.0 | Repository Foundation |
| v0.2.0 | Master Database |
| v0.3.0 | Radio Export Engine |
| v0.4.0 | Regional Frequency Database |
| v0.5.0 | Documentation |
| v0.6.0 | Field Operations Toolkit |
| v0.7.0 | GIS Integration |
| v0.8.0 | Automation Platform |
| v1.0.0 | Stable Public Release |
| v1.1.0 | Communications Intelligence |
| v2.0.0 | Communications Operations Platform |

---

# Guiding Principle

> "One Database. Every Radio. Every Mission."

All project decisions should reinforce the principle that communications data is maintained once, validated once, and exported to every supported platform.

# Core Design Principles

NorthStar-Comms shall be:

1. **Database Driven** – All communications data originates from a single source of truth.

2. **Radio Agnostic** – Support multiple manufacturers without changing channel numbering.

3. **Offline First** – Core functionality must operate without Internet connectivity.

4. **Open Architecture** – New radio models, exporters, and modules can be added without redesign.

5. **Mission Focused** – Communications planning should support real-world operations, not just programming radios.

6. **Automation Preferred** – Repetitive tasks should be automated whenever practical.

7. **Standards Compliant** – Follow FCC regulations, Incident Command System (ICS) practices, and recognized communications standards where applicable.

8. **Extensible** – Every major component should support future expansion.

9. **Documented** – Every release includes documentation and version history.

10. **Tested** – No release is considered complete until verified on supported radio hardware.

---

# Development Philosophy

## Database First

All frequencies, channels, repeaters, and configurations should exist in the master database before being exported.

No manual duplication of channel information between:

- Radios
- Spreadsheets
- Reference cards
- Documentation

# Development Dependencies

The following dependency order should be maintained whenever practical.

Repository
    ↓
Documentation
    ↓
Master Database
    ↓
Validation
    ↓
Export Engine
    ↓
CSV Files
    ↓
Codeplugs
    ↓
Reference Cards
    ↓
Documentation
    ↓
Automation
    ↓
Desktop Application
    ↓
Communications Platform

---

## Radio Agnostic

The system should support multiple manufacturers and radio platforms.

The channel numbering system should remain consistent regardless of radio model.

Example:

Channel 001 - Family Primary
    ↓
UV-5R Channel 001
GM25 Channel 001
DM32 Channel 001

---

## Version Controlled

All changes are tracked through GitHub.

Each release should document:

- Added features
- Configuration changes
- New radio support
- Database updates
- Testing results

---

# Project Status Legend

Each milestone uses the following status indicators:

| Status | Meaning |
|---------|---------|
| ⚪ Planned | Work has not started |
| 🟢 In Progress | Active development |
| 🟡 Testing | Feature complete, undergoing validation |
| 🔵 Complete | Released and verified |
| 🔴 Blocked | Waiting on dependencies or external resources |

---

# Non-Goals

NorthStar-Comms is **not** intended to:

- Replace manufacturer programming software
- Circumvent licensing requirements
- Provide encrypted communications where prohibited by law
- Replace professional dispatch software
- Replace GIS software
- Replace Incident Command software

Instead, NorthStar-Comms complements these systems through planning, documentation, and automation.

---

# Milestone 0 - Project Foundation

## Status

🟢 In Progress

## Goal

Create the project infrastructure and development standards.

## Deliverables

- [x] Repository creation
- [x] README.md
- [x] CHANGELOG.md
- [ ] ROADMAP.md
- [ ] LICENSE
- [ ] .gitignore
- [ ] Folder structure
- [ ] Initial project release

## Definition of Done

Milestone 0 is complete when:

- [x] Public GitHub repository created
- [x] Project licensed under MIT
- [x] README.md completed
- [x] CHANGELOG.md completed
- [x] ROADMAP.md completed
- [ ] LICENSE committed
- [ ] .gitignore committed
- [ ] Initial folder structure committed
- [ ] GitHub Project board configured
- [ ] Initial Issues created
- [ ] Repository tagged as **v0.1.0**
- [ ] Repository successfully cloned and synchronized using GitHub Desktop

## Completion Target

Version: 
v0.1.0

---

# Milestone 1 - Master Database Foundation

## Status

⚪ Planned

## Goal

Create the central communications database.

## Deliverables

Master Excel database containing:

- Channel database
- Frequency database
- Radio compatibility
- Tone information
- Repeater information
- Regional information
- Validation lists
- Change tracking

## Database Categories

Initial categories:

- GMRS
- Amateur Radio
- NOAA Weather
- MURS
- FRS Receive
- Aviation Receive
- Marine Receive
- Railroad
- Emergency Planning

## Definition of Done

Milestone 1 is complete when:

- [ ] Master_Radio_Database.xlsx created
- [ ] Database contains standardized channel numbering
- [ ] Database contains first 128 channels
- [ ] Validation lists implemented
- [ ] Automatic data validation enabled
- [ ] No duplicate channel numbers
- [ ] No duplicate frequency conflicts
- [ ] Channel naming complies with every supported radio
- [ ] Database supports future expansion beyond 1,000 channels
- [ ] Version tagged **v0.2.0**

## Completion Target
Version: 
v0.2.0

---

# Milestone 2 - Radio Export System

## Status

⚪ Planned

## Goal

Generate programming files automatically from the master database.

## Initial Supported Radios

- Baofeng UV-5R
- Baofeng GM25 / GM15 Pro
- Baofeng UV32 / DM32

## Deliverables

- CSV export templates
- Validation checks
- Radio-specific formatting
- Channel name truncation handling
- Import testing

## Testing Requirements

Each export must verify:

- Channel count
- Frequency accuracy
- Tone accuracy
- Power settings
- Scan settings
- Busy lock settings
- Channel naming limits

## Definition of Done

Milestone 2 is complete when:

- [ ] UV-5R export template completed
- [ ] GM25 export template completed
- [ ] UV32 export template completed
- [ ] CSV exports generated automatically
- [ ] Channel names truncate correctly
- [ ] Tones export correctly
- [ ] Scan settings verified
- [ ] Busy Lock verified
- [ ] Power settings verified
- [ ] CSV imports successfully into all supported CPS software
- [ ] Radios verified on-air
- [ ] Version tagged **v0.3.0**

## Completion Target

Version: 
v0.3.0

---

# Milestone 3 - Regional Frequency Database

## Status

⚪ Planned

## Goal

Build verified frequency resources.

## Initial Geographic Focus

Minnesota and surrounding states.

## Data Sets

### GMRS

- Repeaters
- Owners
- Access requirements
- Location
- Coverage estimates

### Amateur Radio

- VHF repeaters
- UHF repeaters
- Digital repeaters
- Emergency resources

### Monitoring

- NOAA
- Aviation
- Railroad
- Marine
- Public safety receive channels where applicable

## Definition of Done

Milestone 3 is complete when:

- [ ] All GMRS repeaters within 75 miles of Eden Prairie verified
- [ ] Minnesota GMRS database completed
- [ ] Wisconsin border repeaters added
- [ ] Minnesota Amateur repeaters added
- [ ] NOAA frequencies verified
- [ ] MURS channels verified
- [ ] National interoperability channels added
- [ ] Aviation receive channels added
- [ ] Marine receive channels added
- [ ] Railroad receive channels added
- [ ] All repeaters include tone information
- [ ] All repeaters include GPS coordinates
- [ ] Coverage estimates added
- [ ] Version tagged **v0.4.0**

## Completion Target

Version: 
v0.4.0

---

# Milestone 4 - Documentation System

## Status

⚪ Planned

## Goal

Generate user-facing communications documentation.

## Deliverables

Reference materials:

- Wallet channel cards
- Vehicle reference sheets
- Base station reference sheets
- Programming instructions
- Communications SOP

Emergency documentation:

- ICS communications planning templates
- Check-in procedures
- Emergency traffic procedures
- Radio etiquette guide

## Definition of Done

Milestone 4 is complete when:

- [ ] Wallet reference card generated
- [ ] Vehicle visor card generated
- [ ] Base station reference sheet generated
- [ ] Programming guide completed
- [ ] Communications SOP completed
- [ ] ICS-205 template completed
- [ ] Family communications plan completed
- [ ] Quick-start guide completed
- [ ] PDF generation automated
- [ ] Version tagged **v0.5.0**

## Completion Target

Version: 
v0.5.0

---

# Milestone 5 - Field Operations Toolkit

## Status

Future

## Goal

Expand beyond programming into communications management.

## Features

Equipment tracking:

- Radio inventory
- Accessories
- Batteries
- Antennas
- Chargers
- Firmware versions

Field testing:

- GPS location
- Radio used
- Antenna used
- Distance
- Signal report
- Notes

Planning tools:

- Mission profiles
- Trip communications plans
- Emergency deployment plans

## Definition of Done

Milestone 5 is complete when:

- [ ] Equipment inventory database completed
- [ ] Battery tracking completed
- [ ] Radio maintenance tracker completed
- [ ] Antenna inventory completed
- [ ] Field test logging completed
- [ ] GPS logging completed
- [ ] Mission profile templates completed
- [ ] Vehicle deployment templates completed
- [ ] Portable deployment templates completed
- [ ] Version tagged **v0.6.0**

## Completion Target

Version: 
v0.6.0+

---

# Milestone 6 - Mapping and GIS Integration

## Status

Future

## Goal

Create visual communications planning tools.

## Features

- Repeater maps
- Coverage estimates
- Travel route planning
- Terrain considerations
- Field test coverage maps

Potential integrations:

- GIS layers
- Offline maps
- GPS data

## Definition of Done

Milestone 6 is complete when:

- [ ] Interactive repeater map created
- [ ] GIS database implemented
- [ ] Coverage estimation implemented
- [ ] GPS import supported
- [ ] Travel route planning completed
- [ ] Terrain overlay implemented
- [ ] Offline map support evaluated
- [ ] Field test data visualized
- [ ] Version tagged **v0.7.0**

---

# Milestone 7 - Automation Platform

## Status

Future

## Goal

Automate project generation.

## Features

Python automation:

- Database validation
- CSV generation
- PDF generation
- Release packaging
- Documentation generation

Target workflow:

Update Database
    ↓
Run Build Script
    ↓
Generate Codeplugs
    ↓
Generate Documentation
    ↓
Create Release Package

## Definition of Done

Milestone 7 is complete when:

- [ ] Python export engine completed
- [ ] Database validation automated
- [ ] CSV generation automated
- [ ] PDF generation automated
- [ ] Release packaging automated
- [ ] Build script completed
- [ ] Error logging implemented
- [ ] Release ZIP generation completed
- [ ] GitHub release workflow documented
- [ ] Version tagged **v0.8.0**

---

# Milestone 8 - Desktop Application

## Status

Long Term

## Goal

Create a dedicated NorthStar-Comms application.

Potential features:

- Graphical database editor
- Radio configuration manager
- Frequency search
- Map interface
- Mission planner
- Equipment manager
- Report generator

---

# Future Radio Support

Potential future platforms:

## Amateur

- Yaesu
- Icom
- Kenwood
- AnyTone

## GMRS

- BTECH
- Midland
- Retevis

## Commercial

- Motorola
- Kenwood
- Icom

---

# Testing Philosophy

Before any stable release:

## Database Validation

Verify:

- Correct frequencies
- Valid tones
- Correct channel limits
- Compatible radios

## Radio Testing

Verify:

- Import success
- Channel names
- Transmit operation where licensed
- Receive operation
- Scan behavior

## Documentation Testing

Verify:

- Printed materials match current database
- Channel references match radios

## Definition of Done

Milestone 8 is complete when:

- [ ] Desktop application architecture finalized
- [ ] GUI framework selected
- [ ] Database connectivity implemented
- [ ] CSV export integrated
- [ ] PDF generation integrated
- [ ] Mapping integrated
- [ ] Settings management completed
- [ ] Automatic update mechanism evaluated
- [ ] Cross-platform compatibility verified
- [ ] Version tagged **v1.0.0**

---

# Milestone 9 - Communications Intelligence & Mission Planning

## Status

Long Term

## Goal

Transform NorthStar-Comms from a communications database into an intelligent planning platform capable of assisting users in designing, validating, and optimizing communications plans for a wide range of missions.

## Objectives

Develop decision-support tools that analyze communications requirements and generate mission-specific recommendations based on available equipment, geographic location, licensing, environmental conditions, and operational objectives.

## Planned Features

### Communications Intelligence

- Frequency conflict detection
- Duplicate channel detection
- Automatic band plan validation
- Channel spacing validation
- Tone conflict detection
- Radio compatibility analysis
- Channel optimization recommendations

### Mission Planning

Generate communications plans for:

- Family preparedness
- Overlanding expeditions
- Off-road recovery operations
- Hunting camps
- Base camp operations
- Search & Rescue
- CERT deployments
- Community emergency response
- Disaster relief
- Homestead operations

### Automatic Plan Generation

Generate:

- Mission-specific codeplugs
- ICS-205 Communications Plans
- Radio assignment sheets
- Channel reference cards
- Equipment checklists
- Battery requirements
- Spare equipment recommendations
- Repeater lists
- Coverage estimates

### Geographic Intelligence

Analyze:

- Available repeaters
- Terrain
- Travel routes
- Coverage gaps
- Emergency communications resources
- Weather monitoring resources
- Alternate communications paths

### Operational Risk Assessment

Provide warnings for:

- Coverage limitations
- Equipment shortages
- Battery endurance concerns
- Single points of failure
- Licensing considerations
- Repeater dependency
- Frequency conflicts

### AI-Assisted Planning (Future)

Potential capabilities:

- Recommend optimal channel layouts
- Suggest repeater usage
- Build mission-specific communications plans
- Recommend equipment based on mission profile
- Identify missing capabilities
- Generate after-action reports from field testing
- Learn from previous deployments to improve future recommendations

## Completion Target

Version:
v1.1.0

## Definition of Done

Milestone 9 is complete when:

- [ ] Frequency conflict detection implemented
- [ ] Band plan validation implemented
- [ ] FCC rules validation (warnings only)
- [ ] Duplicate repeater detection
- [ ] Automatic channel optimization
- [ ] Scan list recommendations
- [ ] Mission-specific codeplug generation
- [ ] Coverage gap analysis
- [ ] Communications risk assessment
- [ ] AI-assisted channel planning
- [ ] Version tagged **v1.1.0**

---

# Milestone 10 - Ecosystem Integration & Communications Operations Platform

## Status

Long Term

## Goal

Evolve NorthStar-Comms into a unified Communications Operations Platform capable of integrating radio communications, mission planning, situational awareness, equipment management, and off-grid infrastructure into a single ecosystem.

The platform should become the central management system for communications planning before, during, and after field operations.

## Objectives

Provide a single interface capable of managing:

- Communications
- Navigation
- Power
- Field equipment
- Mission planning
- Situational awareness
- Documentation
- Operational readiness

## Planned Features

### Base Station Integration

Support management of:

- Home radio stations
- Mobile radio installations
- Portable radio kits
- Portable repeaters
- Antenna systems
- Coax inventory
- Network-connected radios

### Infrastructure Integration

Monitor and document:

- Solar power systems
- Battery storage
- Generator status
- UPS systems
- Charging stations
- Portable power equipment

### Vehicle Integration

Support communications planning for:

- Overland vehicles
- Recovery vehicles
- Command vehicles
- Utility trailers
- Portable communications trailers

Track:

- Installed radios
- Antennas
- Power systems
- Equipment storage
- Maintenance schedules

### Navigation Integration

Support:

- GPS waypoints
- Offline mapping
- Route planning
- Repeater mapping
- Coverage prediction
- Terrain analysis

### Situational Awareness

Integrate information from:

- Weather services
- NOAA alerts
- APRS
- GPS tracking
- Field reports
- Incident logs
- Communications logs

### Mesh Networking

Evaluate and support:

- Meshtastic
- ATAK-compatible workflows
- Winlink
- APRS
- Local network synchronization
- Offline database replication

### Smart Equipment Management

Maintain inventory for:

- Radios
- Batteries
- Chargers
- Antennas
- Cables
- Accessories
- Test equipment
- Portable deployment kits

Provide:

- Maintenance reminders
- Firmware tracking
- Battery lifecycle tracking
- Equipment readiness status

### Automation

Generate:

- Mission deployment packages
- Communications plans
- Equipment checklists
- Radio programming packages
- Printable documentation
- Incident documentation
- After-action reports

### Artificial Intelligence Integration (Future)

Provide optional AI-assisted capabilities for:

- Communications planning
- Frequency recommendations
- Mission planning
- Equipment selection
- Coverage analysis
- Risk assessment
- Documentation generation
- Lessons learned analysis

## Long-Term Vision

NorthStar-Comms should serve as the central communications management platform for:

- Amateur Radio Operators
- GMRS Users
- Overlanding Groups
- Search & Rescue Teams
- CERT Organizations
- Volunteer Emergency Communications
- Homesteads
- Family Preparedness
- Community Emergency Response
- Disaster Relief Operations

The platform should remain modular, extensible, and database-driven, allowing future support for additional radio manufacturers, mapping systems, communications technologies, and automation tools without requiring architectural redesign.

## Completion Target

Version:
v2.0.0

---









