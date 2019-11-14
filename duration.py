#!env python3
# -*- coding: UTF-8 -*-

import sys
import plotly.graph_objects as go
import plotly.offline as py

fps = 120


def ReadFile(fichier_html_graphs, file_path):
    f = open(file_path, 'r')
    total_values = []
    x_values = []
    y_values = []
    colors = []
    sizes = []
    element_num = 0
    total_duration = 0
    first_value = -1
    for line in f.readlines():
        line = line.strip()
        if not len(line) or line.startswith('#'):
            continue
        strs = line.split()
        values = list(map(int, strs))
        element_num = len(values)
        if element_num < 2:
            print("need two timestamp")
            return None, None
        diff = values[1] - values[0]
        if diff < 0:
            print("ignore broken value: [{0} - {1}]".format(
                values[1], values[0]))
            continue
        if first_value == -1:
            first_value = values[0]
            print("first_value = ", first_value)
        total_values.append(values)
        x_values.append((values[0] - first_value) / 1000)
        total_duration += diff
        y_values.append(diff / 1000)
        colors.append(0)
        sizes.append(3)

    min_gap = min(y_values)
    max_gap = max(y_values)
    gap_strs = []
    gaps = []
    times = []
    ratios = []

    t = int((max_gap - min_gap) * fps / 1000) + 2
    t_index = int(min_gap * fps / 1000)
    for i in range(t):
        down = t_index * 1000 / fps
        up = (t_index + 1) * 1000 / fps
        t_index += 1
        gap_strs.append('(' + str(down) + ',' + str(up) + ']')
        gaps.append([down, up])
        times.append(0)
    v_index = 0
    for v in y_values:
        for k in range(len(gaps)):
            pair = gaps[k]
            if v > pair[0] and v < pair[1]:
                times[k] = times[k] + 1
                colors[v_index] = 2 * (k + 1) * (k + 1)
                if fps <= 60:
                    sizes[v_index] = (k + 1) * (k + 1) + 2
                else:
                    sizes[v_index] = k * (k**0.5) + 2
        v_index += 1
    for tt in times:
        ratios.append(int(tt * 100 / len(y_values)))

    traces = []
    trace_name = file_path.split('/')[-1].split('.')[0]
    traces.append(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines+markers',
            marker=dict(
                size=sizes,
                color=colors,
                colorscale='Viridis',  # one of plotly colorscales
                showscale=True),
            name=trace_name))
    layout = go.Layout(title=(trace_name + ' 耗时'),
                       xaxis=dict(title='当前时间戳(ms)'),
                       yaxis=dict(title='耗时时长(ms)'))
    fig = go.Figure(data=traces, layout=layout)
    py.plot(fig, filename=trace_name + '_duration0.html', auto_open=False)
    fichier_html_graphs.write("  <object data=\"" + trace_name +
                              '_duration0.html' +
                              "\" width=\"1600\" height=\"480\"></object>" +
                              "\n")

    print("最小耗时: ", min_gap)
    max_gap_idx = y_values.index(max_gap)
    print("最大耗时(idx+1={0}): {1}，发生在[{2}({3}) - {4}({5})]".format(
        max_gap_idx + 1, max_gap, total_values[max_gap_idx][0] - first_value,
        total_values[max_gap_idx][0],
        total_values[max_gap_idx][1] - first_value,
        total_values[max_gap_idx][1]))
    print("平均帧率: ", len(y_values) * 1000000 / total_duration)
    for i in range(len(times)):
        if times[i] > 0:
            print("{0}: {1}次，{2}% ".format(gap_strs[i], times[i], ratios[i]))

    trace1 = go.Bar(x=gap_strs, y=times, name='次数')
    trace2 = go.Scatter(x=gap_strs, y=ratios, name='占比(%)', yaxis='y2')
    l = go.Layout(title=(trace_name + ' 区间次数'),
                  yaxis=dict(title='次数'),
                  yaxis2=dict(title='占比 %', overlaying='y', side='right'))
    data = [trace1, trace2]
    fig2 = go.Figure(data=data, layout=l)
    py.plot(fig2, filename=trace_name + '_duration_bar.html', auto_open=False)
    fichier_html_graphs.write(" <object data=\"" + trace_name +
                              '_duration_bar.html' +
                              "\" width=\"650\" height=\"480\"></object>" +
                              "\n")

    return x_values, y_values


def main():
    print('处理耗时:', str(sys.argv[1]))
    filepath = sys.argv[1]
    trace_name = filepath.split('/')[-1].split('.')[0]
    fichier_html_graphs = open(trace_name + "_duration.html", 'w')
    fichier_html_graphs.write("<html><head></head><body>" + "\n")

    x_values, y_values = ReadFile(fichier_html_graphs, filepath)

    fichier_html_graphs.write("</body></html>")


if __name__ == "__main__":
    main()
