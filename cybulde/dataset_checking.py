import pandas as pd

test_df = pd.read_parquet("gs://cyberbully-bucket-3/data/processed/rebalanced_splits/dev.parquet")
# test_df = pd.read_parquet("gs://cyberbully-bucket-3/data/processed/default_run/test.parquet")

print(test_df.shape)
print(test_df.columns.values)

samples_per_dataset = test_df.groupby("dataset_name").size()
print(samples_per_dataset)
