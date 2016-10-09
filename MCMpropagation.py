# -*- coding: utf-8 -*-
"""
Initiated on Sun Aug 30 12:00:22 2015
Added multiprocessing 24.04.2016
@author: pawelec
"""
#!/usr/bin/python
# propagacja.py

from numpy import random
from random import WichmannHill
from multiprocessing import Pool
import multiCPU #module used in order to recognize number of available CPU cores 
from time import clock
from re import search, match
from math import expm1,exp,log1p,log10,log,sqrt,acosh,asinh,atanh,cosh,sinh,tanh,atan2,acos,asin,atan,cos,sin,tan,pi,e
from sys import stdout

def printAssigned(name,type_f):
    print "Assigned new variable: %s, pdf type: %s" % (name, dict.values()[int(type_f)-1]['name'])
    
def trimExp(expression=''):
    """the methode eliminates all unexpected characters from the beggining of the expression
"""    
    str(expression).strip()
    while match('[^a-zA-Z0-9]',expression):
        t=match('[^a-zA-Z0-9]',expression)

        if t:
            if t.group()<>'(' and t.group()<>'-': 
                expression = expression[1:]
            elif (t.group()=='(' and match('[^a-zA-Z0-9(-]',expression[1])) or (t.group()=='-' and match('[^a-zA-Z0-9(]',expression[1])):
                expression=expression[1:]
            else:
                break
    
    #eliminate all unexpected characters from the end of the expression
    while match('[^a-zA-Z0-9]',expression[len(expression)-1]): 
        t=match('[^a-zA-Z0-9]',expression[len(expression)-1])
        if t:
            if t.group()<>')' : 
                expression=expression[:-1]

            else:
                break
    return expression

def expSort(name_var=[]):
	"""The method is sorting the list of variables with the best order from perspective of farther processing.
"""
	name_var.sort(cmp=lambda x,y: cmp(len(x), len(y)))
	name_var.reverse()
	return name_var

def expVer(express='', var_n=[] ):
    """The method is verifying if the expression contains only variables defined.
"""
    express = trimExp(express)
    express_n = express[:]
    len_zm = 0
    exp_cpy = 0    
    exp_cpy=len(express)
    
    #the list of the math functions to use in a model expression 
    mathf=('expm1(','exp(','log1p(','log10(','log(','sqrt(','acosh(','asinh(','atanh(','cosh(','sinh(','tanh(','atan2(','acos(','asin(','atan(','cos(','sin(','tan(','pi(','e(')
    maths=('+','-','/','*',')','(')    
        
    #parentheses parity verification
    prl = 0
    prr = 0
    pzz = 1
    wrong = False

    for pr in express_n:
        t = match('[^a-zA-Z0-9()*]',pr) 
        if pzz < len(express):
            t1 = match('[^a-zA-Z0-9()*]',express_n[pzz])
        else: t1 = None
        if pr=='(':
            prl+=1
            if pzz<len(express_n) and express_n[pzz]==')':
                wrong = True

        if pr==')':
            prr+=1
            if pzz<len(express_n) and express_n[pzz]=='(':
                wrong = True

        if t and t1:
            wrong = True
        pzz+=1 

    for zm in mathf: #eliminate from the expression all the math functions 
        express_n=express_n.replace(zm,'')
       
    for zm in var_n: #eliminate from the expression all the variables defined
        express_n=express_n.replace(zm,'')
        len_zm+=len(zm)

    if (len(express_n)<len(var_n)-1) or (exp_cpy < len_zm+(len(var_n)-1)):
        wrong = True

    for zm in maths: #eliminate from the expression all the math operators 
        express_n=express_n.replace(zm,'')

    txr='' 
    while search('[^0-9.]',express_n):
        tx=search('[^0-9]',express_n) #searching all alfa characters
        express_n=express_n.replace(tx.group(),'') #eliminating all such characters
        txr+=tx.group()

    while search('[0-9]',express_n):
        tx=search('[0-9]',express_n) #searching all numerical characters
        express_n=express_n.replace(tx.group(),'') #eliminating all such characters

    if len(txr)>0:
        return txr
    elif  wrong:
        print 'Wrong expression! Please verify'
        return 1
    elif prl<>prr:
        print 'an odd number of parentheses has been used, please verify' 
        return 2
    else:
        print 'Expression OK!'
        return 0    
   
 
