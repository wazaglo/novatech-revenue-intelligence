import asyncio, json
from work.nav import connect, shot
async def ask(page, q, shot_name, min_wait=20, stable_rounds=3):
    box = page.locator("div[contenteditable=true], textarea").first
    await box.click()
    await box.fill(q)
    await asyncio.sleep(0.5)
    await box.press("Enter")
    prev = await page.inner_text("body")
    stable = 0; waited = 0
    while waited < 600:
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
    await page.goto("https://us-west-2.quicksight.aws.amazon.com/sn/account/UdacityQuicksightLab/start/chat", wait_until="domcontentloaded")
    await asyncio.sleep(8)
    nc = page.get_by_role("button", name="New chat")
    if await nc.count():
        await nc.first.click(); await asyncio.sleep(4)
    chip = page.locator("text=All data").first
    await chip.click(); await asyncio.sleep(2.5)
    opt = page.get_by_text("Specific data")
    if await opt.count():
        await opt.first.click(); await asyncio.sleep(2)
        for ds in ["novatech_crm_deals", "novatech_marketing_campaigns", "novatech_support_tickets"]:
            try:
                await page.locator(f"text={ds}").first.click(timeout=5000); await asyncio.sleep(1)
            except Exception: print("miss", ds)
    for label in ["Done","Apply","Confirm","Save"]:
        b = page.get_by_role("button", name=label)
        if await b.count() and await b.first.is_visible():
            await b.first.click(); break
    await asyncio.sleep(2)
    await shot(page, "252_scope_set")
    qs = json.load(open("work/q_before.json"))
    results = {}
    for name, q in qs.items():
        body = await ask(page, q, f"qc_{name}")
        results[name] = {"q": q, "tail": body[-1500:]}
        print("="*25, name, "="*25)
        print(body[-1200:])
    json.dump(results, open("work/q_before.json.out","w"), indent=1)
asyncio.run(main())
