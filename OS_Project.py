import threading
import time

counter = -1
readyQueue=[]
waitingQueue = []
RR = []
listofProcesses=[]
Q = int(10)
StartEnd=[]
requestQueue =[]
ReqList=[]
DeadLoakList=[]
copylist=[]
j=0
Resources = [{"name":"R[1]" , "work" : -1 , "request" : []},
             {"name":"R[2]" , "work" : -1 , "request" : []},
             {"name":"R[3]" , "work" : -1 , "request" : []},
             {"name":"R[4]" , "work" : -1 , "request" : []},
             {"name":"R[5]" , "work" : -1 , "request" : []}]

IO_Queue =[]
threadlist =[]
Deadtime=[] 
IOLIST=[]

CPU = False

fileName = "Process.txt" 
#fileName = "s.txt" 

def parse_operations(operations_str):
    operations = []
    # Split operations based on "  " (double spaces are the separator)
    ops = operations_str.split("  ")
    for op in ops:
        if "{" in op:  # Ensure it's a valid operation
            op_type, details = op.split("{")
            details = details.rstrip("}").split(", ")
            # Convert details into the new format
            parsed_details = []
            for d in details:
                if ":" in d:  # Check if it's a key-value pair (e.g., "R: 2")
                    key, value = d.split(": ")
                    parsed_details.append(f"{key.strip()}{value.strip()}")
                else:
                    parsed_details.append(int(d) if d.isdigit() else d)
            operations.append({"type": op_type.strip(), "details": parsed_details})
    return operations

def read_and_store_data(fileName):
    global copylist
    data = []
    with open(fileName, "r") as file:
        for line in file:
            if line.strip():  # Skip empty lines
                # Split the line into the first three fields and the rest
                parts = line.strip().split(maxsplit=3)
                row = {
                    "PID": int(parts[0]),
                    "Arrival Time": int(parts[1]),
                    "Priority": int(parts[2]),
                    "Sequence": parse_operations(parts[3]) if len(parts) > 3 else [],
                }
                row0={
                    "PID": int(parts[0]),
                    "Arrival Time": int(parts[1]),
                    "Priority": int(parts[2]),
                    "Sequence": parse_operations(parts[3]) if len(parts) > 3 else [],
                }
                data.append(row)
                copylist.append(row0)
    return data


def timer ()-> None :
    global  counter
    global requestQueue
    global waitingQueue
    global readyQueue
    global Resources
    global dataList
    global DeadLoakList
    while len (dataList) != 0 or len (readyQueue) != 0  or len(waitingQueue) != 0 or  len(RR)!= 0 or  len(IO_Queue) != 0 or len(requestQueue) != 0 or len(DeadLoakList)!=0 :
            if j==0:
                counter+=1
                #print(counter)
                time.sleep(0.5)

       # if len (dataList) != 0 or len (readyQueue) != 0  or len(waitingQueue) != 0  :
           # break

def addProcess () -> None:
    global counter
    global dataList
    global readyQueue
    #print(len(dataList))
    while len(dataList) > 0 :
        

        for i in list(dataList) :
           # print(i["Sequence"][0]["type"])
            if int(i["Arrival Time"]) <= int(counter):
                if str(i["Sequence"][0]["type"])==str("CPU"):
                    readyQueue.append(i)
                    readyQueue.sort(key=lambda x: x["Priority"])
                    print("ADD Process :)")
                    dataList.remove(i)
                elif str(i["Sequence"][0]["type"])==str("IO"): 
                    waitingQueue.append(i)
                    IO_Queue.append(i)
                    print("ADD Process to waiting:)")
                    dataList.remove(i)

