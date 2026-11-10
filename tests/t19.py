import asyncio, os, json
from playwright.async_api import async_playwright
from common import route
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1000,'height':640}); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        pg.on('console',lambda m: errs.append(m.text[:150]) if m.type=='error' else None)
        await pg.route('**/*',route)
        await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(20000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        await pg.evaluate("()=>document.getElementById('tTap').click()")
        await pg.wait_for_function("()=>__game.state==='count'||__game.state==='race'",timeout=30000)
        print('進教學', await pg.evaluate("()=>[__game.state,document.getElementById('tutBox').textContent,!!__game.tutRun]"))
        await pg.evaluate("()=>{window.__ts=3}")
        await pg.wait_for_function("()=>__game.state==='race'",timeout=30000)
        await pg.screenshot(path='s_tut1.png')
        await pg.keyboard.down('ArrowLeft'); await pg.wait_for_timeout(1200)  # 1.5s game time @ts3 small
        txt=lambda: pg.evaluate("()=>document.getElementById('tutBox').textContent")
        for _ in range(12):
            t=await txt()
            if t.startswith('2'): break
            await pg.wait_for_timeout(500)
        print('步驟', await txt()); await pg.screenshot(path='s_tut2.png')
        await pg.keyboard.down('Shift')
        for _ in range(30):
            t=await txt()
            if t.startswith('4'): break
            await pg.wait_for_timeout(500)
        print('步驟', await txt())
        await pg.keyboard.up('Shift'); await pg.keyboard.up('ArrowLeft'); await pg.keyboard.press('z'); await pg.wait_for_timeout(300)
        for _ in range(10):
            t=await txt()
            if t.startswith('5') or t.startswith('6'): break
            await pg.wait_for_timeout(500)
        print('步驟', await txt())
        await pg.wait_for_function("()=>!document.getElementById('tutDone').classList.contains('hidden')",timeout=240000)
        print('完成', await pg.evaluate("()=>[document.getElementById('tutDoneTxt').textContent, JSON.parse(localStorage.twq_save_v1).tut, JSON.parse(localStorage.twq_save_v1).coins]"))
        await pg.screenshot(path='s_tutdone.png')
        await pg.evaluate("()=>document.getElementById('tutDoneOk').click()")
        # 快速開跑
        await pg.wait_for_timeout(500); await pg.screenshot(path='s_main2.png')
        print('quick',await pg.evaluate("()=>document.getElementById('quickTxt').textContent"))
        print('stats', await pg.evaluate("()=>__game.statsText()"))
        print('errs',errs[:5]); await b.close()
asyncio.run(main())