def assignVar(*args): 
    """the function assigns the PDF type and initiate an instance of an appropriate object
"""
    if args[2]=='1':
        varF = args[1]
        varF = Trapez()
        varF.assignName(args[1])
        varF.genTrials( 0,args[0], args[3],args[4],args[5],args[6])
        printAssigned(args[1], args[2])
        
    elif args[2]=='2':
        varF = args[1]
        varF = Rectang()
        varF.assignName(args[1])
        varF.genTrials( 0,args[0], args[3],args[4],args[5])
        printAssigned(args[1], args[2])
                
    elif args[2]=='3':
        varF = args[1]
        varF = TriangAsym()
        varF.assignName(args[1])
        varF.genTrials( 0,args[0], args[3],args[4],args[5],args[6])
        printAssigned(args[1], args[2])
            
    elif args[2]=='4':
        varF = args[1]
        varF = TrapezC()
        varF.assignName(args[1])
        varF.genTrials( 0,args[0], args[3],args[4],args[5],args[6])
        printAssigned(args[1], args[2])
            
    elif args[2]=='5':
        varF = args[1]
        varF = Gauss()
        varF.assignName(args[1])
        varF.genTrials( 0,args[0], args[3],args[4],args[5])
        printAssigned(args[1], args[2])
           
    elif args[2]=='6':
        varF = args[1]
        varF = Exponen()
        varF.assignName(args[1])
        varF.genTrials( 0,args[0], args[3],args[4])
        printAssigned(args[1], args[2])
     
    elif args[2]=='7':
        varF = args[1]
        varF = Student()
        varF.assignName(args[1])
        varF.genTrials( 0,args[0], args[3],args[4],args[5],args[6])
        printAssigned(args[1], args[2])
                
    elif args[2]=='8':
        varF = args[1]
        varF = Chi2()
        varF.assignName(args[1])
        varF.genTrials( 0,args[0], args[3],args[4])
        printAssigned(args[1], args[2])
        
    elif args[2]=='9':
        varF = args[1]
        varF = ArcSin()
        varF.assignName(args[1])
        varF.genTrials( 0,args[0], args[3],args[4],args[5])
        printAssigned(args[1], args[2])
        
    elif args[2]=='10':
        varF = args[1]
        varF = Triangul()
        varF.assignName(args[1])
        varF.genTrials( 0,args[0], args[3],args[4],args[5])
        printAssigned(args[1], args[2])
    else: 
        print 'Undefined PDF type'
                    
    return varF
    
#dictionary which contains of all suported types of PDF's   
dict={1:{"name": "Trapezoidal", "parm": 3}, 2:{"name": "Rectangular", "parm": 2}, 3:{"name": "Triangular_Asym", "parm": 3}, 4:{"name": "CTrap", "parm": 3}, 
      5:{"name": "Gaussian", "parm": 2}, 6:{"name": "Exponential", "parm": 1}, 7:{"name": "t_Student", "parm": 3}, 8:{"name": "Chi^2", "parm": 1},
      9:{"name": "U_Arcsin", "parm":2}, 10:{"name": "Triangular", "parm": 2}}    

#dictionary which contains description of all suported types of PDF's and list of parameters
descPDF={1:"You are defining Trapezoidal PDF, enter the following parameters: a, b, beta:",2:"You are defining Rectangular PDF, enter the following parameters: a, b:",
	  3:"You are defining Triangular symetric PDF, enter the following parameters: a, b, c.",4:"You are defining Curvilinear Trapezoid PDF, enter the following parameters: a, b, d:",
	  5:"You are defining Gaussian PDF, enter the following parameters: x-best estimate, u(x)-associated standard uncertainty:",6:"You are defining Exponential PDF, enter the following parameters: x-best estimate and non-negative qty:",
	  7:"You are defining Student's t PDF, enter the following parameters: df-effective degrees of freedom, x-best estimate & ux-expanded uncertainty:",
	  8:"You are defining Chi^2 PDF, enter the following parameters: f-effective degrees of freedom:",9:"You are defining Arc sine (U-shaped) PDF, enter the following parameters: lower and upper limits a, b:",
	  10:"You are defining Triangular PDF, enter the following parameters: a, b: "}

