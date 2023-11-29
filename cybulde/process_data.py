from hydra.utils import instantiate
from pathlib import Path

import os

from dask.distributed import Client
import dask.dataframe as dd
from cybulde.config_schemas.data_processing.dataset_cleaners_schema import DatasetCleanerManagerConfig

from cybulde.config_schemas.data_processing_config_schema import DataProcessingConfig
from cybulde.utils.config_utils import get_pickle_config, custom_instantiate
from cybulde.utils.data_utils import get_raw_data_with_version
from cybulde.utils.gcp_utils import access_secret_version
from cybulde.utils.utils import get_logger
from cybulde.utils.io_utils import write_yaml_file


def process_raw_data(df_partition: dd.core.DataFrame, dataset_cleaner_manager: DatasetCleanerManagerConfig) -> dd.core.Series:
    return df_partition["text"].apply(dataset_cleaner_manager)

@get_pickle_config(config_path="cybulde/configs/automatically_generated", config_name="data_processing_config")
def process_data(config: DataProcessingConfig) -> None:
    """  print(config)
        from omegaconf import OmegaConf
        print(60*"#")
        print(OmegaConf.to_yaml(config))
        return """
    
    logger =  get_logger(Path(__file__).name)
    logger.info("Processing raw data ...")

    processed_data_save_dir = config.processed_data_save_dir

    cluster =  custom_instantiate(config.dask_cluster)
    client = Client(cluster)

    try:

        """ print(config)
        from omegaconf import OmegaConf
        print(60*"#")
        print(OmegaConf.to_yaml(config))
        return """

        """ github_access_token = access_secret_version(config.infrastructure.project_id, config.github_access_token_secret_id)

        get_raw_data_with_version(
            version=config.version,
            data_local_save_dir=config.data_local_save_dir,
            dvc_remote_repo=config.dvc_remote_repo,
            dvc_data_folder=config.dvc_data_folder,
            github_user_name=config.github_user_name,
            github_access_token=github_access_token,
        )
 """
        dataset_reader_manager = instantiate(config.dataset_reader_manager)
        dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)
        
        df = dataset_reader_manager.read_data(config.dask_cluster.n_workers)

        """ print(df.compute().head())

        exit(0) """
        

        """ print(60*"#")
        print(f"{df.npartitions=}")
        print(60*"#")

        exit(0) """


        logger.info("Cleaning data ... ")
        df =  df.assign(cleaned_text=df.map_partitions(process_raw_data, dataset_cleaner_manager=dataset_cleaner_manager, meta=("text", "object")))
        df =  df.compute()

        train_parquet_path = os.path.join(processed_data_save_dir, "train.parquet")
        dev_parquet_path = os.path.join(processed_data_save_dir, "dev.parquet")
        test_parquet_path = os.path.join(processed_data_save_dir, "test.parquet")

        df[df["split"] == "train"].to_parquet(train_parquet_path)
        df[df["split"] == "dev"].to_parquet(dev_parquet_path)
        df[df["split"] == "test"].to_parquet(test_parquet_path)

        docker_info = {"docker_image": config.docker_image_name, "docker_tag": config.docker_image_tag}
        docker_info_save_path = os.path.join(processed_data_save_dir, "docker_info.yaml")

        write_yaml_file(docker_info_save_path, docker_info)
        # with open_file(docker_info_save_path, "w") as f:
        #     f.write[docker_info]

        logger.info("Data processing finished !")

        """ sample_df = df.sample(n=5)

        for _, row in sample_df.iterrows():
            text = row["text"]
            cleaned_text = dataset_cleaner_manager(text)

            print(60*"#")
            print(f"{text=}")
            print(f"{cleaned_text=}")
            print(60*"#") """

    finally: # close all resources after create and used, to save costs
        logger.info("Closing dask client and cluster...")
        client.close()
        cluster.close()


    """  print(df.head())
        print(df["dataset_name"].unique().compute())  """

    

    """     version = "v10"
        data_local_save_dir = "./data/raw"
        dvc_remote_repo = "https://github.com/Charleschua/cyberbully-data.git"
        dvc_data_folder = "data/raw"
        github_user_name = "Charleschua"  """

    
if __name__ == "__main__":
    process_data()
