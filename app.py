from flask import Flask, render_template, request, send_file, jsonify
# from ocr import pdf2images, mal_ocr
# import joblib
# from format import split_into_texts_custom
# from gpt4 import chatGPT_Trans
from totext import text_extraction

import threading
import glob
import re
from summa import summarize

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# lines = []
# comp_texts = []
pdf_path = None
fname = None
pdf_file = None
# textss = session.get('texts', '')
textss = ''
texts = []
paras = []
cancel_task = None
ocr_done = False

@app.context_processor
def inject_pdf_path():
    def pdf_path_get():
        global pdf_path
        return pdf_path
    return dict(pdf_path=pdf_path_get)

# @app.route('/getocr', methods=['GET'])
# def get_ocr():
#     convert_pdf()
#     global texts
#     textss = ''
#     for sent in texts:
#         textss += sent
#     return jsonify({"ocr_text": textss})

@app.route('/cancel_task', methods=['POST'])
def cancel():
    global cancel_task
    cancel_task = True
    return jsonify({'status': 'canceled', 'message': 'Task canceled'})

@app.route('/file_upload', methods=['POST'])
def upload():
    global pdf_path, pdf_file, fname
    pdf_file = request.files['pdf_file']

    pdf_file.save(f"static/documents/{pdf_file.filename}")
    pdf_path = f"static/documents/{pdf_file.filename}"
    fname = pdf_file.filename.rsplit('.', 1)[0]

    return jsonify({'status': 'success', 'message': 'File uploaded successfully', 'pdf_path':pdf_path})

@app.route('/doc_ocr', methods=['POST'])
def start_ocr():
    global cancel_task, textss, pdf_path, texts, paras
    cancel_task = False
    # ocr_thread = threading.Thread(target=convert_pdf)
    # ocr_thread.daemon = True
    # ocr_thread.start()
    # ocr_thread.join()
    convert_pdf()
    # print(textss,"**hi")
    txts = '\n'.join(paras)
    if ocr_done == True and cancel_task == False:
        return jsonify({'status': 'success', 'message': 'Text Extraction Successful','sentences':textss, 'sentences_list':paras, 'pdf_path':pdf_path})
    elif ocr_done == True and cancel_task == True:
        return jsonify({'status': 'success', 'message': 'Text Extraction partially Successful','texts':textss, 'pdf_path':pdf_path})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid pdf File'})



def convert_pdf():
    global pdf_path, textss, texts, fname, pdf_file, ocr_done, paras
    textss = ''
    # with open(pdf_file.filename, 'ren') as pdfn_file:
    #     print(pdfn_file)
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        # pages = pdf2images(pdf_file)

        # lines = []
        # ocr_textls = []
        # lnes = []

        directory = 'static/documents'
        pattern = directory + '/*.pdf'

        texts = []
        # file_list = []
        file_list = glob.glob(pattern)

        for file in file_list:
            texts += text_extraction(file)
            print(file)
        
        # for i in texts:
        #     print(i)

        print(len(texts))
        textss = '\n'.join(texts)
        paras = re.split(r'\r?\n\r?\n+', textss)
        # paras = textss.split('\n+')
        print(len(paras))
        for i,para in enumerate(paras):
            print(f"\nParagraph: {i}")
            print(para)

        def is_unimportant(sentence):
            unimportant_patterns = [r"Page \d+ of \d+"]
            rv = False
            for pattern in unimportant_patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    rv =  True
            return rv

        for i,p in enumerate(paras):
            tf = is_unimportant(p)
            words = p.split(" ")
            if tf and len(words)>25:
                # print("\nskipped\n", p, ':', tf)
                continue
            elif tf and len(words)<5:
                # print("\ndeleted\n", p, ':', tf)
                del paras[i]
            else:
                pass# print("\nskipped\n", p, ':', tf)

            for i,p in enumerate(paras):
                words = p.split(" ")
                if len(words)<5:
                    if i != len(paras)-1:
                        paras[i] += "\n" + paras[i+1]
                        del paras[i+1]
        textss = '\n'.join(paras)
        # print('**texts',textss, "**end")
        print(len(paras))
        ocr_done = True
        del file_list
    return

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    print(data)
    global paras
    summa = summarize(paras)
    return jsonify({'status': 'success', 'message': 'Translated Successfully', 'translated': summa})
    # with open('output.txt', 'w', encoding='utf-8') as text_file:
    #     text_file.write("\n".join(translated))

    # return send_file('output.txt', as_attachment=True, download_name=f'{fname}.txt')

# loc_path = None
# @app.route('/display')
# def display_pdf():
#     global pdf_path, loc_path
#     if pdf_path:
#         loc_path = pdf_path
#         pdf_path = None
#     else:
#         pdf_path = loc_path
#     return render_template('index.html')


if __name__ == '__main__':
    # import threading
    # ocr_thread = threading.Thread(target=convert_pdf)
    # ocr_thread.daemon = True
    # ocr_thread.start()

    app.run(debug=True)
