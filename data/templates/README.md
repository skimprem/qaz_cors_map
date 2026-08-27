# Station table template

This folder contains a CSV template for the station candidate table used in the QGEO IGS submission workflow.

File: `station_table_template.csv`

Column descriptions:
- `StationCode`: 4-character site code (e.g. EIND). Must be globally unique.
- `IGS_ID`: Full IGS 9-character identifier if assigned.
- `SiteName`: Human-readable site name or locality.
- `Latitude_deg`, `Longitude_deg`: Geographic coordinates in decimal degrees (WGS84).
- `Ellipsoidal_height_m`: Ellipsoidal height (meters, WGS84).
- `Monument_type`: Description of monument (concrete pillar, braced pillar, roof mount, etc.).
- `Monument_tie_N_m`, `Monument_tie_E_m`, `Monument_tie_U_m`: Vector tie from monument to local benchmark (meters), if available.
- `Antenna_model`: ANTEX name of the antenna (include radome if applicable).
- `Antenna_serial`: Antenna serial number.
- `Antenna_height_m`: Antenna reference point height above monument (m).
- `Antenna_calibration_available`: Yes/No and link if available.
- `Receiver_model`, `Receiver_serial`: Receiver model and serial number.
- `Obs_start_date`, `Obs_last_date`: First and last observation dates (YYYY-MM-DD).
- `Obs_span_yr`: Observation span in years (decimal).
- `Data_availability_count`: Number of available RINEX/daily files.
- `Data_availability_pct`: Percent completeness (optional).
- `Processed_count`, `Not_estimated_count`, `No_solution_count`: Processing inventory counts from GipsyX/Hector.
- `Repeatability_N_mm`, `Repeatability_E_mm`, `Repeatability_U_mm`: Scatter (RMS) in mm for each component.
- `Velocity_N_mm_per_yr`, `Velocity_E_mm_per_yr`, `Velocity_U_mm_per_yr`: Estimated trends (mm/yr).
- `Velocity_uncertainty_N_mm_per_yr`, `Velocity_uncertainty_E_mm_per_yr`, `Velocity_uncertainty_U_mm_per_yr`: Uncertainties (1-sigma) for velocities.
- `Discontinuities_notes`: Dates and short notes about known offsets or anomalous intervals.
- `Regional_consistency_flag`: OK / Flagged / Excluded (consistency versus Eurasia-relative field).
- `DOMES_number`: IERS DOMES if assigned, or 'pending'.
- `Data_transfer_method`: NTRIP / push-RINEX / FTP / other.
- `Archive_centres`: Data centres where files are archived (links or names).
- `SiteLog_URL`: Link to IGS SiteLog or SLM entry.
- `Site_photos_URLs`: Links to required site photos (4 views).
- `Operator_institution`, `Contact_email`: Operator and contact email.
- `Commitment_3yr`: Yes/No — operator commitment to maintain station for at least 3 years.
- `AnnexA_plot_path`: Local path to the Annex A plot (e.g. `data/stations/EIND.pdf`).
- `Status_recommendation`: Candidate / Needs review / Excluded.
- `Notes_action_items`: Short free-text field with next actions (e.g., 'request DOMES', 'assign new 4-char code').

Usage:
1. Copy `station_table_template.csv` to a working file and fill values for each candidate station.
2. Use `scripts/generate_web_assets.py` to publish available fields to the web UI.
