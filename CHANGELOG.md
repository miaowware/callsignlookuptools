# Changelog for callsignlookuptools
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]


## [1.1.2] - 2025-08-05
### Fixed
- Parsing of multi-word cities for callook (#39).


## [1.1.1] - 2023-08-31
### Fixed
- Compatibility with newer typer versions (#33).
- Compatibility with newer pydantic versions.


## [1.1.0] - 2023-01-29
### Added
- Implementation of `__str__` for `QslStatus` for easier display (#23).
### Fixed
- Issue where trustee or image from QRZ could be empty (#22).
- Improve handling of malformed dates in received data (#24).
- Issue where callsigns containing '/' were marked invalid (#20).


## [1.0.1] - 2021-09-27
### Fixed
- Packaging issue.


## [1.0.0] - 2021-09-27
### Added
- Support for QRZ lookup.
- Support for Callook lookup.
- Support for HamQTH lookup.
- Support for QRZCQ lookup.
- Documentation.
- Command-line interface.


[Unreleased]: https://github.com/miaowware/callsignlookuptools/compare/v1.1.2...HEAD
[1.1.2]: https://github.com/miaowware/callsignlookuptools/releases/tag/v1.1.2
[1.1.1]: https://github.com/miaowware/callsignlookuptools/releases/tag/v1.1.1
[1.1.0]: https://github.com/miaowware/callsignlookuptools/releases/tag/v1.1.0
[1.0.1]: https://github.com/miaowware/callsignlookuptools/releases/tag/v1.0.1
[1.0.0]: https://github.com/miaowware/callsignlookuptools/releases/tag/v1.0.0
