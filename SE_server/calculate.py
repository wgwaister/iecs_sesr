from SE_server.models import *
import json
import datetime
import pytz
from operator import itemgetter


def calculate():
    people_result()
    project_result()


def people_result():
    project = Project.objects.all()
    taipei_time_zone = pytz.timezone('Asia/Taipei')
    now = datetime.datetime.now()
    now_taipei_time_zone = now.astimezone(taipei_time_zone)
    print(now_taipei_time_zone)
    open = 0
    click = 0
    attachment = 0
    for p in project:
        limittime = datetime.timedelta(seconds=p.IgnoreSecond)
        p.OpenRecord = None
        p.ClickRecord = None
        p.AttachmentRecord = None
        p.save()
        start = p.CalculateStartDate
        end = p.CalculateEndDate
        start_taipei_time_zone = start.astimezone(taipei_time_zone)
        end_taipei_time_zone = end.astimezone(taipei_time_zone)
        if start_taipei_time_zone <= now_taipei_time_zone <= end_taipei_time_zone:
            member_list = p.TestML.all()
            print(p.ProjectCode)
            try:
                for member in member_list:
                    log = Log.objects.filter(uuid__contains=member.UUID)
                    result = '{'
                    mail_list = p.Mail.all().order_by('MailNumber')
                    for i in mail_list:
                        result = result + '"%s":{"name":"","open":0,"click":0},' % i.MailNumber
                    result = result + '"Total":{"name":"總和","open":0,"click":0}}'
                    data = json.loads(result)
                    for mail in mail_list:
                        data[mail.MailNumber]['name'] = mail.MailTag
                        if mail.HasAtt:
                            data[mail.MailNumber]['attachment'] = 0
                            data['Total']['attachment'] = 0
                    if log:
                        for mail in mail_list:
                            project_mail = log.filter(html__contains=mail.Address)
                            if project_mail:
                                open_list = project_mail.filter(html__contains=mail.Open)
                                last_time_str = '2000-01-10 11:30:20'  # 用於第一個判斷不要錯誤
                                last_time = datetime.datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
                                for open_mail in open_list:
                                    if p.OpenRecord:
                                        o_list = p.OpenRecord
                                    else:
                                        o_list = []
                                    this_time_str = str(open_mail.date) + ' ' + str(open_mail.time)
                                    this_time = datetime.datetime.strptime(this_time_str, '%Y-%m-%d %H:%M:%S')
                                    tt = this_time - last_time
                                    if tt > limittime:
                                        data[mail.MailNumber]['open'] += 1
                                        o_list.append(
                                            {"open": {"Date": str(open_mail.date) + ' ' + str(open_mail.time),
                                                      "Mail": mail.Title,
                                                      "Sender": mail.Sender,
                                                      "Unit": member.UnitName, "Email": member.Email}})
                                        open += 1
                                        o_list = sorted(o_list, key=lambda k: k['open']['Date'], reverse=True)
                                        p.OpenRecord = o_list
                                        p.save()
                                        last_time_str = str(open_mail.date) + ' ' + str(open_mail.time)
                                        last_time = datetime.datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
                                click_list = project_mail.filter(html__contains=mail.Click)
                                last_time_str = '2000-01-10 11:30:20'  # 用於第一個判斷不要錯誤
                                last_time = datetime.datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
                                for click_mail in click_list:
                                    if p.ClickRecord:
                                        c_list = p.ClickRecord
                                    else:
                                        c_list = []
                                    this_time_str = str(click_mail.date) + ' ' + str(click_mail.time)
                                    this_time = datetime.datetime.strptime(this_time_str, '%Y-%m-%d %H:%M:%S')
                                    tt = this_time - last_time
                                    if tt > limittime:
                                        data[mail.MailNumber]['click'] += 1
                                        c_list.append(
                                            {"click": {"Date": str(click_mail.date) + ' ' + str(click_mail.time),
                                                       "Mail": mail.Title, "Sender": mail.Sender,
                                                       "Unit": member.UnitName,
                                                       "Email": member.Email}})
                                        click += 1
                                        c_list = sorted(c_list, key=lambda k: k['click']['Date'], reverse=True)
                                        p.ClickRecord = c_list
                                        p.save()
                                        last_time_str = str(click_mail.date) + ' ' + str(click_mail.time)
                                        last_time = datetime.datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
                                if mail.HasAtt:
                                    print(p.ProjectCode + ' ' + mail.MailNumber + ' Has Attachment')
                                    attachment_list = project_mail.filter(html__contains=mail.Attachment)
                                    last_time_str = '2000-01-10 11:30:20'  # 用於第一個判斷不要錯誤
                                    last_time = datetime.datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
                                    for attachment_mail in attachment_list:
                                        if p.AttachmentRecord:
                                            attachment_list = p.AttachmentRecord
                                        else:
                                            attachment_list = []
                                        this_time_str = str(attachment_mail.date) + ' ' + str(attachment_mail.time)
                                        this_time = datetime.datetime.strptime(this_time_str, '%Y-%m-%d %H:%M:%S')
                                        tt = this_time - last_time
                                        if tt > limittime:
                                            data[mail.MailNumber]['attachment'] += 1
                                            attachment_list.append(
                                                {"attachment": {
                                                    "Date": str(attachment_mail.date) + ' ' + str(attachment_mail.time),
                                                    "Mail": mail.Title, "Sender": mail.Sender,
                                                    "Unit": member.UnitName,
                                                    "Email": member.Email}})
                                            attachment += 1
                                            attachment_list = sorted(attachment_list,
                                                                     key=lambda k: k['attachment']['Date'],
                                                                     reverse=True)
                                            p.AttachmentRecord = attachment_list
                                            p.save()
                                            last_time_str = str(attachment_mail.date) + ' ' + str(attachment_mail.time)
                                            last_time = datetime.datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
                    member.Result = data
                    member.save()
            except:
                print('%s error' % p.ProjectCode)


