import requests
import cv2 as cv
import base64


def vehicle_detect(img):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect"
    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image)
    params = {"image": base64_image}
    access_token = '24.d1da0a939b4fa66efc92ba6f039ef016.2592000.1722479243.282335-89935016'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)

    num = 0
    if response:
        data = response.json()
        #print("API返回的数据：", data)  # 打印API返回的数据进行调试

        if 'vehicle_num' in data:
            num = data['vehicle_num']['car']
        else:
            print("API返回的数据中没有'vehicle_num'键")

        if 'vehicle_info' in data:
            for item in data['vehicle_info']:
                location = item['location']
                x1 = location['left']
                y1 = location['top']
                x2 = x1 + location['width']
                y2 = y1 + location['height']
                cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                # 定义要绘制的文字
                text = item['type']
                position = (x1, y1 - 2)
                font = cv.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                color = (0, 0, 255)  # 红色
                thickness = 2
                img = cv.putText(img, text, position, font, font_scale, color, thickness, cv.LINE_AA)
    else:
        print("未收到API响应")

    return img, num
