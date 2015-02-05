# HymHub

* Homepage: http://brendelgroup.github.io/HymHub
* Data (courtesy of fig**share**): coming soon!
* Code (courtesy of GitHub): https://github.com/BrendelGroup/HymHub

## Building HymHub yourself

[![HymHub build status](https://api.travis-ci.org/BrendelGroup/HymHub.svg?branch=master)](https://travis-ci.org/BrendelGroup/HymHub)

Every change to HymHub is verified by an automated build process (courtesy of [Travis CI](https://travis-ci.org/BrendelGroup/HymHub)).
If you would like to build HymHub yourself, you must first install the [GenomeTools](http://genometools.org) library and the [AEGeAn Toolkit](http://standage.github.io/AEGeAn).
HymHub's Travis configuration file (`.travis.yml`) contains an executable description of how to install these prerequisites on a UNIX system, assuming you have administrative rights.

HymHub provides two alternative build scripts.
The `ci-build.sh` script is very stripped-down, with code that is dead simple to read and understand.
The `build.sh` script does essentially the same task, but additionally provides a command-line interface (complete with a usage statement and description of options) and the option to run the build process in parallel.
While these features are indeed very nice, they bloat up the build file and the code is much less readable.

To run the default build process, simply execute `./ci-build.sh` on the command line.
If you would like more control over the process, run `./build.sh -h` for a description of the options.
