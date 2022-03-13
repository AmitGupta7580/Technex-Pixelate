arena= [[0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 3, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 2, 0, 3, 0, 1, 0, 1, 0, 1, 0, 2, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 3, 0, 3, 0, 0, 0, 1, 0, 2, 0, 1, 0, 2, 0, 0, 0, 4, 0, 4, 0, 0, 0],
        [0, 0, 4, 0, 4, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 4, 0, 4, 0, 0],
        [0, 4, 0, 4, 0, 0, 0, 1, 0, 0, 0, 3, 0, 3, 0, 0, 0, 2, 0, 0, 0, 3, 0, 3, 0],
        [3, 0, 3, 0, 0, 0, 2, 0, 0, 0, 2, 0, 7, 0, 4, 0, 0, 0, 1, 0, 0, 0, 4, 0, 3],
        [0, 3, 0, 1, 0, 0, 0, 1, 0, 2, 0, 1, 0, 1, 0, 4, 0, 2, 0, 0, 0, 4, 0, 4, 0],
        [0, 0, 1, 0, 1, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0, 1, 0, 2, 0, 0, 0, 1, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 2, 0, 3, 0, 1, 0, 4, 0, 3, 0, 2, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 1, 0, 4, 0, 3, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0]]
n=len(arena)
m=len(arena[0])


def findCost(start,end,w1=1,w2=1):
    global arena
    global n
    global m

    arena[start[0]][start[1]]=w1;
    arena[end[0]][end[1]]=w2;

    par=[[[-1,-1] for x in range(m)] for x in range(n)]
    took=[[0 for x in range(m)] for x in range(n)]
    took[start[0]][start[1]]=1;
    ready=[[start[0],start[1],0]]
    cost=0
    # print(arena[0][9]);
    while(took[end[0]][end[1]]==0):
        mini=10**10
        miniIdx=[0,0,0]
        miniPar=[-1,-1]
        # print(arena[0][9])
        for i in ready:
            if(i[1]-2>=0 and arena[i[0]][i[1]-2] and took[i[0]][i[1]-2]==0 and i[2]+arena[i[0]][i[1]-2]<mini):
                mini=i[2]+arena[i[0]][i[1]-2]
                miniIdx=[i[0],i[1]-2,mini]
                miniPar=[i[0],i[1]]

            if(i[1]+2<m and arena[i[0]][i[1]+2] and took[i[0]][i[1]+2]==0 and i[2]+arena[i[0]][i[1]+2]<mini):
                mini=i[2]+arena[i[0]][i[1]+2]
                miniIdx=[i[0],i[1]+2,mini]
                miniPar=[i[0],i[1]]

            if(i[1]+1<m and i[0]+1<n and arena[i[0]+1][i[1]+1] and took[i[0]+1][i[1]+1]==0 and i[2]+arena[i[0]+1][i[1]+1]<mini):
                mini=i[2]+arena[i[0]+1][i[1]+1]
                miniIdx=[i[0]+1,i[1]+1,mini]
                miniPar=[i[0],i[1]]

            if(i[1]+1<m and i[0]-1>=0 and arena[i[0]-1][i[1]+1] and took[i[0]-1][i[1]+1]==0 and i[2]+arena[i[0]-1][i[1]+1]<mini):
                mini=i[2]+arena[i[0]-1][i[1]+1]
                miniIdx=[i[0]-1,i[1]+1,mini]
                miniPar=[i[0],i[1]]

            if(i[1]-1>=0 and i[0]+1<n and arena[i[0]+1][i[1]-1] and took[i[0]+1][i[1]-1] ==0 and i[2]+arena[i[0]+1][i[1]-1]<mini):
                mini=i[2]+arena[i[0]+1][i[1]-1]
                miniIdx=[i[0]+1,i[1]-1,mini]
                miniPar=[i[0],i[1]]
            
            if(i[1]-1>=0 and i[0]-1>=0 and arena[i[0]-1][i[1]-1] and took[i[0]-1][i[1]-1]==0 and i[2]+arena[i[0]-1][i[1]-1]<mini):
                mini=i[2]+arena[i[0]-1][i[1]-1]
                miniIdx=[i[0]-1,i[1]-1,mini]
                miniPar=[i[0],i[1]]
        if(miniPar!=[-1,-1]):
            ready.append(miniIdx)
            took[miniIdx[0]][miniIdx[1]]=1
            par[miniIdx[0]][miniIdx[1]]=miniPar
            if(miniIdx[0]==end[0] and miniIdx[1]==end[1]):
                cost=mini     
    path=[]
    curr=[end[0],end[1]]
    while(curr[0]!=start[0] or curr[1]!=start[1]):
        p=par[curr[0]][curr[1]]
        if(p[0]==curr[0] and p[1]==curr[1]+2):
            path.append(4)#left

        if(p[0]==curr[0] and p[1]==curr[1]-2):
            path.append(1)#right

        if(p[0]==curr[0]+1 and p[1]==curr[1]+1):
            path.append(5)#left top

        if(p[0]==curr[0]+1 and p[1]==curr[1]-1):
            path.append(0)#right top
        
        if(p[0]==curr[0]-1 and p[1]==curr[1]+1):
            path.append(3)#left bottom
        
        if(p[0]==curr[0]-1 and p[1]==curr[1]-1):
            path.append(2)#right bottom
        
        curr=p

    path.reverse()
    return cost,path;

def getBest(start,spiderman,enemy,antitode):
    per1=[[0,1],[1,0]]
    per2=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]
    mini=10**10
    miniPath=[]

    for p1 in per1:
        for p2 in per2:
            for i in spiderman:
                arena[i[0]][i[1]]=0
            for i in enemy:
                arena[i[0]][i[1]]=0
            for i in antitode:
                arena[i[0]][i[1]]=0
            cost=0
            path=[]

            c,t=findCost(start,spiderman[p1[0]]);                   #first spiderman
            cost+=c
            path.extend(t)

            c,t=findCost(spiderman[p1[0]],spiderman[p1[1]])         #second spiderman
            cost+=c
            path.extend(t)

            c,t=findCost(spiderman[p1[1]],antitode[p2[0]])         #first antidode
            cost+=c
            path.extend(t)

            c,t=findCost(antitode[p2[0]],antitode[p2[1]])         #second antidode
            cost+=c
            path.extend(t)

            c,t=findCost(antitode[p2[1]],antitode[p2[2]])         #third antidode
            cost+=c
            path.extend(t)

            c,t=findCost(antitode[p2[2]],enemy[p2[0]],1,p2[0]+2)         #first villan
            cost+=c
            path.extend(t)

            c,t=findCost(enemy[p2[0]],enemy[p2[1]],p2[0]+2,p2[1]+2)         #second villan
            cost+=c
            path.extend(t)

            c,t=findCost(enemy[p2[1]],enemy[p2[2]],p2[1]+2,p2[2]+2)         #third villan
            cost+=c
            path.extend(t)

            if(cost<mini):
                mini=cost;
                miniPath=path;


    return miniPath;

# print(findCost([6,12],[9,21]))

if __name__ == '__main__':
    start=[6,12]
    spiderman=[[9,21],[9,3]]
    enemy=[[8, 6],[8,18],[2,12]]
    antitode=[[0,6],[4,12],[0,18]]
    print(getBest(start,spiderman,enemy,antitode))
