# Inspired by https://developers.google.com/optimization/assignment/assignment_example
# Author: Sajjad Hashemi
import numpy as np
from ortools.linear_solver import pywraplp


def get_device_links(device, links):
    """
    Returns the indices of the links in which device appears in.
    device: device name (str)
    links: list of link names (list of strings)
    Returns: set
    """
    link_indices = set()
    for idx, link_name in enumerate(links):
        if device in link_name:
            link_indices.add(idx)
    return link_indices


def get_token_links(token):
    """
    Returns the indices of the links which are contained in token.
    token: (1, 0, 1, ...) (tuple)
    Returns: set
    """
    link_indices = set()
    for idx, i in enumerate(token):
        if i == 1:
            link_indices.add(idx)
    return link_indices


def score_set_difference(set1, set2):
    """
    Distance score
    """
    total_set_diff = set1.difference(set2).union(set2.difference(set1))
    #total_set_diff = set1.difference(set2)
    return len(total_set_diff)


def get_cost_matrix(device_names, cluster_centers, links):
    # construct cost matrix with device_names as rows and cluster_centers as columns 
    costs = np.zeros(shape=(len(device_names), len(cluster_centers)))
    for i, device_name in enumerate(device_names):
        device_links = get_device_links(device_name, links)
        for j, cluster_center in enumerate(cluster_centers):
            token_links = get_token_links(cluster_center)
            costs[i][j] = score_set_difference(device_links, token_links)
    return costs


def match(devices, cluster_centers, links):
    costs = get_cost_matrix(devices, cluster_centers, links)
    num_devices = len(devices)
    num_clusters = len(cluster_centers)
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return
    
    # Create variables
    # x[i, j] is an array of 0-1 variables, which will be 1
    # if device i is assigned to cluster_center j.
    x = {}
    for i in range(num_devices):
        for j in range(num_clusters):
            x[i, j] = solver.IntVar(0, 1, 'x_'+str(i)+", "+str(j))
    
    # Create constraints
    # # Each device is assigned to at most 1 cluster_center.
    # for i in range(num_devices): # for all devices
    #     solver.Add(solver.Sum([x[i, j] for j in range(num_clusters)]) <= 1)

    # # Each cluster_center is assigned to exactly one device.
    # for j in range(num_clusters):
    #     solver.Add(solver.Sum([x[i, j] for i in range(num_devices)]) == 1)
    
    # new constraints: 
    # Each device is assigned to exactly 1 cluster_center.
    for i in range(num_devices): # for all devices
        solver.Add(solver.Sum([x[i, j] for j in range(num_clusters)]) == 1)

    # Each cluster_center is assigned to at most one device.
    for j in range(num_clusters):
        solver.Add(solver.Sum([x[i, j] for i in range(num_devices)]) <= 1)

    # Create objective function
    objective_terms = []
    for i in range(num_devices):
        for j in range(num_clusters):
            objective_terms.append(costs[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # optimize
    status = solver.Solve()
    #print(solver.ExportModelAsLpFormat(False).replace('\\', '').replace(',_', ','), sep='\n')
    # print solution
    result=""
    cost_values = []
    total_cost = 0
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        #print(f'Total cost = {solver.Objective().Value()}\n')
        total_cost = solver.Objective().Value()
        result+=f'Total cost = {total_cost}\n'
        for i in range(num_devices):
            for j in range(num_clusters):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if x[i, j].solution_value() > 0.5:
                    result += f'Device {devices[i]} assigned to cluster center {cluster_centers[j]}.' + f' Cost: {costs[i][j]}\n'
                    cost_values.append(costs[i][j])
                    #print(f'Device {devices[i]} assigned to cluster center {cluster_centers[j]}.' +
                     #   f' Cost: {costs[i][j]}')
                    #print(f"{devices[i]}\t{cluster_centers[j]}")
    else:
        result += 'No solution found.\n'
        print('No solution found.')

    return result, total_cost


def match_devices(centers, links):
    """
    Matches centers to devices found in links.
    
    centers: List of tokens representing cluster centers (list)
    links: List of link names (list)

    returns: None
    prints out device matches, cost of each match, and the overall cost.
    """
    device_names = []
    for link_name in links:
        device1, device2 = link_name.split(".")
        if device1 not in device_names:
            device_names.append(device1)
        if device2 not in device_names:
            device_names.append(device2)
    results, total_cost = match(devices=device_names, cluster_centers=centers, links=links)
    print(results)


def save_results(result, file_name):
    loc = "../../results/"+file_name
    with open(loc, 'w') as f:
        f.write(result)
    print(f"file saved in {loc}")
