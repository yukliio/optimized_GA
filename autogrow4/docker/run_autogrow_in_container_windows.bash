#!/bin/bash
# This script runs AutoGrow4 from within the docker container (Windows path style).
# It serves as the ENTRYPOINT of the docker.

set -e
cd /

# Ensure output directory exists and we can write (volume may be empty)
mkdir -p /Outputfolder
echo "AutoGrow4 container started at $(date)" >> /Outputfolder/container_started.txt

# Run AutoGrow4; use python from PATH (autogrow env with Python 3.8)
# Logs go to Outputfolder root so they appear on the host mount
echo "Running AutoGrow4..."
python /autogrow4/run_autogrow.py -j /UserFiles/docker_json_vars.json >> /Outputfolder/output.txt 2>> /Outputfolder/error.txt
echo "AutoGrow4 run finished at $(date)" >> /Outputfolder/container_started.txt
