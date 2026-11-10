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
        await js("()=>{const s=JSON.parse(localStorage.getItem('twq_save_v1')||'{}'); s.tut=1; s.coins=1000; s.parts={engine:2,tire:1,weight:2}; s.equip={engine:2,tire:1,weight:2}; localStorage.setItem('twq_save_v1',JSON.stringify(s));}")
        await pg.reload(); await pg.wait_for_timeout(10000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        sv=lambda: js("()=>{const s=JSON.parse(localStorage.twq_save_v1);return JSON.stringify({coins:s.coins,w:s.parts.weight,enh:s.enh})}")
        print('舊輕量化藍色退費後(預期約 1000+900+登入獎勵):', await sv())
        await js("()=>document.getElementById('tTap').click()")
        await js("()=>document.getElementById('mGarage').click()"); await pg.wait_for_timeout(300)
        print('欄位數(預期8):', await js("()=>document.querySelectorAll('.slotRow').length"))
        m0=await js("()=>JSON.stringify(__game.getMods())")
        c0=await js("()=>JSON.parse(localStorage.twq_save_v1).coins")
        for _ in range(3): await js("()=>document.querySelectorAll('.slotRow')[0].querySelector('.eBtn').click()")
        await js("()=>document.querySelectorAll('.slotRow')[3].querySelector('.eBtn').click()")
        c1=await js("()=>JSON.parse(localStorage.twq_save_v1).coins")
        print('強化引擎x3+氮氣瓶x1 花費(預期200+400+600+125=1325):', c0-c1, await sv())
        print('強化前:', m0); print('強化後:', await js("()=>JSON.stringify(__game.getMods())"))
        await js("()=>{const s=JSON.parse(localStorage.twq_save_v1); s.coins=99999; s.enh={engine:4}; localStorage.twq_save_v1=JSON.stringify(s)}")
        await pg.reload(); await pg.wait_for_timeout(9000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        await js("()=>document.getElementById('tTap').click()"); await js("()=>document.getElementById('mGarage').click()"); await pg.wait_for_timeout(300)
        await js("()=>document.querySelectorAll('.slotRow')[0].querySelector('.eBtn').click()"); 
        print('強化滿後按鈕:', await js("()=>document.querySelectorAll('.slotRow')[0].querySelector('.eBtn').textContent"))
        await pg.screenshot(path='s_enh.png')
        print('errs',errs[:5]); await b.close()
asyncio.run(main())
