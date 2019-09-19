import pandas as pd


from src.data import find_available_core_images
from src.pandas_tricks import filter_dataframe_by_keeping_values

########################################################################################
# Extracting data
########################################################################################
print('Reading excel data. Might take a while!')
fname = "data/RealPore_Por_Perm_Lithology_data_1240_Wells_Norway_public.xlsx"
df = pd.read_excel(fname)


########################################################################################
# Initial filtering
########################################################################################
# let's remove all entries that belong to wells that we do not have iages from.
images = find_available_core_images()

# example: licence == '6407'; well_name == '6_1' --> '6407_6-1'
to_keep = images["license"] + "_" + images["well_name"].str.replace("_", "-")
filtered_df = filter_dataframe_by_keeping_values(df, "Well Name", to_keep)

previous_number_of_rows = df.shape[0]
current_number_of_rows = filtered_df.shape[0]
diff = previous_number_of_rows - current_number_of_rows
as_pct = int((diff / previous_number_of_rows) * 100)
print(f'Removed {diff} rows (approx. {as_pct}%')
