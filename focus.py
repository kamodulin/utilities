import time
from datetime import *
import re

hosts = '/private/etc/hosts'
localhost = '127.0.0.1'
urls = ['www.twitter.com', 'twitter.com']

# 'm.facebook.com', 'upload.facebook.com', 'apps.facebook.com', 'newsroom.fb.com', 'developers.facebook.com', 'touch.facebook.com', 'pixel.facebook.com', 'static.facebook.com', 'beta.facebook.com', 'graph.facebook.com', 'login.facebook.com', 'inyour.facebook.com', 'secure.facebook.com', 'latest.facebook.com'


def main():
    morning = 7
    evening = 17
    now = datetime.now()

    assert morning < evening, f'{morning} is not less than {evening}'
    
    working = morning < now.hour < evening

    if working:
      with open(hosts, "r+") as f:
        content = f.read()

        for url in urls:
            if url not in content:
                f.write(f'{localhost}	{url}\n')   

        print('Working hours activated')

    else:
        with open(hosts, "r+") as f:
            content = f.read()

            for url in urls:
                if url in content:
                    content = re.sub(f'{localhost}	{url}\n', '', content)

            f.seek(0)
            f.write(content)
            f.truncate()
            
        print('Working hours deactivated')

if __name__ == '__main__':
    main()