def addRR ()-> None:
    global RR
    global readyQueue
    global dataList
    global waitingQueue
    global DeadLoakList,j
    time.sleep(0.1)

    while len (dataList) != 0 or len (readyQueue) != 0  or len(waitingQueue) != 0 or len(IO_Queue)!=0 or len(RR)!=0 or len(DeadLoakList)!=0:
     #print("s")
     #if len(RR)==0 and len(readyQueue)!=0:
     if len(readyQueue)!=0:
       #print(len(RR),len(readyQueue),"+++++++++++++++++++++++++++")
       #mostPriority=readyQueue[0]["Priority"]
        if int(len(RR))!=0:
            #print("saleh")
            
            mostPriority=RR[0]["Priority"]
            for i in list(readyQueue):
                if int(i["Priority"])==int(mostPriority):
                    #print("saleh1",mostPriority,RR[0])
                    RR.append(i)
                    readyQueue.remove(i)                
                    readyQueue.sort(key=lambda x: x["Priority"])

                elif int(i["Priority"])<int(mostPriority):
                    for z in RR:
                         readyQueue.append(z)
                         RR.remove(z)
                   # print("saleh2")
                    RR.append(i)
                    readyQueue.sort(key=lambda x: x["Priority"])
                     
        else:
           
           mostPriority=readyQueue[0]["Priority"] 
           for i in list(readyQueue):
               if int(i["Priority"])==mostPriority:
                    #print("saleh3")
                    RR.append(i)
                    readyQueue.remove(i)                
                    readyQueue.sort(key=lambda x: x["Priority"])
                    
           
                                  
               
                    

def IO_count(process)-> None:
    global counter
    global IO_Queue
    global waitingQueue
    global readyQueue
    try:
       
        IO_burst=int(process['Sequence'][0]['details'][0])
        timeFinish=int(counter)+int(IO_burst)
        #print(counter,IO_burst,timeFinish,"***********************************")
        while int(counter)!=int(timeFinish):
         pass
        process['Sequence'].remove(process['Sequence'][0])
        #print(process)
        if(len(process['Sequence'])==0):
            IO_Queue.remove(process)
            waitingQueue.remove(process)  
        else:
            #print("enter")
            readyQueue.append(process)
            IO_Queue.remove(process)
            waitingQueue.remove(process)
            readyQueue.sort(key=lambda x: x["Priority"])
            #print(IO_Queue,waitingQueue,readyQueue) 
    except Exception as e:
        print(f"An error occurred in IO_count: {e}")


def cheakeDeadeLoak(Resources:list,pid:int,pidm:int):
    global j
    j=1
    for R in Resources:
        if int(pid) in R["request"]:
            if int(R["work"])==pidm:
                return pidm
            if int(R["work"]==-1):
                pass
            elif int(cheakeDeadeLoak(Resources,R["work"],pidm))==-1:
                pass
            elif int(cheakeDeadeLoak(Resources,R["work"],pidm))==pidm:
                return pidm
    j=0        
    return -1       

def solveDeadLock(Resources:list,pid:int):
    global j
    j=1
    for R in Resources:
        if R['work']==pid :
            R['work']=-1
        if pid in R['request']:
            R['request'].remove(pid)
    j=0        

def resolveDeadloak():
    global DeadLoakList ,dataList,readyQueue,RR,waitingQueue,IO_Queue,requestQueue,j,Deadtime

    while len (dataList) != 0 or len (readyQueue) != 0 or len(RR)!= 0  or len(waitingQueue) != 0 or   len(IO_Queue) != 0 or len(requestQueue) != 0 or len(DeadLoakList)!=0 :                     
        if len (dataList) == 0 and len (readyQueue) == 0 and len(RR)== 0  and len(waitingQueue) == 0 and   len(IO_Queue) == 0 and len(requestQueue) == 0 :
            if len(DeadLoakList)!=0:
                j=1
                #print(DeadLoakList)
                time.sleep(1)
                for i in list(DeadLoakList):
                    readyQueue.append(i)
                    readyQueue.sort(key=lambda x: x["Priority"])
                    DeadLoakList.remove(i)
                    for p in list(Deadtime):
                        if p["PID"]==i["PID"]:
                            p["end"]=counter
                    #print(Resources)
                j=0    

def IO()-> None:
    global IO_Queue
    global dataList
    global readyQueue
    global waitingQueue
    global DeadLoakList

    while len (dataList) != 0   or len(waitingQueue) != 0 or len(IO_Queue)!=0 or len(RR)!=0 or len (readyQueue) != 0 or len(DeadLoakList)!=0:
        #print("*******************",len(IO_Queue))
   
        if(len(IO_Queue)!=0):
            #print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            for Process in list(IO_Queue):
                #print("enter IO")
                threadT = threading.Thread(target=IO_count,args=(Process,))
                threadT.start()
                threadlist.append(threadT)
            for threadi in list(threadlist) :
                threadi.join()
            for threadi in list(threadlist) :
                threadlist.remove(threadi)


