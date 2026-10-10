import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
OUT='/mnt/user-data/outputs/storyboard_charts/'
d=pd.read_excel('/root/.claude/uploads/04f01b9a-4c42-5394-b8ce-17dc7dfaf136/f5800993-Section16_Improved_Tableau_Ready1.xlsx',sheet_name='Removed Avondale and Batchelor')
BLUE='#2a78d6'; GRAY='#8a8983'; INK='#0b0b0b'; INK2='#52514e'; RED='#e34948'; SURF='#ffffff'
plt.rcParams.update({'font.size':13,'axes.edgecolor':'#c9c8c2','axes.labelcolor':INK2,'xtick.color':INK2,'ytick.color':INK2,
 'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':SURF,'axes.facecolor':SURF})
def title(fig,t,s):
    fig.text(0.04,0.95,t,fontsize=20,weight='bold',color=INK,va='top')
    fig.text(0.04,0.885,s,fontsize=12.5,color=INK2,va='top')
def src(fig,t='Source: Dept of Education, Section 16 Equity Performance Data 2024 (Table A & B providers)'):
    fig.text(0.04,0.02,t,fontsize=9.5,color=GRAY)
nat=d[d['Region Type']=='National']
def series(m,g): s=nat[(nat.Metric==m)&(nat['Equity Group']==g)].set_index('Year')['Rate (%)'].sort_index(); return s

# 1 access
a=series('Access Rate','Low SES by SA1')
fig,ax=plt.subplots(figsize=(10,6.2)); fig.subplots_adjust(top=0.78,bottom=0.13,left=0.08,right=0.84)
ax.axhline(25,color=GRAY,lw=2,ls=(0,(4,3)))
ax.text(2024.3,25,'25%\npopulation\nshare',color=INK2,va='center',fontsize=11.5)
ax.fill_between(a.index,a.values,25,color=BLUE,alpha=.10,lw=0)
ax.plot(a.index,a.values,color=BLUE,lw=2.5,marker='o',ms=6,markeredgecolor=SURF,markeredgewidth=1.5)
ax.text(2024.3,a[2024],f'{a[2024]:.1f}%\nlow-SES\nstudents',color=INK,va='center',fontsize=11.5,weight='bold')
ax.text(2011,a[2011]-1.3,f'{a[2011]:.1f}%',color=INK2,fontsize=11.5,ha='center',va='top')
ax.set_ylim(0,30); ax.set_xlim(2010.5,2024.2); ax.set_yticks([0,10,20,30]); ax.set_yticklabels(['0%','10%','20%','30%'])
ax.grid(axis='y',color='#ebeae6',lw=1); ax.set_axisbelow(True); ax.set_xticks(range(2011,2025,2))
title(fig,'Low-SES students are still under-represented','Share of commencing domestic students from low-SES areas (SA1), Australia, 2011–2024')
src(fig); fig.savefig(OUT+'panel2_lowSES_access_trend.png',dpi=200); plt.close()

# 2 retention gap
l=series('Retention Rate','Low SES by SA1').dropna(); al=series('Retention Rate','All Domestic').dropna()
fig,ax=plt.subplots(figsize=(10,6.2)); fig.subplots_adjust(top=0.78,bottom=0.13,left=0.08,right=0.84)
ax.fill_between(l.index,l.values,al.values,color=RED,alpha=.12,lw=0)
ax.plot(al.index,al.values,color=GRAY,lw=2.5,marker='o',ms=6,markeredgecolor=SURF,markeredgewidth=1.5)
ax.plot(l.index,l.values,color=BLUE,lw=2.5,marker='o',ms=6,markeredgecolor=SURF,markeredgewidth=1.5)
ax.text(2023.3,al[2023]+.3,f'All domestic\n{al[2023]:.1f}%',color=INK2,va='center',fontsize=11.5)
ax.text(2023.3,l[2023]-.3,f'Low-SES\n{l[2023]:.1f}%',color=INK,va='center',fontsize=11.5,weight='bold')
for y in (2011,2023):
    g=al[y]-l[y]; ax.annotate('',xy=(y,l[y]+.15),xytext=(y,al[y]-.15),arrowprops=dict(arrowstyle='<->',color=RED,lw=1.6))
    ax.text(y+(.25 if y==2011 else -.25),(al[y]+l[y])/2 if y==2011 else 79.2,f'{g:.1f} pts',color=RED,weight='bold',fontsize=12.5,va='center',ha='left' if y==2011 else 'right')
