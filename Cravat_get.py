import requests
inputfile = "/Users/iwanhidding/Internship_Helsinki_2020_2021/installed_tools/test_vcf.vcf"


r = requests.post('http://www.cravat.us/CRAVAT/rest/service/submit',
                  files={'inputfile': open(inputfile)},
                  data={'email': 'i.j.hidding@st.hanze.nl', 'analyses': 'CHASM'})
r.text # contains the submission result as a string. Check "status" field.

#r = requests.get('http://www.cravat.us/CRAVAT/rest/service/submit',
#                 params={'email': 'test@test.com', 'analyses': '',
#                 'mutations': 'TR1 chr22 30025797 + A T sample_1'})
#r.text # contains the submission result as a string. Check "status" field.

r = requests.get('http://www.cravat.us/CRAVAT/rest/service/status',
                 params={'jobid':'test_20170315_103245'})
r.text # contains the job status as a string.