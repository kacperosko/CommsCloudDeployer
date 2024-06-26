import yaml
import os
import resources.printcolors as clr
from settings import MANIFEST_ONLY, BASE_DIR

def get_comms_cloud_paths(paths: list, comms_cloud_catalog_name: str) -> list:
    results =[]
    for path in paths:
        parts = path.split('/')

        # Check line for correct comms cloud data path
        if len(parts) > 2 and parts[0] == comms_cloud_catalog_name and not parts[-1].startswith('.') and parts[2].find('.') == -1:
            path = f"{parts[1]}/{parts[2]}"
            if path not in results:
                results.append(path)

    return list(set(results))

def write_changes_to_yaml(manifest_lines: list, comms_cloud_catalog_name: str, manifest_only: bool) -> bool:
    yaml_path = os.path.join(BASE_DIR, 'PyCommsCloud.yaml')
    clr.print_info(f'yaml path: {yaml_path}')
    data = {
        'projectPath': f"./{comms_cloud_catalog_name}",
        'manifestOnly': manifest_only,
        'separateProducts': True,
        'oauthConnection': True,
        'activate': True
    }
    if manifest_only:
        data['manifest'] = [f"{manifest_line}" for manifest_line in manifest_lines]

    try:
        with open(yaml_path, 'w') as yaml_file:
            yaml.safe_dump(data, yaml_file, default_flow_style=False)
    except Exception as e:
        clr.print_error(f"Error during writing do yaml file: {e}")
        return False
    return True