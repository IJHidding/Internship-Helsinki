import requests
import time
import argparse
import zipfile
import io
import json
#himport StringIO

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('job_id',
                    help='The job id from the cravat put.')
parser.add_argument('output_directory',
                    help='The output directory for the content of the zipfile')
args = parser.parse_args()
#inputfile = args.inputfile

time.sleep(360)
#inputfile = "/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/test_vcf.vcf"
#print(r.text) # contains the job status as a string.
r = requests.get('http://www.cravat.us/CRAVAT/rest/service/status',
                     params={'jobid': args.job_id})
status = json.loads(r.text)['status']
while status == "Running":
    r = requests.get('http://www.cravat.us/CRAVAT/rest/service/status',
                     params={'jobid': args.job_id})
    status = json.loads(r.text)['status']
    time.sleep(360)
    #status = r.text['status']

#if status == "Succes":
zip_file_url = json.loads(r.text)["resultfileurl"]
#r = requests.get(url, allow_redirects=True)
#download
r_file = requests.get(zip_file_url)
z = zipfile.ZipFile(io.BytesIO(r_file.content))
z.extractall(args.output_directory)

#3else:
# #   print("Something went wrong during vest annotation")
#    exit()

