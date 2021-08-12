import sys, time, os

CRT_RESOLUTION = True

input_paths = sys.argv
vid_filenames = []

for it in range(1, len(input_paths)):
	input_path = input_paths[it]

	if os.path.isdir(input_path):
		vid_directories = os.listdir(input_path)

		for directory in vid_directories:
			temp_path = os.path.join(input_path, directory)
			if os.path.isdir(temp_path):
				for file in os.listdir(temp_path):
					if not os.path.isdir(file):
						vid_filenames.append(os.path.join(temp_path, file))
			else:
				vid_filenames.append(temp_path)

	else:
		vid_filenames.append(input_path)


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
		os.system('ffmpeg -hide_banner -loglevel error -i \"' + vid_to_convert + '\" -vf scale=-2:\'min(480,ih)\' -c:v h264 -acodec ac3 \"' + os.path.join(converted_dir, new_filename) + '\"')
	else:
		os.system('ffmpeg -hide_banner -loglevel error -i \"' + vid_to_convert + '\" -c:v h264 -acodec ac3 \"' + os.path.join(converted_dir, new_filename) + '\"')
	
	vid_iterator += 1
