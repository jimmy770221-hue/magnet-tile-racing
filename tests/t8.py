import asyncio, os
from playwright.async_api import async_playwright
from common import route
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1000,'height':640}); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        await pg.add_init_script("if(!localStorage.getItem('twq_save_v1')) localStorage.setItem('twq_save_v1',JSON.stringify({v:1,coins:300,cars:['taxi'],parts:{},equip:{},daily:'',streak:0,adDraw:'',races:0,tut:1}))"); await pg.route('**/*',route)
        await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(20000)
        await pg.screenshot(path='s_title.png')
        await pg.click('#dailyOk'); await pg.wait_for_timeout(300); await pg.screenshot(path='s_title.png')
        await pg.click('#tTap'); await pg.screenshot(path='s_main.png')
        await pg.click('.mbtn[data-go=item]'); await pg.click('#toCar'); await pg.screenshot(path='s_item_car.png')
        await pg.evaluate('()=>{window.__auto=true;window.__ts=3;__game.setStage(1)}')
        await pg.click('#startBtn'); 
        seen=set(); shot=False
        for k in range(60):
            await pg.wait_for_timeout(1000)
            it=await pg.evaluate('()=>__game.racers().map(r=>[r.item,r.stun>0,r.shield>0,r.bless>0])')
            for x in it:
                if x[0]: seen.add(x[0])
            if not shot and it[0][0]:
                await pg.screenshot(path='s_item_hold.png'); shot=True
                await pg.evaluate('()=>window.dispatchEvent(new KeyboardEvent("keydown",{code:"KeyX"}))')
                await pg.wait_for_timeout(400); await pg.screenshot(path='s_item_use.png')
            st=await pg.evaluate('()=>__game.state')
            if st=='result': break
        print('items seen',seen,'state',st)
        await pg.click('#mItem') if False else None
        print('errs',errs[:6]); await b.close()
asyncio.run(main())
