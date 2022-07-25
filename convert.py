import pandas as pd
import json
def getData(path,sheetName="",):
    data = pd.read_excel(path)
    return data
def saveJson(data,path):
    with open(path,'w') as f:
        f.write(data)
if __name__ == "__main__":
    excelData = getData("/Users/a111/Downloads/词汇表.xlsx",sheetName="Sheet1")
    jsonData= excelData.to_json(force_ascii=False)
    print(jsonData)
    saveJson(jsonData,"./wordsList.json")