def request () -> None:
    global requestQueue
    global waitingQueue
    global readyQueue
    global Resources
    global dataList
    global counter
    global ReqList
    global DeadLoakList
    while len (dataList) != 0 or len (readyQueue) != 0  or len(waitingQueue) != 0 or len(RR) != 0 or len(DeadLoakList)!=0:
     #print("s")
     while len(requestQueue) != 0 : 
        requestQueue.sort(key=lambda x: x["Priority"])
        
        for Process in requestQueue :
            for Res in Resources : 
                if (Process["PID"]) in Res["request"] and Res["work"] == -1 :
                    Res["work"] = Process["PID"]
                    Res["request"].remove(int(Process["PID"]))
                    readyQueue.append(Process)
                    readyQueue.sort(key=lambda x: x["Priority"])
                    waitingQueue.remove(Process)
                    requestQueue.remove(Process)
                    for x in ReqList:
                        if int(x["pid"])==int(Process["PID"]):
                            x["end"]=counter


def scheduling():
    global CPU
    global counter
    global Q
    global dataList
    global readyQueue
    global waitingQueue
    global requestQueue
    global RR
    global Resources
    global StartEnd
    global listofProcesses
    global IOLIST
    global ReqList
    global j
    global DeadLoakList
    global copylist
    global Deadtime
    while len (dataList) != 0 or len (readyQueue) != 0 or len(RR)!= 0  or len(waitingQueue) != 0 or   len(IO_Queue) != 0 or len(requestQueue) != 0 or len(DeadLoakList)!=0 :
            #print("ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
        #if not CPU:
           # CPU = True
            #print("CPU is now in use")
            #stop = counter
            while len(RR)!=0:
                #print(RR)

               
                for ind in range(len(RR)):
                    
                    Process=RR[0]
                #for Process in list(RR): #loop for each process , like P1 , P2
                    
                    #start=20
                    #endofQu=30
                    #while(counter<endofQu)
                    index = 0 # for number of Sequence
                    endofqu = int(counter) + int(Q)
                    start = int(counter)
                    
                    #print("l")
                    while index < len(Process["Sequence"]) and (Process in RR) and counter<endofqu   : # loop for seque
                        #print("s")
                        
                        l = Process["Sequence"][index]
                        
                        if l["type"] == "CPU": # to check the type of preocess in sequance

                            print("Sequence11" , l , "Counter : ",counter)

                                                    #and len(l['details'])!=0
                            #print ("end",endofqu)
                            #print ("start",start)

                            while(counter<endofqu and (Process in RR) and (l in Process["Sequence"] ) and len(l['details'])!=0):
                                #print("**")
                           
                                #for i in list( l['details']) : # loop for details list in  Sequence
                                    i=l['details'][0]
                                    #print(i)
                                    #print("**")
                               
                                    if str(i).startswith('R') :
                                        #j=1

                                        for Res in Resources : # for loop to requset or give the process resourses
                                               
                                            if i == Res["name"] :#to check which resourse
                                                if Res["work"] == -1 : # to check if the resourese is avalable
                                                    # give the resourse to the process
                                                    if i in Res["request"] :
                                                        Res["request"].remove( Process["PID"])
                                                        Res["work"] = int(Process["PID"])
                                                    else:
                                                        Res["work"] = int(Process["PID"])
                                                        l['details'].remove(i)
                                                        if (len(l["details"]) == 0 ):
                                                                Process["Sequence"].remove(l)
                                                        if(len(Process["Sequence"])==0):
                                                                RR.remove(Process)    
                                                        #print(i1["name"])
                                                else : # if the resourse is not avalable , add the PID process to the request list
                                                    Res["request"].append(int( Process["PID"]))
                                                    l['details'].remove(i) # remove it because we add it to the request List
                                                    Dead=cheakeDeadeLoak(Resources,int( Process["PID"]),int( Process["PID"]))
                                                    if Dead==-1:
                                                        print("there are no Deadloak")
                                                        #print(DeadLoakList)
                                                        waitingQueue.append(Process)
                                                        requestQueue.append(Process)
                                                        x={"pid":Process["PID"] ,"start":counter , "end":0}
                                                        ReqList.append(x)
                                                        RR.remove(Process)
                                                    
                                                        
                                                    else:
                                                        print("there are Deadloak",int(Process["PID"]))
                                                        j=1
                                                        for a in copylist:
                                                             if int(a["PID"])==int(Process["PID"]):
                                                                 time0={"start":counter,
                                                                        "end":0,
                                                                        "PID":Process["PID"]}
                                                                 Deadtime.append(time0)
                                                                 DeadLoakList.append(a)
                                                                 #print(a,"**********************")
                                                                 break
                                                        j=0                
                                                        #se={"PID":Process["PID"],"Start":start,"End":counter ,"Arrival Time":Process["Arrival Time"] } # store in decit
                                                        #StartEnd.append(se) #store in the start end list for guin chart
                                                        solveDeadLock(Resources,int(Process["PID"]))
                                                        RR.remove(Process) 
                                                        #print(RR)   
                                                        #print(Resources)
                                                    #waitingQueue.append(Process)
                                                    #requestQueue.append(Process)
                                                    #RR.remove(Process) 
                                        #j=0            
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    #if (len(l["details"]) == 0 ):
                                                        #Process["Sequence"].remove(l)
                                                    #if(len(Process["Sequence"])==0):
                                                       #RR.remove(Process)
                                                       
                                         #*******************************waitQ******************************************************************************
                                    elif str(i).startswith('F') :#to finsh the allocate resourse
                                        #print("*****************")
                                        j=1
                                        new_char = "R"
                                        TF = new_char + i[1:]
                                        for re in Resources : # for loop to find and remove the given instance resourses
                                            #print(re["name"])

                                            if str(TF) == str(re["name"]) : # to find the instance that had been given
                                               # print(str(TF),str(re["name"]),TF,re["name"])
                                                #print("saleh")
                                                re["work"] = -1 # reset the instance is avilable
                                                #print(Resources)
                                                l['details'].remove(i) # remove the detales from the secq , Like F[x]
                                                if (len(l["details"]) == 0 ):
                                                    Process["Sequence"].remove(l)
                                                if(len(Process["Sequence"])==0): # to check if the sequance is empty
                                                    RR.remove(Process) # then remove it
                                        j=0            
                                       
                                    else : # for the CPU burst
                                   
                                        #20
                                        #print(i,"*********************")
                                        #qu =int (i)
                                        if int (i) < Q: # if the reminder cpu burst less than Quntum
                                            start=counter
                                            while(counter!=start+int (i)): # for waiting to let the process to finsh it's work
                                                pass
                                            se={"PID":Process["PID"],"Start":start,"End":counter ,"Arrival Time":Process["Arrival Time"] } # store in decit
                                            StartEnd.append(se) #store in the start end list for guin chart

                                            l['details'].remove(i) # remove the cpu burst from details list when it finsh
                                            if (len(l["details"]) == 0 ):
                                                Process["Sequence"].remove(l)
                                            if(len(Process["Sequence"])==0): # # to check if the sequance is empty
                                                RR.remove(Process) # then remove it
                                        else:
                                            start=counter
                                            while(counter!=start+Q):#edit i*************************************************************
                                                pass
                                            se={"PID":Process["PID"],"Start":start,"End":counter ,"Arrival Time":Process["Arrival Time"] } # store in decit
                                            StartEnd.append(se)
                                            newburst = l['details'].index(i)
                                            l['details'][newburst] = int(i) - int(Q)
                                            if  int(l['details'][newburst]) == 0 :

                                              l['details'].remove(0)
                                              #time.sleep(1.3)
                                              #print("*+*+*+*+*++*+*+*+*+*+*+*+*+")
                                            if (len(l["details"]) == 0 ):
                                                Process["Sequence"].remove(l)
                                                if(len(Process["Sequence"])!=0):
                                                    if Process["Sequence"][0]["type"]==str("IO"):
                                                        waitingQueue.append(Process)
                                                        IO_Queue.append(Process)
                                                        j=1
                                                        Dicat1={"PID":int(Process["PID"]),"burst":int(Process["Sequence"][0]["details"][0])}
                                                        IOLIST.append(Dicat1)
                                                        #print(IOLIST)
                                                        RR.remove(Process)
                                                        j=0
                                                        

                                                #time.sleep(1.3)
                                                #print("**")
                                            if(len(Process["Sequence"])==0): # # to check if the sequance is empty
                                                RR.remove(Process) # then remove it
                                                #time.sleep(1.3)
                                                #print("***")




                            if counter==endofqu and Process in list(RR):
                                #print("*************************************")
                                if len(RR)>1:
                                    #time.sleep(0.01)
                                    #print("good")

                                    RR.remove(Process)
                                    RR.append(Process)
                                    #time.sleep(0.01)
                                    #print(RR)
                                    #print(IO_Queue)        #mid = (int(start) + int(Q)) if qu > 10 else (int(start) + qu)
                                    
                                
                                    #print("s")        #dictCPU = {"PID" : ,"start" : start , "end" : end , "mid" : mid }                            
                        else :  #for IO
                            #print("sssssssssssssssssssssssssssssssss")
                            waitingQueue.append(Process)#add it to wait queue when we finish it we return it to ready queue without IO
                            IO_Queue.append(Process) #in this queue we need to creat threads =number of len of this queue every thread count this Io berst
                            Dict={"PID":int(Process["PID"]),"burst":int(Process["Sequence"][0]["details"][0])}
                            IOLIST.append(Dict)
                            #print(IOLIST)
                            RR.remove(Process)
                            #print("****")
                    
                    

                                   

                                   
        #elif len (RR) == 0 :
            #print("CPU is not in use")
         #   CPU = False 
                        
