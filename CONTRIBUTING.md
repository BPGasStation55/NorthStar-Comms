# Contributing to NorthStar-Comms

Thank you for contributing to NorthStar-Comms.

NorthStar-Comms is a database-driven communications planning toolkit intended to support radio programming, communications planning, documentation, mapping, equipment management, and field operations.

The project follows the guiding principle:

> **One Database. Every Radio. Every Mission.**

All contributions should support this principle and preserve the integrity of the project's canonical communications data.

---

# 1. Contribution Philosophy

NorthStar-Comms favors:

* Accurate data
* Reproducible outputs
* Clear documentation
* Modular architecture
* Offline-capable workflows
* Stable identifiers
* Automated validation
* Hardware verification where practical

Changes should improve the project without unnecessarily duplicating existing functionality or creating isolated data sources.

---

# 2. Ways to Contribute

Contributions may include:

* Adding support for a new radio model
* Correcting frequency or repeater information
* Adding verified repeaters
* Improving documentation
* Developing export templates
* Writing validation rules
* Improving scripts
* Adding tests
* Reporting bugs
* Proposing features
* Adding field test data
* Improving maps or geographic data

---

# 3. Canonical Data Principle

The master database is the primary source of truth for communications data.

Generated files such as:

* CSV exports
* Codeplugs
* Reference cards
* PDFs
* Mission packages

should generally be generated from validated source data rather than edited independently.

Manual changes to generated files should not replace corresponding changes to the source database.

---

# 4. Canonical Identifiers

NorthStar-Comms uses stable internal identifiers.

Channel identifiers use the format:

```text
NSC-XXX
```

Examples:

```text
NSC-001
NSC-002
NSC-043
```

Canonical identifiers must remain stable once assigned.

A channel's:

* Memory position
* Display name
* Radio assignment
* Scan list
* Mission role

may change without changing its canonical identifier.

Identifiers should not be reused after a record is retired.

---

# 5. Repository Structure

Contributions should be placed in the appropriate project directory.

```text
NorthStar-Comms/
│
├── Database/
│   ├── Master/
│   ├── Repeaters/
│   ├── Validation/
│   └── Archive/
│
├── Exports/
│   ├── CSV/
│   ├── Codeplugs/
│   └── Releases/
│
├── Documentation/
│   ├── SOP/
│   ├── Guides/
│   ├── Reference_Cards/
│   └── ICS/
│
├── Maps/
│
├── Scripts/
│   ├── Build/
│   ├── Validation/
│   └── Utilities/
│
├── Assets/
│
├── Tests/
│
└── Archive/
```

Do not create new top-level folders without documenting the architectural reason.

---

# 6. Branching Strategy

During early development, small changes may be committed directly to:

```text
main
```

As the project grows, development should transition toward feature branches.

Recommended naming:

```text
feature/<description>
fix/<description>
data/<description>
docs/<description>
radio/<model>
```

Examples:

```text
feature/csv-export-engine
fix/uv5r-tone-export
data/mn-gmrs-repeaters
docs/programming-guide
radio/anytone-878
```

Stable releases should originate from validated code and data.

---

# 7. Commit Messages

Commit messages should clearly describe the change.

Preferred format:

```text
Action + subject
```

Examples:

```text
Add master database schema
Add UV-5R export template
Update Minnesota GMRS repeater data
Fix channel name truncation
Document radio validation process
Add frequency conflict detection
```

Avoid vague messages such as:

```text
Update files
Changes
Fix stuff
New version
```

One logical change per commit is preferred whenever practical.

---

# 8. Pull Requests

When multiple contributors become active, significant changes should use Pull Requests.

A Pull Request should explain:

* What changed
* Why the change is needed
* What files are affected
* How the change was validated
* Whether radio hardware was tested
* Whether documentation was updated

Large changes should reference the related GitHub Issue when applicable.

---

# 9. Issues

GitHub Issues should be used for:

* Bugs
* Feature requests
* New radio support
* Repeater corrections
* Data validation problems
* Documentation improvements
* Architecture proposals

