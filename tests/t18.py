import asyncio
from playwright.async_api import async_playwright
from common import route
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':852,'height':393}); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        async def rt(r):
            if r.request.url.startswith('http://localhost:8765'): await r.continue_()
            else: await route(r)
        await pg.route('**/*',rt)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(25000)
        r=await pg.evaluate("""async()=>{const regs=await navigator.serviceWorker.getRegistrations(); const ks=await caches.keys(); const c=ks.length?await caches.open(ks[0]):null; return [typeof __game, regs.length, regs[0]&&regs[0].active&&regs[0].active.state, ks, c?(await c.keys()).map(k=>k.url.split('/').pop()):0]}""")
        print(r); print('errs',errs[:4]); await b.close()
asyncio.run(main())
