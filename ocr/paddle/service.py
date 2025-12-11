from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import io
from paddleocr import PaddleOCR
import os
from flask_cors import CORS
import re
# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # 打开图片文件
            img = Image.open(file)
            
            # 转换为灰度图像
            gray_img = img.convert('L')
            
            # 将图像转换为 numpy 数组
            img_array = np.array(gray_img)

            output = ""
            result = ocr.predict(img_array, cls=True)
            for idx in range(len(result)):
                res = result[idx]
                for line in res:
                    output += line[1][0] + '\n'
            # 检查图像数组的形状
            #shape = img_array.shape
            
            return jsonify({
                'message': 'Image processed successfully',
                'output': output,
                'total': get_total(output)
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'File processing failed'}), 500

def find_first_float(string):
    # 正则表达式模式，用于匹配浮点数
    pattern = r'[-+]?\d{1,3}(,\d{3})*(\.\d+)?'
    
    # 使用 re.search() 找到第一个匹配的浮点数
    match = re.search(pattern, string)
    
    # 如果找到了匹配的内容，返回匹配的浮点数
    if match:
        float_str = match.group().replace(',', '')
        return float(float_str)
    else:
        return None
    
def find_first_match_index(string, array):
    # 将数组中的元素连接成一个正则表达式模式
    pattern = '|'.join(map(re.escape, array))
    
    # 使用 re.search() 找到第一个匹配的元素
    match = re.search(pattern, string)
    
    # 如果找到了匹配的内容，返回匹配的起始索引
    if match:
        return match.start()
    else:
        return -1

def get_total(output:str):
    index = find_first_match_index(output, ["应收", "应付"])
    if index == -1:
        index = find_first_match_index(output, ["实付合计", "Total", "合计", "总计"])

    if index == -1:
        return None
    else:
        return find_first_float(output[index:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
