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
        await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(20000)
        await pg.screenshot(path='s_title.png')
        await pg.click('#dailyOk'); await pg.wait_for_timeout(300); await pg.screenshot(path='s_title.png')
        await pg.click('#tTap'); await pg.screenshot(path='s_main.png')
        await pg.evaluate("()=>localStorage.setItem('twq_lb_a',JSON.stringify([{t:150.66,car:'小黃',tod:'白天',d:'競速賽'},{t:158.2,car:'小轎車',tod:'夜間',d:'道具賽'}]))")
        await pg.click('#mBoard'); await pg.screenshot(path='s_board.png')
        await pg.click('#scrBoard [data-back=scrMain]'); await pg.click('#mGarage'); await pg.click('#coinDraw'); await pg.wait_for_timeout(300); await pg.screenshot(path='s_draw.png')
        print('errs',errs[:6]); await b.close()
asyncio.run(main())
