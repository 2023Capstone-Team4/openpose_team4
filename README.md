# Team4 Openpose

자세 교정 온라인 공부 플랫폼

</br>

## 🔎자세교정 모델
사용자가 진행중인 스터디(캠스터디)에 참여하면 사용자와 다른 사용자가 학습하는 모습이 실시간으로 송출된다. 시스템은 다음의 일련의 과정을 통해 사용자의 자세가 올바른 상태로 유지될 수 있도록 한다. 사용자의 자세가 올바르지 않으면 사용자에게 자세 교정 경고를 준다.

<img src="https://github.com/2023Capstone-Team4/openpose_team4/assets/74875490/051f4436-ebb2-4ceb-92da-8dd930c1e5eb"  width="360" height="400"/>

자세 교정은 Human Pose Estimation을 위한 방법 중 OpenPose를 사용한다. OpenPose는 딥러닝 합성곱 신경망을 이용하여 이미지에서 신체를 특징하는 점들을 추론하고 관절을 이어주는 방식으로 자세를 분석하는 라이브러리이다. 데이터셋은 가장 대중적인 데이터셋 중 하나인 mpii를 사용한다.
사용자의 기울어진 자세를 판단할 수 있는 모델 개발을 목표로 한다. 사용자의 척추가 기울어진 상태면 올바르지 못한 자세로 판단하고, 척추가 곧은 상태면 바른 자세로 판단한다. 이때, 신체가 올바르게 인식되어야 시스템이 정상 동작할 수 있으므로 몸의 일부가 가려져 있거나 카메라 환경이 지나치게 어둡거나 밝은 경우를 고려해야 한다.

</br>

## 🔎알고리즘
자세 교정 모델에서 기울어진 자세를 판단하는 알고리즘은 다음과 같다.

![알고리즘 순서도_front](https://github.com/2023Capstone-Team4/openpose_team4/assets/74875490/beed149f-fb65-4374-b690-3baf00b20579)

</br>

![알고리즘_openpose](https://github.com/2023Capstone-Team4/openpose_team4/assets/74875490/835a9022-3b57-4c88-813d-590ada6c8e85)

① 이미지 프레임 수신
딥러닝 서버는 일정 시간 간격으로 이미지 프레임을 수신한다. 수신된 이미지 프레임은 학습 네트워크에 맞는 형식으로 전처리하기 위해 이미지를 블롭(blob) 형식으로 변환한다. 

② “Neck”과 “Chest” 신체부위 검출
자세교정 모델에서 척추의 기울어짐 정도를 파악하기 위해 MPII 데이터셋의 신체 부위 중 Neck과 Chest 값만을 추출해 사용한다. 

![image](https://github.com/2023Capstone-Team4/openpose_team4/assets/74875490/8e1f5ed9-b9c2-4af0-a910-b004774a7339)

⇒ 1: “Neck”, 14: “Chest”

③ 관절의 신뢰도 값 분석
OpenPose로 인식된 각각의 관절점들은 0~1 사이의 신뢰도 값을 가진다. 실험을 통해 본 캠스터디 환경에 적합한 임계값이라고 판단된 0.1 이상의 신뢰도를 가지는 관절점만을 분석 대상으로 한다. 이때, 분석에 필요한 Neck과 Chest관절의 신뢰도 값이 0.1을 넘지 못하면 분석을 진행하지 않는다.

④ “Neck”과 “Chest” 관절점의 x좌표 분석
실험을 통해 명백히 바른 자세와 기울어진 자세를 구분한다고 판단되는 20 을 기준으로 바른 자세와 기울어진 자세를 구분한다.

![image](https://github.com/2023Capstone-Team4/openpose_team4/assets/74875490/4e6c5ff5-bb89-4938-8c1d-7f8bc4c4c9be)

![image](https://github.com/2023Capstone-Team4/openpose_team4/assets/74875490/27b844ff-9e4a-4d7f-951c-5bdf31d3023e)

</br>

## 🔎실행 매뉴얼
1. Openpose 파일 다운받기
    
    https://github.com/CMU-Perceptual-Computing-Lab/openpose
    
    위 링크에서 파일을 다운받는다.(Download ZIP)
    ![image](https://github.com/2023Capstone-Team4/openpose_team4/assets/74875490/36d7c088-ce50-4381-b520-6c7d8cfcb4b3)


2. 파일을 압축해제 후, models 폴더의 getModels 파일 실행한다. 파일이 실행되면서 모델들이 다운로드 된다.
    ![image](https://github.com/2023Capstone-Team4/openpose_team4/assets/74875490/5dc5980a-773e-4c4e-85a0-e1b0c9cbf6aa)

3. 다운로드된 모델 중 pose_deploy_linevec_faster_4_stages.prototxt, pose_iter_160000.caffemodel을 사용한다. 해당 파일들을 실행파일과 같은 위치로 이동시킨다.
4. 실행파일을 실행한다.

</br>

## 🔎실행결과

![시연3_0527](https://github.com/2023Capstone-Team4/openpose_team4/assets/74875490/5fee600c-53f6-4b35-a7ca-723583eb1a2d)

