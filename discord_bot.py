from datetime import datetime
import requests
from dotenv import load_dotenv
import os
from firebase_db import ref

load_dotenv()

def push_message(fetched):
    message_content = ""
    message_content += '-'*100 + '\n'
    name = fetched.get('name', 'No name provided')
    starts_at = datetime.fromisoformat(fetched.get('starts_at')).strftime('%Y-%m-%d')
    ends_at = datetime.fromisoformat(fetched.get('ends_at')).strftime('%Y-%m-%d')
    reg_end = datetime.fromisoformat(fetched.get('reg_end')).strftime('%Y-%m-%d')
    reg_url = fetched.get('reg_url', 'No registration URL provided')
    
    reg_end_date = datetime.fromisoformat(fetched.get('reg_end'))
    days_left = (reg_end_date - datetime.now(reg_end_date.tzinfo)).days
    message_content += f"📛 **Name**: {name}\n"
    message_content += f"🗓️ **Starts At**: {starts_at}\n"
    message_content += f"🗓️ **Ends At**: {ends_at}\n"
    message_content += f"⏰ **Registration Ends At**: {reg_end}\n"
    message_content += f"🔗 **Registration URL**: {reg_url}\n"
    message_content += f"⏳ **Days Left for Registration**: {days_left} days\n"
 
    data = {
        "content": message_content
    }
    result = requests.post(os.getenv('WEBHOOK_URL'), json = data)
    return result.status_code



if __name__ == '__main__':
    prev_response = requests.get(os.getenv('DATABASE_URLS')).json()
    params = {
        'opportunity': 'hackathons',
        'page': 1,
        'per_page': '6',
        'oppstatus': 'open',
        'domain': '2',
        'course': '6',
        'specialization': 'Computer Science and Engineering',
        'usertype': 'students',
        'passingOutYear': '2028',
        'quickApply': 'true',
    }

    response = requests.get('https://unstop.com/api/public/opportunity/search-result', params=params)

    data = response.json()['data']['data']
    for i in data:
        flag = True
        for key, values in prev_response.items():
            if (values.get('id') == i.get('id')):
                flag = False
        if flag:
            hackathon = {
            'id': i.get('id'),
            'name': i.get('title') + ' - '+ i.get('organisation').get('name'),
            'starts_at': i.get('start_date'),
            'ends_at':i.get('end_date'),
            'reg_end': i.get('regnRequirements').get('end_regn_dt'),
            'reg_url': f'{i.get('seo_url')}'
            }
            if i.get('region') == "online":
                hackathon['is_online'] = True;
            ref.push(hackathon)
            status_code = push_message(hackathon)
            # print("Pushed!")