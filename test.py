import httpx

headers = {
    "referer": "https://meirentu.cc/pic/263309270685.html"
}
res = httpx.get("https://cdn2.mmdb.cc/file/20220401/263291667412/0.jpg")
with open("0.jpg","wb")as f:
    f.write(res.content)

# print(res.status_code)