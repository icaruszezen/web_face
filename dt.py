import dlib
import cv2

def resize(img, width=None, height=None, inter=cv2.INTER_AREA):
    """
    initialize the dimensions of the input image and obtain
    the image size
    """

    dim = None
    (h, w) = img.shape[:2]

    if width is None and height is None:
        return img
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    # resize the image
    resized = cv2.resize(img, dim, interpolation=inter)
    # return the resized image
    return resized


def dt(frame_list):
    detector = dlib.get_frontal_face_detector()
    # 使用 detector 检测器来检测图像中的人脸
    img = frame_list.pop()
    img = resize(img, width=512)
    faces = detector(img, 1)
    print("人脸数 / Faces in all: ", len(faces))
    for i, d in enumerate(faces):
        w = d.right() - d.left()
        h = d.bottom() - d.top()
        d_left = int(d.left() - w * 0.25)
        d_right = int(d.right() + w * 0.25)
        d_top = int(d.top() - w * 0.70)
        d_bottom = int(d.bottom() + w * 0.2)
        # print("第", i + 1, "个人脸的矩形框坐标：",
        #       "left:", d_left, "right:", d_right, "top:", d_top, "bottom:", d_bottom)
        cv2.rectangle(img, tuple([d_left, d_top]), tuple([d_right, d_bottom]), (0, 255, 255), 2)
    if (len(faces) != 0):
        #cv2.imshow("img", img)
        #cv2.waitKey(0)
        #cv2.imwrite('./result.jpg', img)
        return True, img
    else:
        return False, img