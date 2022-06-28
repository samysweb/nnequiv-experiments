# Experiments on `NNEquiv`
This repository contains the experimental setup for the [NNEquiv tool](https://github.com/samysweb/nnequiv).

An overview on the benchmarks can be found [here](/benchmarks.md)

- The most important benchmarks can be found in `/benchmarks-versions`
- Information on the construction of these networks can be found in the jupyter notebooks in `/networks`
- Analyses of the benchmark runs can be found in `/analysis`
- Benchmarks can be run using the Conda environment stored in `environment.yml` by executing `run-par.sh`.
- Benchmarks on the tool be [Kleine Büning et al.}(https://github.com/phK3/NNEquivalence) can be run through `run-buening.sh`
- Benchmarks on [ReluDiff](https://github.com/pauls658/ReluDiff-ICSE2020-Artifact) can be run through `run-paulsen.sh` (note that this one requires some adjustment of file paths and previous installation of the tool)
- Benchmark runs can be configured in `variables.sh`

Unfortunately the full benchmark result logs (usually stored in folders `/result*`) cannot be obtained in the GitHub repo due to GitHub's file size constraints (some of the logs became rather large).
If you are interested in the full log files, feel free to reach out.

## Citation
If you use this work in your research please:
- Cite the work by [Stanley Bak et al. on which we base our implementation](https://link.springer.com/chapter/10.1007/978-3-030-53288-8_4)
- Cite [our work which extends the Geometric Path Enumeration Algorithm to multiple networks](https://ieeexplore.ieee.org/document/9643328)