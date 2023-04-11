import csv


def clean_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            cleaned_row = []
            print(row)
            for cell in row:
                if '[' in cell:
                    break
                else:
                    cleaned_row.append(cell)
            writer.writerow(cleaned_row)


if __name__ == "__main__":
    input_file = "eval_data(basic).csv"
    output_file = "eval_data(basic)nocov.csv"
    clean_data(input_file, output_file)
