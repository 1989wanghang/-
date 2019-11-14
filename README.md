* trace.py: 将所有数据绘制到一张图上
* diff_last_time.py: 统计前后次时间间隔分布情况，并打印出平均帧率
* duration.py: 统计函数耗时分布情况，并打印出平均耗时；与diff_last_time.py结合方便确定过多的间隔是否由于函数耗时引起

使用方法：
``` shell
./trace.py pen_move.txt repaint_req.txt build_displaylist.txt draw_frame.txt swapbuffers.txt
./diff_last_time.py swapbuffers.txt
./duration.py swapbuffers.txt
```
