import asyncio, os
from playwright.async_api import async_playwright
from common import route
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':852,'height':393},device_scale_factor=2,has_touch=True,is_mobile=True)
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.add_init_script("if(!localStorage.getItem('twq_save_v1')) localStorage.setItem('twq_save_v1',JSON.stringify({v:1,coins:300,cars:['taxi'],parts:{},equip:{},daily:'',streak:0,adDraw:'',races:0,tut:1}))"); await pg.route('**/*',route)
        await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(20000)
        await pg.click('#dailyOk'); await pg.wait_for_timeout(300); await pg.screenshot(path='s_phone_title.png')
        print(await pg.evaluate("()=>{const c=document.getElementById('c').getBoundingClientRect();return [innerWidth,innerHeight,c.x,c.y,c.width,c.height]}"))
        await pg.tap('#tTap'); await pg.wait_for_timeout(500); await pg.screenshot(path='s_phone_main.png')
        await pg.tap('#mSpeed') if await pg.query_selector('#mSpeed') else await pg.tap('.mbtn[data-go=speed]')
        await pg.wait_for_timeout(300); await pg.tap('#toCar'); await pg.wait_for_timeout(300); await pg.tap('#startBtn'); await pg.wait_for_timeout(9000)
        await pg.screenshot(path='s_phone_race.png'); print(errs[:5]); await b.close()
asyncio.run(main())
