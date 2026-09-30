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

The ERA5 workflow uses one complete initial-time intermediate file and a separate sequence of SST/sea-ice intermediate files. Inspection of the original surface file's `xtime` confirms 3-hourly records, beginning on 19 July 2022. The tutorial generates records every 10800 seconds through 30 July 06:00. The original atmosphere surface-read setting is hourly and is retained; this is distinct from the input record spacing. Users prepare these inputs themselves; they are not packaged here.

The earlier installation audit established a working GNU/MPI/NetCDF dependency stack. The new documentation is checked against official HKUST-MPAS `hkust-dev` commit [c4f208931c008a7578a42cdc23d854f77d7de4cc](https://github.com/HKUST-MPAS/HKUST-MPAS/commit/c4f208931c008a7578a42cdc23d854f77d7de4cc). A full compile, initialization and atmosphere integration of this newly assembled case has not been performed.

## Documentation checks

- Namelist option names checked against the official initialization, atmosphere, Noah-MP and sounding registries.
- Streams XML parsed; paths and local document links checked.
- Bash code blocks syntax-checked, without executing compilation or model jobs.
- PDF pages rendered and reviewed for readability, margins and page transitions.

These checks assess documentation consistency, not numerical correctness or long-run stability.
