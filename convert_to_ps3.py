import sys, time, os

CRT_RESOLUTION = True

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
            add_files_from_paths(paths_list)
        else:
            vid_filenames.append(input_path)


add_files_from_paths(input_paths)


converted_dir = os.path.join(os.path.dirname(__file__), 'converted')
if not os.path.exists(converted_dir):
    os.makedirs(converted_dir)

vid_iterator = 1

for vid_to_convert in vid_filenames:
    filename = os.path.basename(vid_to_convert)
    print('CURRENT: ' + filename)
    new_filename = os.path.splitext(filename)[0] + '.mp4'

    print(str(vid_iterator) + '/' + str(len(vid_filenames)))
    if CRT_RESOLUTION:
        # Old
        # ffmpeg -hide_banner -loglevel error -i "test.mkv" -vf scale=-2:'min(480,ih)' -c:v h264 -acodec ac3 "converted\test.mp4"
        # New with subtitles
        # ffmpeg -hide_banner -loglevel error -i "breakingbad.mkv" -vf "scale=-2:'min(480,ih)', subtitles='breakingbad.mkv':si=0" -c:v libx264 -pix_fmt nv12 -acodec aac -b:a 192k -ac 2 -ar 44100 -af "aresample=async=1:min_hard_comp=0.100000:first_pts=0" -f mp4 "converted\breakingbad_subs.mp4"
        
        # Normal convert
        os.system('ffmpeg -hide_banner -loglevel error -i \"' + vid_to_convert + '\" -vf scale=-2:\'min(480,ih)\' -c:v libx264 -pix_fmt nv12 -acodec aac -b:a 192k -ac 2 -ar 44100 -af \"aresample=async=1:min_hard_comp=0.100000:first_pts=0\" -f mp4 \"' + os.path.join(converted_dir, new_filename) + '\"')
        
        # Burn first subtitle track in video (subtitles must be in video file)
        # command = 'ffmpeg -hide_banner -loglevel error -i \"' + vid_to_convert + '\" -vf \"scale=-2:\'min(480,ih)\', subtitles=\'' + vid_to_convert + '\':si=0\" -c:v libx264 -pix_fmt nv12 -acodec aac -b:a 192k -ac 2 -ar 44100 -af \"aresample=async=1:min_hard_comp=0.100000:first_pts=0\" -f mp4 \"' + os.path.join(converted_dir, new_filename) + '\"'
        #os.system(command)
    else:
        os.system('ffmpeg -hide_banner -loglevel error -i \"' + vid_to_convert + '\" -c:v libx264 -pix_fmt nv12 -acodec aac -b:a 192k -ac 2 -ar 44100 -af \"aresample=async=1:min_hard_comp=0.100000:first_pts=0\" -f mp4 \"' + os.path.join(converted_dir, new_filename) + '\"')
    

    vid_iterator += 1