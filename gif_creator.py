#script to create gifs from videos
import gc
import psutil
import moviepy.editor
import os
import random
import fnmatch
import timeit
import time
import sys
outputs = []
directory = r'' #Directory of video files (needs slash at the end)
ext ="*mp4"
gif_outputs = []
gif_out = r''# Directory to save finished gifs to
completed_files=[]
filename = ''
prefix = 'test'#prefix for gif file title


def runEncode():
    global gid
    gid=0
    while gid < 5: #change to create more gifs
        try:
            getTitle()
            makeGif()
            gc.collect()
            gid+=1
        except KeyboardInterrupt:
            exit()

def getTitle():
    global filename
    filename = prefix+str(gid)

def makeGif():
    number_inputs = random.randint(3,10)
    inputs =[os.path.join(directory,f)for f in os.listdir(directory)if os.path.isfile(os.path.join(directory,f))and fnmatch.fnmatch(f,ext)]
    random_select = random.sample(inputs,number_inputs)
    clips=[]
    for i in random_select:
        clips.append(i)
        print(i)
    for o in clips:
        print(filename)
        gif_out_path = gif_out + filename+'.gif'
        gif = random.choice(clips)
        gif_clip = moviepy.editor.VideoFileClip(gif).resize((640,360))
        gif_length =10/number_inputs
        #select a random time point
        print('gif clip type is : ',type(gif_clip))
        start=round(random.uniform(0,gif_clip.duration-gif_length),2)
        if start-gif_length < 0: 
            while start-gif_length < 0:
                gif_length =random.uniform(3,gif_clip.duration)
        print('gif starts at', start)
        gif_end=start + gif_length # to make the clips a specific length change _ gif length to a time in seconds 
        print('gif  ends aT:',gif_end)
        #cut a subclip
        out_gif = gif_clip.subclip(start,gif_end)
        print('clip is ',out_gif.duration, ' in length')
        gif_outputs.append(out_gif)
        print('number of gifs in list is:', len(gif_outputs))
        gif_mix = moviepy.editor.concatenate_videoclips(gif_outputs)
        print('estimated gif time is: ',gif_mix.duration)
    print('Creating Gif')
    try:
        gif_mix.write_gif(gif_out_path,program='imageio',fps=10, fuzz=10)
    except KeyboardInterrupt:
        exit()
    print("Gif Created")
    completed_files.append(gif_out_path)
    gif_mix.close()

runEncode()

