#!/usr/bin/env python3
import datetime as dt, json, os, re, sys, urllib.request
from zoneinfo import ZoneInfo

ICAL_URL='https://calendar.google.com/calendar/ical/77c4c1acf0953d6696c56478c582644845830faa3b640859cc84fa7cf9ac889f%40group.calendar.google.com/public/basic.ics'
TZ=ZoneInfo('America/New_York')

def unfold(text):
    out=[]
    for line in text.replace('\r\n','\n').split('\n'):
        if line.startswith((' ','\t')) and out: out[-1]+=line[1:]
        else: out.append(line)
    return out

def unescape(v): return v.replace('\\n','\n').replace('\\,',',').replace('\\;',';').replace('\\\\','\\')

def parse_dt(prop,value):
    if 'VALUE=DATE' in prop or re.fullmatch(r'\d{8}',value):
        d=dt.datetime.strptime(value[:8],'%Y%m%d').date(); return dt.datetime.combine(d,dt.time.min,TZ),True
    tz=TZ
    m=re.search(r'TZID=([^;:]+)',prop)
    if m:
        try: tz=ZoneInfo(m.group(1))
        except Exception: pass
    if value.endswith('Z'):
        p=dt.datetime.strptime(value,'%Y%m%dT%H%M%SZ').replace(tzinfo=dt.timezone.utc); return p.astimezone(TZ),False
    fmt='%Y%m%dT%H%M%S' if len(value)>=15 else '%Y%m%dT%H%M'
    return dt.datetime.strptime(value,fmt).replace(tzinfo=tz).astimezone(TZ),False

def events(text):
    result=[]; cur=None
    for line in unfold(text):
        if line=='BEGIN:VEVENT': cur={}
        elif line=='END:VEVENT':
            if cur and 'SUMMARY' in cur and 'DTSTART' in cur: result.append(cur)
            cur=None
        elif cur is not None and ':' in line:
            prop,value=line.split(':',1); key=prop.split(';',1)[0]
            if key in {'SUMMARY','DTSTART'}:
                cur[key]=(prop,value) if key=='DTSTART' else unescape(value)
    return result

def icon(summary):
    s=summary.upper()
    if any(x in s for x in ['GIGANTAMAX','DYNAMAX','MAX BATTLE','MAX MONDAY','G-MAX','D-MAX']): return '🟣'
    if 'MEGA' in s: return '🟠'
    if any(x in s for x in ['RAID','SHADOW']): return '🔴'
    if any(x in s for x in ['COMMUNITY','CATCH MASTERY','HATCH DAY']): return '🟢'
    if 'SPOTLIGHT' in s: return '🟡'
    if 'GBL' in s or 'GO BATTLE' in s: return '🔵'
    if 'ROCKET' in s: return '🩷'
    if 'WILD AREA' in s or 'GO FEST' in s: return '🌊'
    if 'DEADLINE' in s or 'TICKET' in s: return '⚪'
    return '🩵'

def main():
    webhook=os.environ.get('DISCORD_WEBHOOK_URL')
    if not webhook:
        print('DISCORD_WEBHOOK_URL is not set.',file=sys.stderr); return 2
    req=urllib.request.Request(ICAL_URL,headers={'User-Agent':'PoGoCalendarDiscord/1.0'})
    with urllib.request.urlopen(req,timeout=30) as r: text=r.read().decode('utf-8',errors='replace')
    now=dt.datetime.now(TZ); cutoff=now+dt.timedelta(hours=24); rows=[]
    for ev in events(text):
        start,all_day=parse_dt(*ev['DTSTART'])
        if now <= start < cutoff:
            when='All day' if all_day else start.strftime('%-I:%M %p')
            rows.append((start,f"{icon(ev['SUMMARY'])} **{when}** — {ev['SUMMARY']}"))
    rows.sort(key=lambda x:x[0])
    if not rows:
        print('No events starting in the next 24 hours; nothing posted.'); return 0
    payload={'username':'Pokémon GO Calendar','embeds':[{'title':'📅 Pokémon GO — next 24 hours','description':'\n'.join(r[1] for r in rows)[:3900],'color':5793266,'footer':{'text':f"Updated {now.strftime('%b %-d, %Y %-I:%M %p ET')} • Live group calendar"}}]}
    data=json.dumps(payload).encode()
    request=urllib.request.Request(webhook,data=data,headers={'Content-Type':'application/json','User-Agent':'PoGoCalendarDiscord/1.0'},method='POST')
    with urllib.request.urlopen(request,timeout=30) as r:
        if r.status not in (200,204): raise RuntimeError(f'Discord returned HTTP {r.status}')
    print(f'Posted {len(rows)} event(s) to Discord.')
    return 0

if __name__=='__main__': raise SystemExit(main())
