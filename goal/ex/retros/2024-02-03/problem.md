# 문제
main.cpp를 분석하고
scan(), result() 함수를 작성하여 gTotalCost 를 최소화 하시오.

- 방안에는 적어도 한대 이상의 기기가 존재한다.
- 주어지는 맵의 마주보는 벽과 벽사이 공간의 수는 10 이상이 되도록 주어진다.
- 벽에 부딛치지 않고 탐지 가능한 장치들 끼리 연결하면
  같은 방에 있는 모든 장치끼리는 연결됨을 보장한다.

## 제한 사항
- 메모리 : heap + global + stack = 256MB    단, stack size = 1MB
- 제한시간 10초
- 제출 횟수 제한 10회

## 주의 사항
- User Code 안에는  malloc.h 외에 어떤 헤더파일도 추가할 수 없다.
- 채점시 main.cpp 는 그대로 사용된다.
- 제출한 코드에 대하여 엄격한 코드 리뷰를 실시한다.
따라서 main.cpp의 변수에 직접 접근할 수 없다.
- 본 검정은 c++만 지원한다.

## API
user.cpp에서 구현해야 하는 API함수는 다음과 같다.

### void scan( int mDevicedId, int mTotalDevice )
- 룸별 장치를 찾는 함수이다.
- mDevicedId 는 mTotalDevice 개의 장치중 하나의 아이디이다.
- mTotalDevice 는 전체 장치수 이다.

### void result( int mDeviceIds[][MAX_DEVICE] )
- 룸별 장치 id를 찾은 결과를 mDeviceIds[][MAX_DEVICE] 에 저장하여 반환한다.
- 룸별 장치 id는 오름차순으로 정렬되어야 한다.
- 룸은 룸별 첫 장치 id의 오름차순으로 정렬되어야 한다.
보다 자세한 것은 main.cpp를 분석하여 알 수 있다.

main.cpp에서 제공하는 API함수는 다음과 같다.

### int scan_device( int mDevicedId, int mScanPower, DetectedDevice mDetected[] )
- mScanPower로 찾을 수 있는 장치를 mDetected[] 에 담고 그 개수를 돌려준다.
- 보다 자세한 것은 main.cpp를 분석하여 알 수 있다.
