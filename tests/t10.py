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
        await pg.evaluate('()=>{window.__auto=true;window.__ts=8}')
        await pg.click('#mCup')
        for r in range(2):
            for k in range(200):
                await pg.wait_for_timeout(1000)
                if await pg.evaluate('()=>__game.state')=='result': break
            print('round',r,await pg.inner_text('#resSub'), '|', await pg.inner_text('#againBtn'))
            if r==0: await pg.screenshot(path='s_cup1.png'); await pg.click('#againBtn')
        await pg.click('#menuBtn'); await pg.click('#mBoard'); await pg.screenshot(path='s_board.png')
        await pg.click('[data-back=scrMain]'); await pg.click('#mGarage'); await pg.click('#coinDraw'); await pg.wait_for_timeout(300); await pg.screenshot(path='s_draw.png')
        print('errs',errs[:6]); await b.close()
asyncio.run(main())
