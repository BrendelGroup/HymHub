---
layout: page
title: "Frequently Asked Questions"
description: ""
group: navigation
---
{% include JB/setup %}

## Where does all this data come from?

We have done our best to locate and incorporate as much relevant data as possible from the [NCBI FTP site](ftp://ftp.ncbi.nlm.nih.gov/genomes).
We’ve also included some data from [HymenopteraBase](ftp://ftp.ncbi.nlm.nih.gov/genomes), as well as some unpublished data produced by our lab members and collaborators.

## What can I do if HymHub doesn't include data for my favorite Hymenopteran?

Has its genome been sequenced, assembled, and annotated?
Is the relevant data publicly available, or would you be willing to make it publicly available?
If so, send us a note with information about how we can access the data.
Or even better, [fork](https://help.github.com/articles/fork-a-repo/) our [GitHub repository](http://github.com/BrendelGroup/HymHub), add instructions for downloading and incorporating your data, and send us a [pull request](https://help.github.com/articles/using-pull-requests/).

## Are there any known issues with the data?

Several of the raw data sets have some minor issues, which are described below.
All of these issues are addressed in the process that builds the final HymHub sequence files, annotations, and data tables, and require no action on the part of end users.
These issues are shared on a for-your-information basis.

* **Pseudogenes**: In the annotations obtained from NCBI, many pseudogenes are erroneously labeled as genes.
  Fortunately these are easy to detect, as they typically have a ``pseudo=true`` attribute in the 9th column.
  To avoid misinterpretation of the data, our build process corrects any pseudogenes incorrectly labeled as genes with the correct Sequenc Ontology feature type (`pseudogene`).
  
  This issue has not yet been reported to NCBI, but presumably this should be addressed with a bug fix to the ``annotwriter`` program in the NCBI C++ Toolkit.

* **Ribosomal slippage**: The ornithine decarboxylase antizyme in *Drosophila* and *Tribolium* has a ribosomal slippage anomaly that introduces a 2bp gap in the coding sequence.
  This gene is discarded when calculating exon-level statistics, but is included in all other calculations.

* **_Camponotus floridanus_**: Two sequence IDs in the *Camponotus floridanus* data set appear in the GFF3 annotation but not in the genome Fasta file.
  These IDs are ``C3809596`` and ``C3873680``.
  This issue was reported the HymenopteraBase by email in February 2013.
  A week later, HymenopteraBase acknowledged the report and indicated they would respond soon, but as of today we have received no response.
  As it turns out, there is only 1 single-exon gene associated with each of these scaffolds, so we addressed this issue by simply removing these features from the annotation.

  The *C. floridanus* annotation also includes several duplicated features: coding exons with exactly the same coordinates and ```Parent``` relationships.
  This issue has not been reported to HymenopteraBase, and we addressed it by removing the duplicated features.

* **_Drosophila melanogaster_**: The NCBI's annotation of tRNAs in *D. melanogaster* is a bit odd.
  In many (most?) cases, a gene feature corresponding to the tRNA is reported explicitly, but the relationship between the tRNA and its gene parent is not properly defined using GFF3's ``ID/Parent`` mechanism.
  Luckily, other contextual information in the feature attributes makes it possible to resolve the relationships, which we do with a Python script included in the HymHub source code distribution.
  
  The *D. melanogaster* annotation also includes several trans-spliced genes.
  The way these genes are encoded does not follow the GFF3 spec and is not handled correctly by the GenomeTools GFF3 parser, so these genes are discarded during the build process.

* **_Harpegnathos saltator_**: The NCBI annotation for *H. saltator* includes a few "uncharacterized transcription/translation discrepancies"--genome edits that result in unusual annotation artifacts.
  For now we have elected to discard these features, although we may try to incorporate them in the future.

## Why make this data resource available online?

We are staunch proponents of reproducibility and transparency in scientific research: we are not confident in our work if it is not reproducible, and being open/transparent with collaborators reduces friction and enables quicker progress in research.
If you and your collaborators are already applying these principles in your research---and make no mistake, **you should be**---then going the extra step to make things transparent to the community at large is trivial.

Over the last few years we have frequently been frustrated by the low standards of reproducibility in the literature.
HymHub was created primarily to support our own research efforts and facilitate others in reproducing and building on our work.
However, we also hope that sharing this resource will provide a model that encourages others to take the principles of reproducibility and transparency seriously.
