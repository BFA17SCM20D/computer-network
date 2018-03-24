import os
network = []
weights = {}
inActive = []
source = None 
end = None
#creates a topology matrix by accepting a text file as input
def createTopology():
    global network
    network = []
    try:
        with open(raw_input("Please enter the file name \nHere:")) as fp:
            for line in fp:
                network.append(map(int,line.split()));
            print "Review original topology matrix:"
        for _ in range(len(network)):
            for _weight in network[_]:
                print _weight, 
            print
        calculateDistances()
    except Exception as e:
        print e, "Please try again"
        createTopology()
#calculates the distances using Dijkstras algorithm
def calculateDistances():
    global weights
    network
    weights = {}
    for i in range(len(network)):
        _ = {}
        for j in range(len(network)):
            if i !=j and network[i][j] > 0:
                _[j+1] = network[i][j]
        weights[i+1] = _
    return 
def dj(start):
    network, weights
    uncovered = {router : None for router in range(1,len(network)+1)}
    covered = {router : None for router in  range(1,len(network)+1)}
    previous = {router : None for router in  range(1,len(network)+1)}
    interface = {router : None for router in  range(1,len(network)+1)}
    currentCost = 0 
    current = int(start)
    uncovered[current] = currentCost
    while True: 
        for router,cost in weights[current].items():
            if router not in uncovered: continue 
            totalCost = currentCost + cost
            if not uncovered[router] or uncovered[router] > totalCost:
                uncovered[router] = totalCost
                previous[router] = current 
                interface[router] = router if not interface[current] else interface[current]
        
        covered[current] = currentCost
        del uncovered[current]
        _flag = True
        for x in uncovered:
            if uncovered[x]:
                _flag = False
                break
        if not uncovered or _flag:
            break
    
        _current_nodes = []
        for k, v in uncovered.items():
            if v:
                _current_nodes.append((k,v)) 
        
        if len(_current_nodes) > 0:
            current,currentCost =  sorted(_current_nodes, key = lambda x: x[1])[0]
    return previous,covered, interface   

    
#PrintOptins function prompts the user to select the available options and execute                     
def printOptions():
    global selectedOption
    option = raw_input("Please enter 1 of the following options \n 1: To create topology \n 2: get the instances \n 3: To get the shortest path \n 4: To delete a router \n 5: To find the most accisable router \n 6: Exit \n Here:")
    if option.isdigit():
        option = int(option)
        if option < 7 and option > 0:
            selectedOption = option
        else:
            print "Enter valid option"
            printOptions()
    else:
        print "Enter valid option"
        printOptions()
#deleteRouter fuction deletes the router which is to be downed.

def deleteRouter(n):
    global network 
    network
    
    for i in range(len(network)):
        network[i][n-1] = -1
        network[n-1][i] = -1
        
    print "New topology"
    for _ in range(len(network)):
        for _weight in network[_]:
            print _weight, 
        print
#ShortestPath calculates the shortest path between the source and destination router
def shortestPath(start, end,previous,visited): 
    global path

    path = []
    dest = int(end)
    src = int(start)
    path.append(dest)
    while dest != src:
        print dest
        path.append(previous[dest])
        dest = previous[dest]
        
    cost = 0
    if visited[int(end)]:
        cost = visited[int(end)]
    
    return path, cost    
#validateOption checks if the given input  options are valid/invalid
def validateOption(inp):       
    _ = inp
    if _.isdigit():
        _ = int(_)
        if _ <= len(network) and  _ > 0: 
            return True 
        else:
            return False
    else:
        return False
#input the source router
def getSource():
    source = raw_input("Enter source router: ")
    if validateOption(source):
        source = int(source)
        return source
    else: 
        print "Invalid entry try again"
        getSource()
#input the destination router
def getDest():
    end = raw_input("Enter end router: ")
    if validateOption(end):
        end = int(end)
        return end
    else: 
        print "Invalid entry try again"
        getDest()
#Prints the main menu on prompt based on the selected option by user        
    
printOptions()
while(selectedOption != 6):
    
    if selectedOption ==1:
        if network:
            print "Network present, Do you want to over writer?"
            ans = raw_input("Y or type anything to continue with the same network")
            if ans.capitalize() == "Y": 
                createTopology()
                printOptions()
            else:
                print "Continuting with the existing network"
                printOptions()
        else:     
            createTopology()
            printOptions()
            
    elif selectedOption ==2 : 
        if network:
            source = getSource()
            if source not in inActive:
                source = int(source)
                _, _x,interface = dj(source)
                print "Destination \t  Interface"
                print "==========================="
                for k, v in interface.items():
                    print "\t",k,"\t    ", v
                printOptions()
            else:
                print "Source inactive"
                selectedOption =2     
        else:
            print "please create the network topology first"
            printOptions()  
            
    elif selectedOption == 3:
        if network: 
            end = getDest()
            if end not in inActive:
                if source != end:
                    _previous, _covered,_interface = dj(source)
                    _path, _cost = shortestPath(source,end,_previous,_covered)
                    for _ in reversed(_path): 
                        print _, "->",
                    print "and the total cost is", _cost
                    print 
                    nextStep = raw_input("Press 'Y' to test other router (or) type anything for main menu")
                    if nextStep.capitalize() == "Y":
                        selectedOption = 3
                    else:
                        printOptions()
                else:
                    print "Source and destination match"
                    selectedOption = 3
            else: 
                 print "destination inactiv"
                 selectedOption = 3
                
        else:
            print "please create the network topology first"
            printOptions()   

    elif selectedOption == 4:
        print "Source is : ", source ," End is ", end
        if network:
            router = raw_input("Please select the router to make it down: ")
            if validateOption(router):
                router = int(router)
                if source == router or end == router:
                    print "The router is disabled from the network" 
                    printOptions()
                else:
                    deleteRouter(router)
                    calculateDistances()
                    inActive.append(router)
                    if source == None or end == None: 
                        _input = raw_input("Press Y to enter the source or destination router: ")
                        if _input.capitalize() == 'Y':
                            if source == None:
                                source = getSource()
                                print source
    
                            if end == None:
                                end = getDest()
                                print end
                            print source, router, end
                            if source == router or end == router:
                                print "Exiting to main menu : Source or destination matches the router"
                                printOptions()
                            else:
                                _previous, _covered, _ = dj(source)
                                _path, _cost = shortestPath(source,end,_previous,_covered)
                                for route in reversed(_path):
                                    print route, "-->", 
                                print "And the total is", _cost
                                printOptions()
                                
                        else:
                            print "Main Menu"
                            printOptions()
                    else:
                        if source != None or end != None: 
                            _previous, _covered, _ = dj(source)
                            _path, _cost = shortestPath(source,end,_previous,_covered)
                            for route in reversed(_path):
                                print route, "-->", 
                            print "And the total is", _cost
                            printOptions()
                        else:
                            print "Main Menu"
                            printOptions()                            

            else: 
                print "Please enter a valid router to make it down"
                selectedOption = 4        
        else:
            print "please create the network topology first"
            printOptions()                            
    
    elif selectedOption == 5:
        if network: 
            track = []
            calculateDistances()
            for router in range(1, len(network)+1):
                _1,_2,_3 = dj(router)
                track.append(_2)
            least = float('inf')
            for i in range(len(track)):
                total = 0 
                for v in track[i].values():
                    if v !=None:
                        total += v
                if total > 0:
                    if total < least: 
                        least = total 
                        router = i + 1
            print "router is" ,router, "And total is", least
            printOptions()
             
        else:
            print "please create the network topology first"
            printOptions()   
print("thanks for the business")
