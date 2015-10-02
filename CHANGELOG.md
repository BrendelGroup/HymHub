# Change Log

All notable changes to this project will be documented in this file.

## [v0.2.0] - 2015-10-02

### Changed
- Handling of overlapping iLoci (refined iLocus parsing as handled by AEGeAn).

### Fixed
- Use feature accession numbers rather than (unstable) GFF3 IDs for tracking.

### Added
- Scripts for performing gene tree analysis on hiLocus data.
- Scripts for genome breakdown.
- Analysis of iLocus neighbor statistics.

## [v0.1.0] - 2015-06-16
### Fixed
- When parsing iLoci, `scripts/feature-desc.py` will now use the iLocus position
  as a default locusid (rather than causing an assertion failure).
- Fixed species GFF3 checksums to account for improved pseudogene correction in
  AEGeAn.
- Formatting task used to impose `-retainids` at a downstream step of the
  pipeline, after a previous step had not. Removed this and updated the data
  checksums accordingly.
- Updated checksums to account for updates to several genome annotations.
- Updated checksums to account for updates to AEGeAn's `tidygff3` program.
- All ant species are now sourced from NCBI rather than HymenopteraBase.

### Added
- New ant genome annotations.
- Parsing of miLoci (merged iLoci), complete with functional tests.
- A classification for each iLocus/miLocus: geneless, mRNA, tRNA, rRNA, or
  ncRNA.
- A field for N content (percent ambiguous nucleotides) for each data type.
- Compliance to pep8 style for Python code.
- New data sets: *Apis mellifera* data from OGS 1.1 and OGS 3.2. These are not
  integrated into aggregate stats however.
- An ISSUES file. FAQ page on the site will continue to show the current known
  issues, but we need to have a record of issues in the version history. Thus,
  this file was born.
- Protein clustering for determining homologous iLoci (hiLoci).
- Scripts for identifying hiLoci with representatives from all 4 major lineages
  (ants, bees, vespid wasps, parasitic wasps), and extracting the protein
  quartets associated with these hiLoci.

## [v0.0.1] - 2015-02-12

First public release.
