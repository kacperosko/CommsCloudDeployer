import os
from pathlib import Path

# Mark this to False if you want to skip retrieving diff and generating manifest file
MANIFEST_ONLY = True

# Add as many 'parent' as this file depth than main repo path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Path to directory where temporary CSV files are saving
TEMP_CSV_DIR = os.path.join(BASE_DIR, "bin", "temp")

TAG_PREFIX = "commsCloudDeployer"
