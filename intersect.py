import pandas as pd

# Load the Flickr IDs CSV (present_ids_commons_query_service.csv)
flickr_ids_file = "present_ids_commons_query_service.csv"
flickr_df = pd.read_csv(flickr_ids_file, names=["file", "bhl_id", "flickr_id"], skiprows=1)

# Extract MID values from the "file" column (strip the 'M' prefix for matching)
flickr_df["mid"] = flickr_df["file"].str.extract(r'M(\d+)')

# Load the petscan result CSV
petscan_file = "petscan_result.csv"
petscan_df = pd.read_csv(petscan_file, on_bad_lines='skip')

# Ensure 'pageid' column is treated as strings for matching
petscan_df["pageid"] = petscan_df["pageid"].astype(str)

# Filter out rows where the 'pageid' does not match the 'mid' from the Flickr IDs
not_in_flickr = petscan_df[~petscan_df["pageid"].isin(flickr_df["mid"])]

# Create a simplified output with file name, MID, and URL
simplified_output = pd.DataFrame({
    "file_name": not_in_flickr["title"],
    "mid": not_in_flickr["pageid"],
    "url": "https://commons.wikimedia.org/entity/M" + not_in_flickr["pageid"]
})

# Save the simplified output to a new CSV
output_file = "bhl_files_from_flickr_without_sdc.csv"
simplified_output.to_csv(output_file, index=False)

print(f"Saved simplified output to {output_file}.")
