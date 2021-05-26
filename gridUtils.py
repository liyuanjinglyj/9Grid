import os
import cv2
import imageio
import moviepy.editor as mp


# 生成9宫格视频
def gird9_Video(srcVideoFileName, outputVideoFilename):
    cap = cv2.VideoCapture(srcVideoFileName)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videoWriter = cv2.VideoWriter(outputVideoFilename + ".avi", fourcc, fps, (width, height))
    i = 1
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            cv2.line(frame, (0, int(height / 3)), (width, int(height / 3)), (255, 255, 255), 3)
            cv2.line(frame, (0, int(height / 3 * 2)), (width, int(height / 3 * 2)), (255, 255, 255), 3)
            cv2.line(frame, (int(width / 3), 0), (int(width / 3), height), (255, 255, 255), 3)
            cv2.line(frame, (int(width / 3 * 2), 0), (int(width / 3 * 2), height), (255, 255, 255), 3)
            videoWriter.write(frame)
        else:
            break
    cap.release()


# 生成9宫格图片
def grid9_image(imageFileName):
    if not os.path.exists('image'):
        os.makedirs('image')
    image = cv2.imread(imageFileName, 1)
    height, width, n = image.shape
    if width >= height:
        image = cv2.resize(image, (width, width))
        height=width
    else:
        image = cv2.resize(image, (height, height))
        width = height
    height = int(height / 3)
    width = int(width / 3)
    x = 1
    for i in range(0, 3):
        for j in range(0, 3):
            print(i * height, height * (i + 1), j * width, width * (j + 1))
            result = image[i * height:height * (i + 1), j * width:width * (j + 1)]
            print('image/' + str(x) + ".png")
            cv2.imwrite('image/' + str(x) + ".png", result)
            x += 1


# 短视频生成9宫格动图
def grid9_gif(srcVideoFileName):
    if not os.path.exists('gif'):
        os.makedirs('gif')
    all_frames = []
    cap = cv2.VideoCapture(srcVideoFileName)
    fps = cap.get(cv2.CAP_PROP_FPS)
    for i in range(9):
        list = []
        all_frames.append(list)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            height, width, n = frame.shape
            if width >= height:
                frame = cv2.resize(frame, (width, width))
                height = width
            else:
                frame = cv2.resize(frame, (height, height))
                width = height
            height = int(height / 3)
            width = int(width / 3)
            frame_list = []
            for i in range(0, 3):
                for j in range(0, 3):
                    result = frame[i * height:height * (i + 1), j * width:width * (j + 1)]
                    frame_list.append(result)
            for index, image in zip(range(9), frame_list):
                all_frames[index].append(image)
        else:
            break
    for index, frames in zip(range(9), all_frames):
        imageio.mimsave("gif/" + str(index + 1) + ".gif", frames, 'GIF', duration=float(1 / fps))
    cap.release()


# GIF生成9宫格动图
def grid9_gif2(srcGIFFileName):
    clip = mp.VideoFileClip(srcGIFFileName)
    clip.write_videofile("gifVideo.mp4")
    grid9_gif('gifVideo.mp4')
