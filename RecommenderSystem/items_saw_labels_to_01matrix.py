# Code description:
# Based on "D:\Recommender Systems\User A/B/C's ratings of the programs they have watched in the past three months.xls"
# Generate "D:\Recommender Systems\01 matrix of all programs watched by users and their types.xlsx"
import pandas as pd
import numpy as np

if __name__ == '__main__':

    all_users_names = ['A', 'B', 'C']

    # Names of programs watched by all users all_items_users_saw = [item2, item3, item4]
    # Types corresponding to the program names that all users have watched all_items_users_saw_labels = ["label2 label3", "label3", ...]
    all_items_users_saw = []
    all_items_users_saw_labels = []

    for j in range(len(all_users_names)):

        fileToBeRead = r"C:\Users\CodeMad\Documents\GitHub\RecommenderSystem\data\User " + all_users_names[j] + " ratings of the programs he has watched in the past three months.xls"
        df = pd.read_excel(fileToBeRead)
        (m, n) = df.shape
        data_array = np.array(df)

        for i in range(m):
            # 不重复记录相同的节目
           if data_array[i][2] not in all_items_users_saw:
               all_items_users_saw.append(data_array[i][2])
               all_items_users_saw_labels.append(data_array[i][3])

    # Generate "01 matrix of programs watched by all users and their types"
    all_labels = ['education', 'drama', 'suspense', 'sci-fi', 'thriller', 'action', 'information', 'martialarts', 'drama', 'police', 'life', 'military', 'romance', 'sports', 'adventure', 'documentary', 'children education', 'kids', 'varietyshow', 'costume', 'plot', 'funny', 'advertisement', 'comedy', 'physical', 'lanka', 'india']
    #all_labels = ['教育', '戏曲', '悬疑', '科幻', '惊悚', '动作', '资讯', '武侠', '剧情', '警匪', '生活', '军事', '言情', '体育', '冒险', '纪实', '少儿教育', '少儿', '综艺', '古装', '搞笑', '广告']
    labels_num = len(all_labels)

    all_items_labels_01_vectors = []

    for i in range(len(all_items_users_saw)):
        vector = [0] * labels_num
        labels_names = all_items_users_saw_labels[i].split(" ")

        for j in range(len(labels_names)):
            location = all_labels.index(labels_names[j].lower())
            vector[location] = 1

        all_items_labels_01_vectors.append(vector)

    df = pd.DataFrame(all_items_labels_01_vectors, index=all_items_users_saw, columns=all_labels)
    df.to_excel(r"C:\Users\CodeMad\Documents\GitHub\RecommenderSystem\data\01 matrix of all programs watched by users and their categories.xlsx")

    # PS: Remember to type "Program Name" in the first blank cell of the program name column in the generated "01 matrix table of programs watched by all users and their types"