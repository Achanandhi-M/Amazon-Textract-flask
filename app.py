import boto3
import json
from flask import Flask, request, render_template


app = Flask(__name__)
s3 = boto3.client('s3')
s3_bucket = 'mydemobucket-7'


@app.route('/', methods=['GET'])
def index():
   return render_template('index.html')



@app.route('/upload', methods=['POST'])


def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            try:
                s3.upload_fileobj(file, s3_bucket, file.filename)

                textract_result, amount=process_textract(file.filename)
                return render_template('result.html',textract_result=textract_result,amount=amount)

            except Exception as e:
                return str(e)
        else:
            return 'No file selected'

#Textract Code

def process_textract(image_key):
    textract_client = boto3.client('textract')
    # image location print(image_key)
    
    response = textract_client.start_document_text_detection(
        DocumentLocation={'S3Object': {'Bucket': s3_bucket, 'Name': image_key}}
    )

    job_id = response['JobId']
    print(f"Textract JobId: {job_id}")

    while True:
        response = textract_client.get_document_text_detection(JobId=job_id)
        status = response['JobStatus']

        if status in ['SUCCEEDED', 'FAILED']:
            break

    # Check if the job was successful
    if status == 'SUCCEEDED':
        blocks = response['Blocks']

        for block in blocks:
            if block['BlockType'] == 'LINE':
                print(f"Detected text: {block['Text']}")
    else:
        print(f"Textract job failed with status: {status}")

    amount=calculate()
    return blocks, amount



def calculate():

    S_No= '00047796'
    totalunit=800
    unit=int(totalunit)

    if(S_No=='00047796'):
        print('You are Authenticated')

        if unit>500:
            amount=totalunit*8;
            return amount
        
        elif unit>=500 and unit <=100:
            amount=totalunit*6;
            return amount
        else:
            return 'No charge'
    else:
        print('Error')

   

if __name__ == '__main__':
    app.run(debug=True)