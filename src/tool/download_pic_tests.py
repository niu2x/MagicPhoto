import urllib
data = urllib.urlopen("http://image.baidu.com/detail/newindex?col=%E6%98%8E%E6%98%9F&tag=%E6%98%8E%E6%98%9F%E5%86%99%E7%9C%9F&pn=3&pid=14038810817&aid=&user_id=700357451&setid=29716&sort=0&ftag1=&ftag2=&from=1").read()
print data
