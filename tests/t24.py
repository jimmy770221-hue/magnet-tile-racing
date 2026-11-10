import asyncio, os
from playwright.async_api import async_playwright
from common import route
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1000,'height':700}); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.route('**/*',route)
        await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(10000)
        js=lambda s: pg.evaluate(s)
        await js("()=>{const s=JSON.parse(localStorage.getItem('twq_save_v1')||'{}'); s.tut=1; s.coins=30000; s.cars=['taxi','truck','sedan','jeep']; s.parts={engine:2,tire:4,susp:3,tank:1,gear:2,brake:0,exhaust:4,weight:1,aero:0,look:1,horn:0}; s.equip={engine:2,tire:4,susp:3,tank:1,gear:2,exhaust:4,weight:1,look:1}; localStorage.setItem('twq_save_v1',JSON.stringify(s));}")
        await pg.reload(); await pg.wait_for_timeout(10000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        await js("()=>document.getElementById('tTap').click()")
        await js("()=>document.getElementById('mGarage').click()"); await pg.wait_for_timeout(400)
        await pg.screenshot(path='s_garage1.png')
        await js("()=>document.getElementById('slotsList').scrollIntoView(false)")
        # 買 brake 藍→要先買綠
        await js("()=>[...document.querySelectorAll('.slotRow')][5].querySelectorAll('.lv')[2].click()"); 
        print('跳級購買:', await js("()=>(JSON.parse(localStorage.twq_save_v1).parts.brake)"))
        for k in (1,2,3,4): await js(f"()=>[...document.querySelectorAll('.slotRow')][5].querySelectorAll('.lv')[{k}].click()")
        print('煞車連買到橘:', await js("()=>JSON.stringify([JSON.parse(localStorage.twq_save_v1).parts.brake,JSON.parse(localStorage.twq_save_v1).coins])"))
        print('mods:', await js("()=>JSON.stringify(__game.getMods?__game.getMods():0)"))
        await pg.wait_for_timeout(300); await pg.screenshot(path='s_garage2.png',full_page=True)
        await js("()=>{const c=document.getElementById('slotsList'); c.scrollTop=9999; c.parentElement.scrollTop=9999;}"); await pg.wait_for_timeout(200); await pg.screenshot(path='s_garage3.png')
        print('errs',errs[:5]); await b.close()
asyncio.run(main())
