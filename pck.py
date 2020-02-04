import os
from flask import Flask, render_template, jsonify, redirect, url_for, request
from urlextract import URLExtract
from googleapiclient.discovery import build
from werkzeug.utils import secure_filename

#----------------------|  ASSIGNMENT  |--------------------------------
extractor = URLExtract()
my_api_key = "AIzaSyCaugQenN9PpH5I6agQTcFlkf8hbyAEOKw"
my_cse_id = "000757437883487112859:wtcjp5mwqmu"

app = Flask(__name__, template_folder = './')

#---------------------------------------------------------------------
# allow specific files
ALLOWED_FILES = set(['pdf', 'docx', 'odt', 'txt'])

def allowed_files(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_FILES

#--------------------------------------------------------------------------

# allow specific images
ALLOWED_IMAGES = set(['png', 'jpg', 'jpeg'])

def allowed_images(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGES

#--------------------|  HANDLERS  |------------------------------------

def google_search(search_term, api_key, cse_id, **kwargs):
    try:
          service = build("customsearch", "v1", developerKey=api_key)
          res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
          return res['items']
    except KeyError:
        return ['No match', 'No match', 'No match']

#---------------------------------------------------------------------
#txt = input('Please enter or paste text below:\n')	#file
#---------------------------------------------------------------------
# Function to open txt
def open_txt(filename,content):
     a = open(filename,'r');c = a.read();a.close();content = c

#---------------------------------------------------------------------
# Homepage
@app.route('/')
def homepage():
    return render_template('index.html')

# Handler for file upload -----------------------------
@app.route('/file', methods=['GET','POST'])
def filehandle():
    
    if request.method == 'POST':
        # check if file is present
        if 'myfile' not in request.files:
            return render_template('index.html', filename='Click to select file')
        # Store the file in the input
        myfile = request.files['myfile']
        # check if a file is selected
        if myfile.filename == '':
            return render_template('index.html', filename='No file selected')

        if myfile and allowed_files(myfile.filename):
            filename = secure_filename(myfile.filename)
            myfile.save(os.path.join('./',filename))
            # read the file
            with open(filename) as f:
                txt = f.read()
            # Handler length of words
            try:
                txt = ' '.join(txt.split()[0:50])
            except:
                txt = ' '.join(txt.split()[0::])
            # Handler for google search
            result = google_search(txt, my_api_key, my_cse_id, num=2)
            gen = list(result)
            # Getting things ready
            end_result = []
            probables = []
            for url in extractor.gen_urls(str(gen[0])):
                end_result.append(url)

            frequency = 1
            for all in end_result:
                if end_result[2] == all:
                    frequency=frequency+1   
            if frequency == 1: 
                frequency = '20%'
                comments = "A few words were found to be similar, this text doesn't seem to be plagirised.\nYou can try entering a longer length of text."
            elif frequency == 2:
                frequency = '40%'
                comments = "There is a high possibility of this text being plagiarised"
            elif frequency == 3:
                frequency = '60%'
                comments = "Our system detected a lot of plagiarised texts in your content"            
            elif frequency == 4:
                frequency = '80%'
                comments = "The text has most of it's contents plagiarised"
            elif frequency >= 5:
                frequency = '100%'
                comments = "Warning!! This text is plagiarised."
            #-------------------------------------------------------------------------------------------------------------------------------------------------frequency $ comments   ~~~~~~Done!
            for d in extractor.gen_urls(str(gen[0])):
                if d != end_result[2] and str(end_result[2]).find(str(extractor.gen_urls(str(gen[0])))) != 0:	
                    probables.append(all)
            probables = '\n'.join(probables)#-----------------------------------------------------------------------------------------------------------------probables    ~~~~~Done!
            # Check for valid result
            try:
                end_result = end_result[2]
                print(end_result)	#-------------------------------------------------------------------------------------------------------------------------end_result     ~~~~~~~~Done!
            except:
                end_result = "Some scrambled texts gotten, hence, no result found. \nPlease check your input and try again."
                frequency = '0%'	#-----------------------------exception 

            return render_template('index.html', frequency=frequency, comments=comments, probables=probables, end_result=end_result)
        
        else:
            return render_template('index.html', end_result="An error occured! Please check your file type and try again.")

    return render_template('index.html')


# Handler for text input -------------------------------------
@app.route('/text', methods=['GET','POST'])
def texthandle():
    # check if text is available
    if request.method == 'POST':
        if 'text' not in request.files:    
            return render_template('index.html')

        txt = request.form['text']

        try:
            txt = ' '.join(txt.split()[0:50])
        except:
            txt = ' '.join(txt.split()[0::])
        # Handler for google search
        result = google_search(txt, my_api_key, my_cse_id, num=2)
        gen = list(result)
        # Getting things ready
        end_result = []
        probables = []
        for url in extractor.gen_urls(str(gen[0])):
            end_result.append(url)

        frequency = 1
        for all in end_result:
            if end_result[2] == all:
                frequency=frequency+1   
            if frequency == 1: 
                frequency = '20%'
                comments = "A few words were found to be similar, this text doesn't seem to be plagirised.\nYou can try entering a longer length of text."
            elif frequency == 2:
                frequency = '40%'
                comments = "There is a high possibility of this text being plagiarised"
            elif frequency == 3:
                frequency = '60%'
                comments = "Our system detected a lot of plagiarised texts in your content"            
            elif frequency == 4:
                frequency = '80%'
                comments = "The text has most of it's contents plagiarised"
            elif frequency >= 5:
                frequency = '100%'
                comments = "Warning!! This text is plagiarised."
            #-------------------------------------------------------------------------------------------------------------------------------------------------frequency $ comments   ~~~~~~Done!
            for d in extractor.gen_urls(str(gen[0])):
                if d != end_result[2] and str(end_result[2]).find(str(extractor.gen_urls(str(gen[0])))) != 0:	
                    probables.append(all)
            probables = '\n'.join(probables)#-----------------------------------------------------------------------------------------------------------------probables    ~~~~~Done!
            # Check for valid result
            try:
                end_result = end_result[2]
                print(end_result)	#-------------------------------------------------------------------------------------------------------------------------end_result     ~~~~~~~~Done!
            except:
                end_result = "Some scrambled texts gotten, hence, no result found. \nPlease check your input and try again."
                frequency = '0%'	#-----------------------------exception 

            return render_template('index.html', frequency=frequency, comments=comments, probables=probables, end_result=end_result)

    return render_template('index.html')

    
if __name__ == '__main__':
    app.run()
