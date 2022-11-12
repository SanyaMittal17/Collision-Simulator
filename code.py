class almostcompletebinarytree:
    class Node:
        def __init__(self,E):
            self.element=E
            self.parent=None
            self.lchild=None
            self.rchild=None
    def __init__(self):
        self.data,self.list,self.numberofelts,self.root=[],[],0,None
    def addelement(self,E):
        if self.numberofelts==0:
            self.root=self.Node(E)
            self.data.append(self.root)
            self.list.append(self.root)
        else:
            newelt=self.Node(E)
            if self.numberofelts%2==1:
                self.data[int((self.numberofelts-1)/2)].lchild=newelt
                newelt.parent=self.data[int((self.numberofelts-1)/2)]
            else:
                self.data[int(self.numberofelts/2)-1].rchild=newelt
                newelt.parent=self.data[int(self.numberofelts/2)-1]
            self.data.append(newelt)
            if newelt.element[1]<len(self.list):
                self.list[newelt.element[1]]=newelt
            else:
                self.list.append(newelt)
        self.numberofelts+=1
    def removeelement(self):
        if self.numberofelts==1:
            y=self.root
            self.root=None
            self.data,self.list=[],[]
            self.numberofelts-=1
            return y
        if self.numberofelts>1:
            if self.numberofelts%2==1: 
                self.data[(self.numberofelts-2)//2].rchild=None
            else:
                self.data[(self.numberofelts-1)//2].lchild=None
            x=self.data[-1]
            x.parent=None
            self.data.pop()
            self.numberofelts-=1
            return(x)
def enqueue(a,x):   #O(log(n))
    a.addelement(x)
    if a.numberofelts>1:
        current_node=a.data[-1]
        while (current_node!=a.root and x<((current_node).parent).element):
            pos_of_current_node=(current_node.element)[1]
            swapping_node=current_node.parent.element[1]
            k=((current_node).parent).element
            ((current_node).parent).element=x
            (current_node).element=k
            (a.list[pos_of_current_node],a.list[swapping_node])=(a.list[swapping_node],a.list[pos_of_current_node])
            current_node=current_node.parent
    return a
def heapdown(a,u): #O(log(n))
    current_node=u
    x=current_node.element
    if ((current_node.rchild)!=None and (current_node.lchild)!=None):
        while ((current_node.rchild)!=None and (current_node.lchild)!=None and (current_node.lchild.element<x or current_node.rchild.element<x)):
            y=min(current_node.lchild.element,current_node.rchild.element)
            pos_of_current_node=current_node.element[1]
            current_node.element=y
            swapping_node=y[1]
            if current_node.lchild.element<=current_node.rchild.element:
                current_node.lchild.element=x
                current_node=current_node.lchild
            else:
                current_node.rchild.element=x
                current_node=current_node.rchild
            (a.list[pos_of_current_node],a.list[swapping_node])=(a.list[swapping_node],a.list[pos_of_current_node])
    if ((current_node.rchild)==None and (current_node.lchild)!=None):
        y=(current_node.lchild.element)
        x=current_node.element
        pos_of_current_node=x[1]
        if y<x:
            swapping_node=current_node.lchild.element[1]
            current_node.lchild.element=x
            current_node.element=y
            (a.list[pos_of_current_node],a.list[swapping_node])=(a.list[swapping_node],a.list[pos_of_current_node])
def ExtractMin(a):   #O(log(n))
    if a.root!=None:
        w=a.root.element
        a.list[w[1]].element=None
        x=a.data[-1].element
        a.removeelement()
        if len(a.data)!=0:
            a.root.element=x
            a.list[x[1]]=a.root
            heapdown(a,a.root)
        return w
def ExtractNode(a,i):  #O(log(n))
    if a.root!=None:
        w=a.list[i].element
        x=a.data[-1].element
        a.removeelement()
        if len(a.data)!=0:
            a.list[i].element=x
            a.list[x[1]]=a.list[i]
            heapdown(a,a.list[i])
        return w
def buildheap(l):  #O(n)
    a=almostcompletebinarytree()
    for w in range(len(l)):
        a.addelement(l[w])
    for w in range(len(l)-1,-1,-1):
        heapdown(a,a.data[w])
    return(a)
def collision(M,x,v):  #O(1)
    [m1,m2]=M
    [x1,x2]=x
    [v1,v2]=v
    if v2-v1<0:
        v11=(((m1-m2)/(m1+m2))*v1)+(((2*m2)/(m1+m2))*v2)
        v22=-(((m1-m2)/(m1+m2))*v2)+(((2*m1)/(m1+m2))*v1)
        x=[(x2*v1-x1*v2)/(v1-v2)]*2
        v=[v11,v22]
        if v2!=0:
            t=(x[0]-x2)/v2
        else:
            t=(x[0]-x1)/v1
    else:
        t=float('inf')
    return (M,x,v,t)
def storelistofcollisioninpairs(M,x,v):   #O(1)
    l2=[]
    for i in range(len(M)-1):
        M1=[M[i],M[i+1]]
        x1=[x[i],x[i+1]]
        v1=[v[i],v[i+1]]
        (m2,x2,v2,t)=(collision(M1,x1,v1))
        (l2).append((t,i,x2[0]))
    return l2
def listCollisions(M,x,v,m,t):  #O(n+m*log(n))
    l=storelistofcollisioninpairs(M,x,v)
    a=buildheap(l)  #O(n)
    l2=[]
    l3=[]
    timeoflatestcollision=[0]*len(M)
    while (m>=0 and t>=0):   #m*(O(log(n)))
        if a.root!=None:
            w=(a).root.element 
            i=w[1]
            w=ExtractMin(a)  #O(log(n))
            if w[0]!=float('inf'):
                m-=1
                r=w
                if (l2!=[] and w[0]-l3[-1][0]!=0):
                    t-=w[0]-l3[-1][0]
                elif (l2==[]):
                    t-=w[0]
                if (t>=0 and m>=0):
                    p=(round(r[0],4),r[1],round(r[2],4))
                    l3.append(r)
                    l2.append(p)
                temp=collision([M[i],M[i+1]],[x[i]+(v[i]*(w[0]-timeoflatestcollision[i])),x[i+1]+(v[i+1]*(w[0]-timeoflatestcollision[i+1]))],[v[i],v[i+1]])[2] 
                var=collision([M[i],M[i+1]],[x[i]+(v[i]*(w[0]-timeoflatestcollision[i])),x[i+1]+(v[i+1]*(w[0]-timeoflatestcollision[i+1]))],[v[i],v[i+1]])[1][0]
                x[i+1]=collision([M[i],M[i+1]],[x[i]+(v[i]*(w[0]-timeoflatestcollision[i])),x[i+1]+(v[i+1]*(w[0]-timeoflatestcollision[i+1]))],[v[i],v[i+1]])[1][1]
                x[i]=var
                v[i],v[i+1]=temp[0],temp[1]
                timeoflatestcollision[i],timeoflatestcollision[i+1]=w[0],w[0]
                new_time2=collision([M[i],M[i+1]],[x[i],x[i+1]],[v[i],v[i+1]])[3]
                new_x2=(collision([M[i],M[i+1]],[x[i],x[i+1]],[v[i],v[i+1]])[1])[0]
                enqueue(a,(new_time2+w[0],i,new_x2))  #O(log(n))
                if i!=0:
                    w1=a.list[i-1].element
                    if w1[1]==(i-1):
                        newt=collision([M[i-1],M[i]],[x[i-1]+(v[i-1])*(w[0]-timeoflatestcollision[i-1]),x[i]],[v[i-1],v[i]])[3] 
                        newx=collision([M[i-1],M[i]],[x[i-1]+(v[i-1])*(w[0]-timeoflatestcollision[i-1]),x[i]],[v[i-1],v[i]])[1][1]
                        p=(newt+w[0],i-1,newx)
                        ExtractNode(a,i-1)  #O(log(n))
                        enqueue(a,p)   #O(log(n))
                if i<len(l)-1:
                    w1=a.list[i+1].element
                    if w1[1]==(i+1):
                        newt=collision([M[i+1],M[i+2]],[x[i+1],x[i+2]+(v[i+2]*(w[0]-timeoflatestcollision[i+2]))],[v[i+1],v[i+2]])[3] 
                        newx=collision([M[i+1],M[i+2]],[x[i+1],x[i+2]+(v[i+2]*(w[0]-timeoflatestcollision[i+2]))],[v[i+1],v[i+2]])[1][1]
                        p=(newt+w[0],i+1,newx)
                        ExtractNode(a,i+1)  #O(log(n))
                        enqueue(a,p)   #O(log(n))
            else:
                break
        else:
            break
    return l2
