import base64, json, math
R=json.load(open('real.json'))
xy=R['xy']; mx=R['mx']; my=R['my']
def loc(lat,lon): return ((lon-121.572)*mx, -(lat-25.080)*my)
def nearest(p): return min(range(len(xy)),key=lambda i:(xy[i][0]-p[0])**2+(xy[i][1]-p[1])**2)
lm={}
for k,(la,lo) in {'temple':(25.0971,121.5876),'bridge':(25.0994,121.5872),'t101':(25.0340,121.5645)}.items():
    x,z=loc(la,lo); lm[k]={'x':round(x,1),'z':round(z,1),'idx':nearest((x,z))}
lm['peak']={'idx':343}
out={'xy':xy,'el':R['el'],'grid':R['grid'],'gnx':28,'gny':32,'lat0':25.080,'lat1':25.142,'lon0':121.572,'lon1':121.624,'mx':mx,'my':my,'lm':lm}
import os, shutil
T=open('template.html').read()
js=json.dumps(out,separators=(',',':'))
# 單檔離線版（資源內嵌）
b=base64.b64encode(open('tw_cars.glb','rb').read()).decode()
s=T.replace('__REAL_JSON__',js).replace('__GLB_B64__',b).replace('__ASSET_BASE__','')
open('game.html','w').write(s); print('單檔版',len(s))
# 外部資源版（網頁用）
os.makedirs('dist/assets',exist_ok=True)
open('dist/assets/real.json','w').write(js)
open('dist/assets/tw_cars.json','w').write(json.dumps({'b64':base64.b64encode(open('tw_cars.glb','rb').read()).decode()}))
e=T.replace('__REAL_JSON__','null').replace('__GLB_B64__','').replace('__ASSET_BASE__','assets/')
open('dist/index.html','w').write(e); print('外部版',len(e))
