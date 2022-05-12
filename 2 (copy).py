import random as rd;import numpy as np;import sys as s;import pickle
import torch
import torch.nn as nn
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import torch.optim as optim
import matplotlib.pyplot as plt
import math
#-------------------------------------------------------------------------------
def DampedPend(b,k,t,m):
    if t==0:
        position=1
    else:
        dump=math.exp(-(b/2*m)*t)
        omega=np.sqrt(k/m)*np.sqrt(1-(b**2)/(4*m*k))
        osc=np.cos(omega*t)
        position = dump*osc
    return position
#-------------------------------------------------------------------------------
    #   GERANDO O BANCO DE DADOS SORTEANDO K E B NO SEU INTERVALO ESPECÍFICO
def Box_1_dataset_with_Constants(n_batch,batch_size,exemplos_por_batch):
    inp=[];    question=[];    m=1
    T=[i for i in range(0,50)]
    K=np.linspace(5, 11, num=50)
    B=np.linspace(0.5, 1.1, num=50)
    KK=[];    BB=[]
#    K=np.linspace(5, 11, num=100)          #those are default values
#    B=np.linspace(0.5,1.1, num=100)        #those are default values
#'''         THIS IS FOR A RANDOM CONFIG OF K AND B'''
    for i in range(n_batch):
        t=[];        position=[];        full=0
        while full!=batch_size:
            ki=rd.randint(0,49);        bi=rd.randint(0,49)
            k=K[ki];        b=B[bi]
            KK.append(k);           BB.append(b)
            y=[];            tpred=[]
            for l in T:
                yy=DampedPend(b,k,l,m)
                y.append(yy)
                tpred.append(l)
#            plt.clf()                   #uncoment to graph
#            plt.xlim([0, 50])           #uncoment to graph
#            plt.ylim([-1, 1])           #uncoment to graph
#            plt.plot(tpred,y)           #uncoment to graph
#            plt.pause(0.5)              #uncoment to graph

            t.append(tpred)
            position.append(y)
            full+=1
        inp.append(position)
        question.append(t)
    KK=np.array(KK).reshape(n_batch,batch_size,1)   # To works on scynet
    BB=np.array(BB).reshape(n_batch,batch_size,1)   # To works on scynet
    Constantes=[KK,BB]
    inp=torch.as_tensor(inp)
    question=torch.as_tensor(question)
    plt.show()
    print('shape(question) =',np.shape(question))
    print('Constantes =',np.shape(Constantes))
#    sys.exit()
    address = open("positions","wb")
    pickle.dump(inp, address)
    address.close()
    address = open("question","wb")
    pickle.dump(question, address)
    address.close()
    address = open("Constantes","wb")
    pickle.dump(Constantes, address)
    address.close()
#Box_1_dataset_with_Constants(5,1000,50)
#s.exit()
#-----------------------------------------------------------------------
#------------------LOAD DATA-----------------------------------------------------
#-----------------------------------------------------------------------
inp = pickle.load( open( "positions", "rb" ) )
question= pickle.load( open( "question", "rb" ) )
out =  pickle.load( open( "positions", "rb" ) )
Constantes =  pickle.load( open( "Constantes", "rb" ) )
K=Constantes[0];B=Constantes[1]
n_batch=np.shape(inp)[0]
batch_size=np.shape(inp)[1]
n_examples=np.shape(inp)[2]
#-----------------------------------------------------------------------
#plt.plot(question[0][0].detach().numpy(),out[0][0].detach().numpy())
#plt.show();s.exit()
#-------------------------------------------------------------------------------
#------------------DEFINE O MODELO----------------------------------------------
#-------------------------------------------------------------------------------
class Autoencoder(nn.Module):
    def __init__(self):
        # N, 50
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(50,400),
            nn.Tanh(),
            nn.Linear(400,300),
            nn.Tanh(),
            nn.Linear(300,200),
            nn.Tanh(),
            nn.Linear(200,3),
            nn.Tanh(),
        )
        self.project=nn.Linear(1,3)
        self.decoder=nn.Sequential(
            nn.Linear(6,100),
            nn.Tanh(),
            nn.Linear(100,200),
            nn.Tanh(),
            nn.Linear(200,450),
            nn.Tanh(),
            nn.Linear(450,50),
            nn.Tanh(),
            nn.Linear(50,1),
        )
    def forward(self, x, t):
        encoded = self.encoder(x)
        t=self.project(t)
        aux=torch.cat((encoded,t),1)
        decoded = self.decoder(aux)
        return decoded,encoded
