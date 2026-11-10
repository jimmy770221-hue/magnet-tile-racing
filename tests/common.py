import asyncio, sys, os
from playwright.async_api import async_playwright

NM = os.path.abspath('node_modules/three')

async def route(r):
    url = r.request.url
    if 'cdn.jsdelivr.net/npm/three@0.170.0/' in url:
        rel = url.split('three@0.170.0/')[1]
        p = os.path.join(NM, rel)
        if os.path.exists(p):
            return await r.fulfill(path=p, content_type='application/javascript')
    if 'fonts.g' in url:
        return await r.fulfill(body='', content_type='text/css')
    return await r.continue_()

async def main():
    shots = sys.argv[1:] if len(sys.argv) > 1 else []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome',
                                    args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        pg = await b.new_page(viewport={'width': 1100, 'height': 700})
        errs = []
        pg.on('console', lambda m: errs.append(m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append('PAGEERR: ' + str(e)))
        await pg.route('**/*', route)
        await pg.goto('file://' + os.path.abspath('game.html'))
        await pg.wait_for_timeout(4000)
        print('loadMsg:', await pg.inner_text('#loadMsg'))
        await pg.screenshot(path='shot_menu.png')
        await pg.click('#startBtn')
        await pg.wait_for_timeout(2000)
        await pg.screenshot(path='shot_count.png')
        await pg.wait_for_timeout(9000)
        # drive: hold up, steer with simple autopilot via evaluating game state
        await pg.keyboard.down('ArrowUp')
        for k in range(60):
            info = await pg.evaluate('''()=>{const g=window.__game, p=g.player; return {idx:p.idx, lap:p.lap, spd:p.speed, state:g.state}}''')
            # crude steering: use AI-like logic inside the page
            await pg.evaluate('''()=>{const g=window.__game,p=g.player; const rs=g.racers();}''')
            await pg.wait_for_timeout(250)
            if k == 12:
                await pg.screenshot(path='shot_race1.png')
            if k == 20:
                await pg.keyboard.down('ArrowLeft'); await pg.keyboard.down('Space')
            if k == 26:
                await pg.screenshot(path='shot_drift.png')
                await pg.keyboard.up('Space'); await pg.keyboard.up('ArrowLeft')
        print('final', info)
        st = await pg.evaluate('''()=>window.__game.standings().map(r=>[r.name,r.lap,r.idx,Math.round(r.speed)])''')
        print('standings', st)
        await pg.screenshot(path='shot_race2.png')
        print('\n'.join(errs[:20]))
        await b.close()

if __name__=="__main__": asyncio.run(main())
