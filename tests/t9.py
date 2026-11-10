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
        for n,nm in [(3,'night')]:
            await pg.click('.mbtn[data-go=speed]'); await pg.click(f'#tods .opt:nth-child({n})'); await pg.screenshot(path=f's_tod_{nm}_menu.png')
            await pg.click('#toCar'); 
            await pg.evaluate('()=>{window.__auto=true;window.__ts=3;__game.setStage(1)}')
            await pg.click('#startBtn'); await pg.wait_for_timeout(9000); await pg.screenshot(path=f's_tod_{nm}.png')
            await pg.click('#pauseBtn'); await pg.click('#pMenu') if await pg.query_selector('#pMenu') else None
            await pg.wait_for_timeout(500)
            break
        print('errs',errs[:6]); await b.close()
asyncio.run(main())
