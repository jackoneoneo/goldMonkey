
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
import plotly.graph_objs as go
import plotly
from data import *
from Dbutils import Dbutils


def createHtml(databaseName,htmlName):
    print('start')
    colors = ['#8dd3c7', '#d62728', '#ffffb3', '#bebada',
              '#fb8072', '#80b1d3', '#fdb462',
              '#b3de69', '#fccde5', '#d9d9d9',
              '#bc80bd', '#ccebc5', '#ffed6f'];
    colorsX = ['#1f77b4', '#d62728', '#9467bd', '#ff7f0e', '#bebada']
    traces = []
    '''获取数据'''
    util = Dbutils(databaseName)
    conn = util.connectDb()
    listArr = SOCAndBusVolandBusCurData(conn)

    '''获取实时数据库里面的DMU中SOC、V、I的数据'''
    SocValue = listArr[0]
    VolValue = listArr[1]
    CurValue = listArr[2]
    ''''''
    traces.append(go.Scatter(
        mode='lines', line=dict(color=colorsX[0], width=0.1),
        connectgaps=False,  # 对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
        #x=monomerVolTemp['x'],
        #y=monomerVolTemp['y'],
        yaxis='电芯电压(V)',  # 标注轴名称
        #name="" + str(i + 1) + "bmu" + str(j + 1) + "monomer",  # 标注鼠标移动时的显示点信息
        text=['电压1', '电压2'],
        marker=dict(color=colorsX[0], size=12, ),
        legendgroup=1,
        showlegend=False,
    ))

    '''获取一簇下的bmu数量'''
    '''
    BmuNum = BmuNumber(conn)
    for i in range(BmuNum):
        monomerArr = MonomerVol(conn,"bcbmuzone"+str(i+1))
        length = len(monomerArr)
        for j in range(length):
            monomerVolTemp = monomerArr[j]
            traces.append(go.Scatter(
                        mode='lines', line=dict(color=colorsX[0], width=0.1),
                        connectgaps=False,  # 对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
                        x=monomerVolTemp['x'],
                        y=monomerVolTemp['y'],
                        yaxis='电芯电压(V)',  # 标注轴名称
                        name=""+str(i+1)+"bmu"+str(j+1)+"monomer",  # 标注鼠标移动时的显示点信息
                        text=['电压1', '电压2'],
                        marker=dict(color=colorsX[0], size=12, ),
                        legendgroup=1,
                        showlegend=False,
                    ))
    '''
    conn.close()

    trace2 = (go.Scatter(
                mode='lines', line=dict(color=colorsX[1], width=0.5),
                connectgaps=False,
                 x = SocValue['x'],
                 y = SocValue['y'],
                name='簇SOC',
                # 决定y轴取那个轴，y2——>yaxis2,
                yaxis='y2',
                legendgroup=2,
                showlegend=False,
            )
            )
    trace3 = (go.Scatter(
                mode='lines', line=dict(color=colorsX[2], width=0.5),
                connectgaps=False,
                x = VolValue['x'],
                y = VolValue['y'],
                name='簇电压V',
                # 决定y轴取那个轴，y3——>yaxis3,
                yaxis='y3',
                legendgroup=2,
                showlegend=False,
            )
            )
    trace4 = (go.Scatter(
                mode='lines', line=dict(color=colorsX[3], width=0.5),
                connectgaps=False,
                 x=CurValue['x'],
                 y=CurValue['y'],
                name='簇电流A',
                # 决定y轴取那个轴，y4——>yaxis4,
                yaxis='y4',
                legendgroup=2,
                showlegend=False,
            )
            )

    traces.append(trace2)
    traces.append(trace3)
    traces.append(trace4)
    layout = go.Layout(
                width=1280,
                xaxis=dict(
                    domain=[0.1, 0.9],
                    showline=True,
                    showgrid=True,
                    showticklabels=True,
                    linewidth=2,
                    autotick=True,
                    ticks='outside',
                    tickwidth=2,
                    ticklen=5,
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='rgb(82, 82, 82)',
                    ),
                    hoverformat="%Y/%m/%d %H:%M:%S",
                ),
                # 第一个y轴
                yaxis=dict(
                    title='电芯电压(V)',
                    linecolor=colorsX[0],
                    showgrid=True,
                    zeroline=False,  # 是否显示基线,即沿着(0,0)画出x轴和y轴
                    showline=True,
                    showticklabels=True,
                    titlefont=dict(color=colorsX[0]),
                    tickfont=dict(color=colorsX[0]),
                ),
                # 第二个y轴
                yaxis2=dict(
                    title='簇SOC',
                    linecolor=colorsX[1],
                    showgrid=True,
                    zeroline=False,  # 是否显示基线,即沿着(0,0)画出x轴和y轴
                    showline=True,
                    showticklabels=True,
                    titlefont=dict(color=colorsX[1]),
                    tickfont=dict(color=colorsX[1]),
                    range=[0, 100],
                    anchor='x',
                    overlaying='y',
                    side='right',
                ),
                # 第三个y轴
                yaxis3=dict(
                    title='簇电压V_aver',
                    linecolor=colorsX[2],
                    showgrid=True,
                    zeroline=False,  # 是否显示基线,即沿着(0,0)画出x轴和y轴
                    showline=True,
                    showticklabels=True,
                    titlefont=dict(color=colorsX[2]),
                    tickfont=dict(color=colorsX[2]),
                    anchor='free',
                    overlaying='y',
                    side='left',
                    position=0.05
                ),
                # 第四个y轴
                yaxis4=dict(
                    title='簇电流I_aver',
                    linecolor=colorsX[3],
                    showgrid=True,
                    zeroline=False,  # 是否显示基线,即沿着(0,0)画出x轴和y轴
                    showline=True,
                    showticklabels=True,
                    titlefont=dict(color=colorsX[3]),
                    tickfont=dict(color=colorsX[3]),
                    anchor='free',
                    overlaying='y',
                    side='right',
                    position=0.95
                ),
                # autosize=True,
                margin=dict(
                    autoexpand=False,
                    l=20,
                    r=20,
                    t=100,
                ),
                showlegend=True,
            )
    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                    xanchor='left', yanchor='bottom',
                                    text='电芯分析图',
                                    font=dict(family='Arial',
                                              size=30,
                                              color='rgb(37,37,37)'),
                                    showarrow=False))

    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.05,
                                    xanchor='center', yanchor='top',
                                    text='数据来源: 实时sqlite数据 & ' +
                                         '调频数据',
                                    font=dict(family='Arial',
                                              size=12,
                                              color='rgb(150,150,150)'),
                                    showarrow=False))
    layout['annotations'] = annotations
    fig = go.Figure(data=traces, layout=layout)
    plot_url = plotly.offline.plot(fig, filename='templates/'+htmlName, auto_open=False)
    print('finish')

#createHtml("000203004bcms1.db","1.html")
