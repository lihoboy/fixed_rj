from random import randrange
def main(num_r_j,num_jobs):
    p_j=10
    path="data/data_"+str(num_r_j)+"_"+str(num_jobs)+"_v6"
    f=open(path,"w")
    r_1=int((num_jobs / 2) * int(p_j/2) / 2)
    f.writelines(str(num_r_j)+","+str(num_jobs)+"\n")
    f.writelines(str(0)+","+str(r_1)  +"\n" )
    for i in range(num_jobs):
        if i< num_jobs/2:
            r=0
        else:
            r=r_1
        f.writelines(str(i) + "," +str(r) + ","+ str(randrange(1,p_j))+ "\n")
    f.close()



if __name__=="__main__":
    num_r_j=2
    num_jobs=10
    main(num_r_j,num_jobs)