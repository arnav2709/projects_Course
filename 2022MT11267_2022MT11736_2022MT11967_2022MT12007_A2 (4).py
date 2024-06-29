import numpy as np
EPSILON = 1e-6
def gomory_cut_algo():
    def Read_Input():
        objective = None
        A = None
        B = None
        T = None
        C = None
        with open("input_ilp.txt", "r") as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()  
            
                if not line: 
                    i += 1
                    continue
            
                if line.startswith("[objective]"):
                    objective = lines[i + 1].strip()
                    i += 2
                elif line.startswith("[A]"):
                    A_lines = []
                    i += 1
                    while i < len(lines) and not lines[i].startswith("[") and lines[i].strip(): 
                        A_lines.append(lines[i])
                        i += 1
                    A = np.array([[int(x) for x in row.strip().split(",")] for row in A_lines])
                elif line.startswith("[b]"):
                    
                    B_lines = []
                    i += 1
                    while i < len(lines) and not lines[i].startswith("[") and lines[i].strip():  
                        B_lines.append(lines[i])
                        i += 1
                    B = np.array([[int(x)] for x in B_lines])
                elif line.startswith("[constraint_types]"):
                    T_lines = []
                    i += 1
                    while i < len(lines) and not lines[i].startswith("[") and lines[i].strip(): 
                        constraint_type = lines[i].strip()
                        if constraint_type == "<=":
                            T_lines.append(0)
                        elif constraint_type == ">=":
                            T_lines.append(1)
                        elif constraint_type == "=":
                            T_lines.append(2)
                        i += 1
                    T = np.array(T_lines)
                elif line.startswith("[c]"):
                    C_lines = lines[i + 1].strip().split(",")
                    C = np.array([int(x) for x in C_lines])
                    i += 2
        
        return objective,A,B,T,C
        
    objective,A,B,T,C=Read_Input()
    temp=C
    ori_m,ori_n=A.shape
    m,n=A.shape
    B=B.flatten()
    if(objective=="maximize"):
        C=-1*C
    def modify_matrix(A, c):
        m, n = A.shape
        for i in range(len(c)):
            if c[i] == 0:
                new_column = np.zeros((m, 1))
                new_column[i] = 1
            elif c[i] == 1:
                new_column = np.zeros((m, 1))
                new_column[i] = -1
            elif c[i]==2:
                continue
            A = np.hstack((A, new_column))
        return A

    A=modify_matrix(A,T)
    for i in range(len(B)):
        if(B[i]<0):
            A[i]=-1*A[i]
            B[i]=-1*B[i]

    def ini_bfs(matrix_A, vector_b, vector_c, num_vars):
        orig_num_vars = num_vars
        aux_A = np.concatenate((matrix_A, np.identity(len(matrix_A))), axis=1)
        b_reshaped = vector_b.reshape(-1, 1)
        initial_tableau = np.concatenate((b_reshaped, aux_A), axis=1)
        aux_c = np.concatenate((np.zeros(len(matrix_A.T)), np.ones(len(matrix_A))))
        aux_basic_indices = np.array(range(len(matrix_A.T), len(aux_A.T)))
        basic_indices, neg_cost, reduced_costs, tableau, type1, _ = Simplex_Iteration(aux_A, vector_b, aux_c, aux_basic_indices)
        if abs(neg_cost) >= EPSILON:
            return -1, -1, -1, initial_tableau, -1, -1, orig_num_vars, tableau
        if any(basic_indices >= len(matrix_A.T)):
            artificial_vars = []
            for i in range(len(basic_indices)):
                if(basic_indices[i]>=len(matrix_A.T)):
                    artificial_vars.append(i)
            to_delete = []
            for var in artificial_vars:
                row = tableau[var][1:]
                for i in range(0, len(row)):
                    if i not in basic_indices and row[i] != 0 and i < len(matrix_A.T):
                        basic_indices[var] = i
                        break
                if basic_indices[var] >= len(matrix_A.T):
                    to_delete.append(var)
            for var in to_delete:
                tableau = np.delete(tableau, basic_indices[var] + 1, axis=1)
                basic_indices = np.delete(basic_indices, var)
                vector_b = np.delete(vector_b, var)
                matrix_A = np.delete(matrix_A, var, axis=0)
                tableau = np.delete(tableau, var, axis=0)

        table = np.delete(tableau.T[1:], range(0, len(matrix_A.T)), 0).T
        return basic_indices, matrix_A, vector_b, initial_tableau, table, 0, orig_num_vars, tableau

    def Simplex_Iteration(A, b, c, basic_indices):
        basis = get_cols(A, basic_indices)
        basis_inverse = np.linalg.inv(basis)
        tableau = np.concatenate((np.atleast_2d(np.dot(basis_inverse, b)).T, 
            np.dot(basis_inverse, A)), axis=1)
        
        basic_cost_coeff = get_cols(c, basic_indices)[0]
        neg_cost = -np.dot(basic_cost_coeff, tableau.T[0])
        reduced_costs = c - np.dot(basic_cost_coeff, tableau.T[1:].T)
        while not all(reduced_costs > np.zeros(len(reduced_costs)) - EPSILON):
            entering_index = 0
            for index in range(len(reduced_costs)):
                if reduced_costs[index] < -EPSILON:
                    entering_index = index
                    break
            entering_col = tableau.T[1:][entering_index]
            ratios = []
            for i in range(len(basic_indices)):
                if entering_col[i] > 0:
                    ratios.append(tableau.T[0][i] / entering_col[i])
                else: 
                    ratios.append(float('inf'))
            if not any(np.array(ratios) < float('inf')):
                return -2,-2,-2,tableau,-2,-2
            exiting_index = ratios.index(min(ratios))
            for row in range(len(tableau)):
                if row != exiting_index:
                    tableau[row] -= (tableau[exiting_index] * 
                    entering_col[row] / entering_col[exiting_index])
                else:
                    tableau[row] /= entering_col[exiting_index] 
            basic_indices[exiting_index] = entering_index
            neg_cost -= (reduced_costs[entering_index] 
                * tableau.T[0].T[exiting_index])
            reduced_costs -= (reduced_costs[entering_index] 
                * tableau.T[1:].T[exiting_index])
        return basic_indices, neg_cost, reduced_costs, tableau,0,basis_inverse
                

    def get_cols(M, indices): 
        return np.column_stack([M.T[i] for i in indices])       
    def optimize(matrix_A, vector_b, vector_c, num_vars):
        basic_indices, matrix_A, vector_b, tableau, table, type1, orig_num_vars, first_phase_tableau = ini_bfs(matrix_A, vector_b, vector_c, num_vars)
        initial_tableau = tableau
        if type1 == -1:
            return -1, -1, -1, initial_tableau, -1, -1, -1, orig_num_vars, first_phase_tableau
        basic_indices, neg_cost, reduced_costs, tableau, type2, b_inv = Simplex_Iteration(matrix_A, vector_b, vector_c, basic_indices)
        return -neg_cost, basic_indices, tableau, initial_tableau, table, type2, b_inv, orig_num_vars, first_phase_tableau
    def Simplex_Iteration_output(basis_indices,optimal_cost,table,ini_tableau,tableau,type,b_inv,ori_n,first_phase_tableau):
        initial_tableau=ini_tableau.tolist()
        if type==-1:
            initial_tableau=ini_tableau
            final_tableau=first_phase_tableau
            solution_status = "infeasible"
            optimal_solution = None
            optimal_value = None
            output_dict = {
            "initial_tableau":initial_tableau,
            "final_tableau": final_tableau,
            "solution_status": solution_status,
            "optimal_solution": optimal_solution,
            "optimal_value": optimal_value
            }
            return output_dict
        elif type==-2:
            final_tableau = tableau.tolist()
            initial_tableau=ini_tableau
            final_tableau=tableau
            solution_status = "unbounded"
            optimal_solution = None
            optimal_value = None
            output_dict = {
            "initial_tableau":initial_tableau,
            "final_tableau": final_tableau,
            "solution_status": solution_status,
            "optimal_solution": optimal_solution,
            "optimal_value": optimal_value
            }
            return output_dict   
        m, q = tableau.shape
        n=q-1
        tableau_f= np.zeros((m, n + 1+m))
        

        tableau_f[:, 0] = tableau[:,0]
        for j in range(1, n + 1):
            tableau_f[:, j] = tableau[:,j]
        for k in range(n+1,n+m+1):
            tableau_f[:,k]=np.dot(b_inv,table[:,k-n-1])
            solution_status = "optimal"
            optimal_solution=[0]*ori_n
            for i in range(0,len(basis_indices)):
                if(basis_indices[i]<ori_n):
                    optimal_solution[basis_indices[i]]=tableau[i,0]
            optimal_value = optimal_cost
        final_tableau = tableau.tolist()
        output_dict = {
            "initial_tableau": ini_tableau,
            "final_tableau": tableau,
            "solution_status": solution_status,
            "optimal_solution": optimal_solution,
            "optimal_value": optimal_value,
            "basic_indices":basis_indices
        }
        return output_dict
    C=C.tolist()
    C=C+[0]*(len(A[0])-len(C))
    C=np.array(C)
    cost,indices,tableau,ini_tableau,table,type,b_inv,ori_n,first_phase_tableau=optimize(A,B,C,ori_n)
    if(objective=="maximize"):
        cost=-1*cost
    C=C.tolist()
    C=C+[0]*(len(A[0])-len(C))
    C=np.array(C)
    output=Simplex_Iteration_output(indices,cost,table,ini_tableau,tableau,type,b_inv,ori_n,first_phase_tableau)
    solution_status=output["solution_status"]
    if(solution_status=="infeasible"):
        print("initial_solution: ",None)
        print("final_solution: ",None)
        print("solution_status: ",solution_status)
        print("number_of_cuts: ",0)
        print("optimal_value: ",None)
        return
    elif(solution_status=="unbounded"):
        print("initial_solution: ",None)
        print("final_solution: ",None)
        print("solution_status: ",solution_status)
        print("number_of_cuts: ",0)
        print("optimal_value: ",None)
        return 
    tableau=output["final_tableau"]
    inital_sol=output["optimal_solution"]
    basic_indices_simplex=output["basic_indices"]
    basic_cost_coeff = get_cols(C,basic_indices_simplex)[0]
    neg_cost=-np.dot(basic_cost_coeff, tableau.T[0])
    reduced_costs = C - np.dot(basic_cost_coeff, tableau.T[1:].T)
    reduced_costs=reduced_costs.tolist()
    zeroth_row=[neg_cost]+reduced_costs
    zeroth_row=np.array(zeroth_row)
    tableau=np.vstack((zeroth_row,tableau))
    basic_indices_simplex+=1
    cols=len(tableau[0])
    rows=len(tableau)
    def dual_simplex(tableau,basic_indices):
        while not all(tableau[1:, 0] > np.zeros(len(tableau[1:])) - EPSILON):
            exiting_index=0
            for index in range(len(tableau[1:])):
                    if (tableau[1:, 0][index]<-EPSILON):
                        exiting_index=index
                        break
            exiting_row=tableau[exiting_index+1] 
            ratios=[]
            for i in range(len(exiting_row)-1):
                    if exiting_row[i+1]<-EPSILON:
                        ratios.append(-1*(tableau[0][i+1] / exiting_row[i+1]))
                    else:
                        ratios.append(float('inf'))          
            if not any(np.array(ratios) < float('inf')):
                    return False
            entering_index=ratios.index(min(ratios))
            for row in range(len(tableau)):
                if row != exiting_index+1:
                    tableau[row]=tableau[row]-(tableau[exiting_index+1] * 
                    tableau[row][entering_index+1] / tableau[exiting_index+1][entering_index+1])
                else:
                    tableau[row] /= tableau[exiting_index+1][entering_index+1]
                    basic_indices[exiting_index]=entering_index+1

        return True
    def solve(rows,cols,tableau,solution_status,basis,m,n):
        t=True
        if(solution_status=="infeasible" or solution_status=="unbounded"):
            t=False
        ct=0
        while(True):
            if t == False:
                return [None,ct]
            
            k = 0
            ratios=[]
            ratio_indices=[]
            for i in range(1,rows):
                if(tableau[i,0]%1 <= EPSILON or 1-tableau[i,0]%1 <= EPSILON):
                    continue
                else:
                    ratios.append(min(tableau[i,0]%1, 1-tableau[i,0]%1))
                    ratio_indices.append(i)
            if len(ratios)!=0:
             index_of_entering_ratio = ratios.index(max(ratios))
             k=ratio_indices[index_of_entering_ratio]
            if(k == 0):
                solution = np.zeros(n)
                for i in range(1,rows):
                    if(basis[i-1] <= n):
                        solution[basis[i-1]-1] =tableau[i,0]
                return [list(map(round, solution.tolist())),ct]
            tableau = np.concatenate((tableau, np.zeros(rows).reshape(-1,1)), axis=1)
            cols+=1
            tableau = np.concatenate((tableau, np.zeros(cols).reshape(1,-1)), axis=0)
            rows+=1
            ct+=1
            for i in range(0,cols-1):
                if(tableau[k,i]%1 <= EPSILON or 1-tableau[k,i]%1 <= EPSILON):
                    continue
                else:
                    tableau[rows-1, i] = - (tableau[k,i]%1)
            tableau[rows-1,cols-1] = 1
            basis = np.concatenate((basis,np.array([cols-1]).reshape(1)))
            t = dual_simplex(tableau,basis)
            if t == False:
                return [None,ct]

 

    [final_sol,cuts]=solve(rows,cols,tableau,solution_status,basic_indices_simplex,m,n)
    if(final_sol==None):
        print("initial_solution:",end=" ")
        print(', '.join(map(str, inital_sol)))
        print("final_solution: ","None")
        print("solution_status: ","infeasible")
        print("number_of_cuts: ",cuts)
        print("optimal_value: ","None")
    else:
        optimal_cost=np.dot(temp,final_sol)
        print("initial_solution:",end=" ")
        print(', '.join(map(str, inital_sol)))
        print("final_solution:",end=" ")
        print(', '.join(map(str, final_sol)))
        print("solution_status: ",solution_status)
        print("number_of_cuts: ",cuts)
        print("optimal_value: ",optimal_cost)

