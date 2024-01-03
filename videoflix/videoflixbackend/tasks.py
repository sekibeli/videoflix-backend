import subprocess
import os


def convert_480p(source, output):
    print('hey convert_480p wird ausgeführt')

    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd480',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        output
    ]
    run = subprocess.run(cmd, capture_output=True)
  
    
    
    

def convert_720p(source, output):
           
        cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd720',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        output
    ]
        run = subprocess.run(cmd, capture_output=True)
