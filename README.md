# 텀블러 측면 사진을 이용한 용량 측정

> 2022-01 인간컴퓨터상호작용시스템 팀 프로젝트 2조

### 컴퓨터 비전의 영역

1. Classification
2. Object Detection
3. Image Segmentation
4. Visual relationship

### 프로세스

1. 가이드 박스를 이용한 입력 이미지 촬영
2. 이미지에서 텀블러 추출
   - otsu binarization -> find contours -> draw big contours(with filled option)
   - 
