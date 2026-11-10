import asyncio, os
from playwright.async_api import async_playwright
from common import route
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1000,'height':640},device_scale_factor=2); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.route('**/*',route)
        await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(25000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        await pg.evaluate("()=>{document.getElementById('tTap').click()}"); await pg.wait_for_timeout(500); await pg.evaluate("()=>{document.querySelector('.mbtn[data-go=speed]').click()}"); 
        await pg.evaluate("()=>document.getElementById('toCar').click()"); await pg.wait_for_timeout(800); await pg.evaluate("()=>document.getElementById('startBtn').click()"); await pg.wait_for_function("()=>__game.state==='race'",timeout=60000); await pg.evaluate("()=>{window.__auto=false}"); await pg.wait_for_timeout(2500)
        await pg.screenshot(path='s_close.png',clip={'x':330,'y':250,'width':340,'height':330}); print(errs[:3]); await b.close()
asyncio.run(main())
