from shutil import rmtree
from typing import Optional

import dask.dataframe as dd
import psutil
import pandas as pd

from cybulde.utils.gcp_utils import access_secret_version
from cybulde.utils.utils import run_shell_command


def get_cmd_to_get_raw_data(
    version: str,
    data_local_save_dir: str,
    dvc_remote_repo: str,
    dvc_data_folder: str,
    github_user_name: str,
    github_access_token: str,
) -> str:
    """Get shell command to download the raw data from dvc store

    Parameters
    ----------
    version: str
        data version
    data_local_save_dir: str
        where to save the downloaded data locally
    dvc_remote_repo: str
        dvc repository that holds information about the data
    dvc_data_folder: str
        localtion where the remote data is stored
    github_user_name: str
        github user name
    github_access_token: str
        github access token

    Returns
    -------
    str
        shell command to download the raw data from dvc store
    """
    without_https = dvc_remote_repo.replace("https://", "")
    dvc_remote_repo = f"https://{github_user_name}:{github_access_token}@{without_https}"
    print("1")
    command = f"dvc get {dvc_remote_repo} {dvc_data_folder} --rev {version} -o {data_local_save_dir}"
    print("2")
    return command
    
def get_raw_data_with_version(
    version: str,
    data_local_save_dir: str,
    dvc_remote_repo: str,
    dvc_data_folder: str,
    github_user_name: str,
    github_access_token: str
) -> None:
    rmtree(data_local_save_dir, ignore_errors=True)
    print("3")
    command = get_cmd_to_get_raw_data(version, data_local_save_dir, dvc_remote_repo, dvc_data_folder, github_user_name, github_access_token)
    print("4")
    run_shell_command(command)
    print("5")
    