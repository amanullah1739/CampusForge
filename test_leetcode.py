from database.services.platforms.leetcode import get_leetcode_user


username = "pAZSO55h4I"

data = get_leetcode_user(username)

print("Username:", data["username"])
print("Total Problems:", data["total_problems"])
print("Easy:", data["easy"])
print("Medium:", data["medium"])
print("Hard:", data["hard"])
print("Ranking:", data["ranking"])