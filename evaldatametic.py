import csv
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, shapiro
from statsmodels.tsa.seasonal import seasonal_decompose
from statistics import mean, median, stdev
from math import sqrt

def calculate_metrics(column_data):
    return {
        "mean": mean(column_data),
        "median": median(column_data),
        "standard_deviation": stdev(column_data),
        "maximum": max(column_data),
        "minimum": min(column_data),
        "root_mean_square_error": sqrt(mean(np.square(column_data))),
        "mean_absolute_error": mean(np.abs(column_data))
    }


def main():
    # Read CSV file and parse the data
    filename = 'eval_data(basic)pipedelimit.csv'
    rows = []
    covariance_matrices = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')
        next(csvreader)  # Skip the header
        for row in csvreader:
            print(row)
            row_cov = [np.fromstring(obs, sep=',').reshape(-1, 25) for obs in row[len(row)-1:]]
            rows.append(list(map(float, row[:len(row)-1])))
            covariance_matrices.append(row_cov)
        print(rows)
        print(covariance_matrices)

    # Convert to numpy array for easier processing
    data = np.array(rows)

    # Metrics for each element
    metrics = {
        "position_error": calculate_metrics(data[:, 0]),
        "heading_error": calculate_metrics(data[:, 1]),
        "pp_x": calculate_metrics(data[:, 2]),
        "pp_y": calculate_metrics(data[:, 3]),
        "pp_heading": calculate_metrics(data[:, 4]),
        "t_x": calculate_metrics(data[:, 5]),
        "t_y": calculate_metrics(data[:, 6]),
        "t_heading": calculate_metrics(data[:, 7]),
        "t_velocity": calculate_metrics(data[:, 8]),
        "t_acceleration": calculate_metrics(data[:, 9]),
        "timestep": calculate_metrics(data[:, 10]),
    }

    # Metrics for timestep (mean, median, and standard deviation only)
    metrics["timestep"].pop("maximum")
    metrics["timestep"].pop("minimum")
    metrics["timestep"].pop("root_mean_square_error")
    metrics["timestep"].pop("mean_absolute_error")

    # Calculate correlation between variables
    correlations = {}
    variables = ["position_error", "heading_error", "pp_x", "pp_y", "pp_heading", "t_x", "t_y", "t_heading", "t_velocity", "t_acceleration", "timestep"]
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            var1, var2 = variables[i], variables[j]
            correlation, _ = pearsonr(data[:, i], data[:, j])
            correlations[f"{var1} vs {var2}"] = correlation

    # Perform normality test (Shapiro-Wilk) on the data
    normality_tests = {}
    for i, variable in enumerate(variables):
        _, p_value = shapiro(data[:, i])
        normality_tests[variable] = p_value

    # Save metrics to a file
    output_filename = 'metrics.txt'
    with open(output_filename, 'w') as outfile:
        # Metrics for each element
        for element, element_metrics in metrics.items():
            outfile.write(f'{element.capitalize()} Metrics\n')
            for metric, value in element_metrics.items():
                outfile.write(f'{metric.capitalize()}: {value}\n')
            outfile.write('\n')
        # for cov in covariance_matrices:
        #     outfile.write(f'{cov}\n')

        # Correlations between variables
        outfile.write('Correlations\n')
        for var_pair, correlation in correlations.items():
            outfile.write(f'{var_pair}: {correlation}\n')
        outfile.write('\n')

        # Normality test results
        outfile.write('Normality Test (Shapiro-Wilk) Results\n')
        for variable, p_value in normality_tests.items():
            outfile.write(f'{variable}: p-value = {p_value}\n')
        outfile.write('\n')

    print(f"Metrics saved to '{output_filename}'.")
