import srt
import datetime

input_file = '22.01_lec3-2_example_edit.srt'
output_file = "intervals.txt"
prof = "MICHAEL SHORT"
other = "AUDIENCE"

current_speaker = None
current_interval = []
intervals = []
counter = 1

with open(input_file, "r") as f:
    data = f.read()
    gen = srt.parse(data, ignore_errors=False)
    for subtitle in gen:
        text = subtitle.content
        t_s = subtitle.start.seconds
        t_mus = subtitle.start.microseconds
        start = str(t_s) + "." + str(round(t_mus/1e6, 6)).split('.')[1]
        # unclear exactly when non-prof finishes talking, so end it
        # 1ms before the prof starts talking. Note that in the SRT file,
        # the start and end times of adjacent subtitles are the same.
        end = str(t_s) + "." + str(round((t_mus-1000)/1e6, 6)).split('.')[1]

        if other in text and len(current_interval) == 0:
            # start of a new interval
            current_interval.append(start)
            current_interval.extend([counter, str(datetime.timedelta(seconds=t_s))])
            current_speaker = other

        elif prof in text and current_speaker == other:
            # end of interval
            current_interval.append(end)
            intervals.append(tuple(current_interval + [counter, str(datetime.timedelta(seconds=t_s))]))
            current_interval = []
            current_speaker = prof
        counter += 1

for i in intervals:
    print(i)
# print(intervals)

# make argument to ffmpeg command
# command looks like
# ffmpeg -i test.mp4 -vcodec copy -af "volume=enable='between(t,5,10)+between(t,12,15)': volume=0" out.mp4

# all = []
# for start, end in intervals:
#     all.append('between(t,{},{})'.format(start, end))
# arg = '+'.join(all)
# print(arg)

# ffmpeg -i 22.01_lec3-2_example_edit.mp4 -vcodec copy -af "volume=enable='between(t,48.533,53.922)+between(t,74.383,77.567)+between(t,178.07,181.409)+between(t,183.74,184.951)+between(t,249.68,252.049)+between(t,285.958,289.987)+between(t,738.957,747.639)+between(t,822.855,829.936)+between(t,898.208,909.639)+between(t,1033.77,1047.326)+between(t,1185.607,1188.229)+between(t,1205.1,1209.089)': volume=0" edited.mp4

# with open(output_file, "w") as f:
#     for start, end in intervals:
#         f.write(start + " " + end + '\n')