ax.set_ylim(74,85); ax.set_xlim(2010.5,2023.2); ax.set_xticks(range(2011,2024,2))
ax.yaxis.set_major_formatter(lambda v,p:f'{v:.0f}%'); ax.grid(axis='y',color='#ebeae6'); ax.set_axisbelow(True)
title(fig,'The retention gap for low-SES students has widened','First-year retention rate, low-SES vs all domestic students, Australia, 2011–2023 (latest)')
src(fig); fig.savefig(OUT+'panel3_retention_gap.png',dpi=200); plt.close()

# 3 Aha ranking
i=d[d['Region Type']=='Higher Education Institution']
def get(g,m,y): return i[(i['Equity Group']==g)&(i.Metric==m)&(i.Year==y)].set_index('Region')['Rate (%)']
t=pd.DataFrame({'low':get('Low SES by SA1','Retention Rate',2023),'all':get('All Domestic','Retention Rate',2023)}).dropna().sort_values('low')
short={'The University of Western Australia':'U Western Australia','University of South Australia':'U South Australia','The University of Notre Dame Australia':'U Notre Dame','Federation University Australia':'Federation Uni','Torrens University Australia':'Torrens Uni','The University of ':'U ','University of ':'U ','The ':'',' University':' Uni','Australian Catholic Uni':'ACU','Queensland Uni of Technology':'QUT','Swinburne Uni of Technology':'Swinburne','U Technology Sydney':'UTS','U the Sunshine Coast':'U Sunshine Coast'}
def sh(n):
    for k,v in short.items(): n=n.replace(k,v)
    return n
fig,ax=plt.subplots(figsize=(10,12)); fig.subplots_adjust(top=0.885,bottom=0.06,left=0.30,right=0.95)
y=np.arange(len(t))
ax.hlines(y,t['low'].clip(upper=t['all']),t['all'],color='#d9d8d2',lw=2)
ax.scatter(t['all'],y,s=38,color=GRAY,zorder=3,edgecolor=SURF,lw=1,label='All domestic')
ax.scatter(t['low'],y,s=60,color=BLUE,zorder=4,edgecolor=SURF,lw=1.2,label='Low-SES')
ax.axvline(l[2023],color=BLUE,lw=1,ls=(0,(3,3)),alpha=.7)
ax.text(l[2023]+.3,len(t)-.3,f'National low-SES {l[2023]:.1f}%',color=BLUE,fontsize=10.5,va='bottom')
ax.set_yticks(y); ax.set_yticklabels([sh(n) for n in t.index],fontsize=10.5)
ax.xaxis.set_major_formatter(lambda v,p:f'{v:.0f}%'); ax.set_xlim(55,94); ax.grid(axis='x',color='#ebeae6'); ax.set_axisbelow(True)
ax.set_ylim(-1,len(t)+1)
ax.annotate(f'{t.low.iloc[0]:.0f}%',(t.low.iloc[0],0),xytext=(8,0),textcoords='offset points',va='center',weight='bold',color=INK)
ax.annotate(f'{t.low.iloc[-1]:.0f}%',(t.low.iloc[-1],len(t)-1),xytext=(-8,0),textcoords='offset points',va='center',ha='right',weight='bold',color=INK)
ax.legend(loc='lower right',frameon=False,fontsize=11.5)
fig.text(0.04,0.965,'Where you study matters more than the gap',fontsize=20,weight='bold',color=INK,va='top')
fig.text(0.04,0.935,f'Low-SES first-year retention ranges from {t.low.min():.0f}% to {t.low.max():.0f}% between universities —\na {t.low.max()-t.low.min():.0f}-point spread, vs a {(t["all"]-t.low).median():.1f}-point typical gap within a university. 2023.',fontsize=12.5,color=INK2,va='top')
src(fig); fig.savefig(OUT+'panel4_aha_retention_by_university.png',dpi=200); plt.close()

