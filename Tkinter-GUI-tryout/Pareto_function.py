# zoom in-out
# open file from the plt plot

def remove_duplicate_coordinates(points):
    # Initialize empty dictionary to keep track of maximum coordinate values
    max_coordinates = {}

    # Iterate over each point in the list
    for point in points:
        a, b = point

        # If a coordinate value is already in the dictionary, update the maximum value
        if a in max_coordinates:
            max_coordinates[a] = max(max_coordinates[a], b)
        else:
            max_coordinates[a] = b

    # Create new list of points with unique coordinate values
    unique_points = [[a, b] for a, b in max_coordinates.items()]

    return unique_points


def exclude_dominated_points(pareto_front):
    """Filters a list of points in the Pareto front to exclude any dominated points.
    
    Args:
        pareto_front (list): A list of tuples representing points in the Pareto front.
    
    Returns:
        A filtered list of tuples representing non-dominated points in the Pareto front.
    """
    filtered_pareto_front = []
    for i, point1 in enumerate(pareto_front):
        dominated = False
        for j, point2 in enumerate(pareto_front):
            if i == j:
                continue
            if all(p1 <= p2 for p1, p2 in zip(point1, point2)):
                dominated = True
                break
        if not dominated:
            filtered_pareto_front.append(point1)
    return filtered_pareto_front