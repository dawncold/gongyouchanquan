import os
import os.path
import requests
from pyquery import PyQuery as pq
from lxml import etree

if not os.path.exists('var'):
    os.mkdir('var')

data_url = 'http://120.52.185.48/shh/portal/familyaudit/query_share.aspx'

resp = requests.get(data_url)
d = pq(etree.HTML(resp.content.decode('utf8')))
project_names = [name.strip() for name in d('#project_id option').map(lambda i, e: pq(e).text()) if name.strip()]
if not os.path.exists('var/projects'):
    with open('var/projects', 'w') as f:
        f.write('\n'.join(project_names))
else:
    with open('var/projects') as f:
        existing_projects = [line.strip() for line in f.readlines()]
    new_projects = set(project_names) - set(existing_projects)
    if new_projects:
        print(f"new projects found: {', '.join(new_projects)}")
    else:
        print('same as before')
