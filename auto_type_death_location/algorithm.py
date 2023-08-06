import editdistance

def compare_locations(location_list, known_locations):
    similarity_scores = {}
    for location in location_list:
        lowest_score = float('inf')
        best_match = None
        for known_location in known_locations:
            score = editdistance.eval(location, known_location)
            if score < lowest_score:
                lowest_score = score
                best_match = known_location
        similarity_scores[location] = (best_match, lowest_score)
    most_similar_location = min(similarity_scores, key=similarity_scores.get)

    return most_similar_location
