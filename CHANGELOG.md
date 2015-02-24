# Change Log

All notable changes to this project will be documented in this file.

## [Unreleased][unreleased]
### Fixed
- When parsing iLoci, `scripts/feature-desc.py` will now use the iLocus position
  as a default locusid (rather than causing an assertion failure).

### Added
- Parsing of miLoci (merged iLoci), complete with functional tests.
- A classification for each iLocus/miLocus: geneless, mRNA, tRNA, rRNA, or
  ncRNA.
- A field for N content (percent ambiguous nucleotides) for each data type.
- Compliance to pep8 style for Python code.

## [v0.0.1] - 2015-02-12

First public release.
