#loading inputs
if __name__ == "__main__":
    var_count = int(input())
    domain = {}
    depend_dict = {}

    # loading domain values for the variables
    for v in range(var_count):
        domain[v] = [val.upper() for val in input().split(', ')]
        depend_dict[v] = []

    #creating dependency list and dict and initiating them with 0 do that we can iterate them in future.
    dependencies = []
    probability_dict = {}
    for v1 in range(var_count):
        dependencies.append([int(val) for val in input().split()])
        for v2 in range(var_count):
            if dependencies[v1][v2] ==1:
                depend_dict[v2].append(v1)
        probability_dict[v1] = [0]*(2**(len(depend_dict[v1])+1))

    #number of samples    
    samples_count = int(input())

    #loading samples
    samples = []
    for s in range(samples_count):
        samples.append([val.upper() for val in input().split(',')])

    #counting the number fo dependencies on given variables
        for v in range(var_count):
            dep_vars = depend_dict[v]
            # for non-dependent variables
            if len(dep_vars) == 0:
                indx = domain[v].index(samples[s][v])
                probability_dict[v][indx] += 1
            #for dependent variables
            else:
                dep_indx = 0
                length = 1
                
                for d in range(0,len(dep_vars)):
                    indx = dep_vars[len(dep_vars) -d -1]
                    dep_indx = dep_indx + length*(domain[indx].index(samples[s][indx]))
                    length = length*len(domain[indx])
                    
                dep_indx = dep_indx + length*domain[indx].index(samples[s][v])
                probability_dict[v][dep_indx] += 1
                      

    prob_dist = probability_dict
    ## finding the probability values
    for v in range(var_count):
        dom = domain[v]
        dep_var = depend_dict[v]
        #no dependent variable
        if len(dep_var) == 0:
            denom = sum(probability_dict[v])
            for d in range(len(dom)):
                num = probability_dict[v][d]
                prob_dist[v][d] = round(num/denom,4)

        else:
        #dependent variables
            length = 1
            for d in range(0,len(dep_var)):
                indx = dep_var[d]
                length = length* len(domain[indx])
            for l in range(0,length):
                denom = 0
                m = 0
                for m in range(len(dom)):
                    denom = denom + probability_dict[v][l+length*m]
                for m in range(len(dom)):
                    num = probability_dict[v][l+m*length]
                    prob_dist[v][l+m*length] = round(num/denom,4)


    for v in range(var_count):
        print(*prob_dist[v], sep = " ")
                


            

        
        