# 4 heatmaps per uni
groups=['Low SES by SA1','Regional/Remote','First Nations','Disability','Non-English Speaking Background','All Domestic']
labels=['Low-SES','Regional/Remote','First Nations','Disability','Non-English Speaking Bkgd','All domestic (benchmark)']
metrics=[('Access Rate',2024,'Access'),('Attainment Rate',2024,'Attainment'),('Retention Rate',2023,'Retention'),('Success Rate',2024,'Success')]
cmap=LinearSegmentedColormap.from_list('div',['#c93a39','#f2a3a0','#f0efec','#9ec5f4','#256abf'])
def natval(g,m,y):
    s=nat[(nat['Equity Group']==g)&(nat.Metric==m)&(nat.Year==y)]['Rate (%)']; return s.iloc[0] if len(s) else np.nan
def heat(uni,fname):
    V=np.full((len(groups),4),np.nan); D=V.copy()
    for r,g in enumerate(groups):
        for c,(m,yr,_) in enumerate(metrics):
            s=i[(i.Region==uni)&(i['Equity Group']==g)&(i.Metric==m)&(i.Year==yr)]['Rate (%)']
            if len(s): V[r,c]=s.iloc[0]; D[r,c]=s.iloc[0]-natval(g,m,yr)
    fig,ax=plt.subplots(figsize=(10,6.4)); fig.subplots_adjust(top=0.76,bottom=0.17,left=0.29,right=0.97)
    norm=TwoSlopeNorm(0,-8,8)
    for r in range(len(groups)):
        for c in range(4):
            if np.isnan(V[r,c]):
                ax.add_patch(plt.Rectangle((c+.03,r+.04),.94,.92,color='#f7f7f5',lw=0)); ax.text(c+.5,r+.5,'n/a',ha='center',va='center',color=GRAY,fontsize=11); continue
            col=cmap(norm(np.clip(D[r,c],-8,8)))
            ax.add_patch(plt.Rectangle((c+.03,r+.04),.94,.92,color=col,lw=0))
            dark=abs(D[r,c])>5
            hl=(r==0)
            ax.text(c+.5,r+.42,f'{V[r,c]:.1f}%',ha='center',va='center',fontsize=14 if hl else 12.5,weight='bold' if hl else 'normal',color='white' if dark else INK)
            ax.text(c+.5,r+.74,f'{D[r,c]:+.1f} vs national',ha='center',va='center',fontsize=9,color='white' if dark else INK2)
    ax.add_patch(plt.Rectangle((0.01,0.01),3.98,.98,fill=False,ec=INK,lw=2))
    ax.set_xlim(0,4); ax.set_ylim(len(groups),0)
    ax.set_xticks(np.arange(4)+.5); ax.set_xticklabels([f'{n}\n({y})' for _,y,n in metrics],fontsize=12); ax.xaxis.tick_top()
    ax.set_yticks(np.arange(len(groups))+.5); ax.set_yticklabels(labels,fontsize=12)
    ax.get_yticklabels()[0].set_weight('bold')
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(length=0)
    fig.text(0.04,0.965,uni,fontsize=20,weight='bold',color=INK,va='top')
    fig.text(0.04,0.91,'Equity group performance. Colour = difference from the national rate for the same group',fontsize=12,color=INK2,va='top')
    # legend
    lx=fig.add_axes([0.29,0.085,0.4,0.025]); grad=np.linspace(-8,8,200)[None,:]
    lx.imshow(grad,aspect='auto',cmap=cmap,norm=norm); lx.set_yticks([]); lx.set_xticks([0,100,199]); lx.set_xticklabels(['−8 pts below national','0','+8 above'],fontsize=10)
    for s in lx.spines.values(): s.set_visible(False)
    lx.tick_params(length=0)
    fig.text(0.04,0.012,'Access/attainment = % of domestic students from the group. Retention 2023 = latest year.\nSource: Dept of Education, Section 16 Equity Performance Data 2024',fontsize=9,color=GRAY)
    fig.savefig(OUT+fname,dpi=200); plt.close()
for u in ['Western Sydney University','University of Wollongong','CQUniversity']:
    heat(u,'panel4_heatmap_'+u.replace(' ','_')+'.png')
