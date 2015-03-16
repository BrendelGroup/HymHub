# Change Log

All notable changes to this project will be documented in this file.

## [Unreleased][unreleased]
### Fixed
- When parsing iLoci, `scripts/feature-desc.py` will now use the iLocus position
  as a default locusid (rather than causing an assertion failure).
- Fixed species GFF3 checksums to account for improved pseudogene correction in
  AEGeAn.
- Formatting task used to impose `-retainids` at a downstream step of the
  pipeline, after a previous step had not. Removed this and updated the data
  checksums accordingly.

### Added
- Parsing of miLoci (merged iLoci), complete with functional tests.
- A classification for each iLocus/miLocus: geneless, mRNA, tRNA, rRNA, or
  ncRNA.
- A field for N content (percent ambiguous nucleotides) for each data type.
- Compliance to pep8 style for Python code.
- New data sets: *Apis mellifera* data from OGS 1.1 and OGS 3.2.
- An ISSUES file. FAQ page on the site will continue to show the current known
  issues, but we need to have a record of issues in the version history. Thus,
  this file was born.

## [v0.0.1] - 2015-02-12

First public release.
