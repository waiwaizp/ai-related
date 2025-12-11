import pytesseract
from PIL import Image
import pandas as pd

# Load the image from file
image_path = 'D:\\work\\python\\paddle\\nongfu2.png'
image = Image.open(image_path)

# Perform OCR on the image
ocr_result = pytesseract.image_to_string(image, lang='chi_sim')

# Split the result into lines
lines = ocr_result.split('\n')

# Initialize list to store the rows
table_data = []

# Manually define the column headers as extracted
columns = ["订单号", "订单类型", "订单金额", "优惠金额", "实际支付金额", "支付方式", "客户信息", "客户电话", "客户姓名", "下单时间", "操作"]

# Iterate through the lines and extract relevant data
for line in lines:
    if line.strip():
        row_data = line.split()
        if len(row_data) >= 11:
            # Join the excess columns in '客户信息'
            row = [
                row_data[0],  # 订单号
                row_data[1],  # 订单类型
                row_data[2],  # 订单金额
                row_data[3],  # 优惠金额
                row_data[4],  # 实际支付金额
                row_data[5],  # 支付方式
                " ".join(row_data[6:-5]),  # 客户信息
                row_data[-5],  # 客户电话
                row_data[-4],  # 客户姓名
                row_data[-3] + " " + row_data[-2],  # 下单时间
                row_data[-1]  # 操作
            ]
            table_data.append(row)

# Create a DataFrame
df = pd.DataFrame(table_data, columns=columns)

# Display the DataFrame
print(df)
