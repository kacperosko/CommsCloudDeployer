import subprocess
import os
from datetime import datetime
import resources.printcolors as clr
from settings import TAG_PREFIX, BASE_DIR


def get_last_tag_with_prefix(branch: str, org: str) -> str:
    """
    Gets the last tag matching the prefix and branch.

    :param org:
    :param branch:
    :return:
    """
    # Go to repository catalog
    original_cwd = os.getcwd()
    os.chdir(BASE_DIR)

    try:
        # Get all merged tags
        result = subprocess.run(['git', 'tag', '--merged', branch], stdout=subprocess.PIPE)
        tags = result.stdout.decode('utf-8').strip().split('\n')
        if not tags or tags == ['']:
            return None

        # Filter by tag prefix
        filtered_tags = [tag for tag in tags if tag.startswith(TAG_PREFIX + org)]
        if not filtered_tags:
            return None

        # Find the newest tag
        latest_tag = max(filtered_tags, key=lambda tag: subprocess.run(['git', 'log', '-1', '--format=%at', tag],
                                                                       stdout=subprocess.PIPE).stdout.decode('utf-8').strip())
        return latest_tag
    except Exception as e:
        clr.print_error(f'Error during retrieving last tag: {e}')
        return None
    finally:
        # Go back to work catalog
        os.chdir(original_cwd)


def get_changes_since_last_tag(last_tag: str, comms_cloud_catalog_name: str) -> list:
    """
    Gets the changes since the last tag inside the given comms cloud catalog name.

    :param last_tag:
    :param comms_cloud_catalog_name:
    :return:
    """
    original_cwd = os.getcwd()
    os.chdir(BASE_DIR)

    try:
        if last_tag:
            result = subprocess.run(['git', 'diff', last_tag, '--name-only', '--', f'{comms_cloud_catalog_name}/'],
                                    stdout=subprocess.PIPE)
        else:
            result = subprocess.run(['git', 'ls-files', f'{comms_cloud_catalog_name}/'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip().split('\n')
    except Exception as e:
        clr.print_error(f'Error retrieving changes since last tag: {e}')
        return None
    finally:
        os.chdir(original_cwd)


def add_tag_with_prefix(org) -> bool:
    success = False

    original_cwd = os.getcwd()
    os.chdir(BASE_DIR)

    try:
        current_time = datetime.now()

        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        tag_name = f"{TAG_PREFIX + org}{formatted_time}"

        # Creating and pushing tag
        subprocess.run(['git', 'tag', tag_name], check=True)
        subprocess.run(['git', 'push', 'origin', tag_name], check=True)
        print(f"Tag '{tag_name}' was added and pushed '{org}'.")
        success = True
    except Exception as e:
        clr.print_error(f'Error during adding tag: {e}')
        return False
    finally:
        os.chdir(original_cwd)
    return success


if __name__ == '__main__':
    pass