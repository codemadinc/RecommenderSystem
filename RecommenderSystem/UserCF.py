# Code description:
# Specific implementation of user-based collaborative filtering algorithm

import math
import numpy as np
import pandas as pd

# Use the modified cosine similarity calculation formula with the Pearson correlation coefficient to calculate the similarity between two users
# Remember sim(user1, user2) = sigma_xy /sqrt(sigma_x * sigma_y)
# Both user1 and user2 are expressed as [[program name, implicit score], [program name, implicit score]], such as user1 = [['Program One', 3.2], ['Program Four', 0.2], [ 'Program 8', 6.5], ...]

def calCosDistByPearson(user1, user2):
    x = 0.0
    y = 0.0

    sigma_xy = 0.0
    sigma_x = 0.0
    sigma_y = 0.0

    for item in user1:
        x += item[1]

    # user1’s average rating of all the shows he has watched
    average_x = x / len(user1)

    for item in user2:
        y += item[1]

    # user2’s average rating of all the shows he has watched
    average_y = y / len(user2)

    for item1 in user1:
        for item2 in user2:
            if item1[0] == item2[0]: # Only programs that user1 and user2 have watched together will be considered.
                sigma_xy += (item1[1] - average_x) * (item2[1] - average_y)
                sigma_x += (item1[1] - average_x) * (item1[1] - average_x)
                sigma_y += (item2[1] - average_y) * (item2[1] - average_y)

    if sigma_x == 0.0 or sigma_y == 0.0: # If the denominator is 0, the similarity is 0
        return 0

    return sigma_xy/math.sqrt(sigma_x * sigma_y)


# Create viewing information for all users (including implicit rating information), "from users to programs"
# Format example: users_to_items = {User one: [['Program one', 3.2], ['Program four', 0.2], ['Program eight', 6.5]], User two: ... }
def createUsersDict(df):
    
    (m, n) = df.shape
    data_array = np.array(df.iloc[:m + 1, 1:])
    users_names = np.array(df.iloc[:m + 1, 0]).tolist()
    items_names = np.array(df.columns)[1:]

    users_to_items = {}

    for i in range(len(users_names)):
        user_and_scores_list = []
        for j in range(len(items_names)):
            if data_array[i][j] > 0:
                user_and_scores_list.append([items_names[j], data_array[i][j]])
        users_to_items[users_names[i]] = user_and_scores_list

    return users_to_items

# Create a dictionary of which users watch all programs, that is, create an inverted table items_and_users "from programs to users"
# items_to_users = {Program 1: [User 1, User 3], Program 2: ... }
def createItemsDict(df):
    
    (m, n) = df.shape
    data_array = np.array(df.iloc[:m + 1, 1:])
    users_names = np.array(df.iloc[:m + 1, 0]).tolist()
    items_names = np.array(df.columns)[1:]
    items_to_users = {}

    for i in range(len(items_names)):
        users_list = []
        for j in range(len(users_names)):
            if data_array[j][i] > 0:
                users_list.append(users_names[j])
        items_to_users[items_names[i]] = users_list

    return items_to_users


# Find all users (i.e. neighbors) related to user user_name and sort them according to similarity
# neighbors_distance = [[user name, similarity size], [...], ...] = [['user four', 0.78],[...], ...]
def findSimilarUsers(users_dict, items_dict, user_name):

    neighbors = [] # neighbors represents all users who have watched the same program as this user

    for items in users_dict[user_name]:
        for neighbor in items_dict[items[0]]:
            if neighbor != user_name and neighbor not in neighbors:
                neighbors.append(neighbor)

    # Calculate the similarity between the user and all its neighbors and sort them in descending order
    neighbors_distance = []
    for neighbor in neighbors:
        distance = calCosDistByPearson(users_dict[user_name], users_dict[neighbor])
        neighbors_distance.append([neighbor, distance])

    neighbors_distance.sort(key=lambda item: item[1], reverse=True)

    return neighbors_distance


# User-based collaborative filtering algorithm
# K is the number of neighbors, which is an important parameter and is used when tuning parameters.
def userCF(user_name, users_dict, items_dict, K, all_items_names_to_be_recommend):

    # recommend_items = {Program name: the similarity between a neighbor of the user user_name who has watched the program and the user, ...}
    recommend_items = {}
    # Convert the above recommended_items into a list and sort them as recommended_items_sorted = [[Program One, the user's level of interest in Program One],[...], ...]
    recommend_items_sorted = []

    # Programs watched by user user_name
    items_user_saw = []
    for item in users_dict[user_name]:
        items_user_saw.append(item[0])

    # Find the K users (neighbors) with the greatest similarity to the user
    similar_users = findSimilarUsers(users_dict, items_dict, user_name)
    if len(similar_users) < K:
        k_similar_user = similar_users
    else:
        k_similar_user = similar_users[:K]

    # Get the recommended program collection for the user
    for user in k_similar_user:
        for item in users_dict[user[0]]:
            # Only programs that the user user_name has not watched are added and can be recommended to the user.
            if item[0] not in items_user_saw:
                # And the program must be in the alternative recommended program set
                if item[0] in all_items_names_to_be_recommend:
                    if item[0] not in recommend_items:
                        # recommend_items is a dictionary. In the first iteration, it means adding the similarity between the first neighbor user and the user to the program name. In subsequent iterations, if other neighbor users have also watched the program,
                        # Also add the similarity to the user to the program name. The result of the iteration is the user's interest in the program.
                        recommend_items[item[0]] = user[1]

                    else:
                        # If a program has been watched by k neighbor users, add the similarities between the k neighbor users and the user to get the user's level of interest in a certain program.
                        recommend_items[item[0]] += user[1]

    for key in recommend_items:
        recommend_items_sorted.append([key, recommend_items[key]])

    # Sort recommended program collections in descending order by user interest
    recommend_items_sorted.sort(key=lambda item: item[1], reverse=True)

    return recommend_items_sorted

# Output the list of programs recommended to the user
# max_num: The maximum number of recommended programs output
def printRecommendItems(recommend_items_sorted, max_num):
    count = 0
    for item, degree in recommend_items_sorted:
        print("Program name: %s, recommendation index: %f" % (item, degree))
        count += 1
        if count == max_num:
            break

# Main program
if __name__ == '__main__':

    all_users_names = ['A', 'B', 'C']

    df1 = pd.read_excel(r"C:\Users\CodeMad\Documents\GitHub\RecommenderSystem\data\Alternative recommended program collection and type 01 matrix.xlsx")
    (m1, n1) = df1.shape
    # Names of programs watched by all users arranged in the order of "Alternative Recommended Program Sets and Type 01 Matrix"
    items_to_be_recommended_names = np.array(df1.iloc[:m1 + 1, 0]).tolist()

    df2 = pd.read_excel(r"C:\Users\CodeMad\Documents\GitHub\RecommenderSystem\data\Rating matrix of all users for the programs they have watched.xlsx")

    # users_dict = {User one: [['Program one', 3.2], ['Program four', 0.2], ['Program eight', 6.5]], User two: ... }
    users_dict = createUsersDict(df2)
    # items_dict = {Program 1: [User 1, User 3], Program 2: [...], ... }
    items_dict = createItemsDict(df2)

    for user in all_users_names:
        print("对于用户 %s 的推荐节目如下：" % user)
        recommend_items = userCF(user, users_dict, items_dict, 2, items_to_be_recommended_names)
        printRecommendItems(recommend_items, 3)
        print()









