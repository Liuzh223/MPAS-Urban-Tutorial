# Review notes

Reviewed 30 September 2026.

## Changes from the earlier tutorial

- Replaced the previous rainfall example with a July 2022 Hong Kong heatwave teaching case.
- Kept the official HKUST-MPAS build, MPI/NetCDF setup and single-workspace layout.
- Removed modified-source branches, experiment-specific table changes and bundled case-data downloads.
- Linked the mesh repository cited in Cao et al. (2026); described ERA5 preparation instead of distributing data.
- Kept soil background and one optional BNU explanation in the initialization guide.
- Use one initialization namelist/streams pair, with the static, initial-condition and surface-update edits explained in Guide 2; retain one atmosphere pair.

## Evidence and limits

The teaching dates, time step, model length scale, urban physics and Noah-MP settings were checked against the available July 2022 case configuration. File paths were replaced with the shared workspace layout. The inspected run's physics choices are retained; its custom runtime tables and source modifications are not copied.

The basic workflow uses one complete initial-time ERA5 intermediate file, with SST updates disabled. This differs from the original case, which enabled them. Optional SST/sea-ice inputs use 3-hourly records, confirmed from the original surface file's `xtime`. If selected, the tutorial generates records every 10800 seconds through 30 July 06:00 and enables the original hourly atmosphere surface-read setting. Users prepare these inputs themselves; they are not packaged here.

The static-stage command uses one MPI process (`mpirun -np 1`). Initial-condition generation, optional surface-update generation and atmosphere integration still use the selected partition/task count.

The earlier installation audit established a working GNU/MPI/NetCDF dependency stack. The new documentation is checked against official HKUST-MPAS `hkust-dev` commit [c4f208931c008a7578a42cdc23d854f77d7de4cc](https://github.com/HKUST-MPAS/HKUST-MPAS/commit/c4f208931c008a7578a42cdc23d854f77d7de4cc). A full compile, initialization and atmosphere integration of this newly assembled case has not been performed.

## Documentation checks

- Namelist option names checked against the official initialization, atmosphere, Noah-MP and sounding registries.
- Streams XML parsed; paths and local document links checked.
- Bash code blocks syntax-checked, without executing compilation or model jobs.
- PDF pages rendered and reviewed for readability, margins and page transitions.

These checks assess documentation consistency, not numerical correctness or long-run stability.
