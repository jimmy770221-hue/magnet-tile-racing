import asyncio, os
from playwright.async_api import async_playwright
from common import route
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':852,'height':393},device_scale_factor=2,has_touch=True,is_mobile=True); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.route('**/*',route); await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(22000)
        await pg.evaluate("()=>document.getElementById('dailyOk').click()")
        await pg.evaluate("()=>document.getElementById('tTap').click()")
        await pg.wait_for_function("()=>__game.state==='race'",timeout=60000); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='s_tut_phone.png'); print(errs[:3]); await b.close()
asyncio.run(main())
