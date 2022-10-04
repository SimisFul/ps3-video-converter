import os
import sys
import time
import re

CRT_RESOLUTION = True
MAXIMUM_HEIGHT = 720
SUBTITLE_TRACK = 0
FONT_SIZE = 15


input_paths = sys.argv[1:]
vid_filenames = []

if len(input_paths) == 0:
    exit()


def add_files_from_paths(paths):
    for input_path in paths:
        paths_list = []
        # print(os.path.isdir(input_path))
        # print(paths)
        if os.path.isdir(input_path):
            for path in os.listdir(input_path):
                paths_list.append(os.path.join(input_path, path))
                # print(os.path.join(input_path, path))
                # input()
            add_files_from_paths(paths_list)
        else:
            vid_filenames.append(input_path)


add_files_from_paths(input_paths)

converted_dir = os.path.join(os.path.dirname(__file__), 'converted')
temporary_dir = os.path.join(converted_dir, 'temporary_files')

if not os.path.exists(converted_dir):
    os.makedirs(converted_dir)
    
if not os.path.exists(temporary_dir):
    os.makedirs(temporary_dir)

if os.path.exists(os.path.join(temporary_dir, 'subs.srt')):
    os.remove(os.path.join(temporary_dir, 'subs.srt'))

vid_iterator = 1

for vid_to_convert in vid_filenames:
    filename = os.path.basename(vid_to_convert)
    print('CURRENT: ' + filename)
    print(str(vid_iterator) + '/' + str(len(vid_filenames)))
    new_filename = os.path.splitext(filename)[0] + '.mp4'

    if SUBTITLE_TRACK is not None:
        subtitle_file_path = os.path.join(temporary_dir, 'subs.srt')
        command = 'ffmpeg -y -hide_banner -loglevel error -i \"' + vid_to_convert + '\" -map 0:s:' + str(SUBTITLE_TRACK) + ' ' + subtitle_file_path + '\"'
        os.system(command)

        with open(subtitle_file_path) as f:
            newText = re.sub(r'font face="(.*?)"', 'font face="Consolas"', f.read())

        with open(subtitle_file_path, "w") as f:
            f.write(newText)

    # Old
    # ffmpeg -hide_banner -loglevel error -i "test.mkv" -vf scale=-2:'min(480,ih)' -c:v h264 -acodec ac3 "converted\test.mp4"
    # New with subtitles
    # ffmpeg -hide_banner -loglevel error -i "breakingbad.mkv" -vf "scale=-2:'min(480,ih)', subtitles='breakingbad.mkv':si=0" -c:v libx264 -pix_fmt nv12 -acodec aac -b:a 192k -ac 2 -ar 44100 -af "aresample=async=1:min_hard_comp=0.100000:first_pts=0" -f mp4 "converted\breakingbad_subs.mp4"

    # Normal convert
    # os.system('ffmpeg -hide_banner -loglevel error -i \"' + vid_to_convert + '\" -vf scale=-2:\'min(480,ih)\' -c:v libx264 -pix_fmt nv12 -acodec aac -b:a 192k -ac 2 -ar 44100 -af \"aresample=async=1:min_hard_comp=0.100000:first_pts=0\" -f mp4 \"' + os.path.join(converted_dir, new_filename) + '\"')

    # Burn first subtitle track in video (subtitles must be in video file)
    #command = 'ffmpeg -y -hide_banner -loglevel error -i \"' + vid_to_convert + '\" -vf \"scale=-2:\'min(1080,ih)\', subtitles=' + subtitles_path + ':si=0:force_style=\'Fontname=Helvetica,Fontsize=15,BackColour=&H202020&,BorderStyle=1,Outline=0,Shadow=1\'\" -c:v libx264 -pix_fmt nv12 -acodec aac -b:a 192k -ac 2 -ar 44100 -af \"aresample=async=1:min_hard_comp=0.100000:first_pts=0\" -f mp4 \"' + os.path.join(
    #    converted_dir, new_filename) + '\"'

    command = 'ffmpeg -y -hide_banner -loglevel error -i \"' + vid_to_convert + '\" -vf \"scale=-2:\'min(' + str(MAXIMUM_HEIGHT) + ',ih)\', subtitles=converted/temporary_files/subs.srt:si=0:fontsdir=.:force_style=\'Fontname=Consolas,Fontsize=' + str(FONT_SIZE) + ',BackColour=&H202020&,BorderStyle=1,Outline=0,Shadow=1\'\" -c:v libx264 -pix_fmt nv12 -acodec aac -b:a 192k -ac 2 -ar 44100 -af \"aresample=async=1:min_hard_comp=0.100000:first_pts=0\" -f mp4 \"' + os.path.join(
        converted_dir, new_filename) + '\"'

    os.system(command)

    if os.path.exists(os.path.join(temporary_dir, 'subs.srt')):
        os.remove(os.path.join(temporary_dir, 'subs.srt'))

    vid_iterator += 1

os.removedirs(temporary_dir)
