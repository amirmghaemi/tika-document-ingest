#!/usr/bin/python3

import sys
import json
import email
import re

orig_msg = ["[ \-\t]+Original Message[ \-]+", "[ \-\t]+Forwarded by", "[_ \t]+Reply Separator[_ \t]+"]
forward_ends = " ---------------------------"
condition1 = r'[=]+\d\d'
condition2 = r'[=]+[ \n]+'

tss = ['to:', 'sent:', 'from:', 'subject:']
toIgnore = {'GT_200':[], 'GT_300':[], 'GT_400':[], 'GT_500':[], 'GT_1000':[]}

def find_info(info_str):
    reg_to = r'To:.*[\s\S]*cc:.*[\s\S]*Subject:.*'
    res = re.search(reg_to, info_str)
    # print("to_str:", to_str)
    # print("res:", res.span())
    # print("res:", info_str[res.start()])
    # print("res:", info_str[res.end()+1:])
    triple_match = res.group() if res is not None else ""
    triple_split = triple_match.split("Subject:")
    both_match = triple_split[0]
    both_split = both_match.split("cc:")
    to_s = both_split[0].split("To:")[1].strip()
    cc_s = both_split[1].strip()
    subject_s = triple_split[1].strip()
    body_s = info_str[res.end()+1:]
    return (to_s, cc_s, subject_s, body_s)

def find_cc(cc_str):
    str_split = cc_str.split('\n')
    from_s = str_split[0]
    count = 0
    while from_s == "":
        count += 1
        from_s = str_split[count]
    return from_s

def find_from(from_str):
    str_split = from_str.split('\n')
    from_s = str_split[0]
    count = 0
    while from_s == "":
        count += 1
        from_s = str_split[count]
    return from_s

def find_date(date_str):
    reg_pm = r'\d+\/\d+\/\d+ [\d+:]+ PM'
    reg_am = r'\d+\/\d+\/\d+ [\d+:]+ AM'
    res = re.search(reg_pm, date_str) if re.search(reg_pm, date_str) is not None else re.search(reg_am, date_str)
    return res.group()

import traceback
#:D :D :D
ignored_list_due_to_subMSG = []
def parseSubEmails(sent_str, file_name):
    global ignored_list_due_to_subMSG
    eml = email.message_from_string(sent_str)
    ret_dict = ''
    emlPL = eml.get_payload()
    if(type(emlPL)==type([])): return -1;
    if(eml.get_payload() is None or eml.get_payload() == eml):
        ignored_list_due_to_subMSG.append(file_name)
    else:
        # print("****************************")
        # print("eml:\n", eml)
        try:
            get_info = find_info(sent_str)
            get_from = find_from(sent_str)
            get_date = find_date(sent_str)
            if get_date in get_from:
                get_from = get_from.replace('From: ', '')
                get_from = get_from.replace('on ', '')
                find_date_ind = get_from.find(get_date)
                get_from = get_from[:find_date_ind].strip()
            TO = get_info[0] # eml['To'] if eml['To'] is not None else get_info[0]
            CC = get_info[1] # eml['cc'] if eml['cc'] is not None else get_info[1]
            FROM= get_from # eml['From'] if eml['From'] is not None else get_from
            DATE= get_date # eml['Sent'] if eml['Sent'] is not None else get_date
            SUB = get_info[2] #eml['Subject'] if eml['Subject'] is not None else get_info[2]
            ret_dict = {'to': re.sub('[\n]', ',', re.sub('[ \t]+', ' ', TO)), 'cc': re.sub('[\n]', ',', re.sub('[ \t]+', ' ', CC)), 'from': re.sub('[\n]', ',', re.sub('[ \t]+', ' ', FROM)), 'date':re.sub('[\n]', ',', re.sub('[ \t]+', ' ', DATE)), 'subject':re.sub('[\n]', ',', re.sub('[ \t]+', ' ', SUB)), 'body':get_info[3]}
            # print("ret_dict:\n", ret_dict)
            # print("find_from:\n", find_from(sent_str))
            # print("find_date:\n", find_date(sent_str))
        except Exception as e:
            print("Exception in parseSubEmails with:", e)
            print("Filename:", file_name)
    return ret_dict

