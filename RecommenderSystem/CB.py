# Code description:
# Specific implementation of content-based recommendation algorithm

import math
import numpy as np
import pandas as pd

#Create program portrait
# Parameter Description:
# items_profiles = {item1:{'label1':1, 'label2': 0, 'label3': 0, ...}, item2:{...}...}
def createItemsProfiles(data_array, labels_names, items_names):

    items_profiles = {}

    for i in range(len(items_names)):

        items_profiles[items_names[i]] = {}

        for j in range(len(labels_names)):
            items_profiles[items_names[i]][labels_names[j]] = data_array[i][j]

    return items_profiles

#Create user portrait
# Parameter Description:
# data_array: Rating matrix of all users for the programs they have watched data_array = [[2, 0, 0, 1.1, ...], [0, 0, 1.1, ...], ...]
# users_profiles = {user1:{'label1':1.1, 'label2': 0.5, 'label3': 0.0, ...}, user2:{...}...}
def createUsersProfiles(data_array, users_names, items_names, labels_names, items_profiles):

    users_profiles = {}

    # Calculate the average implicit rating of each user for all programs they have watched
    # users_average_scores_list = [1.2, 2.2, 4.3,...]
    users_average_scores_list = []

    # Count the programs watched by each user (without adding implicit rating information)
    # items_users_saw = {user1:[item1, item3, item5], user2:[...],...}
    items_users_saw = {}

    # Count the programs watched by each user and their ratings
    # items_users_saw_scores = {user1:[[item1, 1.1], [item2, 4.1]], user2:...}
    items_users_saw_scores = {}

    for i in range(len(users_names)):

        items_users_saw_scores[users_names[i]] = []
        items_users_saw[users_names[i]] = []
        count = 0
        sum = 0.0

        for j in range(len(items_names)):

            # The user's implicit rating for the program is positive, which means that the user has actually watched the program
            if data_array[i][j] > 0:
                items_users_saw[users_names[i]].append(items_names[j])
                items_users_saw_scores[users_names[i]].append([items_names[j], data_array[i][j]])
                count += 1
                sum += data_array[i][j]

        if count == 0:
            users_average_scores_list.append(0)
        else:
            users_average_scores_list.append(sum / count)

    for i in range(len(users_names)):

        users_profiles[users_names[i]] = {}

        for j in range(len(labels_names)):
            count = 0
            score = 0.0

            for item in items_users_saw_scores[users_names[i]]:

                # Parameters:
                # User user1’s implicit score for type label1: user1_score_to_label1
                # User user1’s score for the program item i that he has watched with type label1: score_to_item i
                # User user1’s average rating of all the programs he has watched: user1_average_score
                #Total number of programs watched by user user1: items_count

                # 公式： user1_score_to_label1 = Sigma(score_to_item i - user1_average_score)/items_count

                # This program contains specific labels labels_names[j]
                if items_profiles[item[0]][labels_names[j]] > 0:
                    score += (item[1] - users_average_scores_list[i])
                    count += 1

            # If the calculated value is too small, set it to 0 directly
            if abs(score) < 1e-6:
                score = 0.0
            if count == 0:
                result = 0.0
            else:
                result = score / count

            users_profiles[users_names[i]][labels_names[j]] = result

    return (users_profiles, items_users_saw)


# Calculate the distance (similarity) between the user portrait vector and the program portrait vector
# Vector similarity calculation formula:
# cos(user, item) = sigma_ui/sqrt(sigma_u * sigma_i)

# Parameter Description:
# user_profile: The portrait of a certain user user = {'label1':1.1, 'label2': 0.5, 'label3': 0.0, ...}
# item: Portrait of a certain program item item = {'label1':1, 'label2': 0, 'label3': 0, ...}
# labels_names: all type names
def calCosDistance(user, item, labels_names):

    sigma_ui = 0.0
    sigma_u = 0.0
    sigma_i = 0.0

    for label in labels_names:
        sigma_ui += user[label] * item[label]
        sigma_u += (user[label] * user[label])
        sigma_i += (item[label] * item[label])

    if sigma_u == 0.0 or sigma_i == 0.0: # If the denominator is 0, the similarity is 0
        return 0

    return sigma_ui/math.sqrt(sigma_u * sigma_i)


# Content-based recommendation algorithm:
# With the help of the user_profile of a specific user and the items_profiles of the alternative recommended program set, the recommended program set is obtained by calculating the similarity between the vectors

