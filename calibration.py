import cv2
import numpy as np
import json

def calibrate(device, frame_width, frame_height, filename):
    camera = cv2.VideoCapture(device)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    if camera.isOpened():
        pass
    else:
        print("can not open camera")


    # objp = np.zeros((7*7,3), np.float32)
    # objp = np.zeros((5*4,3), np.float32)
    objp = np.zeros((5*3,3), np.float32)
    # objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)
    # objp[:,:2] = np.mgrid[0:5,0:4].T.reshape(-1,2)
    objp[:,:2] = np.mgrid[0:5,0:3].T.reshape(-1,2)
    obj_points = []
    img_points = []
    img_names_undistort = []
    criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)


    timeF = 20
    pic_num=0
    c=1
    firstFrame = None
    while True:
        rval, frame = camera.read()
        print(frame.shape)
        cv2.imshow("S", frame)
        if c % timeF == 0:
            pic_num = pic_num+1
            # cv2.imwrite("frame" + str(c) + ".bmp", frame)
            size = frame.shape[:2]
            gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
            # ima = cv2.GaussianBlur(gray, (7,7), 8)
            # ima = cv2.GaussianBlur(gray, (5,4), 8)
            ima = cv2.GaussianBlur(gray, (5,3), 8)
            # ret, corners = cv2.findChessboardCorners(ima, (7,7), None)
            # ret, corners = cv2.findChessboardCorners(ima, (5,4), None)
            ret, corners = cv2.findChessboardCorners(ima, (5,3), None)
            if ret:
                obj_points.append(objp)
                # corners2 = cv2.cornerSubPix(gray, corners, (7,7), (-1,-1), criteria)
                # corners2 = cv2.cornerSubPix(gray, corners, (5,4), (-1,-1), criteria)
                corners2 = cv2.cornerSubPix(gray, corners, (5,3), (-1,-1), criteria)
                img_points.append(corners2)
        c = c + 1
        cv2.waitKey(1)
        if pic_num > 16:
            break

    camera.release()
    cv2.destroyAllWindows()

    print("[*]", obj_points, img_points, size)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)
    if ret:
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (frame_width, frame_height), 1, (frame_width, frame_height))
        print(newcameramtx)
        with open(filename, 'w') as json_file:
            json_file.write(json.dumps(
                {
                    'mtx': mtx.tolist(),
                    'dist': dist.tolist(),
                    'newcameramtx': newcameramtx.tolist()
                }
            ))



if __name__ == "__main__" :
    # calibrate(1, 640, 480, 'back.json')
    calibrate(0, 640, 480, 'back.json')

'''
 dtype=float32)] (480, 640)
[[8.95841980e+02 0.00000000e+00 3.99142283e+02]
 [0.00000000e+00 1.12955554e+03 2.39982303e+02]
 [0.00000000e+00 0.00000000e+00 1.00000000e+00]]

'''
