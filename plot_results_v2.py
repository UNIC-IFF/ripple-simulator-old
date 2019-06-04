import pandas as pd
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
fname="./results/case_N_nodesvsMalnodes_3/cases_output.csv"
if len(sys.argv)>1:
    fname=sys.argv[1]

cols= ['Num_nodes' , 'Num_malicious', 'consensus_percent', 'num_outbound_links', 'max_unl', 'min_unl', 'unl_threshold','overlappingUNLs' , 'min_c2c_latency', 'max_c2c_latency', 
        'min_e2c_latency' , 'max_e2c_latency', 'convergence_time','unprocessed_messages', 'total_messages_sent', 'unprocessed_messages ratio' , "noConvergence", "malicious nodes portion"]

#load csv
res=pd.read_csv(fname, sep="\t", names=cols, header=None,index_col=False)

# ex 
#   Num_nodes   Num_malicious   consensus_percent   num_outbound_links  max_unl min_unl unl_threshold   min_c2c_latency max_c2c_latency min_e2c_latency max_e2c_latency convergence_time    unprocessed_messages    
#   2000        1200            80                  10                  30      20      10              5               200             5               50              2031                152048                  1712564 0.081544        0       60

#  std::cout << myConfig.Num_Nodes <<"\t"<< myConfig.Num_Malicious << "\t" << myConfig.consensus_percent << "\t" <<  myConfig.Num_Outbound_Links << "\t" << myConfig.Max_UNL << "\t" <<myConfig.Min_UNL << "\t" <<myConfig.UNL_threshold 
            # << "\t" << myConfig.Min_c2c_latency << "\t" << myConfig.Max_c2c_latency << "\t" << myConfig.Min_e2c_latency<< "\t" <<myConfig.Max_e2c_latency
            # << "\t" << network.master_time<< "\t" << mc<< "\t" <<total_messages_sent << "\t"<< isFatal<< std::endl ;

# print(res)
if "unprocessed_messages ratio" not in res.columns:
    res['unprocessed_messages ratio']=res['unprocessed_messages']/(res['total_messages_sent']+res['unprocessed_messages'])

if ("malicious nodes portion" not in res.columns):
    res['malicious nodes portion']=res['Num_malicious']/res['Num_nodes']
elif pd.isna(res["malicious nodes portion"][0]):
    res['malicious nodes portion']=res['Num_malicious']/res['Num_nodes']
  
unique_NumNodes=pd.unique(res['Num_nodes'])
N_unique_NumNodes=pd.unique(res['Num_nodes']).shape[0]
#N_cases_per_Nnodes=int(res.shape[0]/N_unique_NumNodes)

unique_malpC=pd.unique(res['malicious nodes portion'])

# print(res[ res[res['malicious nodes portion']==unique_malpC[0]][res['Num_nodes']==50]])
# res[res['malicious nodes portion']==unique_malpC[19]].drop_duplicates()


# Plot figure 1 for convergence time vs Num_nodes for each malicious nodes portion value
# Plot figure 2 for unutilized messages vs Num_nodes for each malicious nodes portion value
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()


for i,mpc in enumerate(unique_malpC):
    tmp=res[res['malicious nodes portion']==mpc].drop_duplicates()
    ax1.semilogy(tmp['Num_nodes'] , tmp['convergence_time'], color=fig_fmts[i][0] ,marker=fig_fmts[i][1], linestyle=fig_fmts[i][2],label=str(mpc)+' Mal Nodes portion')#plot
    ax2.plot(tmp['Num_nodes'] , tmp['unprocessed_messages ratio'], color=fig_fmts[i][0],marker=fig_fmts[i][1], linestyle=fig_fmts[i][2],label=str(mpc)+' Mal Nodes portion')
    
    # plt.yscale('symlog', linthrehy=0.001)

