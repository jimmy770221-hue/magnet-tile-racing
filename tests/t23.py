import asyncio, os
from playwright.async_api import async_playwright
from common import route
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1000,'height':640}); await pg.route('**/*',route)
        await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(10000)
        js=lambda s: pg.evaluate(s)
        await js("()=>{const s=JSON.parse(localStorage.getItem('twq_save_v1')||'{}'); s.tut=1; s.cars=['taxi','truck','sedan','jeep']; s.last={mode:'item',stage:0,car:'jeep',diff:2,tod:'night'}; localStorage.setItem('twq_save_v1',JSON.stringify(s));}")
        await pg.reload(); await pg.wait_for_timeout(10000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        await js("()=>document.getElementById('tTap').click()"); await pg.wait_for_timeout(300)
        print('A 快速開跑文字:', await js("()=>document.getElementById('quickTxt').textContent"))
        await js("()=>document.getElementById('mQuick').click()"); await pg.wait_for_function("()=>__game.state==='race'",timeout=60000)
        print('A2 進場後 last:', await js("()=>JSON.stringify(JSON.parse(localStorage.twq_save_v1).last)"))
        await b.close()
asyncio.run(main())
