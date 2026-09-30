# Install and compile MPAS-Urban

Guide 1 of 3 | LIU Zhuo | The Hong Kong University of Science and Technology

This guide builds the standard HKUST-MPAS `hkust-dev` version. Work in a Linux Bash shell. Use one compiler/MPI/NetCDF stack for both compilation and execution.

## Step 1 | Prepare the environment

On a cluster, load the site's GNU compiler, MPI, NetCDF-C, NetCDF-Fortran and PnetCDF modules. Module names are machine-specific. If these tools are unavailable, complete [Appendix A: environment installation commands](https://github.com/Liuzh223/MPAS-Urban-Tutorial/blob/main/docs/appendix-dependencies.md), also included at the end of this PDF. It covers the basic tools, MPI, all required libraries, METIS and restoring the environment after login.

```bash
export MPAS_ROOT="$HOME/MPAS"
mkdir -p "$MPAS_ROOT"
command -v gcc gfortran mpicc mpif90 mpiexec
command -v nc-config nf-config pnetcdf-config
```

Each command must be found.

You also need METIS `gpmetis` to partition the mesh in Guide 2. Load your site's METIS module or use the Ubuntu installation command in Appendix A, then check:

```bash
command -v gpmetis
```

Set the MPAS build variables:

```bash
export NETCDF="$(nc-config --prefix)"
export NETCDFF="$(nf-config --prefix)"
export PNETCDF="$(pnetcdf-config --prefix)"
unset PIO
test -s "$NETCDF/include/netcdf.h"
test -s "$NETCDFF/include/netcdf.mod"
test -s "$PNETCDF/include/pnetcdf.h"
```

`unset PIO` removes any PIO setting inherited from an earlier session. This workflow uses the SMIOL library bundled with MPAS, together with PnetCDF; it does not require a separate PIO2 installation.

Exports apply to the current shell only. After logging in again, reload your modules or the Appendix A library paths, then repeat the exports. Do the same in your batch job's environment.

## Step 2 | Download HKUST-MPAS and this tutorial

```bash
cd "$MPAS_ROOT"
git clone --depth 1 --branch hkust-dev --single-branch \
  https://github.com/HKUST-MPAS/HKUST-MPAS.git
git clone https://github.com/Liuzh223/MPAS-Urban-Tutorial.git
export MPAS_BUILD="$MPAS_ROOT/HKUST-MPAS"
cd "$MPAS_BUILD"
git rev-parse HEAD
```

Record the printed commit with your experiment. `MPAS_BUILD` means the source directory containing your compiled executables. This tutorial does not require a separate modified source tree. Access to this tutorial's repository is required while it remains private.

## Step 3 | Compile initialization

```bash
cd "$MPAS_BUILD"
make -j 1 gfortran CORE=init_atmosphere PRECISION=single
test -x init_atmosphere_model
```

Successful compilation produces `init_atmosphere_model` in the source directory. Stop here if compilation fails.

## Step 4 | Compile the atmosphere model

```bash
make clean CORE=atmosphere
make -j 1 gfortran CORE=atmosphere PRECISION=single
test -x init_atmosphere_model
test -x atmosphere_model
ls -lh init_atmosphere_model atmosphere_model
```

The clean command targets the atmosphere core and retains the initialization executable. Use `make -j 1` for both cores because parallel compilation may cause Fortran module dependency errors on some systems.

## Step 5 | Check runtime files

```bash
ls streams.init_atmosphere streams.atmosphere
ls stream_list.atmosphere.*
ls -lh vertical_levels/urban_ZR_75.txt
ls -lh *TBL *DATA*
```

Keep the runtime tables supplied by this source version. Do not replace them with another experiment's tables. Guide 3 links these files into the case directory.

Both executables must exist before moving to Guide 2. Downloading the source alone is not enough to run MPAS.

## References

- [HKUST-MPAS source and urban-model instructions](https://github.com/HKUST-MPAS/HKUST-MPAS/tree/hkust-dev)
- [Official MPAS tutorial](https://www2.mmm.ucar.edu/projects/mpas/tutorial/StAndrews2025/)

<!-- DEPENDENCY_APPENDIX -->
