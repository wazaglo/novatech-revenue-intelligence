import asyncio, json
from work.nav import connect, shot
async def askq(page, q, shot_name, min_wait=20, stable_rounds=3):
    box = page.locator("div[contenteditable=true], textarea").first
    await box.click()
    await box.fill(q)
    await asyncio.sleep(0.5)
    await box.press("Enter")
    prev = await page.inner_text("body")
    stable = 0; waited = 0
    while waited < 480:
        await asyncio.sleep(5); waited += 5
        if waited < min_wait: continue
        cur = await page.inner_text("body")
        if cur == prev:
            stable += 1
            if stable >= stable_rounds: break
        else:
            stable = 0; prev = cur
    await shot(page, shot_name, full=True)
    return prev
async def main():
    pw, br, ctx, _ = await connect()
    page = [p for p in ctx.pages if "quick" in p.url and "awsapps" not in p.url][0]
    await page.bring_to_front()
    await page.locator("text=NovaTech Revenue Intelligence").last.click()
    await asyncio.sleep(1.5)
    await page.get_by_role("button", name="Save").last.click()
    await asyncio.sleep(3)
    t = await page.evaluate("() => document.body.innerText")
    print("scoped:", "NovaTech Revenue Intelligence" in t)
    await shot(page, "275_topic_in_scope")
    qs = json.load(open("work/q_before.json"))
    results = {}
    for name, q in qs.items():
        after = name.replace("before", "after")
        body = await askq(page, q, f"qc_{after}")
        results[after] = {"q": q, "tail": body[-1500:]}
        print("="*25, after, "="*25)
        print(body[-1000:])
    json.dump(results, open("work/q_after.json.out","w"), indent=1)
asyncio.run(main())
