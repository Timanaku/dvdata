import csv
import numpy as np
import ast


def local_to_global(x_local, y_local, heading):
    c, s = np.cos(heading), np.sin(heading)
    R = np.array(((c, -s), (s, c)))
    global_xy = np.dot(R, np.array([x_local, y_local]))
    return global_xy


def merge_data(cone_data, eval_data):
    merged_data = []
    for cone, eval_datum in zip(cone_data, eval_data):
        pp_x, pp_y, pp_heading  = eval_datum[2], eval_datum[3], eval_datum[4]
        for obs in cone['observations']:
            x_local, y_local = obs[0], obs[1]
            global_xy = local_to_global(x_local, y_local, pp_heading)
            obs[0], obs[1] = global_xy[0] + pp_x, global_xy[1] + pp_y

        merged_data.append({
            'cones': cone['cones'],
            'observations': cone['observations'],
            'eval_data': eval_datum
        })

    return merged_data


def string_to_array(string_array):
    # Use ast.literal_eval to safely evaluate the string
    array = ast.literal_eval(string_array)
    return array


def read_cone_data(file_path):
    data = []
    observations = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            cones = int(row[0])
            for list in row[1:-1]:
                observations.append(string_to_array(list))
            # observations = [np.fromstring(obs, sep=',').reshape(-1, 8) for obs in row[1:-1]]
            data.append({
                'cones': cones,
                'observations': observations
            })
            observations = []

    return data



def read_eval_data(file_path):
    # Read CSV file and parse the data
    filename = file_path
    rows = []
    covariance_matrices = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')
        next(csvreader)  # Skip the header
        for row in csvreader:
            row_cov = [np.fromstring(obs, sep=',').reshape(-1, 25) for obs in row[len(row)-1:]]
            rows.append(list(map(float, row[:len(row)-1])))
            covariance_matrices.append(row_cov)

    # Convert to numpy array for easier processing
    data = np.array(rows)

    return data

def main():
    cone_file_path = 'cone_data(basic)pipedelimit.csv'
    eval_file_path = 'eval_data(basic)pipedelimit.csv'
    cone_data = read_cone_data(cone_file_path)
    print(cone_data[0]['observations'])
    eval_data = read_eval_data(eval_file_path)
    merged_data = merge_data(cone_data, eval_data)
    '''`coneObservations` is a `[N, 8]` shaped float numpy array, denoting `N` observations. Each observation has elements:
                    - x position, local frame
                    - y position, local frame
                    - 2x2 position covariance matrix, flattened into 4 elements, local frame
                    - colour
                    - ground truth cone ID
                    '''
    '''
    position_error|heading_error|pp_x|pp_y|pp_heading|t_x|t_y|t_heading|t_velocity|t_acceleration|timestep|pose_covariance_array
    '''

    print("Transformed cone observations:")
    output_filename = 'cones_global.txt'
    with open(output_filename, 'w') as outfile:
        outfile.write("Transformed cone observations:")
        outfile.write("\n")
        for idx, entry in enumerate(merged_data):
            print(f"Entry {idx + 1}:")
            outfile.write(f"Entry {idx + 1}:")
            for obs_idx, obs in enumerate(entry['observations']):
                print(f"\tObservation {obs_idx + 1}:")
                outfile.write(f"\tObservation {obs_idx + 1}:")
                x, y = obs[0], obs[1]
                print(f"\t\tx (global): {x}")
                print(f"\t\ty (global): {y}")
                outfile.write(f"\t\tx (global): {x}")
                outfile.write(f"\t\ty (global): {y}")
                print(f"\t\tcovariance matrix: {obs[2:6]}")
                print(f"\t\tcolour: {obs[6]}")
                outfile.write(f"\t\tcolour: {obs[6]}")
                print(f"\t\tground truth cone ID: {obs[7]}")
                outfile.write(f"\t\tground truth cone ID: {obs[7]}")
            print()
            outfile.write("\n")