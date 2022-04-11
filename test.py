from requests import get, post, delete

# print(get('http://128.0.0.1:5000/api/news').json())
print(delete('http://localhost:5000/api/news/1').json())
# print(get('http://127.0.0.1:5000/api/news/999').json())