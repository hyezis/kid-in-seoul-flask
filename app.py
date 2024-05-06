from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import pymysql
import config

app = Flask(__name__)

conn = pymysql.connect(
    host=config.DB_CONFIG['host'], 
    port=3306, 
    user=config.DB_CONFIG['user'], 
    passwd=config.DB_CONFIG['passwd'], 
    db=config.DB_CONFIG['db'], 
    charset='utf8'
)
cursor = conn.cursor()

if __name__ == '__main__':
    app.run(debug=True)
