# NASA Turbofan RUL — Data Directory

This folder is used to store the **CMAPSS** dataset files.

## Download Instructions

1. Visit the NASA dataset page:
   https://data.nasa.gov/Aerospace/CMAPSS-Jet-Engine-Simulated-Data/ff5v-kuh6

2. Download and extract the ZIP archive. You should obtain files like:
   - `train_FD001.txt` — Training set (engine degradation trajectories)
   - `test_FD001.txt`  — Test set (truncated degradation sequences)
   - `RUL_FD001.txt`   — Ground-truth RUL values for the test set

3. Place them in this directory.

## File Format

Each row represents one operating cycle of one engine:
```
unit_id  cycle  op_setting_1  op_setting_2  op_setting_3  sensor_1 ... sensor_21
```

> **Note**: Per `.gitignore`, raw data files (`*.txt`, `*.csv`) are excluded from
> version control to avoid committing large binary assets.
