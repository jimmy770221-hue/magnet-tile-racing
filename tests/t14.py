import asyncio, os
from playwright.async_api import async_playwright
from common import route
EV="""([t,x,y])=>{ const z=document.getElementById('joyZone'); z.dispatchEvent(new PointerEvent(t,{pointerId:7,clientX:x,clientY:y,bubbles:true,pointerType:'touch',isPrimary:true})); }"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':852,'height':393},device_scale_factor=2,has_touch=True,is_mobile=True)
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.add_init_script("if(!localStorage.getItem('twq_save_v1')) localStorage.setItem('twq_save_v1',JSON.stringify({v:1,coins:300,cars:['taxi'],parts:{},equip:{},daily:'',streak:0,adDraw:'',races:0,tut:1}))"); await pg.route('**/*',route); await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(20000)
        await pg.click('#dailyOk'); await pg.tap('#tTap'); await pg.tap('.mbtn[data-go=speed]'); await pg.tap('#toCar'); await pg.tap('#startBtn'); await pg.wait_for_function("()=>__game.state==='race'",timeout=60000); await pg.wait_for_timeout(2500)
        h0=await pg.evaluate('()=>__game.player.heading')
        await pg.evaluate("()=>{window.__auto=false}"); print(await pg.evaluate("()=>{const z=document.getElementById('joyZone');const r=z.getBoundingClientRect();return [r.left,r.top,r.width,r.height,getComputedStyle(z).pointerEvents,getComputedStyle(document.getElementById('touch')).display]}")); await pg.evaluate(EV,['pointerdown',150,280]); await pg.evaluate(EV,['pointermove',100,280]); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='s_joy.png')
        h1=await pg.evaluate('()=>__game.player.heading'); print('heading change left',h1-h0, await pg.evaluate("()=>[document.getElementById('joyKnob').style.transform, __game.player.steerV, __game.player.speed, __game.state]"))
        await pg.evaluate(EV,['pointermove',150,280]); await pg.evaluate(EV,['pointerup',150,280]); await pg.wait_for_timeout(300)
        print(errs[:4]); await b.close()
asyncio.run(main())
