# Code description:
# Generate "D:\Recommender Systems\Alternate recommended program collections and their types.xlsx" based on "D:\Recommender Systems\Alternate recommended program collections and their types.xlsx"

import pandas as pd
import numpy as np

if __name__ == '__main__':

    df = pd.read_excel(r"C:\Users\CodeMad\Documents\GitHub\RecommenderSystem\data\Alternative recommended program collections and their categories.xlsx")
    (m, n) = df.shape

    data_array = np.array(df.iloc[0:m+1,:])
    print(data_array)

    # All tags in the specified order
    all_labels = ['education', 'drama', 'suspense', 'sci-fi', 'thriller', 'action', 'information', 'martialarts', 'drama', 'police', 'life', 'military', 'romance', 'sports', 'adventure', 'documentary', 'children education', 'kids', 'varietyshow', 'costume', 'plot', 'funny', 'advertisement', 'comedy', 'physical', 'lanka', 'india']
    labels_num = len(all_labels)

    # Extract the names of all programs in order
    all_items_names = np.array(df.iloc[:m+1, 0])
    print(all_items_names)

    #Create a 01 matrix, 0 means that the program does not belong to this type, 1 means that the program belongs to this type
    data_to_be_written = []

    for i in range(len(all_items_names)):

        #01 row vector for each program
        vector = [0] * labels_num
        labels_names = str(data_array[i][1]).split(" ")

        for j in range(len(labels_names)):
            location = all_labels.index(labels_names[j].lower())
            vector[location] = 1

        data_to_be_written.append(vector)

    # Write the 01 matrix into the "alternative recommended program collection and type 01 matrix"
    df = pd.DataFrame(data_to_be_written, index=all_items_names, columns=all_labels)
    df.to_excel(r"C:\Users\CodeMad\Documents\GitHub\RecommenderSystem\data\Alternative recommended program collection and type 01 matrix.xlsx")

    # PS: Remember to type "Program Name" in the first blank cell of the program name column in the generated "Alternate Recommended Program Sets and Type 01 Matrix Table"



























