import cv2

# MPII에서 각 파트 번호, 선으로 연결될 POSE_PAIRS
BODY_PARTS = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                "Background": 15 }

POSE_PAIRS = [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]

protoFile = "pose_deploy_linevec_faster_4_stages.prototxt";
weightsFile = "pose_iter_160000.caffemodel";

# 위의 path에 있는 network 모델 불러오기
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile);

inputWidth=320;
inputHeight=240;
inputScale=1.0/255;

# network에 넣어주기
#open = cv2.imread("./open.jpg");
n=1
def getOpenPose(img):
    global n
    #frame=cv2.resize(img,dsize=(320,240),interpolation=cv2.INTER_AREA);
    frame=img;
    frameWidth =  img.shape[1];
    frameHeight = img.shape[0];
    inpBlob = cv2.dnn.blobFromImage(frame, inputScale, (inputWidth, inputHeight), (0, 0, 0), swapRB=False, crop=False)
    
    imgb=cv2.dnn.imagesFromBlob(inpBlob);

    # 결과 받아오기
    #net.setInput(cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0)));
    net.setInput(inpBlob);
    output = net.forward();

    # 키포인트 검출시 이미지에 그려줌
    points = []
    for i in range(0,15):
        # 해당 신체부위 신뢰도 얻음.
        probMap = output[0, i, :, :]

        # global 최대값 찾기
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        # 원래 이미지에 맞게 점 위치 변경
        x = (frameWidth * point[0]) / output.shape[3]
        y = (frameHeight * point[1]) / output.shape[2]

        # 키포인트 검출한 결과가 0.1보다 크면(검출한곳이 위 BODY_PARTS랑 맞는 부위면) points에 추가, 검출했는데 부위가 없으면 None으로    
        if prob > 0.1 :    
            cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 255), thickness=-1, lineType=cv2.FILLED) # circle(그릴곳, 원의 중심, 반지름, 색)
            cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, lineType=cv2.LINE_AA)
            points.append((int(x), int(y)))
        else :
            points.append(None)

    if points[1] and points[14]:
        cv2.line(frame, points[1], points[14], (0, 255, 0), 2)
        cv2.imwrite('./img/img'+str(n)+'.PNG', frame);
        n+=1
        if(points[1][0]-points[14][0]>=20):
            return "bad"
        else:
            return "good"
    return "neutral"

#getOpenPose(open);

"""# 분류 모델 API 개발

- API 기능 제공을 위해 Flask 프레임워크 사용

"""
import io
from flask import Flask, jsonify, request
from PIL import Image
import numpy as np

from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

def stringToRGB(base64_string):
    imgdata = base64.b64decode(base64_string)
    dataBytesIO = io.BytesIO(imgdata)
    image = Image.open(dataBytesIO)
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

@app.route('/hello')
def hello():
    return "hello"


@app.route('/', methods=['POST'])
def predict():
    data = request.get_json();
    class_name = getOpenPose(stringToRGB(data["data"]));
    return jsonify({'class_name': class_name});

app.run(port=5001)
