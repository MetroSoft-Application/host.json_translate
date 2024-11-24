import sys
import json
from collections import OrderedDict
from googletrans import Translator

def translate_dict(data, target_key, translator, target_lang):
    for key, value in data.items():
        if key == target_key and isinstance(value, str) and value is not None and value != "":
            print(f"Translating: {value}")
            translated_value = translator.translate(
                value, dest=target_lang).text
            if translated_value is not None:
                data[key] = translated_value
        elif isinstance(value, dict):
            translate_dict(value, target_key, translator, target_lang)
        elif isinstance(value, list):
            translate_list(value, target_key, translator, target_lang)

def translate_list(data, target_key, translator, target_lang):
    for item in data:
        if isinstance(item, dict):
            translate_dict(item, target_key, translator, target_lang)
        elif isinstance(item, list):
            translate_list(item, target_key, translator, target_lang)

def translate_json(input_file, output_file, target_key, target_lang='ja'):
    # JSONファイルを読み込む
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    # 翻訳オブジェクトを作成
    translator = Translator()

    # 指定されたキーの値を翻訳する
    if isinstance(data, dict):
        translate_dict(data, target_key, translator, target_lang)
    elif isinstance(data, list):
        translate_list(data, target_key, translator, target_lang)

    # 翻訳されたデータを新しいJSONファイルとして保存する
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=False)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = input_file.rsplit('.', 1)[0] + "_translated." + input_file.rsplit('.', 1)[1]
    target_key = "description"
    target_lang = 'ja'

    translate_json(input_file, output_file, target_key, target_lang)
