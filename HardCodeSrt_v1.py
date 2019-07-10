import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
#/usr/share/fonts/truetype/kacst/KacstTitleL.ttf
#/usr/share/fonts/truetype/fonts-arabeyes/ae_AlYarmook.ttf
import arabic_reshaper
# install: pip install python-bidi
from bidi.algorithm import get_display
# install: pip install Pillow
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import time
import os
import os.path



def draw_nonarabic(img,text):
	rows,cols,ch=img.shape
	fontFile="/usr/share/fonts/truetype/sahel/sahel.ttf"
	font = ImageFont.truetype(fontFile, 20)
	lines=text.splitlines()
	x_location=[]
	y_location=[]
	for x in range(len(lines)):
		text_width,text_height=font.getsize(lines[x])
		x_location.append((cols-text_width)//2)
		y_location.append(rows-text_height-55+x*35)
	for x in range(len(lines)):
		cv2.puText(img,lines[x],(x_location[x],y_location[x]),cv2.FONT_HERSHEY_SIMPLEX,20,(0,0,0))
	return img


def draw_arabic(img,text):
	rows,cols,ch=img.shape
	img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	img_pil = Image.fromarray(img)
	fontFile="sahel.ttf"
	font = ImageFont.truetype(fontFile, 20)

	lines=text.splitlines()
	bidi_text_arr=[]
	x_location=[]
	y_location=[]
	for x in range(len(lines)):
		text_width,text_height=font.getsize(lines[x])
		x_location.append((cols-text_width)//2)
		y_location.append(rows-text_height-55+x*35)
		#print(x_location,y_location)
		reshaped_text = arabic_reshaper.reshape(lines[x])    # correct its shape
		bidi_text = get_display(reshaped_text)# correct its direction
		bidi_text_arr.append(bidi_text)
	# start drawing on image
	draw = ImageDraw.Draw(img_pil)
		#draw.text((0, 0), bidi_text, (255,255,255), font=font)
	for x in range(len(bidi_text_arr)):
		draw.text((x_location[x], y_location[x]), bidi_text_arr[x], (0,0,0), font=font)
		
	draw = ImageDraw.Draw(img_pil)	
	img_np = np.asarray(img_pil)
	img_np = cv2.cvtColor(img_np,cv2.COLOR_RGB2BGR)
	return img_np


def convert_srt_time(srt_time):
	#00:00:21,661 --> 00:00:21,661
	srt_time_all=srt_time.split(' ')
	srttime=[]
	finish_time=[]
	srttime.append(srt_time_all[0])
	srttime.append(srt_time_all[2])

	for x in range(2):
		time1,time2=srttime[x].split(',')
		time11=time1[0:2]#hours
		time12=time1[3:5]#minutes
		time13=time1[6:]#seconds
		total_time_ms=(int(time11[0])*10*60*60+int(time11[1])*60*60 + int(time12[0])*10*60+int(time12[1])*60 + int(time13[0])*10+int(time13[1]))*1000
		total_time_ms=total_time_ms+int(time2)
		finish_time.append(total_time_ms)
		#print('new time:',total_time_ms)
	return finish_time

def get_srt_info(filename):
	#reader=open('chem1.srt','r')
	reader=open(filename,'r')
	lines=reader.readlines()
	blockstart=False
	srt_numbers=[]
	srt_time_ms_start=[]
	srt_time_ms_end=[]
	srt_text=[]
	text=''

	for x in range(len(lines)):
		if lines[x][0].isdigit() and int(lines[x][0])!=0 :#we enter block
			srt_num=lines[x]
			srt_numbers.append(int(srt_num))
			blockstart=True
		elif lines[x][0].isdigit() and int(lines[x][0])==0 :
			srt_start_time=lines[x]
			time_ms_all=convert_srt_time(srt_start_time)
			srt_time_ms_start.append(time_ms_all[0])
			srt_time_ms_end.append(time_ms_all[1])

		elif blockstart==True and len(lines[x])>1:
			text=text+lines[x]
		elif blockstart==True and len(lines[x])==1:
			blockstart=False
			srt_text.append(text)
			text=''
		else:
			pass

	reader.close()
	return srt_time_ms_start,srt_time_ms_end,srt_text


##########START HERE ###########################

srt_filename=input('plz input .srt filename:')
video_filename=input('plz input video file name:')

if not os.path.exists(srt_filename) or not os.path.exists(video_filename):
	print('Plz ensure both files exists in this directory!')

else:
	vname,vext=video_filename.split('.')
	split_audio_cmd='ffmpeg -i ' + video_filename + ' ' + vname +'.mp3'
	os.system(split_audio_cmd)
	print('Split Audio Success!')
	#print(merge_video_audio_cmd)
	srt_time_start,srt_time_end,srt_text=get_srt_info(srt_filename)	
	######save srtText.txt file#########
	fh=open(vname + 'SrtText.txt','w+')
	for i in range(len(srt_text)):
		fh.write(str(i) +'>' + srt_text[i])
	fh.close
	###################################
	cap=cv2.VideoCapture(video_filename)
	fps=cap.get(cv2.CAP_PROP_FPS)
	print('fps',fps)#then 1 frame needs 1/fps*1000ms in ms-seconds
	ret,frame=cap.read()
	rows,cols,ch=frame.shape
	frame_count=cap.get(cv2.CAP_PROP_FRAME_COUNT)
	print('frame_count:',frame_count)
	duration_seconds=frame_count/fps
	print('video duration seconds:',duration_seconds)
	duration_ms=duration_seconds*1000

	frame_counter=0
	srt_index=0

	# Define the codec and create VideoWriter object
	#fourcc=cv2.VideoWriter_fourcc(*'XVID')
	fourcc= cv2.VideoWriter_fourcc(*'mp4v')
	out = cv2.VideoWriter(vname + 'Silent.mp4',fourcc, fps, (int(cols),int(rows)))

	while (srt_index<len(srt_time_start)):
		ret,frame=cap.read()
		frame_counter=frame_counter+1
		time1=int(srt_time_start[srt_index])
		the_text=srt_text[srt_index]
		time2=int(srt_time_end[srt_index])
		if time1==time2:
			if srt_index<(len(srt_time_start)-1):
				text_duration=(srt_time_start[srt_index+1]-srt_time_start[srt_index]-500)
			else:
				text_duration=duration_ms-srt_time_start[srt_index]-500
		else:
			textduration=time2-time1

		current_frame_ms=frame_counter/fps*1000#in milliseconds
		#check if current frame is before or inside outside this current frame ms
		if current_frame_ms < time1:#just write normal frame
			out.write(frame)
		elif current_frame_ms >= time1 and current_frame_ms < (time1+text_duration):
			while True:
				firstchar=the_text[0]
				firstchar_int=ord(firstchar)

				if firstchar_int>=1536 and firstchar_int<=1919:#its arabic 
					#print('Its arabic!')
					frame=draw_arabic(frame,the_text)
				else:
					#print('Its not arabic!')
					frame=draw_nonarabic(frame,the_text)

				out.write(frame)
				ret,frame=cap.read()
				frame_counter=frame_counter+1
				current_frame_ms=frame_counter/fps*1000
				if current_frame_ms > (time1+text_duration):
					srt_index=srt_index+1
					print('srt_index',srt_index)
					break
		else:
			pass

	cap.release()
	out.release()
	cv2.destroyAllWindows()
	merge_video_audio_cmd='ffmpeg -i ' + vname + 'Silent.mp4 -i ' + vname + '.mp3 -shortest ' + vname + 'final.mp4'
	os.system(merge_video_audio_cmd)
	print('Merge Success!')
	print('Finished Successfully!')

	print('Srt file text only: ',end='')
	print(vname +'SrtText.txt')


	print('audio file: ',end='')
	print(vname +'.mp3')

	print('Video file with no audio: ',end='')
	print(vname +'Silent.mp4')

	print('Video file with merged srt file: ',end='')
	print(vname +'final.mp4')







