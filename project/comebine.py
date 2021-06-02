import pandas as pd

with open('input/file_path.txt', 'r') as f:
    for file in f.readlines():
        file = file.strip('\n')
        y = 'input/' + file
        x = 'output/' + file

        print(x)
        data1 = pd.read_csv(x, encoding='utf-8', header=None)
        with open(y, 'r', encoding='gb18030', errors='ignore') as f:
            data2 = pd.read_csv(f)

        try:
            data2.loc[data1[0].values - 1, 'lng'] = data1[1].values
            data2.loc[data1[0].values - 1, 'lat'] = data1[2].values
        except Exception as e:
            print(y, '请重新解析经纬度...')
            print('原因：', e)

        try:
            data2 = data2[['投递日期','邮件号','业务种类','重量','投递机构','投递员','道段','投递地址','投递方式','lng','lat']]
        except:
            data2 = data2.rename(columns={'收寄日期': '投递日期', '收寄机构代码': '投递机构', '揽收员': '投递员', '地址': '投递地址', '大客户代码': '客户号'})
            data2 = data2[['投递日期','邮件号','业务种类','重量','投递机构','投递员','投递地址','客户号','lng','lat']]
        
        data2.to_csv(x, index=False, encoding='gb18030')
        print('成功生成包含经纬度的记录文件: %s' % file)