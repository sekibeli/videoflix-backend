import subprocess


def convert_480p(source):
    new_file_name = source + '480p.mp4'
    # cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd720',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        new_file_name
    ]
    run = subprocess.run(cmd, capture_output=True)
    
    
    

def convert_720p(source):
        new_file_name = source + '720p.mp4'
        cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
        run = subprocess.run(cmd, capture_output=True)
