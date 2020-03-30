# Excel 파일을 만들기 위함
import pandas as pd

df = pd.read_json("./products.json")

writer = pd.ExcelWriter("products.xlsx")
df.to_excel(writer, "sheet1")
writer.save()