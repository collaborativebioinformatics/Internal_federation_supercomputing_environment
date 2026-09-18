#!/bin/bash
#SBATCH --job-name=team6-grp1-gefion
#SBATCH --output=superfedmmdjob-%j.out          # %j = job ID
#SBATCH --time=00:15:00                # HH:MM:SS
#SBATCH --gpus=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --account=iu_0141 

echo "Hello from $(hostname) at $(date)"
echo "Job ID:   $SLURM_JOB_ID"
echo "Job dir:  $SLURM_SUBMIT_DIR"
sleep 10

ml load GCCcore/14.3.0 Python/3.13.5
ml load UnZip/6.0
source ../venv/bin/activate
# python prepare_data.py
python job.py

echo "Done."
