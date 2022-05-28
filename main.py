import jieba
import json
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

text = """
但凡是个普通人，都会对警察这个职业产生某种敬畏，李诗情也不例外。
在小时候大人们不住的用“你要做了坏事，警察叔叔就要把你抓走了哟”的吓唬下，从小到大，她连闯红灯、乱丢垃圾这样的错事都没做过。
所以，当这两位警察同志对她说出“李小姐，有一起交通事故，希望你能协助我们进行调查”时，李诗情整个人都是懵逼的。
"""
text_jb = jieba.lcut(text)
# print(' | '.join(text_jb))

# Remove new line characterss at beginning of array
if text_jb[0] == "\n":
    text_jb.pop(0)

# Make sure last element is a new line character for the loop to work properly
if text_jb[len(text_jb) - 1] != "\n":
    text_jb.append("\n")

# Create sub arrays for each line
split_lines = []
last_split = 0
for i in range(len(text_jb)):
    if text_jb[i] == "\n":
        split_lines.append(text_jb[last_split:i])
        last_split = i + 1

# print(split_lines)

# Cross reference HSK vocab
hsk_file = open('hsk.json')
hsk_vocab = json.load(hsk_file)

# Check to see if any HSK vocabulary in segmented text
# If match, replace the word with hsk entry
for sentence in split_lines:
    for i in range(len(sentence)):
        word = sentence[i]
        if word in hsk_vocab:
            sentence[i] = hsk_vocab[word]

# print(split_lines)

# API logic
app = FastAPI()

@app.get("/segmentor")
def segment_chinese():
    json_compatible_item_data = jsonable_encoder(split_lines)
    return JSONResponse(content=json_compatible_item_data)