#-------------------------------------------------------------------------------
#------------------INICIA CAMADAS DE PESOS ORTOGONAIS---------------------------
#-------------------------------------------------------------------------------
model = Autoencoder()
for m in model.modules():
    if isinstance(m, (nn.Conv2d, nn.Linear)):
        nn.init.orthogonal_(m.weight)
criterion = nn.MSELoss() #segundo a investigar
optimizer = torch.optim.Adam(model.parameters())#,lr=1e-4,weight_decay = 1e-5)
#optimizer = torch.optim.SGD(model.parameters(),lr=1e-4,weight_decay = 1e-5)#,momentum=0.5)
#-------------------------------------------------------------------------------
#---------------------TREINO----------------------------------------------------
#-------------------------------------------------------------------------------
def treine(epochs):
    inp = pickle.load( open( "positions", "rb" ) )
    question= pickle.load( open( "question", "rb" ) )
    out =  pickle.load( open( "positions", "rb" ) )
    n_batch=np.shape(inp)[0]
    batch_size=np.shape(inp)[1]
    n_examples=np.shape(inp)[2]
    T=question[0,0]
    t=torch.as_tensor(np.zeros((batch_size,1)))
    answ=torch.as_tensor(np.zeros((batch_size,1)))
    indicedografico=0
    for epoch in range(epochs):
        for batch_idx in range(n_batch):
            inputs = inp[batch_idx]
            inputs=inputs.float()
            t=t.float()
            out=out.float()
            r=rd.randint(0,49)
            for i in range(batch_size):
                r=rd.randint(0,49)
                t[i][0]=question[batch_idx,i,r]
                answ[i][0]=inp[batch_idx,i,r]
            recon,latent = model(inputs,t)
            loss=torch.mean((recon-answ)**2)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print(f'Epoch:{epoch+1},Loss:{loss.item():.4f}')
#treine(10000)
#-------------------------------------------------------------------------------
#---------------------SAVE AND LOAD STATE---------------------------------------
#-------------------------------------------------------------------------------
PATH='Estado_talvez_funcionante.pt'  # esse aqui foi treinado por 10k epochs,
                                      #3 Latent e 6 project of dataset(5,500,50)
#PATH='Estado_talvez_funcionante.pt'
model=Autoencoder()
#torch.save(state, filepath)
model.load_state_dict(torch.load(PATH))
#-------------------------------------------------------------------------------
#---------------------GRÁFICOS--------------------------------------------------
#-------------------------------------------------------------------------------
def Predict_test_Scynet():
    t=torch.as_tensor(np.zeros((batch_size,1)))
    t=t.float()
    Y=np.zeros(50);        T=[i for i in range(0,50)]
    for aux in range(0,n_batch):
        for rdn_batch in range(0,batch_size):
            YY=inp[aux][rdn_batch].detach().numpy()
            r=0
            for interval in range(0,49):
                for i in range(batch_size):
                    t[i][0]=question[0,i,r]
                y,latent=model(inp[aux].float(),t)
                y=y.detach().numpy()[rdn_batch]
                Y[interval]=y
                r+=1
            plt.clf()
            plt.xlim([0, 50])
            plt.ylim([-1, 1])
            plt.plot(T,Y,label='predict',ls='dashed')
            plt.plot(T,YY,label='equation')
            #plt.scatter(T, Y,c='black',label='recon')
            #plt.scatter(T, YY,c='red',label='answ')
            plt.legend()
            plt.pause(0.03)
            #plt.close()
    plt.show()
