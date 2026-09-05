import asyncio, json
from work.nav import connect, shot
async def askq(page, q, shot_name, min_wait=20, stable_rounds=3):
    box = page.locator("div[contenteditable=true], textarea").first
    await box.click(); await box.fill(q); await asyncio.sleep(0.5); await box.press("Enter")
    prev = await page.inner_text("body"); stable=0; waited=0
    while waited < 420:
        await asyncio.sleep(5); waited += 5
        if waited < min_wait: continue
        cur = await page.inner_text("body")
        if cur == prev:
            stable += 1
            if stable >= stable_rounds: break
        else: stable=0; prev=cur
    await shot(page, shot_name, full=True)
    return prev
QS = {
 "qlog2_deal_size_by_company": "What is the average deal size by company size?",
 "qlog3_resolution_crit_low": "What is the average resolution time for critical vs. low-priority tickets?",
 "qlog4_top10_accounts": "What are the top 10 accounts by support ticket volume, and what is their total deal revenue?",
 "qlog5_spend_gt_earn": "Are there any campaigns where we spent more than we earned back?",
}
async def main():
    pw, br, ctx, _ = await connect()
    page = [p for p in ctx.pages if "quick" in p.url and "awsapps" not in p.url][0]
    await page.bring_to_front()
    out = {}
    for name, q in QS.items():
        body = await askq(page, q, f"qc_{name}")
        out[name] = {"q": q, "tail": body[-1800:]}
        print("="*22, name, "="*22)
        print(body[-700:])
    json.dump(out, open("work/qlog_answers2.json","w"), indent=1)
asyncio.run(main())
