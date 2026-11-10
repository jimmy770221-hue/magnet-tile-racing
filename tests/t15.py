import asyncio, os
from playwright.async_api import async_playwright
from common import route
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1000,'height':640}); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        await pg.route('**/*',route)
        await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(15000)
        await pg.evaluate("()=>{const s=JSON.parse(localStorage.getItem('twq_save_v1')||'{}'); s.cars=['taxi','truck','sedan','jeep']; s.coins=9999; localStorage.setItem('twq_save_v1',JSON.stringify(s));}")
        await pg.reload(); await pg.wait_for_timeout(15000)
        
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        await pg.click('#tTap'); await pg.click('.mbtn[data-go=speed]'); await pg.click('#toCar'); await pg.wait_for_timeout(800)
        for i in range(4):
            cars=await pg.query_selector_all('#cars .car'); await cars[i].click(); await pg.wait_for_timeout(300)
            await pg.click('#startBtn'); await pg.wait_for_function("()=>__game.state==='race'",timeout=60000); await pg.evaluate("()=>{window.__auto=false}"); await pg.wait_for_timeout(2500)
            await pg.screenshot(path=f's_tile{i}.png')
            await pg.keyboard.press('Escape'); await pg.evaluate("()=>{document.getElementById('menuBtn')&&0}")
            await pg.reload(); await pg.wait_for_timeout(15000)
            try: await pg.click('#dailyOk',timeout=3000)
            except Exception: pass
            await pg.click('#tTap'); await pg.click('.mbtn[data-go=speed]'); await pg.click('#toCar'); await pg.wait_for_timeout(500)
        print('errs',errs[:6]); await b.close()
asyncio.run(main())
