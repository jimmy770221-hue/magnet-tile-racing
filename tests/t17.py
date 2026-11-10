import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':852,'height':393}); errs=[]
        pg.on('console',lambda m: errs.append(m.text[:120]) if m.type=='error' else None); pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(20000)
        r=await pg.evaluate("""async()=>{const reg=await Promise.race([navigator.serviceWorker.ready,new Promise(r=>setTimeout(()=>r({active:{state:'timeout'}}),8000))]); const m=await (await fetch('manifest.webmanifest')).json(); const ks=await caches.keys(); const c=await caches.open(ks[0]); return [reg.active.state, m.name, ks, (await c.keys()).map(k=>k.url.split('/').pop())]}""")
        print(r); print('errs',errs[:4]); await b.close()
asyncio.run(main())