dataList = read_and_store_data(fileName)



thread2 = threading.Thread(target=addProcess)
thread1 = threading.Thread(target=timer)
thread3 = threading.Thread(target=addRR)
thread4 = threading.Thread(target=IO)
thread5 = threading.Thread(target=request)
thread6 = threading.Thread(target=resolveDeadloak)

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
#thread1.join()
#thread2.join()
#thread3.join()
print("laith")
scheduling ()

L=[]
#print(StartEnd)
avgTurnaroundTime=0
avgWaitingTime=0
def Avg_waiting () -> None: 
 global StartEnd , L ,avgWaitingTime ,IOLIST , ReqList , avgTurnaroundTime
 print()
 print("Gantt Chart 😊")

 for i in StartEnd : 
    print("|" ,i['Start']," ","P",i['PID']," ",i['End'],"|" ,  end=" ")
    flage=0
 
    for z in L:
        if z["PID"]==i["PID"]:
            flage=1
    if flage==0:
        k={"PID":i["PID"],"varible":int(i["Arrival Time"]),"sum":0 , "Arrival Time" : int(i["Arrival Time"])}
        L.append(k)


 for o in StartEnd:
    for l in L:
        if int(o["PID"])==int(l["PID"]):
            index1=L.index(l)
            L[index1]["sum"]+=int(o["Start"])-int(l["varible"])
            L[index1]["varible"]=o["End"]

 for l in L:
    for i in list(IOLIST):
        if int(i["PID"])==int(l["PID"]):
            index2=L.index(l)
            L[index2]["sum"]-=int(i["burst"])
            IOLIST.remove(i)
    #print (ReqList)
    for y in list(ReqList):
        if int(y["pid"])==int(l["PID"]):
            index3=L.index(l)
            L[index3]["sum"]-=int(int(y["end"])-int(y["start"]))
            ReqList.remove(y)
 #print(L)
 for process in L : 
    #print(process["sum"])
    avgWaitingTime += int(process["sum"])
 for p in list(Deadtime):
       avgWaitingTime-=(int(p["end"])-int(p["start"])) 

 avgWaitingTime = int(avgWaitingTime) / len(L)
 print()
 print()
 for i in L : 
    avgTurnaroundTime += int(i ["varible"]) - int(i["Arrival Time"])

 print("Average waiting Time: ",avgWaitingTime)
 print("Average Turnaround Time: ",avgTurnaroundTime / len(L))

Avg_waiting ()
print("done :)")