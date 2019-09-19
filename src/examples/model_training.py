import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.attribute_parsing import (get_gamma_attribute,
                                   get_grain_size_attribute,
                                   get_lithology_attribute,
                                   get_permeability_attribute,
                                   get_porosity_attribute,
                                   get_sorting_attribute)
from src.data import find_available_core_images
from src.model import fit_linear, make_feed_forward
from src.pandas_tricks import (categorical_as_one_hot, digitize,
                               filter_dataframe_by_keeping_values)

########################################################################################
# making features and labels
########################################################################################

fname = "data/RealPore_Por_Perm_Lithology_data_1240_Wells_Norway_public.xlsx"
df = pd.read_excel(fname)

images = find_available_core_images()
to_keep = images["license"] + "_" + images["well_name"].str.replace("_", "-")
x = filter_dataframe_by_keeping_values(df, "Well Name", to_keep)
mask = df["Well Name"].isin(to_keep)
mask.sum()


filtered_df = df

frame_x = pd.concat(
    [
        get_grain_size_attribute(filtered_df),
        get_sorting_attribute(filtered_df),
        get_lithology_attribute(filtered_df),
        get_gamma_attribute(filtered_df),
    ],
    axis=1,
)
frame_y = pd.concat(
    [get_porosity_attribute(filtered_df), get_permeability_attribute(filtered_df)],
    axis=1,
)
to_keep = (~frame_x.isnull().any(1)) & (~frame_y.isnull().any(1))
frame_x, frame_y = (
    frame_x.loc[to_keep],
    frame_y.loc[to_keep],
)

x = np.c_[
    categorical_as_one_hot(frame_x["grain_size"]),
    categorical_as_one_hot(frame_x["sorting"]),
    categorical_as_one_hot(frame_x["lithology"]),
    categorical_as_one_hot(digitize(frame_x['GR'], 7)),
    categorical_as_one_hot(digitize(frame_y['porosity'], 7)),
]

y_poro = categorical_as_one_hot(digitize(frame_y["porosity"], 5))
y_perm = categorical_as_one_hot(digitize(frame_y["permeability"], 5))
x_train, x_test, y_train, y_test = train_test_split(x, y_perm, random_state=420)

########################################################################################
# Creating models and fitting
########################################################################################
reg = fit_linear(x_train, y_train)
accuracy = np.mean(reg.predict(x_test).argmax(1) == y_test.argmax(1))
print(f"With linear regression we got {accuracy}")

model = make_feed_forward(x_train.shape[1], y_train.shape[1])
model.fit(x_train, y_train, epochs=4)
accuracy = np.mean(model.predict(x_test).argmax(1) == y_test.argmax(1))
print(f"Got accuracy {accuracy}")
