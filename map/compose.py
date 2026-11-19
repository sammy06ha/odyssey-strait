import json, random, base64
from PIL import Image
import numpy as np
from scipy import ndimage as nd
random.seed(7)
m=json.load(open('/tmp/mapgen/map2.json')); D=m['d']
land=np.asarray(Image.open('/home/claude/odyssey-strait/map/base.png').convert('L'))<100
dsea=nd.distance_transform_edt(~land); dland=nd.distance_transform_edt(land)
def b64(p): return 'data:image/png;base64,'+base64.b64encode(open(p,'rb').read()).decode()
deco=[('d_ship4.png',520,600,150),('d_ship1.png',250,445,110),('d_ship2.png',130,505,80),('d_dol1.png',470,705,60),('d_dol2.png',540,730,60),('d_serp.png',320,690,120),('d_comp.png',880,770,140)]
boxes=[];dec=''
for f,x,y,w in deco:
    im=Image.open('/tmp/mapai/'+f); h=w*im.height/im.width
    dec+=f'<image href="{b64("/tmp/mapai/"+f)}" x="{x-w/2:.0f}" y="{y-h/2:.0f}" width="{w}" height="{h:.0f}"/>'
    boxes.append((x-w/2-14,y-h/2-10,x+w/2+14,y+h/2+10))
free=lambda x,y: not any(a<=x<=c and b<=y<=d for a,b,c,d in boxes)
waves=''
for row,y in enumerate(range(80,960,28)):
    off=(row%2)*24
    for x in range(80+off,960,48):
        xx=x+random.uniform(-5,5); yy=y+random.uniform(-3,3)
        if 70<xx<954 and 70<yy<954 and dsea[int(yy),int(xx)]>20 and free(xx,yy):
            waves+=f'<path d="M{xx-10:.1f} {yy:.1f}q5 -6 10 0t10 0"/>'
rng=np.random.default_rng(3)
noise=nd.gaussian_filter(rng.random((1024,1024)),40); noise=(noise-noise.min())/(noise.max()-noise.min())
mount=''
for y in range(76,950,15):
    for x in range(76,950,15):
        xx=x+random.uniform(-6,6); yy=y+random.uniform(-5,5); X,Y=int(xx),int(yy)
        if dland[Y,X]>14 and noise[Y,X]>.55 and random.random()<.7:
            s=random.uniform(4,7)
            mount+=f'<path d="M{xx-s:.1f} {yy+s*.55:.1f}L{xx:.1f} {yy-s*.6:.1f}L{xx+s:.1f} {yy+s*.55:.1f}M{xx-s*.3:.1f} {yy+s*.1:.1f}L{xx+s*.15:.1f} {yy+s*.55:.1f}"/>'
C='#d9773a'; INK='#150d08'
# meander unit 48x22 scaled x1.6 -> band 36px tall
def unit(x,y,k):  # k = scale
    p=f'<path d="M{x+4*k} {y+20*k}V{y+5*k}H{x+23*k}V{y+17*k}H{x+9*k}V{y+9*k}H{x+18*k}V{y+13*k}H{x+13*k}" fill="none" stroke="{C}" stroke-width="{2*k}" stroke-linecap="square"/>'
    p+=f'<rect x="{x+29*k}" y="{y+4*k}" width="{14*k}" height="{14*k}" fill="none" stroke="{C}" stroke-width="{2*k}"/>'
    p+=f'<path d="M{x+29*k} {y+4*k}L{x+43*k} {y+18*k}M{x+43*k} {y+4*k}L{x+29*k} {y+18*k}" stroke="{C}" stroke-width="{1.4*k}"/>'
    return p
k=1.5; band_h=22*k; M=14; T=M+band_h+8  # outer margin, inner edge
L=1024
inner=L-2*T
n=round((L-2*M-2*band_h)/(48*k)); ul=(L-2*M-2*band_h)/n  # unit length along side
def side():
    g=''
    for i in range(n):
        g+=f'<g transform="translate({M+band_h+i*ul+(ul-48*k)/2:.2f},0)">'+unit(0,M,k)+'</g>'
    return g
top=side()
frame=f'<rect x="0" y="0" width="{L}" height="{L}" fill="none" stroke="{INK}" stroke-width="{2*T}"/>'
frame+=f'<rect x="{M-5}" y="{M-5}" width="{L-2*M+10}" height="{L-2*M+10}" fill="none" stroke="{C}" stroke-width="2"/>'
frame+=f'<rect x="{T-4}" y="{T-4}" width="{L-2*T+8}" height="{L-2*T+8}" fill="none" stroke="{C}" stroke-width="2"/>'
for rot in (0,90,180,270):
    frame+=f'<g transform="rotate({rot} 512 512)">{top}</g>'
for (cx,cy) in ((M,M),(L-M-band_h,M),(M,L-M-band_h),(L-M-band_h,L-M-band_h)):
    frame+=f'<rect x="{cx+4}" y="{cy+4}" width="{band_h-8}" height="{band_h-8}" fill="none" stroke="{C}" stroke-width="2"/><circle cx="{cx+band_h/2}" cy="{cy+band_h/2}" r="4" fill="{C}"/>'
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
<defs>
<radialGradient id="lg" cx="45%" cy="45%" r="70%"><stop offset="0" stop-color="#e2955a"/><stop offset=".6" stop-color="#c8652e"/><stop offset="1" stop-color="#8e3f17"/></radialGradient>
<clipPath id="lc"><path d="{D}"/></clipPath>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .18 0"/></filter>
</defs>
<rect width="1024" height="1024" fill="url(#lg)"/>
<g fill="none" stroke-linejoin="round">
<path d="{D}" stroke="#9a4419" stroke-width="20" opacity=".55"/>
<path d="{D}" stroke="#d5814a" stroke-width="15"/>
<path d="{D}" stroke="#9a4419" stroke-width="9" opacity=".8"/>
<path d="{D}" stroke="#d27c45" stroke-width="5"/>
</g>
<g fill="none" stroke="#1a0f08" stroke-width="2" stroke-linecap="round" opacity=".5">{waves}</g>
<path d="{D}" fill="#150d08"/>
<g clip-path="url(#lc)">
<path d="{D}" fill="none" stroke="#e9c79a" stroke-width="5" opacity=".75"/>
<path d="{D}" fill="none" stroke="#150d08" stroke-width="3"/>
<g fill="none" stroke="#d9a877" stroke-width="1.1" opacity=".4" stroke-linecap="round">{mount}</g>
</g>
{dec}
<rect width="1024" height="1024" filter="url(#grain)"/>
{frame}
</svg>'''
open('/tmp/mapai/compose.html','w').write('<body style="margin:0;background:#000">'+svg+'</body>')
