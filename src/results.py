def write_results(mapIndex, sol_file):
    results = []
    results_temp = []
    solution = ""
    with open(sol_file, "r") as fd:
        for line in fd:
            results.append(line)
        fd.close()
    
    for n, el in enumerate(results):
        if(n == 0):
            solution = el
        else:
            results_temp = el.split(" ")
            for k in results_temp:
                if(k != "\n"):
                    solution += mapIndex[str(k)] + " "
                else:
                    solution += "\n"

    open(sol_file, "w").close()
    with open(sol_file, "a") as fd:
        fd.write(solution)
    fd.close()