def step(N):
    """the function used to generate single random value
"""
    step = WichmannHill()
    laststate = step.getstate()
    step.setstate(laststate)
    step.jumpahead(N)
    return step.randint(1, 100)

#the main class   
class Rozklad(object):
    next_rozklad=1
    def __init__(self,):  # self - new created instance
        # setup of the instance attributes 
        self.no_rozklad = self.next_rozklad # the class attibute - next number
        self.__class__.next_rozklad = self.next_rozklad + 1
        self.N = 1000 #iniciation of trials number
        self.list_res=[] #initiation of the list for trias values
        self.CPUs = multiCPU.available_cpu_count() #number of available CPU 
        self.name_v=''
        
    def assignName(self, name):
        self.name_v = name #variable name
        
    def multiproc(self, anotherfunc, *args):
        """the function is giving possibility to generate random numbers using many CPU cores simultaneously
    """
        self.list_res=[]
        self.pool = Pool(processes=self.CPUs)
        m=args[0]
        n = args[1]/self.CPUs+1
        print 'N=', n
        if len(args)==6:            
        # Setup a list of processes that we want to run
            self.results = [self.pool.apply_async(anotherfunc,args=(m+n*x,n+n*x,args[2],args[3],args[4],args[5], )) for x in range(self.CPUs)]
        elif len(args)==7: 
            self.results = [self.pool.apply_async(anotherfunc,args=(m+n*x,n+n*x,args[2],args[3],args[4],args[5],args[6], )) for x in range(self.CPUs)]
        elif len(args)==5:
            self.results = [self.pool.apply_async(anotherfunc,args=(m+n*x,n+n*x,args[2],args[3],args[4], )) for x in range(self.CPUs)]
        
        else:
            self.results = [self.pool.apply_async(anotherfunc,args=(m+n*x,n+n*x,args[2],args[3], )) for x in range(self.CPUs)]
        self.output = [p.get() for p in self.results]

        self.pool.close()#necessary to prevent zombies
        self.pool.join() #wait for all processes to finish

        for i in self.output:
			self.list_res += i

        return self.list_res
        
def unwrap_self_Trapez(*args): #the function is necessary to unwrap 'self' parameter from the original metode of the class
    return Trapez().gen_random(*args)

        
class Trapez(Rozklad):
    """ The Trapez class represents Trapezoidal PDF, this is described by three parameters: a, b, beta.
"""
    def __init__(self, N=1000,a=1.0,b=3.0,beta=0.5):
        Rozklad.__init__(self,) # the main class constructor
   
    def gen_random(self, M,N, R_typ,a,b,c):
        """The method is generating random numbers which are representing Trapezoidal PDF
"""
        self.list_res = []
        self.a=a
        self.b=b
        self.beta=c

        self.NpRa1 = random.RandomState()
        self.NpRa1.seed(N*step(N))
        
        self.NpRa2 = random.RandomState()
        self.NpRa2.seed(N*2*step(N))

        if R_typ == 0:
            for i in range(M,N): 
                self.list_res.append(self.a+(self.b-self.a)/2* abs((1+self.beta)* self.NpRa2.random_sample() + (1-self.beta) * self.NpRa1.random_sample()))
          
            return self.list_res
        else:
            self.Ra1 = WichmannHill()
            self.Ra1.jumpahead(N)
            laststate = self.Ra1.getstate()
            self.Ra2 = WichmannHill()
            self.Ra2.setstate(laststate)
            self.Ra2.jumpahead(N)
            for i in range(M,N): 
                self.list_res.append(self.a+(self.b-self.a)/2* abs((1+self.beta)* self.Ra1.random() + (1-self.beta) * self.Ra2.random()))
                 
            return self.list_res
            
    def genTrials(self, *args):
        return self.multiproc(unwrap_self_Trapez, *args)
        
        