ax1.set(xlabel='Number of Nodes', ylabel='Convergence time (ms)', title="Convergence time vs Number of Nodes ")#for different malicious nodes ratio")
ax1.grid()
legend1=ax1.legend(loc='best', shadow=False, fontsize='small')
legend1.get_frame().set_facecolor('C1')
fig1.savefig(fname[:-4]+'convTime_numNodes_malpC_1.png')

ax2.set(xlabel='Number of Nodes', ylabel='Unprocessed messages ratio', title="Unprocessed messages ratio vs Number of Nodes ")#for different malicious nodes ratio")
ax2.grid()
legend2=ax2.legend(loc='best', shadow=False, fontsize='small')
legend2.get_frame().set_facecolor('C1')
fig2.savefig(fname[:-4]+'upmsgs_numNodes_malpC_1.png')


# Plot figure 3 for convergence time vs malicious nodes portion  for each Num_nodes value
# Plot figure 4 for unutilized messages vs malicious nodes portion  for each Num_nodes value
# Plot figure 5 for convergence time per node vs malicious nodes portion for each num_nodes value
# Plot figure 6 for average messages per node vs malicious nodes portion for each num_nodes value
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()
fig5, ax5 = plt.subplots()
fig6, ax6 = plt.subplots()

for i,mnn in enumerate(unique_NumNodes):
    tmp=res[res['Num_nodes']==mnn].drop_duplicates()
    ax3.semilogy(tmp['malicious nodes portion'] , tmp['convergence_time'], color=fig_fmts[i][0] ,marker=fig_fmts[i][1], linestyle=fig_fmts[i][2],label=str(mnn)+' Num Nodes')#plot
    ax4.plot(tmp['malicious nodes portion'] , tmp['unprocessed_messages ratio'], color=fig_fmts[i][0],marker=fig_fmts[i][1], linestyle=fig_fmts[i][2],label=str(mnn)+' Num Nodes')
    ax5.plot(tmp['malicious nodes portion'] , tmp['convergence_time']/mnn, color=fig_fmts[i][0],marker=fig_fmts[i][1], linestyle=fig_fmts[i][2],label=str(mnn)+' Num Nodes')
    ax6.plot(tmp['malicious nodes portion'] , tmp['total_messages_sent']/mnn, color=fig_fmts[i][0],marker=fig_fmts[i][1], linestyle=fig_fmts[i][2],label=str(mnn)+' Num Nodes')
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




# Scatter Plot, figure 7 , to show when consensus reached for all the cases
fig7, ax7 = plt.subplots()
pC_lines=pd.DataFrame()
pC_lines['Num_malicious']=pd.unique(res['Num_malicious'])
pC_lines['Num_malicious']=pC_lines['Num_malicious'].sort_values()

# pC_lines=res[['Num_nodes', 'Num_malicious']]
pC_lines['20pC_line']=(1/0.2)*pC_lines['Num_malicious']
pC_lines['33pC_line']=(1/0.33)*pC_lines['Num_malicious']


tmp_nC=res[res['noConvergence']==1]
tmp_wC=res[res['noConvergence']==0]
ax7.scatter(tmp_wC['Num_malicious'],tmp_wC['Num_nodes'],c='g',alpha=0.5, label="Consensus achieved")
ax7.scatter(tmp_nC['Num_malicious'], tmp_nC['Num_nodes'],c='r',alpha=0.9, label="No consensus")
ax7.plot(pC_lines['Num_malicious'],pC_lines['20pC_line'],'b--',label="20% line")
ax7.plot(pC_lines['Num_malicious'],pC_lines['33pC_line'],'b:',label="33% line")
ax7.set(xlabel="Number of malicious nodes", ylabel='Number of nodes', title="Consensus achievements")
legend7=ax7.legend(loc="best", shadow=False, fontsize='small')
legend7.get_frame().set_facecolor('C1')
fig7.savefig(fname[:-4]+'_consensus_scatter_1.png')


#write csv with titles
res.to_csv(fname[:-4]+'_out.csv',sep="\t")