# Parameter Description:
# user_profile: The portrait of a certain user user_profile = {'label1':1.1, 'label2': 0.5, 'label3': 0.0, ...}
# items_profiles: Program profiles of alternative recommended program sets: items_profiles = {item1:{'label1':1, 'label2': 0, 'label3': 0}, item2:{...}...}
# items_names: All program names in the alternative recommended program set
# labels_names: all type names
# items_user_saw: programs watched by user user

def contentBased(user_profile, items_profiles, items_names, labels_names, items_user_saw):

    # The recommended program set for user user is recommendation_items = [[program name, similarity between the program portrait and the user portrait], ...]
    recommend_items = []

    for i in range(len(items_names)):
        # Select programs that user user has not watched from the set of alternative recommended programs.
        if items_names[i] not in items_user_saw:
            recommend_items.append([items_names[i], calCosDistance(user_profile, items_profiles[items_names[i]], labels_names)])

    # Sort the recommended program collections in descending order of similarity
    recommend_items.sort(key=lambda item: item[1], reverse=True)

    return recommend_items

# Output the list of programs recommended to the user
# max_num: The maximum number of recommended programs output
def printRecommendedItems(recommend_items_sorted, max_num):
    count = 0
    for item, degree in recommend_items_sorted:
        print("Program name: %s, Recommendation index: %f" % (item, degree))
        count += 1
        if count == max_num:
            break


# Main program
if __name__ == '__main__':

    all_users_names = ['A', 'B', 'C']
    #all_labels = ['教育', '戏曲', '悬疑', '科幻', '惊悚', '动作', '资讯', '武侠', '剧情', '警匪', '生活', '军事', '言情', '体育', '冒险', '纪实',
    #              '少儿教育', '少儿', '综艺', '古装', '搞笑', '广告']
    all_labels = ['education', 'drama', 'suspense', 'sci-fi', 'thriller', 'action', 'information', 'martialarts', 'drama', 'police', 'life', 'military', 'romance', 'sports', 'adventure', 'documentary', 'children education', 'kids', 'varietyshow', 'costume', 'plot', 'funny', 'advertisement', 'comedy', 'physical', 'lanka', 'india']
    labels_num = len(all_labels)

    df1 = pd.read_excel(r"C:\Users\CodeMad\Documents\GitHub\RecommenderSystem\data\Rating matrix of all users for the programs they have watched.xlsx")
    (m1, n1) = df1.shape
    # Rating matrix of all users’ programs they have watched
    # data_array1 = [[0.1804 0.042 0.11  0.07  0.19  0.56  0.14  0.3  0.32 0, ...], [...]]
    data_array1 = np.array(df1.iloc[:m1 + 1, 1:])
    # Names of programs watched by all users arranged in column order of "Rating matrix of programs watched by all users"
    items_users_saw_names1 = df1.columns[1:].tolist()


    df2 = pd.read_excel(r"C:\Users\CodeMad\Documents\GitHub\RecommenderSystem\data\01 matrix of all programs watched by users and their categories.xlsx")
    (m2, n2) = df2.shape
    data_array2 = np.array(df2.iloc[:m2 + 1, 1:])
    # Names of programs watched by all users arranged in the order of "01 matrix of programs watched by all users and their types"
    items_users_saw_names2 = np.array(df2.iloc[:m2 + 1, 0]).tolist()

    # Create program portraits for the programs the user has watched
    items_users_saw_profiles = createItemsProfiles(data_array2, all_labels, items_users_saw_names2)

    # Create user portraits users_profiles and the program collection items_users_saw that the user has watched
    (users_profiles, items_users_saw) = createUsersProfiles(data_array1, all_users_names, items_users_saw_names1, all_labels, items_users_saw_profiles)

    df3 = pd.read_excel(r"C:\Users\CodeMad\Documents\GitHub\RecommenderSystem\data\Alternative recommended program collection and type 01 matrix.xlsx")
    (m3, n3) = df3.shape
    data_array3 = np.array(df3.iloc[:m3 + 1, 1:])
    # Names of programs watched by all users arranged in the order of "Alternative Recommended Program Sets and Type 01 Matrix"
    items_to_be_recommended_names = np.array(df3.iloc[:m3 + 1, 0]).tolist()

    # Create program portraits for alternative recommended program sets
    items_to_be_recommended_profiles = createItemsProfiles(data_array3, all_labels, items_to_be_recommended_names)

    for user in all_users_names:
         print("The recommended programs for user %s are as follows:" % user)
         recommend_items = contentBased(users_profiles[user], items_to_be_recommended_profiles, items_to_be_recommended_names, all_labels, items_users_saw[user])
         printRecommendedItems(recommend_items, 3)
         print()



