#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os

#path_prefix='./graph1_case'
path_prefix='./graph1_fixLatency_case'

#########################
# formating colors_list
markers_list=["o", "v", "^" ,"<", ">","s","p","P","*","+","x"]#,"1","2","3","4","8"] #,"s","p","P","*","+","x","X","D","d"]+[ j for j in range(4,12)] + ["." , "," ,"h","H","|","_","None"] +[j for j in range(4)]
colors_list=["b","r","g","k"]
linestyles_list=['-',':','-.','--']

fig_fmts=[]
for lsl in linestyles_list:
    for c in colors_list:
        fig_fmts+=[ (c,j,lsl) for j in markers_list]
        
#######################


MAX_malpC=36
ov_limits=[(0,0.51) , (0.51,0.89) , (0.9,1) ]
Nnodes_cases=[1000]

Ngraphs=len(ov_limits)*len(Nnodes_cases)

## Creating data directories
for ncase in Nnodes_cases:
    for ovlim in ov_limits:
        if os.path.exists(path_prefix+'N%s_%s'%(str(ncase),str(ovlim[1])))==False :
            os.mkdir(path_prefix+'N%s_%s'%(str(ncase),str(ovlim[1])))


fdata1= pd.read_csv("../cases_N1000_fixLatency_out.csv",'\t') #"../case_ovUNL85_out.csv",'\t')
fdata2= pd.read_csv("../cases_varN_fixLatency_out2.csv",'\t') #pd.read_csv("../case_ovUNL90_out.csv",'\t')
fdata3=fdata1.append(fdata2)

#fdata3=pd.read_csv("../cases_N1000_fixLatency_out.csv",'\t')
print(fdata3.shape)
fdata=fdata3[fdata3.columns[1:]].drop_duplicates()
print(fdata.shape)


#malpC_filter=fdata[fdata['malicious nodes portion'] < MAX_malpC].index
malpC_filter=fdata['malicious nodes portion']<MAX_malpC #unique()

print ("malpC_filter length: %s"%malpC_filter.shape[0])

ovlim_filters=[]

for (ovlmin, ovlmax) in ov_limits:
#	indx=fdata[fdata['overlappingUNLs']<=ovlmax].index.intersection(fdata[fdata['overlappingUNLs']>=ovlmin].index)
	indx=(fdata['overlappingUNLs']<=ovlmax) & (fdata['overlappingUNLs']>=ovlmin)
	ovlim_filters.append(indx)
#	print ("ovlim_filter %s,%s length: %s"%(ovlmin, ovlmax, indx.shape[0]))


Nnodes_filters=[]
for ncase in Nnodes_cases:
#	indx=fdata[fdata['Num_nodes']==ncase].index
	indx=fdata['Num_nodes']==ncase
	Nnodes_filters.append(indx)
#	print ("Nnode_filter %s length: %s"%(ncase, indx.shape[0]))


# unique values
unique_ovUNLs=fdata['overlappingUNLs'].unique()

graph1_cols=['malicious nodes portion','convergence_time']

graph_data={}
for j in range(len(Nnodes_cases)):
	graph_data[Nnodes_cases[j]]={}
	for i in range(len(ov_limits)):
		graph_data[Nnodes_cases[j]][ov_limits[i]]={}
		for uni in unique_ovUNLs:
			if (uni< ov_limits[i][0]) or (uni>ov_limits[i][1]):
				continue
			#joint_filter=malpC_filter.intersection(Nnodes_filters[j].intersection(ovlim_filters[i]))
			#joint_filter=malpC_filter & Nnodes_filters[j] & ovlim_filters[i]
			ovlim_filter=(fdata['overlappingUNLs']==uni)
			joint_filter=malpC_filter & Nnodes_filters[j] & ovlim_filter
			#print(joint_filter.shape)
			#print(Nnodes_filters[j].intersection(ov_limits[i]).shape)
			#graph_data.append(fdata.loc[joint_filter])
			#graph_data.append(fdata.loc[joint_filter])
			graph_data[Nnodes_cases[j]][ov_limits[i]][uni]=fdata.loc[joint_filter]
			tmp_df=pd.DataFrame(columns=graph1_cols)
			tmp_df=graph_data[Nnodes_cases[j]][ov_limits[i]][uni][graph1_cols]
			tmp_df.sort_values(graph1_cols[0],inplace=True)
			tmp_df.to_csv(path_prefix+"N%s_%s/Gdata_%s.csv"%(str(Nnodes_cases[j]),str(ov_limits[i][1]),str(uni)),sep="\t",index=False)


### plotting graph_data

fig1, ax1 = plt.subplots(1,len(ov_limits))
#fig2, ax2 = plt.subplots()
#fig3, ax3 = plt.subplots()
#fig6, ax6 = plt.subplots()

for i,lim in enumerate(ov_limits):
	for j,k in enumerate(graph_data[1000][lim].keys()):
		ax1[i].plot(graph_data[1000][lim][k]['malicious nodes portion'],graph_data[1000][lim][k]['convergence_time'],color=fig_fmts[i*len(ov_limits)+j][0] ,marker=fig_fmts[i*len(ov_limits)+j][1], linestyle=fig_fmts[i*len(ov_limits)+j][2],label='ovUNLs '+str(k))
		
#ax1[1].plot(graph_data[1000][(0.51,0.89)]['malicious nodes portion'],graph_data[1000][(0.51,0.89)]['convergence_time'])
#ax1[2].plot(graph_data[1000][(0.9,1)]['malicious nodes portion'],graph_data[1000][(0.9,1)]['convergence_time'])




###### Graph 2


fig2, ax2 = plt.subplots()

unique_Nnodes=fdata['Num_nodes'].unique()

path_prefix='./graph2_fixLatency_case_'
## Creating data dir
if os.path.exists(path_prefix+'ovUNL0.90')==False :
	os.mkdir(path_prefix+'ovUNL0.90')




graph2_cols=['malicious nodes portion','convergence_time']

graph_data2={}
for i,uni in enumerate(unique_Nnodes):
	ovlim_filter=(fdata['overlappingUNLs']==0.9)
	joint_filter=(fdata['Num_nodes']==uni) & ovlim_filter & malpC_filter
	graph_data2[uni]=fdata.loc[joint_filter]

	tmp_df=pd.DataFrame(columns=graph2_cols)
	tmp_df=graph_data2[uni][graph2_cols]
	tmp_df.sort_values(graph2_cols[0],inplace=True)
	tmp_df.to_csv(path_prefix+"ovUNL0.90/Gdata_%s.csv"%(str(uni)),sep="\t",index=False)
		
for i,k in enumerate(graph_data2.keys()):
	ax2.plot(graph_data2[k]['malicious nodes portion'],graph_data2[k]['convergence_time'],color=fig_fmts[i][0] ,marker=fig_fmts[i][1], linestyle=fig_fmts[i][2],label='N '+str(k))
	
	















