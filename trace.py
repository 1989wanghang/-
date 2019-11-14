#!env python3
# -*- coding: UTF-8 -*-

import sys
import plotly.graph_objects as go
import plotly.offline as py
import numpy as np

min_time = -1
max_time = -1
y = 0
y_gap = 1


def ReadFile(file_path):
    global min_time, max_time, y
    y -= y_gap
    f = open(file_path, 'r')
    x_values = []
    y_values = []
    element_num = 0
    tmp_values = []
    for line in f.readlines():
        line = line.strip()
        if not len(line) or line.startswith('#'):
            continue
        strs = line.split()
        values = list(map(int, strs))
        if min_time != -1 and values[-1] < min_time:
            continue
        if max_time != -1 and values[0] > max_time:
            continue
        if min_time == -1:
            min_time = values[0]
        if max_time == -1:
            tmp_values += values
        for i in range(len(values)):
            y_values.append(y)
            values[i] = int((values[i] - min_time) / 1000)
        x_values += values
        element_num = len(values)
        if element_num > 1:
            x_values.append(None)
            y_values.append(None)
    if len(x_values) == 0:
        y += y_gap
    if max_time == -1:
        max_time = max(tmp_values)
    return x_values, y_values, element_num


def main():
    fichier_html_graphs = open("DASHBOARD.html", 'w')
    fichier_html_graphs.write("<html><head></head><body>"+"\n")
    #fig = go.Figure()
    traces = []
    global min_time, max_time, y
    y = len(sys.argv) * y_gap
    print('参数列表:', str(sys.argv))
    for i in range(1, len(sys.argv)):
        filepath = sys.argv[i]
        print('参数 %s 为: %s' % (i, filepath))
        x_values, y_values, element_num = ReadFile(filepath)
        if len(x_values) == 0:
            continue
        trace_name = filepath.split('/')[-1].split('.')[0]
        if element_num == 1:
            traces.append(go.Scatter(x=x_values, y=y_values,
                                     mode='markers', name=trace_name))
        elif element_num > 1:
            traces.append(go.Scatter(x=x_values, y=y_values,
                                     mode='lines+markers', name=trace_name))
        else:
           print('impossiable element_num == 0')
    layout = go.Layout(
        title=('总数据'), xaxis=dict(title='时间戳(ms)'))
    fig = go.Figure(data=traces, layout=layout)
    py.plot(fig, filename='large.html', auto_open=False)
    fichier_html_graphs.write(
        "  <object data=\""+'large.html'+"\" width=\"1024\" height=\"600\"></object>"+"\n")
    fichier_html_graphs.write("</body></html>")


if __name__ == "__main__":
    main()
