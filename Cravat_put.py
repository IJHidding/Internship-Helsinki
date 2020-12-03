import requests
import argparse
import json
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('inputfile', type=str,
                    help='The input file for annotation')
args = parser.parse_args()
inputfile = args.inputfile
#inputfile = "/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/test_vcf.vcf"
#print(inputfile)

r = requests.post('http://www.cravat.us/CRAVAT/rest/service/submit',
                  files={'inputfile': open(inputfile)},
                  data={'email': 'i.j.hidding@st.hanze.nl', 'analyses': 'CHASM;VEST',
                        'hg19': 'on', 'functionalannotation': "on"})
#print(r.text) # contains the submission result as a string. Check "status" field.

job_id = json.loads(r.text)['jobid']
print(job_id)
