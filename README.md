# HymHub

I would like to:

* **download the data**: data is available for download at [doi:m9.figshare.1306864][doi] courtesy of fig**share**.
* **see the code**: the code used to generate the data files is available at [BrendelGroup/HymHub][github] courtesy of GitHub.
  Also included is a basic data analysis demo (implemented both in R and Python) that you can download and use interactively on your local system.
  A static rendering of the demo is available from the following links.
  * [R (RStudio/knitr) demo][rpubs]
  * [Python (IPython Notebook) demo][ipynb]
* **read more about HymHub**: check out [our homepage][homepage].

[doi]: http://dx.doi.org/10.6084/m9.figshare.1306864
[github]: https://github.com/BrendelGroup/HymHub
[rpubs]: http://rpubs.com/danielstandage/hymhubdemo
[ipynb]: http://nbviewer.ipython.org/github/BrendelGroup/HymHub/blob/master/data/HymHubDemo.ipynb
[homepage]: http://brendelgroup.github.io/HymHub

## Building HymHub yourself

[![HymHub build status](https://api.travis-ci.org/BrendelGroup/HymHub.svg?branch=master)](https://travis-ci.org/BrendelGroup/HymHub)

Every change to HymHub is verified by an automated build process (courtesy of [Travis CI][travis]).
If you would like to build HymHub yourself, you must first install the [GenomeTools][genometools] library, the [AEGeAn Toolkit][aegean], and [CD-HIT][cdhit].
HymHub's Travis configuration file (`.travis.yml`) contains an executable description of how to install these prerequisites on a UNIX system, assuming you have administrative rights.

HymHub provides two alternative build scripts.
The `ci-build.sh` script is very stripped-down, with code that is dead simple to read and understand.
The `build.sh` script does essentially the same task, but additionally provides a command-line interface (complete with a usage statement and description of options) and the option to run the build process in parallel.
While these features are indeed very nice, they bloat up the build file and the code is much less readable.

To run the default build process, simply execute `./ci-build.sh` on the command line.
If you would like more control over the process, run `./build.sh -h` for a description of the options.

[travis]: https://travis-ci.org/BrendelGroup/HymHub
[genometools]: http://genometools.org
[aegean]: http://standage.github.io/AEGeAn
[cdhit]: http://weizhongli-lab.org/cd-hit

