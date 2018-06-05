

import plotly.graph_objs as go
import plotly
from data import *
from Dbutils import Dbutils


'''获取Bmu列表'''
def BmuNameList(databaseName):
    util = Dbutils(databaseName)
    conn = util.connectDb()
    list = BmuList(conn)
    conn.close()
    return list


def createBmuHtml(databaseName,htmlName,BmuName):
    print('start')
    colors = ['#8dd3c7', '#d62728', '#ffffb3', '#bebada',
              '#fb8072', '#80b1d3', '#fdb462',
              '#b3de69', '#fccde5', '#d9d9d9',
              '#bc80bd', '#ccebc5', '#ffed6f','#000000'];
    colorsX = ['#FF0000', '#d62728', '#9467bd', '#ff7f0e', '#bebada']
    traces = []
    '''获取数据'''
    util = Dbutils(databaseName)
    conn = util.connectDb()
    listArr = SOCAndBusVolandBusCurData(conn)
    monomerVolList = MonomerVol(conn,BmuName)
    conn.close()
    length = len(monomerVolList)
    '''获取实时数据库里面的DMU中SOC、V、I的数据'''
    SocValue = listArr[0]
    VolValue = listArr[1]
    CurValue = listArr[2]


    for j in range(length):
        monomerVolTemp = monomerVolList[j]
        if(j < 12):
            traces.append(go.Scatter(
                mode='lines', line=dict(color=colorsX[0], width=0.5),
                connectgaps=False,  # 对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
                x=monomerVolTemp['x'],
                y=monomerVolTemp['y'],
                yaxis='电芯电压(V)',  # 标注轴名称
                name="单体"+str(j+1) + "电压",  # 标注鼠标移动时的显示点信息
               # name=str(j + 1) + "monomer",  # 标注鼠标移动时的显示点信息
                text=['电压1', '电压2'],
                marker=dict(color=colorsX[0], size=12, ),
                #legendgroup=1,
                showlegend=True,
            ))
        elif(12 == j):
            traces.append(go.Scatter(
                mode='lines', line=dict(color="00FF00", width=1),
                connectgaps=False,  # 对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
                x=monomerVolTemp['x'],
                y=monomerVolTemp['y'],
                yaxis='电芯电压(V)',  # 标注轴名称
                name="过压线",  # 标注鼠标移动时的显示点信息
                # name=str(j + 1) + "monomer",  # 标注鼠标移动时的显示点信息
                text=['电压1', '电压2'],
                marker=dict(color=colorsX[0], size=12, ),
                # legendgroup=1,
                showlegend=True,
            ))
        else :
            traces.append(go.Scatter(
                mode='lines', line=dict(color="00FF00", width=1),
                connectgaps=False,  # 对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
                x=monomerVolTemp['x'],
                y=monomerVolTemp['y'],
                yaxis='电芯电压(V)',  # 标注轴名称
                name="欠压线",  # 标注鼠标移动时的显示点信息
                # name=str(j + 1) + "monomer",  # 标注鼠标移动时的显示点信息
                text=['电压1', '电压2'],
                marker=dict(color=colorsX[0], size=12, ),
                # legendgroup=1,
                showlegend=True,
            ))



    trace2 = (go.Scatter(
                mode='lines', line=dict(color=colorsX[1], width=0.5),
                connectgaps=False,
                 x = SocValue['x'],
                 y = SocValue['y'],
                name='簇SOC',
                # 决定y轴取那个轴，y2——>yaxis2,
                yaxis='y2',
                legendgroup=2,
                showlegend=True,
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
    '''
    traces.append(trace3)
    traces.append(trace4)
    '''
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


def createBCHtml(databaseName,htmlName):
    print('start')
    colors = ['#8dd3c7', '#d62728', '#ffffb3', '#bebada',
              '#fb8072', '#80b1d3', '#fdb462',
              '#b3de69', '#fccde5', '#d9d9d9',
              '#bc80bd', '#ccebc5', '#ffed6f'];
    colorsX = ['#1f77b4', '#d62728', '#9467bd', '#ff7f0e', '#bebada','#8dd3c7']
    traces = []
    '''获取数据'''
    util = Dbutils(databaseName)
    conn = util.connectDb()
    listArr = SOCAndBusVolandBusCurData(conn)
    dataList = temperatureAndVoltage(conn)
    '''获取实时数据库里面的DMU中SOC、V、I的数据'''
    SocValue = listArr[0]
    VolValue = listArr[1]
    CurValue = listArr[2]
    voltageMax = dataList[0]
    voltageMin = dataList[1]
    voltageAvg = dataList[2]
    temperatureMax = dataList[3]
    temperatureMin = dataList[4]
    '''簇最大单体电压'''
    traces.append(go.Scatter(
        mode='lines', line=dict(color=colorsX[0], width=0.5),
        connectgaps=False,  # 对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
        x=voltageMax['x'],
        y=voltageMax['y'],
        yaxis='电芯电压(V)',  # 标注轴名称
        name='簇最大单体电压V',
        text=['电压1', '电压2'],
        marker=dict(color=colorsX[0], size=12, ),
        legendgroup=1,
        showlegend=False,
    ))
    '''簇最小单体电压'''
    traces.append(go.Scatter(
        mode='lines', line=dict(color=colorsX[0], width=0.5),
        connectgaps=False,  # 对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
        x=voltageMin['x'],
        y=voltageMin['y'],
        yaxis='电芯电压(V)',  # 标注轴名称
        name='簇最小单体电压V',
        text=['电压1', '电压2'],
        marker=dict(color=colorsX[0], size=12, ),
        legendgroup=1,
        showlegend=False,
    ))

    '''簇平均单体电压'''
    traces.append(go.Scatter(
        mode='lines', line=dict(color=colorsX[0], width=0.5),
        connectgaps=False,  # 对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
        x=voltageAvg['x'],
        y=voltageAvg['y'],
        yaxis='电芯电压(V)',  # 标注轴名称
        name='簇平均单体电压V',
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
    '''簇最大温度'''
    trace5 = (go.Scatter(
                mode='lines', line=dict(color=colorsX[5], width=0.5),
                connectgaps=False,
                 x=temperatureMax['x'],
                 y=temperatureMax['y'],
                name='簇最大温度T',
                # 决定y轴取那个轴，y5——>yaxis5,
                yaxis='y5',
                legendgroup=2,
                showlegend=False,
            )
            )
    '''簇最小温度'''
    trace6 = (go.Scatter(
        mode='lines', line=dict(color=colorsX[5], width=0.5),
        connectgaps=False,
        x=temperatureMin['x'],
        y=temperatureMin['y'],
        name='簇最小温度T',
        # 决定y轴取那个轴，y5——>yaxis5,
        yaxis='y5',
        legendgroup=2,
        showlegend=False,
    )
    )
    traces.append(trace2)
    traces.append(trace3)
    traces.append(trace4)
    traces.append(trace5)
    traces.append(trace6)
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
            # 第五个y轴
            yaxis5=dict(
                title='簇温度T',
                linecolor=colorsX[4],
                showgrid=True,
                zeroline=False,  # 是否显示基线,即沿着(0,0)画出x轴和y轴
                showline=True,
                showticklabels=True,
                titlefont=dict(color=colorsX[4]),
                tickfont=dict(color=colorsX[4]),
                anchor='free',
                overlaying='y',
                side='left',
                position=1.2
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