def unwrap_self_TriangAsym(*args): #the function is necessary to unwrap 'self' parameter from the original metode of the class
    return TriangAsym().gen_random(*args)        
        
class TriangAsym(Rozklad):
    """The TriangAsym class represents Asymmetric Triangular PDF, described by three parameters: a, b, c.
"""
    def __init__(self,N=1000,a=0.0,b=1.0, c=0.5):
        Rozklad.__init__(self,)
        
    def gen_random(self, M,N, R_typ,a,b,c):
        """The method is generating random numbers which are representing Asymmetric Triangular PDF
"""
        self.list_res = []
        self.a = a
        self.b = b
        self.c = c

        self.NpRa1 = random.RandomState()
        self.NpRa1.seed(N*step(N))

        if R_typ == 0:        
            for i in range(M,N):

                U = self.NpRa1.random_sample()
                if  U > 0 and U < (self.c-self.a)/(self.b-self.a):
                    self.list_res.append(self.a+sqrt((self.b-self.a) * (self.c - self.a) * U))
                elif U < 1 and U >=(self.c-self.a)/(self.b-self.a):
                    self.list_res.append(self.b - sqrt((self.b-self.a) * (self.b - self.c) * (1-U)))
            return self.list_res
            
    def genTrials(self, *args):
        return self.multiproc(unwrap_self_TriangAsym,*args)
        
def unwrap_self_Rectang(*args): #the function is necessary to unwrap 'self' parameter from the original metode of the class
    return Rectang().gen_random(*args)
        
class Rectang(Rozklad):
    """The Rectang class represents Rectangular PDF, described by two parameters: a, b.
"""
    def __init__(self,N=1000, a=0.0, b=1.0):
        Rozklad.__init__(self,)
        
    def gen_random(self, M,N, R_typ,a,b):
        """The method is generating random numbers which are representing Rectangular PDF
"""
        self.list_res = []
        self.a = a
        self.b = b

        self.NpRa1 = random.RandomState()
        self.NpRa1.seed(N*step(N))
        
        if R_typ == 0:        
            for i in range(M,N):
                self.list_res.append(self.a+(self.b-self.a) * self.NpRa1.random_sample())
   
            return self.list_res
        else:
            Ra = WichmannHill()
            Ra.jumpahead(self.N)
            for i in range(M,N):
                self.list_res.append(self.a+(self.b-self.a) * Ra.random())
   
            return self.list_res
            
    def genTrials(self, *args):
        return self.multiproc(unwrap_self_Rectang, *args)
        
def unwrap_self_TrapezC(*args): #the function is necessary to unwrap 'self' parameter from the original metode of the class

    return TrapezC().gen_random(*args)
        
class TrapezC(Rozklad):
    """The TrapezC class represents Curvilinear Trapezoid PDF, described by three parameters: a, b, c.
"""
    def __init__(self,N=1000,a=0.0,b=1.0,d=0.2):
        Rozklad.__init__(self,) 
        
    def gen_random(self, M,N, R_typ,a,b,d):
        """The method is generating random numbers which are representing Trapezoidal PDF
"""
        self.list_res=[]
        self.a = a
        self.b = b 
        self.d = d

        self.NpRa1 = random.RandomState()
        self.NpRa1.seed(N*step(N))
        
        self.NpRa2 = random.RandomState()
        self.NpRa2.seed(N*2*step(N))
        
        if R_typ == 0: 
            for i in range(M,N): 
                a_s=(self.a-self.d)+2*self.d * self.NpRa1.random_sample()            
                b_s=(self.a+self.b)-a_s
                self.list_res.append(a_s+(b_s-a_s) * self.NpRa2.random_sample())
            return self.list_res  
        else:
            Ra1 = WichmannHill()
            Ra1.jumpahead(N)
            laststate = Ra1.getstate()
            Ra2 = WichmannHill()
            Ra2.setstate(laststate)
            Ra2.jumpahead(N)
            for i in range(M,N): 
                a_s=(self.a-self.d)+2*self.d * Ra1.random()            
                b_s=(self.a+self.b)-a_s
                self.list_res.append(a_s+(b_s-a_s) * Ra2.random())
            return self.list_res 
            
    def genTrials(self, *args):
        return self.multiproc(unwrap_self_TrapezC,*args)
        
