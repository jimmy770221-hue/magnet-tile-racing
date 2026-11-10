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
        await pg.click('.mbtn[data-go=speed]'); await pg.screenshot(path='s_track.png')
        await pg.click('#toCar'); await pg.screenshot(path='s_car.png')
        await pg.click('[data-back=scrTrack]'); await pg.click('[data-back=scrMain]')
        await pg.click('#mSet'); await pg.screenshot(path='s_set.png'); await pg.click('#setHelp'); await pg.screenshot(path='s_help.png'); await pg.click('#helpBack'); await pg.click('#setBack')
        await pg.click('.mbtn[data-go=speed]'); await pg.click('#toCar')
        await pg.evaluate('()=>{window.__auto=true;window.__ts=8;__game.setStage(1)}')
        await pg.click('#startBtn'); await pg.wait_for_timeout(9000)
        await pg.click('#pauseBtn'); await pg.wait_for_timeout(300); print('state',await pg.evaluate('()=>__game.state')); await pg.screenshot(path='s_pause.png')
        i0=await pg.evaluate('()=>__game.player.idx'); await pg.wait_for_timeout(1500); i1=await pg.evaluate('()=>__game.player.idx'); print('paused idx',i0,i1)
        await pg.click('#pResume'); await pg.wait_for_timeout(8000); print('state',await pg.evaluate('()=>__game.state'),await pg.evaluate('()=>__game.player.idx'))
        await pg.screenshot(path='s_race.png')
        for k in range(240):
            await pg.wait_for_timeout(1000)
            if await pg.evaluate('()=>__game.state')=='result': break
        print('final state',await pg.evaluate('()=>[__game.state,__game.player.idx]')); await pg.screenshot(path='s_result.png'); print('result',await pg.inner_text('#resSub'))
        await pg.click('#carBtn'); await pg.wait_for_timeout(500); await pg.screenshot(path='s_car2.png')
        print('errs',errs[:6]); await b.close()
asyncio.run(main())
