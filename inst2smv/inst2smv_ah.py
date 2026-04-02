import os

def inst2smv_ah(run_dir, input_ah, stem):
    with open(input_ah, "r") as f:
        lines = f.readlines()
        # If first line isn't ======= Witnesses ======= then return saying there's no witnesses
        if lines[0].strip() != "======= Witnesses =======":
            print("No witnesses found.")
            return
        # Loop until line that says =========================
        # Then check for SAT or UNSAT
        end = 0
        sat = "Counterexample"
        for line in lines[1:]:
            if end == 2:
                if line.strip() == "SAT":
                    sat = "Witness"
                elif line.strip() == "UNSAT":
                    sat = "Counterexample"
                break
            if end == 1:
                end = 2
                continue
            if line.strip() == "=========================":
                end = 1
                continue
            # Each line will be of the form <Trace>: ({"<Variable>": <Value>, ...}) ({"<Variable>": <Value>, ...})
            # Being the first list of variables the prefix and second the loop
            trace = line.split(":")[0].strip()
            # the prefix will be between the first and second parenthesis
            prefix = line.split("(")[1].split(")")[0].strip()
            # the loop will be between the second and third parenthesis
            loop = line.split("(")[2].split(")")[0].strip()

            # Explicit state (assuming it comes from [A-Z].smv)
            if prefix[0] != "{":
                prefix_states = {}
                loop_states = {}
                new_prefix = ""
                new_loop = ""

                # Go to the original file retrieve how the states would look like in nusmv
                exp_states = {}
                exp_file = os.path.join(run_dir, stem + "-" + trace + "-ah.exp")
                with open(exp_file, "r") as exp_f:
                    exp_lines = exp_f.readlines()
                    for exp_line in exp_lines:
                        if exp_line.startswith("State: "):
                            # Remove the "State: " part and get the state number
                            exp_line = exp_line.replace("State: ", "")
                            # Index of the first space
                            space_index = exp_line.index(" ")
                            state_num = exp_line[:space_index]
                            # Rest of the line after the first space
                            state_vars = exp_line[space_index+1:].strip()
                            state_vars = state_vars.replace("(", "").replace("  ", "").replace(" ", ":").replace(")", ", ")

                            # Ends with ", }" and it's supposed to end with "}"
                            state_vars = state_vars[:-3] + "}"

                            exp_states[state_num] = state_vars
                            continue

                # Loop through prefix
                for state in prefix.split(" "):
                    if state in exp_states:
                        if new_prefix == "(":
                            new_prefix += exp_states[state]
                        else:
                            new_prefix += " " + exp_states[state]
                    else:
                        print(f"State {state} not found in {exp_file}.")
                new_prefix += ""

                # Loop through loop
                for state in loop.split(" "):
                    if state in exp_states:
                        if new_loop == "(":
                            new_loop += exp_states[state]
                        else:
                            new_loop += " " + exp_states[state]
                    else:
                        print(f"State {state} not found in {exp_file}.")
                new_loop += ""

                prefix = new_prefix
                loop = new_loop


            # Remove spaces from prefix and loop
            prefix = prefix.replace(" ", "")
            loop = loop.replace(" ", "")

            # Remove quotes from prefix and loop
            prefix = prefix.replace('"', "")
            loop = loop.replace('"', "")
            
            # Split the prefix and loop into a list of states separated by brackets in the form {<State>}{<State>} ...
            prefix_states = prefix.split("}")
            loop_states = loop.split("}")
            # Remove the last element of the list since it will be empty
            prefix_states.pop()
            loop_states.pop()
            # Remove brackets from each state
            prefix_states = [state[1:] for state in prefix_states]
            loop_states = [state[1:] for state in loop_states]

            # Split each state into a list of tuples of variables and values in the form <"Variable">:<Value>,<"Variable">:<Value>,...
            prefix_states = [
                [tuple(var_val.split(":")) for var_val in state.split(",")]
                for state in prefix_states
            ]
            loop_states = [
                [tuple(var_val.split(":")) for var_val in state.split(",")]
                for state in loop_states
            ]

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

            # Write the trace to the output file
            new_output_file = os.path.join(run_dir, stem + "-" + trace + ".out")
            with open(new_output_file, "w") as out:
                # Write the first 2 lines
                out.write("Trace Description: LTL " + str(sat) + "\nTrace Type: " + str(sat) + "\n")
                # Loop through each number in the number of prefix states
                for i in range(len(prefix_states)):
                    out.write("  -> State: 1." + str(i+1) + " <-\n")
                    for var_val in prefix_states[i]:
                        var_name = var_val[0]
                        if var_name in names_dict:
                            var_name = names_dict[var_name]
                        out.write("    " + var_name + " = " + var_val[1] + "\n")
                # Loop through each number in the number of loop states
                for i in range(len(loop_states)):
                    if i == 0:
                        out.write("-- Loop starts here\n")
                    out.write("  -> State: 1." + str(i+1+len(prefix_states)) + " <-\n")
                    for var_val in loop_states[i]:
                        var_name = var_val[0]
                        if var_name in names_dict:
                            var_name = names_dict[var_name]
                        out.write("    " + var_name + " = " + var_val[1] + "\n")