import asyncio, os
from playwright.async_api import async_playwright
from common import route
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1000,'height':700}); await pg.route('**/*',route)
        await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(10000)
        js=lambda s: pg.evaluate(s)
        await js("()=>{const s=JSON.parse(localStorage.getItem('twq_save_v1')||'{}'); s.tut=1; s.parts={weight:4}; s.equip={weight:4}; localStorage.setItem('twq_save_v1',JSON.stringify(s));}")
        await pg.reload(); await pg.wait_for_timeout(10000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        await js("()=>document.getElementById('tTap').click()")
        await js("()=>document.getElementById('mGarage').click()"); await pg.wait_for_timeout(400)
        print('欄位數:', await js("()=>document.querySelectorAll('.slotRow').length"))
        row=(await pg.query_selector_all('.slotRow'))[7]; await row.scroll_into_view_if_needed(); await pg.wait_for_timeout(200)
        await row.screenshot(path='s_weight.png'); await b.close()
asyncio.run(main())
