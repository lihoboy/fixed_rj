import Job
from Job import JOB
from gurobipy import *
from GanntChart import *
import DrawGan as DG
def main():

    '''read file'''
    file_path="data_2_5"
    num_rj, num_jobs, rj_list, Job_list=read_file("data/"+file_path)

    '''init'''
    num_machines=2
    num_T=0
    for i,j in enumerate(Job_list):
        num_T+=j.processing_time
    num_T=int(num_T*2/3)
    print(num_T)
    try:

        # Create a new model
        m = Model("fixed_rj")

        # Create variables
        Y={}
        for i in range(num_machines):
            for j in range(num_jobs):
                for t in range(num_T):
                    name="y_"+str(i)+"_"+str(j)+"_"+str(t)
                    Y[i,j,t]=m.addVar(vtype=GRB.BINARY, name=name)
        C={}
        for j in range(num_jobs):
            name = "c_" + str(j)
            C[j] = m.addVar(vtype=GRB.INTEGER, name=name)
        S={}
        for i in range(num_machines):
            for j in range(num_jobs):
                for t in range(num_T):
                    for k in range(num_rj):
                        name="s_"+str(i)+"_"+str(j)+"_"+str(k)+"_"+str(t)
                        S[i,j,k,t]=m.addVar(vtype=GRB.BINARY, name=name)
        O={}
        for i in range(num_machines):
            for j in range(num_jobs):
                for k in range(num_rj):

                    name = "o_" + str(i) + "_" + str(j) + "_" + str(k)
                    O[i, j, k] = m.addVar(vtype=GRB.INTEGER, name=name)
        # Set objective
        obj=LinExpr()
        for j in range(num_jobs):
            obj.addTerms(1,C[j])
        m.setObjective(obj, GRB.MINIMIZE)

        # Add constraint 1

        for j in range(num_jobs):
            c_1 = LinExpr()
            for k in range(num_rj):
                for i in range(num_machines):
                    c_1.addTerms(1, O[i,j,k])
            m.addConstr(c_1==Job_list[j].processing_time, "c1")

        # Add constraint 2
        for j in range(num_jobs):
            for t in range(num_T):
                c_2 = LinExpr()
                for i in range(num_machines):
                    c_2.addTerms(1, Y[i,j,t] )
                m.addConstr(c_2 <=1,"c2")

        # Add constraint 3
        for t in range(num_T):
            for i in range(num_machines):
                c_3 = LinExpr()
                for j in range(num_jobs):
                    c_3.addTerms(1, Y[i, j, t])
                m.addConstr(c_3 <= 1, "c3")

        # Add constraint 4
        for j in range(num_jobs):
            for t in range( num_T):
                for i in range(num_machines):
                    c_4 = LinExpr()
                    c_4.addTerms(t,Y[i,j,t])
                    m.addConstr(C[j] >= c_4+1,"c3")

        # Add constraint 5
        M=999
        for j in range(num_jobs):
            for i in range(num_machines):
                for k ,rj in enumerate(rj_list):
                    c_5 = LinExpr()
                    if k==num_rj-1:
                        for t in range(rj,num_T):
                            c_5.addTerms(1,Y[i,j,t])
                    else:
                        for t in range(rj,rj_list[k+1]):
                            c_5.addTerms(1,Y[i,j,t])
                    m.addConstr(c_5-O[i,j,k]+M*(1-S[i,j,k,t])>=0,"c5")
        # Add constraint 6
        for j in range(num_jobs):
            for i in range(num_machines):
                for k ,rj in enumerate(rj_list):
                    c_6=LinExpr()
                    if k==num_rj-1:
                        for t in range(rj,num_T):
                            c_6.addTerms(1,Y[i,j,t])
                    else:
                        for t in range(rj,rj_list[k+1]):
                            c_6.addTerms(1,Y[i,j,t])
                    m.addConstr(c_6 == O[i,j,k], "c5")
        # Add constraint 7
        for j in range(num_jobs):
            for i in range(num_machines):
                for k ,rj in enumerate(rj_list):
                    for t in range(rj,num_T):

                        m.addConstr(Y[i,j,t]+S[i,j,k,t]-2+M*(1-S[i,j,k,t])>=0, "c7")

        # Add constraint 8
        for j in range(num_jobs):
            for i in range(num_machines):
                for k, rj in enumerate(rj_list):
                    for t in range(rj, num_T):
                        m.addConstr( S[i, j, k, t]>= Job_list[j].release_date ,"c8")


        m.optimize()

        for v in m.getVars():
            print('%s %g' % (v.varName, v.x))

        print('Obj: %g' % m.objVal)

        '''GanntChart'''

        gan = GanntChart()
        gan.init(2, num_T, 30)

        schedule_list=[]
        flag=0
        for i in range(num_machines):
            temp=[]
            for t in range(num_T):
                flag = 0
                for j in range(num_jobs):

                    if Y[i,j,t].x==1:
                        temp.append(j)
                        flag=1
                        break
                if flag==0:
                    temp.append(-1)
            schedule_list.append(temp)
        print(schedule_list)
        current_job=-1
        s_j = 0
        p_j_count = 0

        for i in range(num_machines):
            current_job = -1
            s_j = -1
            p_j_count = 0
            for t in range(num_T-1):
                # prit；("t=",t)；
                if schedule_list[i][t]==-1:
                    continue

                if current_job==-1 :
                    # print("Case 1 J= ",schedule_list[i][t])
                    if schedule_list[i][t]==schedule_list[i][t+1]:
                        # print("Case 1.1 J= ", schedule_list[i][t])
                        if s_j==-1:
                            s_j=t
                            p_j_count+=1
                            current_job=schedule_list[i][t]
                            continue
                        else:
                            p_j_count += 1
                            continue
                    else:
                        # print("Case 1.2 J= ", schedule_list[i][t])
                        p_j_count += 1
                        gan.AddJob("J" + str(schedule_list[i][t]), i + 1, t, p_j_count )
                        p_j_count = 0
                        s_j = -1
                        current_job = -1

                else:
                    # print("Case 2 J= ", schedule_list[i][t])
                    if schedule_list[i][t] == schedule_list[i][t + 1]:
                        # print("Case 2.1 J= ", schedule_list[i][t])
                        p_j_count += 1
                        continue
                    else:
                        # print("Case 2.2 J= ", schedule_list[i][t])
                        p_j_count += 1
                        gan.AddJob("J" + str(schedule_list[i][t]), i + 1, s_j, p_j_count)
                        p_j_count = 0
                        s_j = -1
                        current_job = -1
        gan.SavetoFile("Gannt Chart/" + file_path+"_new_gan")


    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')


def read_file(file_path):
    file=open(file_path,"r")
    '''read num_rj num_jobs'''
    r=file.readline().split(",")
    num_rj=int(r[0])
    num_jobs=int(r[1])

    '''read rj_list'''
    r = file.readline().split(",")
    rj_list=[]
    for i,j in enumerate(r):
        rj_list.append(int(j))

    '''read all Jobs'''
    Job_list=[]
    for j in (file):
        r = j.split(",")
        init_job=JOB()
        init_job.index=int(r[0])
        init_job.release_date = int(r[1])
        init_job.processing_time = int(r[2])
        Job_list.append(init_job)

    return num_rj,num_jobs,rj_list,Job_list

if __name__=="__main__":
    main()