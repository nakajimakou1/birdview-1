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
[ WARN:0] global C:\projects\opencv-python\opencv\modules\videoio\src\cap_msmf.cpp (674) SourceReaderCB::~SourceReaderCB terminating async callback
[*] [array([[0., 0., 0.],
       [1., 0., 0.],
       [2., 0., 0.],
       [3., 0., 0.],
       [4., 0., 0.],
       [0., 1., 0.],
       [1., 1., 0.],
       [2., 1., 0.],
       [3., 1., 0.],
       [4., 1., 0.],
       [0., 2., 0.],
       [1., 2., 0.],
       [2., 2., 0.],
       [3., 2., 0.],
       [4., 2., 0.]], dtype=float32), array([[0., 0., 0.],
       [1., 0., 0.],
       [2., 0., 0.],
       [3., 0., 0.],
       [4., 0., 0.],
       [0., 1., 0.],
       [1., 1., 0.],
       [2., 1., 0.],
       [3., 1., 0.],
       [4., 1., 0.],
       [0., 2., 0.],
       [1., 2., 0.],
       [2., 2., 0.],
       [3., 2., 0.],
       [4., 2., 0.]], dtype=float32), array([[0., 0., 0.],
       [1., 0., 0.],
       [2., 0., 0.],
       [3., 0., 0.],
       [4., 0., 0.],
       [0., 1., 0.],
       [1., 1., 0.],
       [2., 1., 0.],
       [3., 1., 0.],
       [4., 1., 0.],
       [0., 2., 0.],
       [1., 2., 0.],
       [2., 2., 0.],
       [3., 2., 0.],
       [4., 2., 0.]], dtype=float32)] [array([[[432.0467 , 358.04938]],

       [[395.8199 , 361.14832]],

       [[359.16708, 362.77213]],

       [[322.86108, 363.2768 ]],

       [[288.27982, 362.23877]],

       [[428.57584, 323.8017 ]],

       [[394.20615, 326.42142]],

       [[358.81912, 328.1886 ]],

       [[324.08823, 329.1019 ]],

       [[290.63147, 329.34543]],

       [[424.7301 , 291.57837]],

       [[391.74182, 293.78442]],

       [[358.31937, 295.47256]],

       [[325.069  , 296.95602]],

       [[293.06238, 297.8999 ]]], dtype=float32), array([[[428.2235  , 172.29893 ]],

       [[390.39655 , 169.25801 ]],

       [[352.06805 , 167.2832  ]],

       [[312.8926  , 166.5359  ]],

       [[276.23578 , 166.62111 ]],

       [[431.17673 , 134.61296 ]],

       [[392.65067 , 131.1252  ]],

       [[352.32092 , 128.65228 ]],

       [[313.12927 , 128.67079 ]],

       [[274.33957 , 129.86815 ]],

       [[433.37375 ,  97.241425]],

       [[393.962   ,  92.57655 ]],

       [[353.77725 ,  90.61727 ]],

       [[312.68845 ,  90.58061 ]],

       [[274.1446  ,  93.338264]]], dtype=float32), array([[[301.71494, 304.70697]],

       [[342.2116 , 301.77542]],

       [[384.88617, 297.87405]],

       [[427.62247, 292.69144]],

       [[468.19836, 286.84775]],

       [[301.52875, 345.6771 ]],

       [[343.2932 , 344.46277]],

       [[387.76273, 341.21753]],

       [[431.8785 , 336.34854]],

       [[474.49432, 329.466  ]],

       [[301.28674, 387.394  ]],

       [[343.94766, 387.70023]],

       [[389.38785, 385.6941 ]],

       [[434.87988, 380.68478]],

       [[478.26364, 373.46033]]], dtype=float32)] (480, 640)
[[8.95841980e+02 0.00000000e+00 3.99142283e+02]
 [0.00000000e+00 1.12955554e+03 2.39982303e+02]
 [0.00000000e+00 0.00000000e+00 1.00000000e+00]]

'''
