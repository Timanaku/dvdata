import re


def main(input_file, output_file):
    input_file = input_file
    output_file = output_file

    def change_delimiter(input_file, output_file):
        with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
            for line in infile:
                new_line = re.sub(r',(?![^\[]*\])', '|', line)
                outfile.write(f"{new_line}")

    change_delimiter(input_file, output_file)
