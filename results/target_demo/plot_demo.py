import pandas as pd
import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt

markers_list=["o", "v", "^" ,"<", ">","1","2","3","4","8"] #,"s","p","P","*","+","x","X","D","d"]+[ j for j in range(4,12)] + ["." , "," ,"h","H","|","_","None"] +[j for j in range(4)]
colors_list=["b","r","g","k"]
linestyles_list=['-',':','-.','--']

fig_fmts=[]
for lsl in linestyles_list:
    for c in colors_list:
        fig_fmts+=[ (c,j,lsl) for j in markers_list]



# fname="./cases_output_test1.csv"
# fname="./results/case_N_nodesvsMalnodes_2/cases_output_comb.csv"
# fname="./results/case_N_nodesvsMalnodes_3/cases_output.csv"
#fname="./cases_demo.csv"
fname="./cases_demo_200.csv"
if len(sys.argv)>1:
    fname=sys.argv[1]

cols= ['Num_nodes' , 'Num_malicious', 'consensus_percent', 'num_outbound_links', 'max_unl', 'min_unl', 'unl_threshold','overlappingUNLs' , 'min_c2c_latency', 'max_c2c_latency', 
        'min_e2c_latency' , 'max_e2c_latency', 'convergence_time','unprocessed_messages', 'total_messages_sent', 'unprocessed_messages ratio' , "noConvergence", "malicious nodes portion"]

#load csv
res=pd.read_csv(fname, sep="\t",  header=0,index_col=0)#names=cols,index_col=False

unique_NumNodes=pd.unique(res['Num_nodes'])
N_unique_NumNodes=pd.unique(res['Num_nodes']).shape[0]
#N_cases_per_Nnodes=int(res.shape[0]/N_unique_NumNodes)
unique_ovUNLs=pd.unique(res['overlappingUNLs'])
N_unique_ovUNLs=unique_ovUNLs.shape[0]

unique_malpC=pd.unique(res['malicious nodes portion'])

# Plot figure 3 for convergence time vs malicious nodes portion  for each Num_nodes value
# Plot figure 4 for unutilized messages vs malicious nodes portion  for each Num_nodes value
# Plot figure 5 for convergence time per node vs malicious nodes portion for each num_nodes value
# Plot figure 6 for average messages per node vs malicious nodes portion for each num_nodes value
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()
fig5, ax5 = plt.subplots()
fig6, ax6 = plt.subplots()

for i,mnn in enumerate(unique_NumNodes):
    tmp1=res[res['Num_nodes']==mnn].drop_duplicates()
    for j,munlov in enumerate(unique_ovUNLs):
        tmp=tmp1[tmp1['overlappingUNLs']==munlov].drop_duplicates()
        tmp['convergence_time_winf']=tmp['convergence_time']*(np.ones(tmp.shape[0])-tmp['noConvergence'])
        # tmp2=tmp[tmp['noConvergence']==0]
        # ax3.semilogy(tmp2['malicious nodes portion'] , tmp2['convergence_time'], color=fig_fmts[i*N_unique_NumNodes+j][0] ,marker=fig_fmts[i*N_unique_NumNodes+j][1], linestyle=fig_fmts[i*N_unique_NumNodes+j][2],label=str(mnn)+' Num Nodes'+str(munlov)+' ovUNLs')#plot
        ax3.semilogy(tmp['malicious nodes portion'] , tmp['convergence_time'], color=fig_fmts[i*N_unique_NumNodes+j][0] ,marker=fig_fmts[i*N_unique_NumNodes+j][1], linestyle=fig_fmts[i*N_unique_NumNodes+j][2],label=str(mnn)+' Num Nodes'+str(munlov)+' ovUNLs')#plot
        ax4.plot(tmp['malicious nodes portion'] , tmp['unprocessed_messages ratio'], color=fig_fmts[i*N_unique_NumNodes+j][0],marker=fig_fmts[i*N_unique_NumNodes+j][1], linestyle=fig_fmts[i*N_unique_NumNodes+j][2],label=str(mnn)+' Num Nodes'+str(munlov)+' ovUNLs')
        ax5.plot(tmp['malicious nodes portion'] , tmp['convergence_time']/mnn, color=fig_fmts[i*N_unique_NumNodes+j][0],marker=fig_fmts[i*N_unique_NumNodes+j][1], linestyle=fig_fmts[i*N_unique_NumNodes+j][2],label=str(mnn)+' Num Nodes'+str(munlov)+' ovUNLs')
        ax6.plot(tmp['malicious nodes portion'] , tmp['total_messages_sent']/mnn, color=fig_fmts[i*N_unique_NumNodes+j][0],marker=fig_fmts[i*N_unique_NumNodes+j][1], linestyle=fig_fmts[i*N_unique_NumNodes+j][2],label=str(mnn)+' Num Nodes'+str(munlov)+' ovUNLs')
        # plt.yscale('symlog', linthrehy=0.001)

ax3.set(xlabel='Malicious Nodes %', ylabel='Convergence time (ms)', title="Convergence time vs malicious nodes %")#ratio for various Number of Nodes")
ax3.grid()
legend3=ax3.legend(loc='best', shadow=False, fontsize='small')
legend3.get_frame().set_facecolor('C1')
fig3.savefig(fname[:-4]+'convTime_malpC_numNodes_1.png')

ax4.set(xlabel='Malicious Nodes %', ylabel='Unprocessed messages ratio', title="Unprocessed messages ratio vs malicious nodes %")# ratio for various Number of Nodes")
ax4.grid()
legend4=ax4.legend(loc='best', shadow=False, fontsize='small')
legend4.get_frame().set_facecolor('C1')
fig4.savefig(fname[:-4]+'upmsgs_malpC_numNodes_1.png')

ax5.set(xlabel='Malicious Nodes %', ylabel='Convergence time per node (ms)', title="Convergence time per Node vs malicious nodes %")#ratio for various Number of Nodes")
ax5.grid()
legend5=ax5.legend(loc='best', shadow=False, fontsize='small')
legend5.get_frame().set_facecolor('C1')
fig5.savefig(fname[:-4]+'_convTimepN_malpC_numNodes_1.png')

ax6.set(xlabel='Malicious Nodes %', ylabel='Average messages per node', title="Average messages per Node vs malicious nodes %")#ratio for various Number of Nodes")
ax6.grid()
legend6=ax6.legend(loc='best', shadow=False, fontsize='small')
legend6.get_frame().set_facecolor('C1')
fig6.savefig(fname[:-4]+'_msgspN_malpC_numNodes_1.png')

