import asyncio, os, json
from playwright.async_api import async_playwright
from common import route
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        ctx=await b.new_context(viewport={'width':1000,'height':640}); await ctx.grant_permissions(['clipboard-read','clipboard-write'])
        pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.route('**/*',route)
        await pg.goto('file://'+os.path.abspath('game.html')); await pg.wait_for_timeout(12000)
        js=lambda s: pg.evaluate(s)
        await js("()=>{const s=JSON.parse(localStorage.getItem('twq_save_v1')||'{}'); s.tut=1; s.coins=9000; s.cars=['taxi','truck','sedan','jeep']; s.last={mode:'item',stage:0,car:'jeep',diff:2,tod:'night'}; localStorage.setItem('twq_save_v1',JSON.stringify(s));}")
        await pg.reload(); await pg.wait_for_timeout(12000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        print('A 快速開跑文字(預期道具賽/越野方塊/困難/夜晚):', await js("()=>document.getElementById('quickTxt').textContent"))
        # B 每日挑戰 / 聯賽不蓋掉
        last0=await js("()=>JSON.stringify(JSON.parse(localStorage.twq_save_v1).last)")
        await js("()=>document.getElementById('mDaily').click()"); await pg.wait_for_function("()=>__game.state==='race'",timeout=60000)
        print('B1 每日挑戰後 last 不變:', last0==await js("()=>JSON.stringify(JSON.parse(localStorage.twq_save_v1).last)"))
        await js("()=>document.getElementById('menuBtn')&&0"); 
        await pg.reload(); await pg.wait_for_timeout(12000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        await js("()=>document.getElementById('mCup').click()"); await pg.wait_for_function("()=>__game.state==='race'",timeout=60000)
        print('B2 聯賽後 last 不變:', last0==await js("()=>JSON.stringify(JSON.parse(localStorage.twq_save_v1).last)"))
        # C 換設定：回主選單→計時賽→按開始，快速開跑應變成計時賽
        await pg.reload(); await pg.wait_for_timeout(12000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        await js("()=>document.querySelector('[data-go=trial]').click()"); await pg.wait_for_timeout(500)
        await js("()=>document.querySelector('#diff button[data-d=\"0\"]').click()")
        await js("()=>document.getElementById('startBtn').click()"); await pg.wait_for_function("()=>__game.state==='race'",timeout=60000)
        print('C1 換設定後 last:', await js("()=>JSON.stringify(JSON.parse(localStorage.twq_save_v1).last)"))
        await pg.reload(); await pg.wait_for_timeout(12000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        print('C2 重開後快速開跑文字:', await js("()=>document.getElementById('quickTxt').textContent"))
        await js("()=>document.getElementById('mQuick').click()"); await pg.wait_for_function("()=>__game.state==='race'",timeout=60000)
        print('C3 快速開跑進入比賽, 模式:', await js("()=>JSON.parse(localStorage.twq_save_v1).last.mode"))
        # D 統計 500 筆上限、複製
        await js("()=>{for(let i=0;i<650;i++) __game.Track.add('x',{i});}")
        n=await js("()=>__game.Track.get().length"); first=await js("()=>__game.Track.get()[0].d.i")
        print('D1 650次後筆數(預期500):',n,' 最舊保留的編號(預期150以上):',first)
        await pg.reload(); await pg.wait_for_timeout(12000)
        try: await pg.click('#dailyOk',timeout=3000)
        except Exception: pass
        for _ in range(5): await js("()=>document.getElementById('verTxt').click()")
        print('D2 統計視窗開啟:', await js("()=>!document.getElementById('statsBox').classList.contains('hidden')"))
        print('D3 統計文字前段:', (await js("()=>document.getElementById('statsTxt').innerText"))[:150].replace('\n',' | '))
        await js("()=>document.getElementById('statsCopy').click()"); await pg.wait_for_timeout(500)
        clip=await js("async()=>{try{return await navigator.clipboard.readText()}catch(e){return 'ERR '+e}}")
        try: print('D4 複製內容為合法 JSON、筆數:', len(json.loads(clip)))
        except Exception as e: print('D4 複製結果:', clip[:80])
        print('errs',errs[:5]); await b.close()
asyncio.run(main())