#Predict_test_Scynet()
#-------------------------------------------------------------------------------
def Latent_values_Scynet1():
    fig = make_subplots(rows=1, cols=3,
                        specs=[[{'is_3d': True}, {'is_3d': True}, {'is_3d': True}]],
                        subplot_titles=['Latent Activation 1', 'Latent Activation 2', 'Latent Activation 3'],
                        )
    t=torch.as_tensor(np.zeros((batch_size,1)))
    t=t.float()
    L1,L2,L3=np.zeros(batch_size),np.zeros(batch_size),np.zeros(batch_size)
    ks,bs=np.zeros(batch_size),np.zeros(batch_size)
    Y=np.zeros(50);        T=[i for i in range(0,50)]
    r=10 # tempo escolhido para a pergunta da rede neural
    for i in range(batch_size):
        t[i][0]=question[0,i,r]
    for aux in range(0,1):#n_batch):
        for rdn_batch in range(0,batch_size):
            y,latent=model(inp[aux].float(),t)
            L1[rdn_batch] = latent[rdn_batch][0].detach().numpy()
            L2[rdn_batch] = latent[rdn_batch][1].detach().numpy()
            L3[rdn_batch] = latent[rdn_batch][2].detach().numpy()
            ks[rdn_batch] = K[aux][rdn_batch]
            bs[rdn_batch] = B[aux][rdn_batch]
        fig.add_trace(go.Scatter3d(x=bs,y=ks,z=L1,mode='markers',marker=dict(
            size=12,color=L1,colorscale='Viridis',opacity=0.8)), 1, 1)
        fig.add_trace(go.Scatter3d(x=bs,y=ks,z=L2,mode='markers',marker=dict(
            size=12,color=L2,colorscale='Viridis',opacity=0.8)), 1, 2)
        fig.add_trace(go.Scatter3d(x=bs,y=ks,z=L3,mode='markers',marker=dict(
            size=12,color=L3,colorscale='Viridis',opacity=0.8)), 1, 3)
        fig.show()
#Latent_values_Scynet1()
#--------------------------------------------------------------------------
def Latent_values_Scynet2():
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax1 = fig.add_subplot(1, 3, 1, projection='3d')
    ax2 = fig.add_subplot(1, 3, 2, projection='3d')
    ax3 = fig.add_subplot(1, 3, 3, projection='3d')
    t=torch.as_tensor(np.zeros((batch_size,1)))
    t=t.float()
    L1,L2,L3=np.zeros(batch_size),np.zeros(batch_size),np.zeros(batch_size)
    Y=np.zeros(50);        T=[i for i in range(0,50)]
    r=25
    for i in range(batch_size):
        t[i][0]=question[0,i,r]
    #rdn_batch=rd.randint(0,batch_size)
    #aux=[i for i in range(0,n_batch)]
    for aux in range(0,n_batch):
        for rdn_batch in range(0,batch_size):
            #YY=inp[aux][rdn_batch].detach().numpy()
            y,latent=model(inp[aux].float(),t)
            #y=y.detach().numpy()[rdn_batch]
            #Y[interval]=y
            L1[rdn_batch] = latent[rdn_batch][0].detach().numpy()
            L2[rdn_batch] = latent[rdn_batch][1].detach().numpy()
            L3[rdn_batch] = latent[rdn_batch][2].detach().numpy()
            um   = latent[rdn_batch][0].detach().numpy()#.reshape(500)
            #um   = latent[rdn_batch][0].detach().numpy()#.reshape(500)
            dois = latent[rdn_batch][1].detach().numpy()#.reshape(500)
            #dois = latent[rdn_batch][1].detach().numpy()#.reshape(500)
            tres = latent[rdn_batch][2].detach().numpy()#.reshape(500)
            #tres = latent[rdn_batch][2].detach().numpy()#.reshape(500)
            um=np.array(um)
            dois=np.array(dois)
            tres=np.array(tres)
            k=np.array(K[aux][rdn_batch])
            b=np.array(B[aux][rdn_batch])
            #print(np.shape(B))
            #print(np.shape(K))
            #print(np.shape(L1))
            #print(um)
            #s.exit()
        surf=ax1.scatter3D(k, b, L1,label='Latent Activation 1' )
        surf=ax2.scatter3D(k, b, L2,label='Latent Activation 2' )
        surf=ax3.scatter3D(k, b, L3,label='Latent Activation 3' )
    plt.show()
#Latent_values_Scynet2()

