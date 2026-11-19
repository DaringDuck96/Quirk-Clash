#!/usr/bin/env python3
"""Refresh roster.html from the live game.
1. In the game page, evaluate tools/roster_dump.js and save the JSON it returns as dump.json
2. python3 tools/gen_roster.py dump.json roster.html   (rewrites roster.html in place)
Sprites, throw/taunt lines and the Best at / Worst at notes already in roster.html are kept."""
import json,re,sys,html
E=lambda t:html.escape(str(t),quote=False).replace("'","&#x27;")
J=json.load(open(sys.argv[1]));path=sys.argv[2];s=open(path).read()
WITH={'pitto':'His pouch throws out a random item from the full list in any match, even with items switched off. Pouch Catch decides what comes out next.',
'ichigo':'Her backpack (Down + B) works whether or not items are switched on.',
'oliver':'Any item he throws locks on and homes in on a rival.',
'aria':'Any item used against her has a 50% chance of simply not working.',
'kimiko':'Immune to Ice Shard and Frost Grenade.','tsuki':'Immune to Ice Shard and Frost Grenade.','evona':'Immune to Ice Shard and Frost Grenade.',
'gomi':'Immune to Flame Capsule and Flame Launcher.','daku':'Immune to Flame Capsule and Flame Launcher.',
'sato':'His own explosives never knock him back and hurt him far less.','sanshou':'No explosion can knock him back.',
'suzume':'Her Side + B web snatches the item a rival is holding.','kichi':'His chain (B) snatches the item a rival is holding.','minato':'His Side + B snatches the item a rival is holding.',
'soran':'His kunai swap also swaps held items.','shi':'When he KOs a rival he takes the item they were holding.',
'mia':'Her force field can jam an item used against her so it backfires.','ryuko':'Items she picks up are mounted and fire on their own.'}
REQ=lambda r:'' if not r else {'c':'play 1 Campaign fight','m':'%d matches','ko':'%d KOs','dmg':'deal %d%% damage','d':'get KO’d %d times','sv':'reach wave %d in Survival'}[r['t']].replace('%d',str(r['n']))
def mv(k,name,desc,fs=False):
    return '<div class="mv%s"><kbd>%s</kbd><div><b>%s</b><p>%s</p></div></div>'%(' fs' if fs else '',k,name,E(desc))
KB=['B','→ + B','↑ + B','↓ + B']
n=0
for C in J['ch']:
    m=re.search(r'<article class="card" id="%s".*?</article>'%re.escape(C['id']),s,re.S)
    if not m: print('no card for',C['id']);continue
    a=m.group(0)
    a=re.sub(r'<p class="d">.*?</p>',lambda _:'<p class="d">%s</p>'%E(C['d']),a,count=1,flags=re.S)
    a=re.sub(r'<p class="na">.*?</p>',lambda _:'<p class="na"><kbd>A</kbd> %s</p>'%E(C['na']),a,count=1,flags=re.S)
    for i,k in enumerate(KB):
        nm=E(re.sub(r'\s*\(.*?\)\s*$','',C['sp'][i]))
        a,c=re.subn(r'<div class="mv"><kbd>%s</kbd>.*?</div></div>'%re.escape(k),lambda _:mv(k,nm,C['g'][i]),a,count=1,flags=re.S)
        if not c: print('no move',C['id'],k)
    if C.get('qa'):
        a=re.sub(r'<div class="mv"><kbd>Shield \+ B</kbd>.*?</div></div>',lambda _:mv('Shield + B',E(C['qa'][0].title()),C['qa'][4]),a,count=1,flags=re.S)
    fsn=E((C['fs'] or 'Heroic Finale').title())+' <i>Heroic Finale</i>'
    a,c=re.subn(r'<div class="mv fs">.*?</div></div>',lambda _:mv('B, meter full',fsn,C['g'][4],True),a,count=1,flags=re.S)
    if not c: print('no finale',C['id'])
    a=re.sub(r'<p class="cos">.*?</p>','',a,flags=re.S)
    named=[(c,sub,r) for c,sub,r in C['looks'] if c]
    plain=len(C['looks'])-len(named)
    parts=[]
    for c,sub,r in named:
        t=c.title()+(': '+sub.title() if sub else '')
        parts.append('<span>%s%s</span>'%(E(t),' <em>'+E(REQ(r))+'</em>' if r else ''))
    cos='<p class="cos"><b>Costumes</b> %d colours%s</p>'%(plain,''.join(' · '+p for p in parts))
    if C['id'] in WITH: cos+='<p class="cos"><b>With items</b> %s</p>'%E(WITH[C['id']])
    a=a.replace('<dl class="id">',cos+'<dl class="id">',1)
    s=s.replace(m.group(0),a,1);n+=1
