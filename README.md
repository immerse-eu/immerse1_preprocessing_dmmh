# immerse1_processing_dmmh
## Processing DMMH data.

This repository is for processing flattened DMMH data. Script that merges all DMMH data from various export folders. 

The script works as follows: 

* Merge data for each center.
* Add base variable (SiteCode)
* Merge all DMMH data across centers.


### Instructions:
- Config YAML file
- Change directory to DMMH flattened data following the right structure.
- Remove one type of result file from Design files. Example, removing `Design_1_0_0` folder as input. 

### Input:

Place flattened DMMH data as csv file, located in the directory specified by the configuration file (\data\dmmh). 
Only "Results" files are processed.

### Output: 

Processed DMMH data, saved to the directory specified by the configuration file (\data_processed\dmmh)

### Additional Notes: 
- Status: Complete 
- TODO: Add exception to ignore Scales, Variables and Trigger files