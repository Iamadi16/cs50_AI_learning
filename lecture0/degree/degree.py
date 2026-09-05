import sys
import csv
from util import *

names = {}
people = {}
movies = {}

def load_data(directory):
    with open(f"{directory}/people.csv" , encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    with open(f"{directory}/movies.csv" , encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    with open(f"{directory}/stars.csv" , encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass
def main():
    if len(sys.argv) > 2:
        sys.exit()
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("name: "))
    if source is None:
        sys.exit()
    target = person_id_for_name(input("name: "))
    if target is None:
        sys.exit()

    path = shortest_path(source , target)
    if path is None:
        print("no path")
    else:
        degrees = len(path)
        path = [(None , source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

def person_id_for_name(name):
    person_ids = list(names.get(name.lower() , set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) == 1 :
        return person_ids[0]
    else:
        print(f"which '{name}' ?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]    
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("enter the id")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None 

def shortest_path(source , target):
    start = Node(state=source , parent=None , action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    explored = set()

    while True:
        if frontier.empty():
            return None
        
        node = frontier.remove()

        if node.state == target:

            solution = []

            while node.parent is not None:
                solution.append((node.action, node.state))
                node = node.parent

            solution.reverse()

            return solution
        explored.add(node.state)

        for action , state in neighbors_per_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state , parent=node , action=action)
                frontier.add(child)

def neighbors_per_person(person_id):
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

if __name__ == "__main__":
    main()
    
