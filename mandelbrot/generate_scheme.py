from sys import argv
from math import ceil
from random import randint

def generate_scheme():
    """
    Generates a color scheme in the colors.py file with 128 different
    RGB color codes.  Any number of color codes under 129 can be provided.
    These codes will then be interpolated between.

    This functionality can be used by executing the python script followed
    by specific arguments:
        python3 generate_scheme.py <scheme name> <Set RGB Code> <RGB Codes to interpolate>...
    
    Example usage:
        python3 generate_scheme.py test_scheme 250,250,250 120,120,120 40,40,40

    Addtional commands:
        -c: Clears the user_schemes file, must be the first argument
        -r: generates a set number of random RGB codes to interpolate bewteen.  Must be
            followed by the total number of codes to interpolated between (less than 129).
                Example usage (Generating a scheme named scheme_name with five codes):
                    python3 generate_scheme.py -r scheme_name 5
    """

    name = argv[1]
    start_codes = []
    full_codes = []

    if argv[1] == "-c":
        with open('user_schemes.py', 'w+') as f:
            f.write('')
        print("File cleared.")
        return
    elif argv[1] == "-r":
        try:
            name = argv[2]
            total = int(argv[3])
            for i in range(total):
                code = (randint(0,255), randint(0,255), randint(0,255))
                if i == 0:
                    full_codes.append(code)
                else:
                    start_codes.append(code)
        except:
            print("Invalid argument input for random flag.")
    elif len(argv) < 4:
        print("Invalid usage, missing required arguments.")
        return
    else:
        full_codes, start_codes = parse_rgb()
        
    between = int(ceil(128 - len(start_codes)) / (len(start_codes) - 1))

    for i, code in enumerate(start_codes[:-1]):
        new_code = list(code)
        full_codes.append(code)
        end_code = start_codes[i+1]
        if i == len(start_codes[:-1]) - 1:
            between = 128 - len(full_codes) + 1
        r_step = (end_code[0] - code[0]) / between
        g_step = (end_code[1] - code[1]) / between
        b_step = (end_code[2] - code[2]) / between
        for i in range(between):
            new_code[0] += r_step
            new_code[1] += g_step
            new_code[2] += b_step
            result = [round(val) for val in new_code]
            full_codes.append(tuple(result))

    with open('user_schemes.py', 'a+') as f:
        f.write(name + " = {")
        for i, code in enumerate(full_codes):
            if i == 0:
                f.write(f" -1: {code},\n")
            else:
                f.write(f"\t{i}: {code},\n")
        f.write("}\n\n")
    
    print("Scheme created successfully.")


def parse_rgb():
    full_codes = []
    start_codes = []
    for i, code in enumerate(argv[2:]):
        code = code.split(',')
        new_code = []
        if len(code) == 3:
            for val in code:
                try:
                    val = int(val)
                    new_code.append(val)
                except:
                    print("Invalid color code argument.")
                    return
            if i != 0:
                start_codes.append(tuple(new_code))
            else:
                full_codes.append(tuple(new_code))
    return full_codes, start_codes

if __name__ == "__main__":
    generate_scheme()