def project_result():
    taipei_time_zone = pytz.timezone('Asia/Taipei')
    now = datetime.datetime.now()
    now_taipei_time_zone = now.astimezone(taipei_time_zone)
    project = Project.objects.all()
    for pp in project:
        start = pp.CalculateStartDate
        end = pp.CalculateEndDate
        start_taipei_time_zone = start.astimezone(taipei_time_zone)
        end_taipei_time_zone = end.astimezone(taipei_time_zone)
        pp.lastCalTime = now_taipei_time_zone
        pp.save()
        data = None
        if start_taipei_time_zone <= now_taipei_time_zone <= end_taipei_time_zone:
            try:
                result = '{'
                mail_list = pp.Mail.all().order_by('MailNumber')
                if mail_list:
                    for i in mail_list:
                        result = result + '"%s":{"name":"","open":0,"click":0},' % i.MailNumber
                    result = result + '"Total":{"name":"總和","open":0,"click":0}}'
                    data = json.loads(result)
                    for mail in mail_list:
                        data[mail.MailNumber]['name'] = mail.MailTag
                        if mail.HasAtt:
                            data[mail.MailNumber]['attachment'] = 0
                            data['Total']['attachment'] = 0
                    member_list = pp.TestML.all()
                    for member in member_list:
                        for i in mail_list:
                            if member.Result:
                                data['%s' % i.MailNumber]['open'] += member.Result['%s' % i.MailNumber]['open']
                                data['%s' % i.MailNumber]['click'] += member.Result['%s' % i.MailNumber]['click']
                                if i.HasAtt:
                                    data['%s' % i.MailNumber]['attachment'] += member.Result['%s' % i.MailNumber][
                                        'attachment']
                    for i in mail_list:
                        data['Total']['open'] += data['%s' % i.MailNumber]['open']
                        data['Total']['click'] += data['%s' % i.MailNumber]['click']
                        if i.HasAtt:
                            data['Total']['attachment'] += data['%s' % i.MailNumber]['attachment']
            except:
                print('%s error' % pp.ProjectCode)
        if data:
            pp.ProjectResult = data
            pp.save()
    print(now_taipei_time_zone)