def unwrap_self_Gauss(*args): #the function is necessary to unwrap 'self' parameter from the original metode of the class
    return Gauss().gen_random(*args)        

class Gauss(Rozklad):
    """The Gauss class represents Gaussian PDF, described by two parameters: x, ux.
"""
    def __init__(self, N=1000, x=0.0, ux=1.0):
        Rozklad.__init__(self, )
        
    def gen_random(self, M,N, R_typ,x,ux):
        """The method is generating random numbers which are representing Gaussian PDF
"""
        self.x = x
        self.ux = ux
        self.list_res=[]

        self.NpRa1 = random.RandomState()
        self.NpRa1.seed(step(N)*N*2)
        self.NpRa2 = random.RandomState()
        self.NpRa2.seed(step(N)*N)

        if R_typ == 0: 

            for i in range(M,N):
                teta=2*pi*self.NpRa1.random_sample() 
                promien=sqrt(-2*log(self.NpRa2.random_sample()))
                self.list_res.append(self.x+self.ux*promien*cos(teta))
                self.list_res.append(self.x+self.ux*promien*sin(teta))
            return self.list_res
        else:
            Ra = WichmannHill()
            Ra.jumpahead(2000000)
            for i in range(M,N): 
                self.list_res.append(Ra.gauss(self.x, self.ux))
            return self.list_res
            
    def genTrials(self, *args):
        return self.multiproc(unwrap_self_Gauss,*args)
        
        
def unwrap_self_Exponen(*args): #the function is necessary to unwrap 'self' parameter from the original metode of the class
    return Exponen().gen_random(*args)         
        
class Exponen(Rozklad):
    """The Exponen class represents Exponential PDF, described by one parameter: x.
"""
    def __init__(self, N=1000, x=0.0):
        Rozklad.__init__(self, )

    def gen_random(self, M,N, R_typ,x):
        """The method is generating random numbers which are representing Exponential PDF
"""
        self.list_res=[]
        self.x = x

        self.NpRa1 = random.RandomState()
        self.NpRa1.seed(N*step(N))

        if R_typ == 0:

            for i in range(M,N):
                self.list_res.append(-1/self.x*log(1-self.NpRa1.random_sample()))
            return self.list_res
        else:
            Ra = WichmannHill()
            Ra.jumpahead(N)
            for i in range(M,N): 
                self.list_res.append(Ra.expovariate(self.x))
            return self.list_res

    def genTrials(self, *args):
        return self.multiproc(unwrap_self_Exponen, *args)
        
def unwrap_self_Student(*args): #the function is necessary to unwrap 'self' parameter from the original metode of the class
    return Student().gen_random(*args)   
    
class Student(Rozklad):
    """The Student class represents Student's t PDF, described by three parameters: x, ux and 
    df - number of freedom degrees.
"""
    def __init__(self, N=1000, x=0, ux=1, df=5):
        Rozklad.__init__(self, )

    def gen_random(self, M,N, R_typ, df,x,ux):
        """The method is generating random numbers which are representing Student's t PDF
"""
        self.list_res=[]
        self.df = df
        self.x = x
        self.ux = ux

        self.NpRa1 = random.RandomState()
        self.NpRa1.seed(N*step(N))
                        
        if self.df>3:  
            if R_typ == 0:
                for i in range(M,N):        
                    self.list_res.append(self.x+self.ux*self.NpRa1.standard_t(self.df))
                return self.list_res
            else:
                Ra = WichmannHill()
                Ra.jumpahead(N)
                for n in range(M,N):
                    self.sx = 0
                    self.sx2 = 0
                    self.l_sx = [] 
                    for i in range(self.df+1):
                        self.l_sx.append(Ra.gauss(0,1))
                        self.sx += self.l_sx[-1]
                    self.sx=1.0/(self.df+1)*self.sx
                
                    for item in self.l_sx:
                        self.sx2 += (item-self.sx)**2
                    self.sx2 = 1.0/self.df*self.sx2
                    self.list_res.append(self.x+self.ux*(self.df+1)**0.5*self.sx/(self.sx2**0.5))
                return self.list_res
        else:
            print "error in processing, to small value of the df parameter degrees of freedom has been given"    
            
    def genTrials(self, *args):
        return self.multiproc(unwrap_self_Student, *args)
        
