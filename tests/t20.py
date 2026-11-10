import asyncio, os, json
from playwright.async_api import async_playwright
from common import route
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1000,'height':640}); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        pg.on('console',lambda m: errs.append(m.text[:150]) if m.type=='error' else None)
        await pg.route('**/*',route)
        await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(15000)
        await pg.evaluate("()=>{const s=JSON.parse(localStorage.getItem('twq_save_v1')||'{}'); s.tut=1; s.coins=5000; s.cars=['taxi','truck','sedan','jeep']; localStorage.setItem('twq_save_v1',JSON.stringify(s));}")
        await pg.reload(); await pg.wait_for_timeout(15000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        js=lambda s: pg.evaluate(s)
        await js("()=>document.getElementById('tTap').click()")
        print('跳過教學直接主選單:', await js("()=>!document.getElementById('scrMain').classList.contains('hidden')"))
        # 禮物盒
        await js("()=>document.getElementById('mGarage').click()"); await pg.wait_for_timeout(300)
        await js("()=>document.getElementById('oddsBtn').click()"); await pg.wait_for_timeout(200); await pg.screenshot(path='s_odds.png')
        print('機率表:', await js("()=>document.getElementById('oddsList').innerText.replace(/\\n/g,' | ')"))
        await js("()=>document.getElementById('oddsOk').click()")
        await js("()=>document.getElementById('coinDraw').click()"); await pg.wait_for_timeout(300); await pg.screenshot(path='s_gift1.png'); await pg.wait_for_timeout(900); await pg.screenshot(path='s_gift2.png')
        print('禮物:', await js("()=>document.getElementById('giftTxt').textContent"))
        await js("()=>document.getElementById('giftOk').click()")
        # 10000 次模擬
        r=await js("()=>{const c={}; for(let i=0;i<10000;i++){const e=__game.drawFromTable(); c[e.id]=(c[e.id]||0)+1;} return c}")
        print('10000次:', {k:v/100 for k,v in r.items()})
        # 開一場比賽、觸發飛散
        await js("()=>document.querySelector('#garage [data-back=scrMain]')&&document.querySelector('#garage [data-back=scrMain]').click()")
        await js("()=>document.getElementById('mQuick').click()")
        await pg.wait_for_function("()=>__game.state==='race'",timeout=60000); await js("()=>{window.__auto=false}"); await pg.wait_for_timeout(1500)
        await js("()=>{ __game.tileBurst(__game.player,8); }"); await pg.wait_for_timeout(220); await pg.screenshot(path='s_burst.png')
        n1=await js("()=>__game.tilePool.filter(t=>t.on).length"); await pg.wait_for_timeout(1500)
        n2=await js("()=>__game.tilePool.filter(t=>t.on).length"); print('飛散片數 0.2秒:',n1,' 1.7秒後:',n2)
        print('上次設定:', await js("()=>JSON.stringify(JSON.parse(localStorage.twq_save_v1).last)"))
        print('追蹤事件:', await js("()=>__game.Track.get().map(e=>e.n).join(',')"))
        print('errs',errs[:5]); await b.close()
asyncio.run(main())