Recommended issue categories:

```text
bug
feature
radio-support
data-update
repeater-update
documentation
validation
mapping
automation
```

Issues should include enough information to reproduce or evaluate the request.

---

# 10. Data Contributions

Frequency and repeater data should include source information whenever practical.

Useful metadata includes:

* Source
* Date verified
* Location
* Callsign
* Owner or organization
* Repeater output frequency
* Repeater input frequency
* Tone or access method
* Access restrictions
* Geographic coordinates
* Coverage notes
* Verification status

Do not mark information as verified unless it has been checked against an appropriate source.

Unverified data should be clearly identified.

---

# 11. Verification Status

Data records should support a verification status.

Recommended values:

```text
Unverified
Community Reported
Source Verified
Field Verified
Deprecated
```

### Unverified

Information has not yet been independently checked.

### Community Reported

Information was submitted by a user or community source but has not been independently confirmed.

### Source Verified

Information has been checked against a recognized source.

### Field Verified

Operation has been confirmed through actual field use or direct testing.

### Deprecated

The resource is no longer considered active or should no longer be used.

---

# 12. Radio Support Contributions

Adding a new radio model should include:

* Manufacturer
* Model
* Maximum memory count
* Supported frequency ranges
* Supported services
* Channel name length
* Supported power levels
* Supported bandwidth settings
* Supported tone formats
* Receive-only capability
* Export/import format
* Programming software
* Known firmware limitations

Where possible, contributors should provide a blank or sanitized export template from the manufacturer's programming software.

No personal callsigns, passwords, access credentials, or sensitive configuration data should be included in example files.

---

# 13. Radio Export Requirements

A radio export should correctly handle:

* Channel number
* Canonical NSC identifier
* RX frequency
* TX frequency
* Offset
* Encode tone
* Decode tone
* Power
* Bandwidth
* Scan settings
* Busy channel lockout
* Receive-only state
* Channel naming limits

Radio-specific limitations should be documented rather than silently ignored.

---

# 14. Channel Naming

The master database may contain a descriptive canonical channel name.

Radio exporters may shorten that name according to hardware limitations.

For example:

```text
Canonical Name:
FAMILY PRIMARY

15-character radio:
FAMILY PRI

6-character radio:
FAMPRI
```

Shortened names must remain recognizable and should be generated consistently.

---

# 15. Regulatory Considerations

Contributions should support lawful operation.

Do not intentionally configure the project to:

* Circumvent licensing requirements
* Enable unauthorized transmissions
* Bypass equipment certification requirements
* Enable prohibited encryption
* Interfere with aviation, public safety, marine, or other protected communications systems

Receive-only monitoring channels should be clearly identified where transmission is not authorized.

Regulatory warnings provided by NorthStar-Comms are informational and do not replace official regulatory guidance.

---

# 16. Database Changes

Changes to the master data model should be treated carefully.

Schema changes should document:

* The field being added or modified
* Data type
* Allowed values
* Whether the field is required
* Default behavior
* Impact on existing exports
* Migration requirements

The project's Data Dictionary should be updated whenever the schema changes.

---

# 17. Data Dictionary

The Data Dictionary defines the meaning and permitted values of canonical fields.

Examples include:

```text
NSC_ID
Channel_Number
Channel_Name
Service
Category
RX_Frequency
TX_Frequency
Tone_Type
Encode_Tone
Decode_Tone
TX_Allowed
Receive_Only
Verification_Status
```

Code and documentation should follow the Data Dictionary rather than creating alternate meanings for existing fields.

---

# 18. Testing

Changes should be tested at the appropriate level.

## Data Validation

Check for:

* Missing required values
* Invalid frequencies
* Invalid tones
* Duplicate canonical IDs
* Duplicate channel assignments
* Unsupported radio settings
* Invalid channel name lengths

## Export Validation

Confirm:

* Correct column order
* Correct field values
* Correct encoding
* Correct filename
* Successful import into programming software

