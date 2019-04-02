from PyPDF2.utils import readNonWhitespace
from flask import Flask,jsonify
from flask import *
from werkzeug import secure_filename
from docx import Document
import pandas as pd
import string
import os
import requests
import pycurl
from StringIO import StringIO
import certifi
import Utility.Word2numParser as wp
import re
import Processor as p
from flask import render_template
import sys
from flask_cors import CORS, cross_origin

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
# initializing a variable of Flask

app = Flask(__name__, static_url_path='',template_folder='templates')

app.config['CORS_HEADERS'] = 'CONTENT-TYPE'
cors = CORS(app, resources={r"/*": {"origins": "localhost"}},headers="Content-Type")


# decorating index function with the app.route
@app.route('/')
def index():
   print("Index")
   return render_template("index.html")

#
# @app.route('/templates/')
# def root():
#     return app.send_static_file('index1.html')

def options(self, *args, **kwargs):
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers[
        'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'



@app.route('/router', methods=['GET','POST','OPTIONS'])
def router():
   print("Router")
   word='liability'
   words=['liability','liable']
   #import Processor.Processor as pp
   #duration=pp.x
   print(request)
   f = request.files['file']
   print("File")
   #f.save((f.filename))
   doc=Document(f)
   print("Document")
   l = list()
   section = list()
   print("File"+str(f.filename))
   file="Output Documents\\"+str(f.filename)+".csv"
   sectionfile="OutputSection\\"+str(f.filename)+"_section.csv"
   for i, paragraphs in enumerate(doc.paragraphs):
      text = (paragraphs.text)
      text = ''.join(x for x in (text.encode('utf-8').decode('latin-1')) if x in string.printable)
      if str(text):
         l.append(str(text))
      if (str(text.lower()).__contains__(word)):    #if [s for s in (text.lower()).split() if any(xs in s for xs in words)]:
         section.append(str(text))
   d = pd.DataFrame(l)
   sectiondf = pd.DataFrame(section)
   sectiondf.to_csv(sectionfile)
   d.to_csv(file)

   ClassifierResponse = AIEngineIntegrator('1079',sectionfile)
   print("Classifier response", ClassifierResponse)

   NERintegration = AIEngineIntegrator('1041',sectionfile)

   print("NER integration", NERintegration)
   Data=formulateResponseforDuration(ClassifierResponse,NERintegration)





   # Data = {
   #         'Start_End':'StartEnd',
   #         'Gap_outcome': "outcome",
   #         'Response': "Response"
   #         }

   jsonOutput=json.dumps(Data)
   print(jsonOutput)
   return jsonOutput  #duration[0]


def AIEngineIntegrator(pipelineId,sectionfile):

    storage = StringIO()

    url = "https://aaie.accenture.com/aceapi/ace-pipeline-execution-service/execute/PipelineExecution/"
    filepath = sectionfile#'OutputSection\\liability_section.csv'
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    # c.setopt(c.HTTPHEADER, ['enctype : multipart/form-data', 'Content-Type: multipart/form-data'])

    c.setopt(c.USERPWD, '%s:%s' % ('ace', 'ace'))

    c.setopt(c.CAINFO, certifi.where())

    c.setopt(c.HTTPPOST, [('file', (c.FORM_FILE, filepath,
                                    c.FORM_CONTENTTYPE, 'multipart/form-data',
                                    )), ('ownerUserName', 's.b.karuppasamy'), ('ownerUserId', '130'),
                          ('executorUserName', 's.b.karuppasamy'), ('executorUserId', '130'), ('pipelineId',pipelineId ),
                          ('getStatusWithResponse', 'true'), ('input', ''), ('bulletHandler', 'true'),
                          ('extractText', 'true')

                          ])
    # writing output to storage NER '1041'
    c.setopt(c.WRITEFUNCTION, storage.write)
    c.perform()
    c.close()
    # Required content
    content = storage.getvalue()
    print content
    content_str = content.decode()
    data = json.loads(content_str)

    return data

def resolveDuration(duration):
    x=list()
    for word in re.split(' |-',duration):
        try:
            if word.isdigit():
                x.append(word)
            else:
                x.append(wp.words_to_num(word))
        except Exception as error:
            continue
    return x

def compareDuration(duration):
    ConfigPath = "C:\Enclave\Git projects\Text Analytics\CDAT Flask\CDAT Config.xlsx"
    ConfigTbl = pd.read_excel(ConfigPath)
    response = "No Gap"
    ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']
    StandardDuration = int(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Values"].values[0])
    if (duration != StandardDuration):
        response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Response"].values[0])
        reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Reason"].values[0])
        return "Gap Found", response,reason  #return True, response
    else:
        reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["PassingRemark"].values[0])
        return "No gap", response,reason #return False, response


def NoDuration():
    ConfigPath = "C:\Enclave\Git projects\Text Analytics\CDAT Flask\CDAT Config.xlsx"
    ConfigTbl = pd.read_excel(ConfigPath)
    response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["ResponseForNoValue"].values[0])
    reason=""
    return "No Duration", response,reason


def formulateResponseforDuration(ClassifierResponse,NERintegration):
    Confidence = (json.loads(((ClassifierResponse['finalOutPut']['finalString']))))['Confidence']
    print("Formulate Response for duration")
    Target = (json.loads(((ClassifierResponse['finalOutPut']['finalString']))))['Target']
    # duration="No duration"
    duration = "0"
    for i in range(NERintegration['finalOutPut']['finalList'].__len__()):
        if (NERintegration['finalOutPut']['finalList'][i]['nerDateOutput']):
            duration = (NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['nervalue'])
            sentence = (NERintegration['finalOutPut']['finalList'][i]['sentence'])
            start = int(NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['start'])
            end = int(NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['end'])
            Start_End = sentence  # [start-3:end+4]
    print('Confidence ' + Confidence)
    if duration==0:
        outcome, response,reason = NoDuration()
        print("Duration not found")
        Start_End="Nothing found"
    else:
        x = resolveDuration(duration)

        print('Duration found:' + str(x[0]))
        outcome, response,reason = compareDuration(int(x[0]))
        Start_End = ' '.join(str(Start_End).split(',')[1:])
    # Start_End=Start_End.split(',')[1:]

    print("Outcome Response", outcome, response,reason)

    #reason = 'Because of the mismatch in the duration of the liability we have categorized it as a gap'
                #'Duration': str(x[0]),
    Data = {
            'Confidence': Confidence,
            'Entity_start': start,
            'Entity_end': end,
            'Start_End': str(Start_End),
            'Gap_outcome': str(outcome),
            'Response': response,
            'Reason': reason
            }

    return Data





if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='127.0.0.1', port=5000)

#<img src="img/load.gif"  id="loader">
# alert(obj['Start_End']);
#       $("#outputBox").show();
#       $(".outputText").text(obj['Start_End']);
#       $(".feedbackHead").text(obj['Response']);
#       $(".gap").text(obj['Gap_outcome']);
#c=' '.join(str(txt).split(',')[1:])