def cleanPayload(thread):
    #assume it's a list separated thing?nope, split by , I guess
    payload = thread.get_payload()
    dividedPayload = payload.split('\n')
    thread_count = 1
    original, threads = {}, {}
    cur_thread = ['']
    for _, lines in enumerate(dividedPayload):
        lines = lines.strip()
        lines = re.sub(r'^([> \?\t]+)', r'', lines)#now emails have no beginning with "[> \?]+" :)
        lines = re.sub(condition1, r'', lines)
        lines = re.sub(condition2, r'', lines)
        if(len(lines)<=0):
            continue
        if(any([   len(re.findall(x, lines)) > 0 for x in orig_msg     ])):
            # print('YES!!!!', lines)
            #we got a new thread :D
            if(original=={}):
                original['payload'] = cur_thread#initial
            else:
                threads[thread_count] = cur_thread
            cur_thread = []
            thread_count += 1
        elif(lines.find(forward_ends)>=0):
            # print('NO!!!!', lines)
            continue#can't think of anything else right now
        else:
            cur_thread.append(lines)
        # print("lines:\n", lines)
        # print("cur_thread:\n", cur_thread)
    if(len(cur_thread)>0):
        if(original =={}):
            original['payload'] = cur_thread
        else:
            threads[thread_count] = cur_thread 
    original['threads'] = threads
    return original

def parseFile(sent_data):
    msg = sent_data['Body']
    thread = email.message_from_string(msg)
    # print("thread:", thread)
    history = cleanPayload(thread)
    # print("History:\n", history)
    
    orig_TO = ""
    count = 0
    while 'email.headers.to.'+str(count) in sent_data:
        orig_TO += sent_data['email.headers.to.'+str(count)] + ", "
        count += 1

    orig_FROM = ""
    count = 0
    while 'email.headers.from.'+str(count) in sent_data:
        orig_FROM += sent_data['email.headers.from.'+str(count)] + ", "
        count += 1

    orig_CC = ""
    count = 0
    while 'email.headers.cc.'+str(count) in sent_data:
        orig_CC += sent_data['email.headers.cc.'+str(count)] + ", "
        count += 1

    orig_BCC = ""
    count = 0
    while 'email.headers.bcc.'+str(count) in sent_data:
        orig_CC += sent_data['email.headers.bcc.'+str(count)] + ", "
        count += 1

    orig_Subject = sent_data['email.headers.subject'] if 'email.headers.subject' in sent_data else ""
    orig_BODY = '\n'.join([msg for msg in history['payload'] if(msg!="")])
    
    # print("orig_TO:", orig_TO)
    # print("orig_CC:", orig_CC)
    # print("orig_BCC:", orig_BCC)
    # print("orig_FROM:", orig_FROM)
    # print("orig_Subject:", orig_Subject)
    # print("orig_BODY:", orig_BODY)
    this_JSON = {}
    this_JSON['history'] = {}
    for turnNO in history['threads']:# will give the turn-wise dictionaries :)
        strMsg = '\n'.join(history['threads'][turnNO])
        # print("strMsg:\n", strMsg)
        json_tr = parseSubEmails(strMsg, sent_data['filename'])
        this_JSON['history'][turnNO] = json_tr
    this_JSON['to'] = orig_TO; 
    this_JSON['from'] = orig_FROM; 
    this_JSON['cc'] = orig_CC; 
    this_JSON['bcc'] = orig_BCC; 
    this_JSON['subject'] = orig_Subject; 
    this_JSON['body']= orig_BODY
    #print("this_JSON:\n", this_JSON)
    return this_JSON

data = json.load(sys.stdin)
print("Data:\n", data)
print("Body:\n", data['Body'])
parseFile(data)

