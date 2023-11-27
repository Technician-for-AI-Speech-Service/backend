# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 17:23:57 2022

@author: user
"""


from flask import Flask , request, render_template,jsonify
from flask import render_template
import evaluate
import os
import socket
import pathlib
try: 
        
    if not os.path.exists('./test_files/'):
        os.makedirs('./test_files/')
except OSError: 
        print("Error: Failed to create the directory.")
app = Flask(__name__)


@app.route("/stt", methods=['GET','POST'])
def uploads():
  
   return render_template('test.html', transcript="데이터를 업로드 해주세요")
   

@app.route("/stt/result", methods=['GET','POST'])
def results():
   if request.method == 'POST':    
       #file = request.form.get('file')
       f = request.files['file']
       f.save('./test_files/'+f.filename)
       
       predict = evaluate.mains('./test_files/'+f.filename)
       #prediction = model.model_classification(path_+"\\testdata\\"+f.filename)
       #return render_template('index.html', label=label)
       return render_template('test2.html', filename =f.filename, transcript=predict[0])
  
if __name__ == "__main__":

   app.run(host='0.0.0.0', port=80)