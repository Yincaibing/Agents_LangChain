import cv2
import pandas as pd
import pytesseract

# 1. 读取图片
img = cv2.imread('1435.jpg')

# 2. 使用pytesseract进行OCR识别
text = pytesseract.image_to_string(img)

# 3. 对文本进行预处理，将其转为表格的形式
lines = text.split('\n')  # 根据换行符进行分割
snippets = [s for s in lines if s.strip() != '']  # 删除空行

table_data = []
for snippet in snippets:
    row = snippet.split(' ')  # 根据空格进行分割
    table_data.append(row)

# 4. 使用pandas库将数据转存为excel文件
df = pd.DataFrame(table_data)
df.to_excel('table.xlsx', index=False, header=False)