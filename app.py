import os
import re
from typing import List, Union, TextIO, Optional
from flask import Flask, request, abort, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def comnad_function(com: str, value: str, file_name: TextIO) -> Union[str, List]:
    if com == 'filter':
        return list(filter(lambda s: value in s, file_name))
    if com == 'map':
        return "\n".join(map(lambda s: s.split()[int(value) + 1], file_name))
    if com == 'limit':
        return list(file_name)[:int(value)]
    if com == 'unique':
        return list(set(file_name))
    if com == 'sort':
        is_rev = value == 'desc'
        return sorted(file_name, reverse=is_rev)
    if com == 'regex':
        regex: re.Pattern = re.compile(value)
        return list(filter(lambda s: regex.findall(s), file_name))


@app.route("/perform_query")
def perform_query():
    file_name: Optional[str] = request.json['file_name']
    com1: Optional[str] = request.json['com1']
    value1: Optional[str] = request.json['value1']
    com2: Optional[str] = request.json['com2']
    value2: Optional[str] = request.json['value2']
    if file_name is None or com1 is None or value1 is None:
        abort(400, "Неверный запрос")
    is_file = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(is_file):
        abort(400, 'file not found')
    with open(is_file, 'r') as file:
        result: Union[List, str, TextIO] = comnad_function(com1, value1, file)
        if com2 and value2:
            result = comnad_function(com2, value2, result)
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
