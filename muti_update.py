import json
import pymysql
import re
import time
from pymysql.converters import escape_string
coon = pymysql.connect(host='1.116.27.26', port=3306, user='root', passwd='LzyLyy', charset='utf8mb4', autocommit=True)
coon.select_db('rookie_word')
cur = coon.cursor()
def replaceFran(str):
    fr_en = [['é', 'e'], ['ê', 'e'], ['è', 'e'], ['ë', 'e'], ['à', 'a'], ['â', 'a'], ['ç', 'c'], ['î', 'i'], ['ï', 'i'],
             ['ô', 'o'], ['ù', 'u'], ['û', 'u'], ['ü', 'u'], ['ÿ', 'y']
             ]
    for i in fr_en:
        str = str.replace(i[0], i[1])
    return str
flag=0
file_list=['其他词汇/GRE_2.json','其他词汇/IELTSluan_2.json','其他词汇/SAT_2.json','其他词汇/TOEFL_2.json','六级词汇/CET6_2.json','六级词汇/CET6luan_1.json','专四专八词汇/Level4luan_1.json','专四专八词汇/Level4luan_2.json','专四专八词汇/Level8_1.json','专四专八词汇/Level8luan_2.json']
for file_path in file_list:
    print('当前正在更新'+file_path)
    file = open(file_path, 'r', encoding='utf-8')
    word_list = []
    for line in file.readlines():
        words = line.strip()
        word_json = json.loads(words)
        # 单词
        word = word_json['headWord']
        if(word=="tap"):
            flag=1
        if(flag==0):continue
        try:
            sentence = word_json['content']['word']['content']['sentence']['sentences']  # 例句
            sentence_list = []
            for se in sentence:
                enSe = se['sContent']
                enTrans = se['sCn']
                sen = str(enSe) + str(enTrans)
                sentence_list.append(sen)
            # 例句资源sentence_res
            sentence_res = ''
            if (len(sentence_list) >= 3):
                for i in range(3):
                    sentence_res += str(sentence_list[i]) + ' | ' if (i < 2) else str(sentence_list[i])
            else:
                for l in range(len(sentence_list)):
                    sentence_res += str(sentence_list[l]) + ' | ' if (l == len(sentence_list)) else str(
                        sentence_list[l])
        except:
            sentence_res = ''
        try:
            phrase = word_json['content']['word']['content']['phrase']['phrases']
            # 短语资源pharse_re
            phrase_re = ''
            if (len(phrase) >= 4):
                for ph in range(4):
                    ph_content = phrase[ph]['pContent']
                    ph_cn = phrase[ph]['pCn']
                    phrase_re += (str(ph_content) + ' ' + str(ph_cn)) + ' | ' if ph < 3 else (
                            str(ph_content) + ' ' + str(ph_cn))
            else:
                for ph in range(len(phrase)):
                    ph_content = phrase[ph]['pContent']
                    ph_cn = phrase[ph]['pCn']
                    phrase_re += (str(ph_content) + ' ' + str(ph_cn)) if ph < len(phrase) - 1 else (
                            str(ph_content) + ' ' + str(ph_cn) + ' | ')
        except:
            phrase_re = ''
        trans = word_json['content']['word']['content']['trans']  # 释义
        # 释义资源
        trans_re = ''
        for tr in range(len(trans)):
            try:
                pos = trans[tr]['pos']
            except:
                pos = ''
            tranCn = trans[tr]['tranCn']
            try:
                tranOther = trans[tr]['tranOther']
            except:
                tranOther = ''
            trans_re += (str(pos) + ' ' + str(tranCn) + ' ' + str(tranOther)) if tr < len(trans) - 1 else (
                    str(pos) + ' ' + str(tranCn) + ' ' + str(tranOther) + ' | ')

        # 释义
        trans_re = replaceFran(trans_re)
        # 例句
        sentence_res = replaceFran(sentence_res)
        # 短语
        phrase_re = replaceFran(phrase_re)
        # print(word_json['wordRank'])
        # print('单词：'+word)
        # print('例句：' + sentence_res)
        # print('音标：' + str(pronounce))
        # print('短语：' + phrase_re)
        # print('释义：' + trans_re)
        sql_word = 'UPDATE word SET explain_word= %s,sentence= %s,other= %s WHERE word= %s'
        cur.execute(sql_word, [trans_re, sentence_res, phrase_re, word])
        coon.commit()
        time.sleep(0.1)
        print('单词：' + word + ' 已更新')

