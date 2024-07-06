import requests
import cv2 as cv
import base64

def car_recognition(img):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/car"

    # 将图像编码成 JPEG 格式，并转化为 base64 编码格式
    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image)

    # 构建请求参数
    params = {"image": base64_image, "top_num": 5}
    access_token = '24.d1da0a939b4fa66efc92ba6f039ef016.2592000.1722479243.282335-89935016'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    # 发送请求
    response = requests.post(request_url, data=params, headers=headers)
    brand, score, year = '', 0, 0  # 初始化三个变量
    if response:
        data = response.json()
        print("API Response: ", data)  # 输出 API 返回的 JSON 数据以调试

        # 解析车辆信息并绘制矩形框和品牌型号文字
        location = data.get('location_result', {})
        if location:
            x1 = location['left']
            y1 = location['top']
            x2 = x1 + location['width']
            y2 = y1 + location['height']
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # 提取品牌、分数和年份
        if 'result' in data and len(data['result']) > 0:
            item = data['result'][0]  # 取第一个识别结果
            brand = item['name']
            score = int(item['score'] * 100)  # 将分数转换为整型
            year_str = item['year']
            if '-' in year_str:
                year = int(year_str.split('-')[0])  # 取年份范围的第一个年份
            else:
                year = int(year_str)

            # 绘制品牌型号文字
            brand_model = f"{brand} ({score}%)"
            text_position = (x1, y1 - 10)  # 调整文字位置以适应矩形框上方
            cv.putText(img, brand_model, text_position, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)

    return img, brand, score, year

# 测试代码，假设 img 是已经读取的图像
# img_path = 'C:/Users/HP/PycharmProjects/Project1/data/image2.jpg'  # 使用绝对路径
# img = cv.imread(img_path)
# if img is None:
#     print("Error: Unable to load image.")
# else:
#     result_img, brand, score, year = car_recognition(img)
#     print(f"Brand: {brand}, Score: {score}, Year: {year}")
#     # 检查变量值
#     print(f"Processed Image: {result_img is not None}")
#     cv.imshow('Car Recognition', result_img)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
