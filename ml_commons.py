# Import the required libraries and dependencies
import pandas as pd
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Disable warnings
import warnings
warnings.simplefilter(action='ignore')

def get_num_cols(df):
	# Get columns names and data types
	cols = df.columns
	typs = df.dtypes.values

	# Get all numerical columns into a list
	num_cols = []
	for c in range(len(cols)):
		if (typs[c] == 'float64') | (typs[c] == 'float64'):
			num_cols.append(cols[c])

	return num_cols

def get_scaled(df, num_cols, dummies_cols):
	# Use the StandardScaler module and fit_transform function to
	# scale all columns with numerical values
	scaled_df = StandardScaler().fit_transform(df[num_cols])
	transformed_df = pd.DataFrame(scaled_df, columns = num_cols)

	# Encode (convert to dummy variables) the EnergyType column
	if len(dummies_cols) > 0:
		dummies_df = pd.get_dummies(df[dummies_cols])

		# Concatenate the encoded dummies with the scaled data DataFrame
		transformed_df = pd.concat([transformed_df, dummies_df], axis=1)

	return transformed_df

def get_elbow(df):

	# Create a a list to store inertia values and the values of k
	inertia = []
	k = list(range(1,11))

	# Create a for-loop where each value of k is evaluated using the K-means algorithm
	# Fit the model using the service_ratings DataFrame
	# Append the value of the computed inertia from the `inertia_` attribute of the KMeans model instance
	for i in k:
		k_model = KMeans(n_clusters=i,random_state=1)
		k_model.fit(df)
		inertia.append(k_model.inertia_)

	# Define a DataFrame to hold the values for k and the corresponding inertia
	elbow_data = {'k': k, 'inertia': inertia}
	df_elbow = pd.DataFrame(elbow_data)

	return df_elbow

def fit_model(df, clusters):
    # Define the model with clusters
    model = KMeans(n_clusters=clusters, random_state=1)

    # Fit the model
    model.fit(df)

    # Make predictions
    k = model.predict(df)

    # Create a copy of the DataFrame
    clusters_df = df.copy()

    # Add a class column with the labels
    clusters_df['cluster'] = k

    return clusters_df