## Hardware Validation

Where practical, confirm:

* Channels appear correctly
* Channel names display correctly
* Scan behavior works
* Tone configuration works
* Receive-only channels cannot transmit when supported
* Repeater operation works when legally authorized

A successful software import alone does not necessarily constitute full hardware verification.

---

# 19. Generated Files

Generated output files should be reproducible.

Examples include:

```text
*.csv
*.pdf
release ZIP files
generated reference cards
generated reports
```

Where practical, the project should document:

* Source database version
* Build version
* Generation date
* Export profile
* Supported radio model

Generated outputs should not contain secrets or personal credentials.

---

# 20. Documentation

New features should include appropriate documentation.

Documentation may include:

* README updates
* User guides
* Architecture documentation
* Programming instructions
* Data Dictionary updates
* CHANGELOG entries
* ROADMAP updates

A feature should not be considered complete if users cannot reasonably understand how to use it.

---

# 21. Versioning

NorthStar-Comms follows Semantic Versioning where practical.

```text
MAJOR.MINOR.PATCH
```

Examples:

```text
v0.1.0
v0.2.0
v1.0.0
```

### MAJOR

Breaking architecture or compatibility changes.

### MINOR

New functionality or significant new capabilities.

### PATCH

Bug fixes, corrections, and minor improvements.

Frequency database updates may be released as patch versions when they do not introduce structural changes.

---

# 22. Changelog

Notable changes should be recorded in:

```text
CHANGELOG.md
```

Typical categories:

```text
Added
Changed
Fixed
Removed
Security
```

Routine development commits do not necessarily require individual changelog entries, but user-visible release changes should be documented.

---

# 23. Definition of Done

A contribution is complete when applicable requirements have been satisfied.

Typical completion criteria include:

* Data entered into the canonical source
* Validation passed
* Tests passed
* Export generated successfully
* Programming software import verified
* Hardware tested where practical
* Documentation updated
* CHANGELOG updated when appropriate
* Related Issue closed or updated

---

# 24. Security and Privacy

Do not commit:

* Passwords
* API keys
* Private encryption keys
* Personal access tokens
* Private repeater credentials
* Sensitive personal data
* Exact private residential coordinates
* Credentials embedded in codeplug files

Use environment variables or local configuration files for secrets.

Files containing private data should be excluded through `.gitignore` or maintained outside the public repository.

---

# 25. Archiving and Deprecation

Records should not normally be deleted solely because they are no longer active.

Where practical, obsolete records should be marked:

```text
Deprecated
```

This preserves historical context and prevents accidental reuse of canonical identifiers.

Deprecated canonical IDs must not be reassigned to unrelated records.

---

# 26. Proposed Feature Review

Before implementing a significant feature, evaluate whether it:

* Supports the Project Charter
* Fits the ROADMAP
* Uses the canonical data model
* Avoids unnecessary duplication
* Preserves offline functionality where practical
* Can be maintained
* Can be tested
* Can be documented
* Preserves modular architecture

Features outside the project charter should be considered for a separate project or integration.

---

# 27. Development Priorities

When priorities conflict, preference should generally be given to:

```text
Safety
    ↓
Data Accuracy
    ↓
Regulatory Awareness
    ↓
Reliability
    ↓
Interoperability
    ↓
Maintainability
    ↓
Usability
    ↓
New Features
```

Reliable communications data is more important than adding features quickly.

---

# 28. Code of Conduct

Contributors should interact professionally and respectfully.

Technical disagreements should focus on:

* Evidence
* Testing
* Standards
* Architecture
* User requirements

Constructive review is encouraged.

Personal attacks, harassment, or intentionally disruptive behavior are not acceptable.

---

# 29. Questions and Proposals

Questions, architecture discussions, and feature proposals should be submitted through GitHub Issues when practical.

Significant design decisions should be documented so future contributors can understand why the decision was made.

---

## Guiding Principle

> **One Database. Every Radio. Every Mission.**
