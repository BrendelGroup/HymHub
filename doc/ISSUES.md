# Known Issues

## Pseudogenes

In the annotations obtained from NCBI, many pseudogenes are erroneously labeled as genes.
Fortunately these are easy to detect, as they typically have a `pseudo=true` attribute in the 9th column.
To avoid misinterpretation of the data, our build process corrects any pseudogenes incorrectly labeled as genes with the correct Sequence Ontology feature type (`pseudogene`).

This issue has not yet been reported to NCBI, but presumably this should be addressed with a bug fix to the `annotwriter` program in the NCBI C++ Toolkit.

## Ribosomal slippage

The ornithine decarboxylase antizyme in *Drosophila* and *Tribolium* has a ribosomal slippage anomaly that introduces a 2bp gap in the coding sequence.
This gene is discarded when calculating exon-level statistics, but is included in all other calculations.

## *Camponotus floridanus*

Two sequence IDs in the *Camponotus floridanus* data set appear in the GFF3 annotation but not in the genome Fasta file.
These IDs are `C3809596` and `C3873680`.
This issue was reported the HymenopteraBase by email in February 2013.
A week later, HymenopteraBase acknowledged the report and indicated they would respond soon, but as of today we have received no response.
As it turns out, there is only 1 single-exon gene associated with each of these scaffolds, so we addressed this issue by simply removing these features from the annotation.

The *C. floridanus* annotation also includes several duplicated features: coding exons with exactly the same coordinates and `Parent` relationships.
This issue has not been reported to HymenopteraBase, and we addressed it by removing the duplicated features.

## *Drosophila melanogaster*

The NCBI’s annotation of tRNAs in *D. melanogaster* is a bit odd.
In many (most?) cases, a gene feature corresponding to the tRNA is reported explicitly, but the relationship between the tRNA and its gene parent is not properly defined using GFF3’s `ID/Parent` mechanism.
Luckily, other contextual information in the feature attributes makes it possible to resolve the relationships, which we do with a Python script included in the HymHub source code distribution.

The *D. melanogaster* annotation also includes several trans-spliced genes.
The way these genes are encoded does not follow the GFF3 spec and is not handled correctly by the GenomeTools GFF3 parser, so these genes are discarded during the build process.

## Uncharacterized transcription/translations discrepancies

NCBI annotations for several species include some *uncharacterized transcription/translation discrepancies*--transcript-informed genome edits that result in unusual annotation artifacts.
For now we have elected to discard these features, although we may try to incorporate them in the future.

## *Apis mellifera*

In the official gene set OGS 3.2, the gene `GB44324` contains two directly adjacent exon features.
Rather than trying to decide whether this is a minor annotation artifact or a serious issue with the gene model, we simply discarded this gene.

In OGS 1.1, there are three genes with overlapping exon features: `GB30545`, `GB30541`, and `GB30085`.
These have been discarded.
There are also several genes with a starting coordinate of 0.
After correcting the starting coordinate to 1, these appear to have intact coding sequences.
Accordingly, we have chosen not to discard these, and therefore associated warning messages are to be expected when running the processing pipeline.