# controls
ctl='''<div class="ctl">
<div><b>Move</b><span>Controller: <em>left stick</em>; tilt it gently to walk · Keyboard: <em>W A S D</em> runs; hold <em>H</em> to walk</span></div>
<div><b>Jump</b><span>Controller: <em>X or Y</em>, or flick the stick up · Keyboard: <em>Space</em>. Jump again in the air.</span></div>
<div><b>Attack (A)</b><span>Controller: <em>A</em> · Keyboard: <em>J</em>. Tap for jabs; in the air for aerials.</span></div>
<div><b>Tilt attack</b><span>Hold a direction + A, or use the <em>right stick</em>. On keyboard, hold <em>H</em> + a direction + <em>J</em>. Quick pokes.</span></div>
<div><b>Smash attack</b><span><em>Flick</em> a direction and press A at the same moment (keyboard: direction + <em>J</em> together). Hold A to charge. These are the finishers.</span></div>
<div><b>Special (B)</b><span>Controller: <em>B</em> · Keyboard: <em>K</em>. B alone, or with left/right, up or down, gives four different moves. Up + B is usually how you get back to the stage.</span></div>
<div><b>Shield and dodge</b><span>Controller: <em>ZL / ZR</em> · Keyboard: <em>L</em>. Hold to shield; flick a direction while shielding to roll or dodge.</span></div>
<div><b>Grab</b><span>Controller: <em>L / R</em>, or shield + A · Keyboard: <em>U</em>. Then press a direction to throw.</span></div>
<div><b>Ability action</b><span><em>Shield + B</em>. A utility move unique to each fighter; most do no damage.</span></div>
<div><b>Heroic Finale</b><span>Dealing and taking damage fills a meter. When it is full, press <em>B with no direction</em>. Every fighter's Finale works differently: some you aim, some you steer, some change the whole stage.</span></div>
<div><b>Items</b><span>Off by default; switch them on at stage select. <em>Attack</em> picks one up and uses it, <em>Grab</em> drops it.</span></div>
<div><b>How you win</b><span>Damage is a percentage: the higher it is, the further a hit sends you. Knock rivals off the screen to take a stock.</span></div>
<div><b>Player 2 on keyboard</b><span><em>Arrows</em> move · <em>M</em> walk · <em>,</em> attack · <em>.</em> special · <em>/</em> jump · <em>Right Shift</em> shield · <em>'</em> grab</span></div>
</div>'''
s=re.sub(r'<div class="ctl">.*?</div>\n</div>',lambda _:ctl,s,count=1,flags=re.S) if '<div class="ctl">' in s else s
# items + stages
s=re.sub(r'<!--X-->.*?<!--/X-->','',s,flags=re.S)
order=['P','T','D','C','E','X']
it='<!--X--><h3 class="sec">Items</h3><p class="lead">%d items in six classes. They are off by default and only appear in Versus.</p><div class="its">'%len(J['items'])
for c in order:
    L=[i for i in J['items'] if i['c']==c]
    it+='<details><summary>%s <span>%d</span></summary><ul>%s</ul></details>'%(E(J['cls'][c]),len(L),''.join('<li><b>%s</b> %s</li>'%(E(i['n']),E(i['d'])) for i in L))
it+='</div><h3 class="sec">Stages</h3><p class="lead">%s</p><!--/X-->'%E(' · '.join(J['stages']))
s=s.replace('<div class="bar">',it+'<div class="bar">',1)
css='.cos{margin:8px 0 0;padding-top:9px;border-top:1px solid var(--line);font-size:13px;color:var(--dim)}.cos b{font:700 15px/1.3 var(--display);letter-spacing:.4px;text-transform:uppercase;color:var(--p1);margin-right:6px}.cos em{font-style:normal;color:#8f88c0}.cos em::before{content:"("}.cos em::after{content:")"}.cos span{white-space:nowrap;color:var(--ink)}.mv kbd{white-space:normal;line-height:1.25}.lead{color:var(--dim);margin:0 0 10px;max-width:70ch}.its{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:8px;align-items:start}.its details{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:9px 12px}.its summary{cursor:pointer;font:700 20px/1.1 var(--display);letter-spacing:.4px;color:var(--gold);text-transform:uppercase}.its summary span{color:var(--dim);font-size:15px}.its ul{margin:8px 0 0;padding:0;list-style:none}.its li{font-size:13.5px;color:var(--dim);padding:5px 0;border-top:1px solid var(--line)}.its li b{color:var(--ink);display:block}/*X*/'
s=re.sub(r'\.cos\{.*?/\*X\*/','',s,flags=re.S).replace('</style>',css+'</style>',1)
s=re.sub(r'<div class="top"><h1>.*?</div>',lambda _:'<div class="top"><h1>PU <span>HERO CLASH</span></h1><p>The full roster: all %d fighters, every special move and Heroic Finale, their costumes and how to earn them, plus the %d items and %d stages.</p><a class="play" href="./">PLAY THE GAME</a></div>'%(len(J['ch']),len(J['items']),len(J['stages'])),s,count=1,flags=re.S)
open(path,'w').write(s);print('cards',n,len(s))