def unwrap_self_Chi2(*args): #the function is necessary to unwrap 'self' parameter from the original metode of the class
    return Chi2().gen_random(*args) 
        
class Chi2(Rozklad):
    """The Chi2 class represents Chi^2 PDF, described by one parameter:df - number of freedom degrees.
"""
    def __init__(self, N=1000, df=5):
        Rozklad.__init__(self, )
        
    def gen_random(self, M,N, R_typ,df):
        """The method is generating random numbers which are representing Chi^2 PDF
"""
        self.list_res=[]
        self.NpRa1 = random.RandomState()
        self.NpRa1.seed(N*step(N))

        for n in range(M,N):
            self.list_res.append(self.NpRa1.chisquare(df))
        return self.list_res
        
    def genTrials(self, *args):
        return self.multiproc(unwrap_self_Chi2, *args)
        
def unwrap_self_ArcSin(*args): #the function is necessary to unwrap 'self' parameter from the original metode of the class
    return ArcSin().gen_random(*args) 
        
class ArcSin(Rozklad):
    """The ArcSin class represents U-shaped PDF, described by two parameters: a, b.
"""    
    def __init__(self, N=1000, a=0.0, b=1.0):
        Rozklad.__init__(self, )
        
    def gen_random(self, M,N, R_typ, a,b):
        """The method is generating random numbers which are representing Arc sine (U-shaped) PDF
"""
        self.a = a
        self.b = b
        self.list_res=[]

        self.NpRa1 = random.RandomState()
        self.NpRa1.seed(N*step(N))

        if R_typ == 0:        
            for i in range(M,N):
                self.list_res.append((self.a+self.b)/2+(self.b-self.a)/2*sin(2*pi*self.NpRa1.random_sample()))
            return self.list_res
        else:
            Ra = WichmannHill()
            Ra.jumpahead(N)
            for i in range(M,N):
                self.list_res.append((self.a+self.b)/2+(self.b-self.a)/2*sin(2*pi*Ra.random()))
            
            return self.list_res    
            
    def genTrials(self, *args):
        return self.multiproc(unwrap_self_ArcSin, *args)
        
def unwrap_self_Triangul(*args): #the function is necessary to unwrap 'self' parameter from the original metode of the class
    return Triangul().gen_random(*args)      
        
class Triangul(Rozklad):
    """The Traiangul class represents Triangular PDF, described by two parameters: a & b.
"""
    def __init__(self,N=1000,a=0.0,b=1.0):
        Rozklad.__init__(self,)
                
    def gen_random(self, M,N, R_typ, a, b):
        """The method is generating random numbers which are representing Triangular PDF
"""
        self.a = a
        self.b = b
        self.los = 0
        self.list_res=[]

        self.NpRa1 = random.RandomState()
        self.NpRa1.seed(N*step(N))
        self.NpRa2 = random.RandomState()
        self.NpRa2.seed(N*2*self.step.randint(1, 100))
        i = M
        if R_typ == 0:
            while i < N-M:
                self.los = self.NpRa1.random_sample() + self.NpRa2.random_sample()
                if self.los != 0.0:
                    self.list_res.append(self.a+(self.b-self.a)/2* self.los )
                    i += 1
                else:
                    pass
            return self.list_res
        else:
            Ra1 = WichmannHill()
            laststate = Ra1.getstate()
            Ra2 = WichmannHill()
            Ra2.setstate(laststate)
            Ra2.jumpahead(N) 
            
            while i < N-M: 
                self.los = Ra1.random() + Ra2.random()
                if self.los != 0.0:
                    self.list_res.append(self.a+(self.b-self.a)/2* self.los)
                    i += 1
                else:
                    pass
            return self.list_res
            
    def genTrials(self, *args):
        return self.multiproc(unwrap_self_Triangul, *args)
        
    
