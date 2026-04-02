import os

def inst2smv_hq(run_dir, input_qcir, input_quabs, stem):
    variables = {}
    traces = set()
    max_state = 0
    with open(input_qcir, "r") as f:
        lines = f.readlines()
        for n in range(len(lines)):
            if n == 0:
                continue
            line = lines[n].strip()

            # Skip until the comments
            if line[0] != "#":
                continue

            # Comments are in the form # <variable number> : <variable name>_<trace>[<state>]

            # Remove spaces and the hashtag
            line = line.replace("#", "").replace(" ", "")

            # Split until the colon
            line = line.split(":")
            variable = line[0].strip()
            line = line[1].strip()
            
            # Split at the last underscore before '[' to allow underscores in names
            bracket_idx = line.find("[")
            if bracket_idx == -1:
                bracket_idx = len(line)
            uscore_idx = line.rfind("_", 0, bracket_idx)
            if uscore_idx == -1:
                # fallback to first underscore if none found before '['
                uscore_idx = line.find("_")
            if uscore_idx == -1:
                # no underscore at all; treat entire string as name and leave remainder
                name = line.strip()
                line = ""
            else:
                name = line[:uscore_idx].strip()
                line = line[uscore_idx+1:].strip()

            # Split until the brackets
            line = line.split("[")
            trace = line[0].strip()
            traces.add(trace)
            line = line[1].strip()

            # Split until the closing bracket
            line = line.split("]")
            state = line[0].strip()
            if int(state) > max_state:
                max_state = int(state)

            variables[variable] = {"trace": trace, "state": state, "name": name, "value": None}

    sat = "Counterexample"
    with open(input_quabs, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == "V":
                values = line[1:].strip().split(" ")
                for value in values:
                    if value == "0":
                        break
                    if value[0] == "-":
                        value = value[1:]
                        variables[value]["value"] = "FALSE"
                    else:
                        variables[value]["value"] = "TRUE"
            # Check for SAT or UNSAT
            elif line[0] == "r":
                if line[1:].strip() == "SAT":
                    sat = "Witness"
                elif line[1:].strip() == "UNSAT":
                    sat = "Counterexample"
    
    # All variables with _ in their names are part of a bitvector
    # Group them by their base name (before the first _) and trace and state
    # Store them in a dictionary where the key is (trace, state, base_name) and the value is the decimal value of the bitvector (suffix = 0 is the LSB)
    # If the value in variables is TRUE, the bit is 1, if FALSE, the bit is 0
    bitvectors = {}
    for var_num in variables:
        var = variables[var_num]
        var_name = var["name"]
        if "_" not in var_name:
            continue
        first_uscore_idx = var_name.find("_")
        base_name = var_name[:first_uscore_idx]
        suffix = var_name[first_uscore_idx+1:]
        if not suffix.isdigit():
            continue
        suffix = int(suffix)
        key = (var["trace"], var["state"], base_name)
        if key not in bitvectors:
            bitvectors[key] = 0
        if var["value"] == "TRUE":
            bitvectors[key] += 2 ** suffix
    
    # Update variables to have the base_name and decimal value, and remove the bitvector parts
    for key in bitvectors:
        trace, state, base_name = key
        decimal_value = bitvectors[key]
        # Find the variable number in variables
        variables_copy = variables.copy()
        for var_num in variables_copy:
            var = variables[var_num]
            if var["trace"] == trace and var["state"] == state and var["name"].startswith(base_name + "_"):
                del variables[var_num]
        # Add a new variable with the base_name and decimal value and make sure its variable number is unique
        new_var_num = "bv_" + trace + "_" + state + "_" + base_name
        variables[new_var_num] = {"trace": trace, "state": state, "name": base_name, "value": str(decimal_value)}

    # Get the unsanitized variable names
    names_file = os.path.join(run_dir, stem + ".smv.names")
    with open(names_file, "r") as names_f:
        names_lines = names_f.readlines()
        names_dict = {}
        for name_line in names_lines:
            # Each line is of the form <unsanitized_name> := <sanitized_name>
            if ":=" not in name_line:
                continue
            unsanitized_name = name_line.split(":=")[0].strip()
            sanitized_name = name_line.split(":=")[1].strip()
            names_dict[sanitized_name] = unsanitized_name
    
    # One file per trace
    for trace in traces:
        new_output_file = os.path.join(run_dir, stem + "-" + trace + ".out")
        with open(new_output_file, "w") as out:
            # Write the first 2 lines
            out.write("Trace Description: LTL " + str(sat) + "\nTrace Type: " + str(sat) + "\n")
            # Loop through each variable in the variables dictionary
            for state in range(max_state + 1):
                if state == max_state:
                    state = max_state
                    out.write("-- Loop starts here\n")
                out.write("  -> State: 1." + str(state+1) + " <-\n")
                for var_num in variables:
                    var = variables[var_num]
                    if var["trace"] != trace:
                        continue
                    if var["state"] != str(state):
                        continue
                    if var["value"] is None:
                        continue
                    var_name = var["name"]
                    # Check if var_name is in names_dict                    
                    if var_name in names_dict:
                        var_name = names_dict[var_name]
                        out.write("    " + var_name + " = " + var["value"] + "\n")