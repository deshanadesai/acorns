def parse_output(filename):
    f = open(filename, "r")
    output = f.read()
    output_array = output.split()
    runtime = output_array[0]
    if len(output_array) > 1:
        values = output_array[1:]
    else:
        values = "No values generated"
    return [values, runtime]