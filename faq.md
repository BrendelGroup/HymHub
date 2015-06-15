---
layout: page
title: "Frequently Asked Questions"
description: ""
group: navigation
---
{% include JB/setup %}

## Where does all this data come from?

We have done our best to locate and incorporate as much relevant data as possible from the [NCBI FTP site](ftp://ftp.ncbi.nlm.nih.gov/genomes).
Historically we’ve also included some data from [HymenopteraBase](http://hymenopteragenome.org/), but as all of those genomes are now available at NCBI we opt for the NCBI annotations.
HymHub also includes some (as of yet) unpublished data produced by our lab members and collaborators.

## What can I do if HymHub doesn't include data for my favorite Hymenopteran?

Has its genome been sequenced, assembled, and annotated?
Is the relevant data publicly available, or would you be willing to make it publicly available?
If so, send us a note with information about how we can access the data.
Or even better, [fork](https://help.github.com/articles/fork-a-repo/) our [GitHub repository](http://github.com/BrendelGroup/HymHub), add instructions for downloading and incorporating your data, and send us a [pull request](https://help.github.com/articles/using-pull-requests/).

## Are there any known issues with the data?

Several of the raw data sets have some minor issues.
These are documented [in the source code distribution](https://github.com/BrendelGroup/HymHub/blob/master/doc/ISSUES.md) to facilitate keeping the issue descriptions in sync with the files they describe.
All of the issues are addressed in the automated process that builds the final HymHub sequence files, annotations, and data tables, and require no action on the part of end users.
These issues are shared on a for-your-information basis.

Did we miss something?
Feel free to let us know by opening up a ticket on [HymHub's GitHub issue tracker](https://github.com/BrendelGroup/HymHub/issues).

## Why make this data resource available online?

We are staunch proponents of reproducibility and transparency in scientific research: we are not confident in our work if it is not reproducible, and being open/transparent with collaborators reduces friction and enables quicker progress in research.
If you and your collaborators are already applying these principles in your research---and make no mistake, **you should be**---then going the extra step to make things transparent to the community at large is trivial.

Over the last few years we have frequently been frustrated by the low standards of reproducibility in the literature.
HymHub was created primarily to support our own research efforts and facilitate others in reproducing and building on our work.
However, we also hope that sharing this resource will provide a model that encourages others to take the principles of reproducibility and transparency seriously.
