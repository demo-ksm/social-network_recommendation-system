import json

def load_data(filename):
    with open(filename, "r") as file:
        return json.load(file)

def clean_data(data):
    data["users"] = [u for u in data["users"] if u["name"].strip()]
    
    for u in data["users"]:
        u["friends"] = list(set(u["friends"]))
    
    data["users"] = [u for u in data["users"] if u["friends"] or u["liked_pages"]]
    
    page_map = {}
    for p in data["pages"]:
        page_map[p["id"]] = p
    data["pages"] = list(page_map.values())
    
    return data

def find_people_you_may_know(user_id, data):
    friends_map = {}
    id_name_map = {}

    for u in data["users"]:
        friends_map[u["id"]] = set(u["friends"])
        id_name_map[u["id"]] = u["name"]

    direct = friends_map[user_id]
    suggestions = {}

    for friend in direct:
        for mutual in friends_map[friend]:
            if mutual != user_id and mutual not in direct:
                suggestions[mutual] = suggestions.get(mutual, 0) + 1

    ordered = sorted(suggestions, key=suggestions.get, reverse=True)
    return [id_name_map[i] for i in ordered]

def find_pages_you_might_like(user_id, data):
    user_page_map = {}
    page_name_map = {}

    for u in data["users"]:
        user_page_map[u["id"]] = set(u["liked_pages"])

    for p in data["pages"]:
        page_name_map[p["id"]] = p["name"]

    liked = user_page_map[user_id]
    suggestions = {}

    for other_id, pages in user_page_map.items():
        if other_id != user_id:
            common = liked.intersection(pages)

            if len(common) > 0:
                for page in pages:
                    if page not in liked:
                        suggestions[page] = suggestions.get(page, 0) + len(common)

    ordered = sorted(suggestions, key=suggestions.get, reverse=True)
    return [page_name_map[i] for i in ordered]

data = load_data("codebook.json")
data = clean_data(data)

user_id = int(input("Enter User ID: "))

print("\nPeople You May Know:")
print(find_people_you_may_know(user_id, data))

print("\nPages You Might Like:")
print(find_pages_you_might_like(user_id, data))