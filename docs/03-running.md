# Run the July 2022 heatwave case

Guide 3 of 3 | LIU Zhuo | The Hong Kong University of Science and Technology

Complete Guides 1 and 2 first. This case uses the unmodified HKUST-MPAS `hkust-dev` source and its supplied runtime tables.

## Step 1 | Restore the runtime environment

Load the same MPI and library environment used for compilation. If you built libraries with Appendix A, restore its PATH and library-path exports. Then set the workspace paths:

```bash
export MPAS_ROOT="$HOME/MPAS"
export MPAS_BUILD="$MPAS_ROOT/HKUST-MPAS"
export TUTORIAL="$MPAS_ROOT/MPAS-Urban-Tutorial"
export CASE="$MPAS_ROOT/CASES/heatwave2022"
export NPROCS=192
cd "$CASE"
```

These exports last only for this shell. `MPAS_BUILD` points to the compiled source, while `CASE` holds inputs and outputs for this experiment. Set `NPROCS` to the partition count chosen in Guide 2 (for example, 112 if you selected that option).

## Step 2 | Link the model and runtime files

```bash
ln -sf "$MPAS_BUILD/atmosphere_model" .
ln -sf "$MPAS_BUILD"/stream_list.atmosphere.* .
ln -sf "$MPAS_BUILD"/*TBL .
ln -sf "$MPAS_BUILD"/*DATA* .
cp "$TUTORIAL/config/namelist.atmosphere" .
cp "$TUTORIAL/config/streams.atmosphere" .
```

The links use the tables already installed by the standard source build. No case-specific replacement table is needed. Check that the model inputs exist:

```bash
test -x atmosphere_model
test -s heatwave2022.init.nc
test -s heatwave2022.sfc_update.nc
test -s "heatwave2022.graph.info.part.$NPROCS"
ls -lh *TBL *DATA*
```

## Step 3 | Review the run settings

Open `namelist.atmosphere`. The supplied configuration uses:

```fortran
&nhyd_model
 config_dt = 8.0
 config_start_time = '2022-07-19_00:00:00'
 config_run_duration = '11_06:00:00'
 config_len_disp = 500.0
/
```

`config_len_disp` is the model's representative horizontal length scale in metres; retain 500 m for this mesh. It is not a soil or initialization setting. The full duration ends at 2022-07-30 06:00 UTC.

The physics configuration retains the reference case's choices: Thompson microphysics, Grell-Freitas convection, YSU boundary layer, YSU gravity-wave drag, RRTMG radiation, revised Monin-Obukhov surface layer, and Noah-MP with SLUCM. The supplied namelist also retains the reference Noah-MP option values.

Radiation is called every 30 minutes. SST updates are enabled. The surface file contains 3-hourly records; `streams.atmosphere` retains the original case's hourly surface-read setting. This does not require hourly ERA5 downloads. History and diagnostics are written hourly. The global mesh does not require atmospheric lateral-boundary forcing.

## Step 4 | Run a short test

First change only this line in `namelist.atmosphere`:

```fortran
 config_run_duration = '00:00:16'
```

Run two 8 s time steps using allocated compute resources:

```bash
mpiexec -n "$NPROCS" ./atmosphere_model
tail -n 40 log.atmosphere.0000.out
```

A successful short test advances the model time to `2022-07-19_00:00:16` and ends normally. Check for missing tables, input files, errors or non-finite values before starting the full integration. This checks startup, not long-run stability.

Use your cluster's scheduler to allocate 192 MPI tasks, or the number matching your graph partition. The commands here are run inside that allocation; batch directives depend on the site.

## Step 5 | Run the full teaching period

Keep the test output separate before the full run:

```bash
mkdir short-test-output
mv log.atmosphere.* short-test-output/
mv history.*.nc diag.*.nc short-test-output/
```

Move only the files created by the short test. Restore `config_run_duration = '11_06:00:00'`, keeping `config_do_restart = false`, then run:

```bash
mpiexec -n "$NPROCS" ./atmosphere_model
```

The full simulation is much longer than the short test. Request adequate wall time and storage through your scheduler; hourly global outputs can require hundreds of GB. No speed estimate is promised for a different machine or MPI configuration.

## Step 6 | Check completion

```bash
tail -n 40 log.atmosphere.0000.out
ls -lh history.2022-07-30_06.00.00.nc
ls -lh diag.2022-07-30_06.00.00.nc
```

Check the final simulated time and normal completion in the log. Preserve the source commit, namelist, streams, input provenance and job resource settings with your outputs.

References: [Cao et al. (2026)](https://doi.org/10.22541/essoar.15007108/v1) | [HKUST-MPAS](https://github.com/HKUST-MPAS/HKUST-MPAS/tree/hkust-dev) | [Official MPAS tutorial](https://www2.mmm.ucar.edu/projects/mpas/tutorial/StAndrews2025/).
