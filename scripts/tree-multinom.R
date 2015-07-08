#!/usr/bin/env Rscript

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
#
# Gene trees inferred from hiLoci are classified based on the 3 possible
# arrangements of the lineages of interest: bees, ants, and vespid wasps. This
# script performs a multinomial exact test to determine whether the proportion
# of the 3 different phylogenetic arrangements differs significantly from a null
# model where all 3 arrangements have equal proportions.
#
# Usage: ./tree-multinom.R Count1 Count2 Count3

args <- commandArgs(trailingOnly=TRUE)
if(length(args) != 3) stop('Expected 3 counts')
library(EMT)
counts <- as.numeric(args)
sink('/dev/stderr')
test <- multinomial.test(counts, prob=c(1/3, 1/3, 1/3))
sink()
cat(sprintf('%e\n', test$p.value))
