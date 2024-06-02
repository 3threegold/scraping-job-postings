s = "daihfowindow.pageData = 今天天气很好 || {}"

# 找到切片位置的前后索引 find方法找字符出现的索引  24
star = s.find('window.pageData = ')+len("window.pageData = ")
end = s.find(" || {}")
print(s[star:end]) #左闭右开

