# MPAS-Urban tutorial: Hong Kong heatwave, July 2022

Author: LIU Zhuo | The Hong Kong University of Science and Technology

New to MPAS? Start with the [official MPAS tutorial](https://www2.mmm.ucar.edu/projects/mpas/tutorial/StAndrews2025/), then follow this urban example.

This tutorial uses the July 2022 Hong Kong heatwave described by [Cao et al. (2026), preprint](https://doi.org/10.22541/essoar.15007108/v1) as its teaching example. It uses the standard [HKUST-MPAS `hkust-dev` branch](https://github.com/HKUST-MPAS/HKUST-MPAS/tree/hkust-dev), based on MPAS v8.2.2. No source changes or experiment-specific parameter tables are required. This is a teaching adaptation, not an exact reproduction of the paper's experiments.

## Start here

1. [Install and compile (PDF)](docs/01-installation.pdf) | [text](docs/01-installation.md)
2. [Prepare static and initial files (PDF)](docs/02-initialization.pdf) | [text](docs/02-initialization.md)
3. [Run MPAS-Urban (PDF)](docs/03-running.pdf) | [text](docs/03-running.md)

Compile both executables before starting initialization or running the model. The installation guide includes a [from-scratch dependency appendix](docs/appendix-dependencies.md).

## One workspace

```text
$HOME/MPAS/
|-- HKUST-MPAS/                 # compiled official source
|-- MPAS-Urban-Tutorial/        # this repository
|   |-- docs/                  # three guides and their PDF versions
|   `-- config/                # reference namelists and streams
|-- DATA/
|   |-- mpas_static/            # geographic datasets, including LCZ
|   `-- heatwave2022/           # mesh, graph and ERA5 intermediate files
|-- CASES/heatwave2022/         # independent case working directory
`-- opt/                       # optional locally installed libraries
```

The guides define `MPAS_BUILD` as the path to the compiled `HKUST-MPAS` directory. Case directories link to its executables and runtime files.

`config/` contains only four files: `namelist.init_atmosphere`, `streams.init_atmosphere`, `namelist.atmosphere` and `streams.atmosphere`. Guide 2 explains how to update the same initialization pair for each stage.

## Teaching case

Case preprint: Cao et al. (2026), [Toward high-resolution urban modeling with MPAS-Urban: System development and sub-kilometer application for record-breaking 2022 Hong Kong Heatwave](https://doi.org/10.22541/essoar.15007108/v1). ESS Open Archive, 6 August 2026.

| Setting | Value |
| --- | --- |
| Simulation period (UTC) | 19 July 2022 00:00 to 30 July 2022 06:00 |
| Initial conditions | One complete ERA5 input at 19 July 2022 00:00 UTC, in WPS intermediate format |
| Surface updates (optional) | Off by default; if enabled, prepare separate ERA5 SST and sea-ice inputs every 3 hours |
| Mesh | Global variable-resolution mesh, approximately 30 km to 500 m around Hong Kong |
| Vertical grid | 55 layers; HKUST-MPAS `vertical_levels/urban_ZR_75.txt` |
| Integration | 8 s time step; hourly history and diagnostics |
| Urban treatment | SLUCM with Noah-MP |

Use the [mesh-generation repository linked by the authors](https://github.com/caomoyu/MPAS-A-mesh-generation). Obtain ERA5 from the Copernicus Climate Data Store: [pressure levels](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels) and [single levels](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels). Mesh and ERA5 data are described in Guide 2; this repository does not package them as downloadable case inputs.

Soil data and the optional BNU choice are explained once in [Guide 2](docs/02-initialization.md#soil-data). The main workflow uses the soil data supported by standard HKUST-MPAS v8.2.2.

## Scope and validation

The general dependency/build workflow is carried forward from the earlier tested tutorial. This new case has been checked against the available case configuration and the official source; the complete new-case workflow has not yet been rerun. See [review notes](docs/review-notes.md).

ChatGPT assisted with document organization, wording and formatting. Technical settings and scientific interpretation should be checked against the cited source documentation and the selected code version.
