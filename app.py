from flask import Flask
from flask import request
from flask import  render_template, Response
import cv2
from flask import url_for
from dt import dt

frame_list = []  #存储视频流

class VideoCamera(object):
    def __init__(self):
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture("/dev/video0")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image= self.video.read()
        frame_list.append(image)
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


app = Flask(__name__)


@app.route('/')  # 主页
def index():
    return render_template('main.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen_res():
    while True:
        if(len(frame_list) != 0):
            t, img = dt(frame_list)
            ret1, jpeg1 = cv2.imencode('.jpg', img)
            frame = jpeg1.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_res')
def video_res():
    return Response(gen_res(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(threaded=True)


