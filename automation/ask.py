import asyncio, json, sys
from work.nav import connect, shot

async def ask(page, q, shot_name, min_wait=20, stable_rounds=3):
    box = page.locator("div[contenteditable=true], textarea").first
    await box.click()
    await box.fill(q)
    await asyncio.sleep(0.5)
    await box.press("Enter")
    prev = await page.inner_text("body")
    stable = 0
    waited = 0
    while waited < 600:
        await asyncio.sleep(5)
        waited += 5
        if waited < min_wait:
            continue
        cur = await page.inner_text("body")
        if cur == prev:
            stable += 1
            if stable >= stable_rounds:
                break
        else:
            stable = 0
            prev = cur
    await shot(page, shot_name, full=True)
    return prev

async def main():
    qs = json.load(open(sys.argv[1]))
    pw, br, ctx, _ = await connect()
    page = [p for p in ctx.pages if "quick" in p.url and "awsapps" not in p.url][0]
    await page.bring_to_front()
    results = {}
    for name, q in qs.items():
        body = await ask(page, q, f"qc_{name}")
        results[name] = {"q": q, "body_tail": body[-2200:]}
        print("=" * 30, name, "=" * 30)
        print(body[-2200:])
    json.dump(results, open(sys.argv[2], "w"), indent=1)
asyncio.run(main())
