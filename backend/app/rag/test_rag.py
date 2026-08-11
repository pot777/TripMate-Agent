from .embedding import encode_text


text = "成都适合老人旅游的地方"


vector = encode_text(text)


print("vector length:")
print(len(vector))


print("first 10 values:")
print(vector[:10])