class Ypdf(Rozklad):
    """ The Ypdf(int(M),int(P),model,var_name_list,var_pdf_object_list) class is representing probability density function calculated with Monte Carlo Method for given model.
    The class is initiated with such parameters like: M - number of trials used for the MC method, 
    P - covarage probability value defined as number in percenatage, model - mathematical expression which represents model of searched PDF,
    var_name_list - list of variable names used in the defined model,var_pdf_object_list-list of all objects, related to the variables. 
    Each initiated object represents a PDF which describes particular variable used in the model. All the PDF's supported you can find in the dict dictionary..
"""
    def __init__(self, N, P, expression='', list_nz=[], list_var_o=[], y=0.0, uy=0.0, prd=0.0, prw=0.0):
        self.N = int(N)   #number of trialas used for Monte Carlo Method     
        self.P = int(P)   #percentage value of coverage probability    
        self.y = y #the best estimate value 
        self.uy = uy #standard uncertainty value
        self.prd = prd #the left border of covarage interval
        self.prw = prw #the right border of covarage interval
        self.list_res=[] #list of results
        self.CPUs = multiCPU.available_cpu_count() #number of available CPU
        self.expression = expression #model expression
        self.list_nz = list_nz #list of the variable names
        self.list_var_o = list_var_o #list of variable objects
        self.progress = 0.0
        
       
  
    def calc_prd(self,Pr=0):
        """The method is calculating coverage interval values related to the PDF. 
        The argument of this method is percentage value of Coverage Probability for which 
        the coverage interval values are calculated.
"""
        if Pr>0:
		self.P = Pr
  
        if len(self.list_res)>0:
		z = int((self.N-(self.N*self.P/100))/2) #the range related to the covarage probability
		self.prd = self.list_res[z] 
		self.prw = self.list_res[self.N-z] 
        else:
            print "Missing data, not all have been calculated"
        
        
    def calculate(self, val_list=[]):
        """The method is calculating the best estimate and standard uncertainty values related to the PDF
        for which a list of representing, discreet values have been passed. 
        The argument of this method is a list of values representing a PDF. 
"""
        sum_v = 0.0 #sum of calcualed values
        sum_2 = 0.0 #sum of square deviation
        if len(val_list)>999:
            self.list_res = val_list
        
        for item in self.list_res:
            sum_v += item
        
        self.y=sum_v/self.N #the average value of calculated values
        
        for i in self.list_res:
            sum_2 +=(i-self.y)**2 
        
        self.list_res.sort()
        self.calc_prd()
        
        if sum_2!= 0.0:        
            self.uy = (1.0/(self.N-1.0)*sum_2)**0.5 #standard uncertainty value for provided list of trials 
            
        else:
            print "An error occurred during calculation"
            
    # the main method, dedicated for the model expression computation
    def procExpression(self ): 
        """the function processes a model given in text format based on the list of defined variables and list of objects 
        initiated as instances of the Rozklad() class. 
        """    
        c_time = clock()
        express_n=''
        self.list_nz = expSort(self.list_nz)
        self.expression = trimExp(self.expression)
        if len(self.list_var_o)==len(self.list_nz):
            for x in range(0,self.N):
                express_n = str(self.expression).strip()
                for it in self.list_nz:
                    for  ot in range(len(self.list_var_o)):
                        if self.list_var_o[ot].name_v==it:
                            list_val=self.list_var_o[ot].list_res
                            express_n = express_n.replace(it, str(list_val[x]))

                try:
                    exec( "f_result=%s"%(express_n) )
					                        
                except ValueError as er:
                    print "An error occurred during calculation: %s. Likely the Model expression has been wrongly defined, fix it and try again " % er
                  
                    break
                
                self.list_res.append(float(f_result))
                
                if x % (self.N/100) == 0:
                    stdout.write('.')
                    self.progress = x

            print ''
            print 'number of new trials=', len(self.list_res)
            print 'expression computing time:', clock() - c_time    
            return self.list_res
        else: 
            print "An error occurred during calculation. Likely the Model expression has been wrongly defined, fix it and try again "

        



          

		
