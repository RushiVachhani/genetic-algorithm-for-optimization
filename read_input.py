file_path = "inputs.txt"

def get_equation_inputs():
    equation_inputs = []
    flag = False
    with open(file_path, 'r', encoding='utf8') as f:
        for line in f:
            if line.startswith('max_degree'):
                max_degree = int(line.split(" ")[2])
            if line.startswith('==='):
                flag = False
            if line.startswith('#equation_inputs'):
                flag = True
                continue
            if flag == True:
                equation_inputs.append(line.strip('\n').split(',')[0:max_degree])

    for i in range(0,len(equation_inputs)):
        equation_inputs[i] = list(map(int, equation_inputs[i]))

    return equation_inputs

def get_constraint_inputs():
    constraint_inputs = []
    flag = False
    with open(file_path, 'r', encoding='utf8') as f:
        for line in f:
            if line.startswith('num_of_variables'):
                num_variables = int(line.split(" ")[2])
            if line.startswith('==='):
                flag = False
            if line.startswith('#constraints'):
                flag = True
                continue
            if flag == True:
                constraint_inputs.append(line.strip('\n').split(',')[0:num_variables])

    for i in range(0,len(constraint_inputs)):
        constraint_inputs[i] = list(map(int, constraint_inputs[i]))
    
    return constraint_inputs

def get_condition_inputs():
    condition_inputs = []
    flag = False
    with open(file_path, 'r', encoding='utf8') as f:
        for line in f:
            if line.startswith('num_of_constraints'):
                num_constraint = int(line.split(" ")[2])
            if line.startswith('==='):
                flag = False
            if line.startswith('#condition'):
                flag = True
                continue
            if flag == True:
                condition_inputs.append(line.strip('\n').split(',')[0:num_constraint])

    for i in range(0,len(condition_inputs)):
        condition_inputs[i] = list(map(int, condition_inputs[i]))
    condition_inputs = condition_inputs[0]
    return condition_inputs

def get_variable_values():
    variable_values = []
    flag = False
    with open(file_path, 'r', encoding='utf8') as f:
        for line in f:
            if line.startswith('===='):
                flag = False
            if line.startswith('min_value_variable'):
                flag = True
            if flag == True:
                variable_values.append(float(line.split(" ")[2]))

    variable_values[2:] = list(map(int, variable_values[2:]))
    return variable_values
