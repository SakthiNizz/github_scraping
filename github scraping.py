import urllib.request		
import requests
from bs4 import BeautifulSoup
import re
import time
from requests.exceptions import Timeout
from this import s
import googlesearch
import pandas
import html5lib
from datetime import datetime
import os

#Here some default content 
company_default = "tesla"
keyword_default = "password"
cookies_default =  "_octo=GH1.1.987531735.1656583239; _device_id=51b7d16ba1ec0c491d50056232fdb9fc; preferred_color_mode=light; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; user_session=4PeQnC_g2q7162ea0-XKb5YgIL-DBswSXHlv2qu7vpVyK17-; __Host-user_session_same_site=4PeQnC_g2q7162ea0-XKb5YgIL-DBswSXHlv2qu7vpVyK17-; logged_in=yes; dotcom_user=SakthiNizzz; tz=Asia%2FCalcutta; has_recent_activity=1; _gh_sess=OL%2F0R8ogNSoAQP6z84l5WBxqY9cp9eaQXmTeS6SNeBUwgCHZ66uwB6ZsnUAmUUoA%2BkhZ%2F5nC1MGw4lYCygebcYfBUTXxrzC%2F%2FX%2FVooLAoCgHWzFZ5%2FoIfsAi89mGJLv%2FpgncxFzftw6gXqjTRtWHfod%2FRZqNSXaQv5xz8us32xrOYCjc3oes5KcrvlEi6a2vylXIinYB4j7101S0QUxzVI%2Fi3DWITsWKFH81xjrNfq63%2B7swOsrTXxL4mbTUip93DDLPadhFJ3Z9Kr9Rwv5Z5TpI6frYmyV9QYQpog%3D%3D--stBmuayeAj32CCDp--L6yyXMrgD2OcLCw7o3n%2Fsg%3D%3D"

#enter domain and key_value that want to search
print("Please press 'ENTER' to accept default values ")
company= input(f"Enter the company name [{company_default}]: ") or company_default
keyword= input(f"Enter the Keyword [{keyword_default}]: ") or keyword_default
#Copy paste the cookies which capture from Burp Suite
cookie_str = input(f"enter the cookie as string [Press 'ENTER' for default]: ") or cookies_default
#Convert input as json format
cookie_str = re.split('=|;',cookie_str)
cookie_key = cookie_str[::2]
cookie_value = cookie_str[1::2]
cookies = {}
for i in range(0,len(cookie_key)):
    cookies[cookie_key[i]] = cookie_value[i]
# print(cookies)#=>To see how cookie converted into json variable

url =f'https://github.com/search?p=1&q={company}+{keyword}&type=code'
header = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}
page = requests.get(url, cookies=cookies, headers=header)
content = page.content
soup = BeautifulSoup(content, "html5lib")
# print(soup)
org = soup.find('em').get_attribute_list('data-total-pages')
x = int(org[0])#=>Finding total pages of the domain.
print(f"Total number of pages available in {company} is : {x}")
g = 1
a = input(f"Enter Starting page [{g}] : ") or g
b = input(f"Enter ending page [{x}]: ") or x
a= int(a)
b= int(b)
now = datetime.now()
dt_tm = now.strftime("%d_%m_%Y&%H_%M_%S")
dt= now.strftime("%d/%m/%Y")
tm = now.strftime("%H:%M:%S")
# print("date and time =", dt_tm)
c = []
d = []
final_op = []
for y in range(a,b+1):
    # if y%20==0:
    #     cookie_str = input(f"enter the fresh cookie as string : ")
    #     cookie_str = re.split('=|;',cookie_str)
    #     cookie_key = cookie_str[::2]
    #     cookie_value = cookie_str[1::2]
    #     cookies = {}
    #     for i in range(0,len(cookie_key)):
    #         cookies[cookie_key[i]] = cookie_value[i]
        
    
    url =f'https://github.com/search?p={y}&q={company}+{keyword}&type=code'
    print("------------------------------------------------------------------------------------")
    print(url)
    print ("-----------------------------------------------------------------------------------")
    header = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}
    try: 
        my_request = requests.get(url, cookies=cookies, headers=header, verify=False, timeout=20) 
    except Timeout:
        print('Timeout has been raised.')
    res = str(my_request.content)
    # def fetch(res):
    #     soup = BeautifulSoup(res)
    #     return soup
    # soup = fetch(res)
    soup = BeautifulSoup(res, "html5lib")
    soup = soup.prettify()
    soup = re.split('"url":|},"originating_url":',soup)
    count = len(soup)
    # print(count)#=>Enable if you want to know the count of link after spliting.
    filtered_list =[]
    for i in range(1,count,2):
        filtered_list.append(soup[i])
    c.append(filtered_list)
    semi_filter = []
    #link
    otx = []
    for url in filtered_list:
        #print(url)#=>To check the link after slipting.
        temp = re.split('https://github.com|blob/|"',url)
        temp_url = "https://raw.githubusercontent.com"+temp[2]+temp[3]
        # print(temp[2])
        # print(temp[3])
        s = temp[3]
        data = ''.join(i for i in s if not i.isdigit())
        srt = (data.split('/'))
        r = '_'
        result = r.join(srt)
        otx.append(result)
        semi_filter.append(temp_url)
    d.append(semi_filter)    
    num = len(semi_filter)
    if num==0:
        break
    else:
        # print(semi_filter)#=>To see the Raw link 
        get_op = []  
        count = 0
        for link in semi_filter:
            try: 
                my_request = requests.get(link, cookies=cookies, headers=header, verify=False, timeout=10) 
            except Timeout:
                print('Timeout has been raised.')
                
            res = str(my_request.content)
            output = {
                'file' : temp[3],
                'date' : dt,
                'time' : tm,
                'page_no' : y,
                'current_count' : count,
                'output' : res
            }
            get_op.append(output)
            time.sleep(10)
            count+=1
        
    final_op.append(get_op)
    y+=1
    if y%20==0:
        cookie_str = input(f"enter the fresh cookie as string : ")
        cookie_str = re.split('=|;',cookie_str)
        cookie_key = cookie_str[::2]
        cookie_value = cookie_str[1::2]
        cookies = {}
    for i in range(0,len(cookie_key)):
        cookies[cookie_key[i]] = cookie_value[i]  
    with open(f'{company}_link.json', 'w') as f:
        for line in c:
            f.write("%s\n" % line)
    with open(f'{company}_raw_link.json', 'w') as f:
        for line in d:
            f.write("%s\n" % line)    
    with open(f'{company}_{dt_tm}.json', 'w') as f:
        for line in final_op:
            f.write("%s\n" % line)