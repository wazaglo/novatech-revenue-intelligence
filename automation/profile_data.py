import pandas as pd
from pathlib import Path

base = Path("/home/wazaglo/udacity/project-starter-resources/Structured Data")
crm = pd.read_csv(base / "novatech_crm_deals.csv")
mkt = pd.read_csv(base / "novatech_marketing_campaigns.csv")
sup = pd.read_csv(base / "novatech_support_tickets.csv")

out = []
def p(*a):
    line = " ".join(str(x) for x in a)
    out.append(line)
    print(line)

for name, df in [("CRM", crm), ("MKT", mkt), ("SUP", sup)]:
    p(f"\n===== {name} shape={df.shape}")
    p(df.dtypes.to_string())
    p("nulls:", {c: int(n) for c, n in df.isna().sum().items() if n > 0})

# CRM facts
p("\n-- CRM --")
p("unique accounts:", crm.account_id.nunique(), "unique opportunities:", crm.opportunity_id.nunique())
p("deal_stage counts:", crm.deal_stage.value_counts().to_dict())
p("date range created:", crm.deal_created_date.min(), crm.deal_created_date.max())
p("date range closed:", crm.deal_closed_date.min(), crm.deal_closed_date.max())
p("total won revenue:", round(crm.loc[crm.deal_stage == 'Won', 'deal_value'].sum(), 2))
p("avg won deal value:", round(crm.loc[crm.deal_stage == 'Won', 'deal_value'].mean(), 2))
p("win rate:", round((crm.deal_stage == 'Won').mean() * 100, 2), "%")
p("loss reasons:", crm.loss_reason.value_counts(dropna=False).to_dict())
p("revenue by region:", crm.groupby('sales_region').apply(lambda d: d.loc[d.deal_stage=='Won','deal_value'].sum(), include_groups=False).round(2).to_dict())
p("win rate by region:", crm.groupby('sales_region').deal_stage.apply(lambda s: round((s=='Won').mean()*100,2)).to_dict())
crm['dtc'] = (pd.to_datetime(crm.deal_closed_date) - pd.to_datetime(crm.deal_created_date)).dt.days
p("avg days to close (won):", round(crm.loc[crm.deal_stage=='Won','dtc'].mean(), 1))
p("avg days to close (lost):", round(crm.loc[crm.deal_stage=='Lost','dtc'].mean(), 1))
p("avg days to close (all):", round(crm.dtc.mean(), 1))
p("revenue by product_category:", crm.groupby('product_category').apply(lambda d: d.loc[d.deal_stage=='Won','deal_value'].sum(), include_groups=False).round(2).to_dict())
p("revenue by company_size_tier:", crm.groupby('company_size_tier').apply(lambda d: d.loc[d.deal_stage=='Won','deal_value'].sum(), include_groups=False).round(2).to_dict())
p("won deals value by segment via mkt? skip")

# MKT facts
p("\n-- MKT --")
p("unique accounts:", mkt.account_id.nunique(), "leads:", mkt.lead_id.nunique())
p("campaign_date range:", mkt.campaign_date.min(), mkt.campaign_date.max())
p("response rate:", round(mkt.campaign_response.mean()*100, 2), "%", "responded:", int(mkt.campaign_response.sum()))
p("funnel_stage counts:", mkt.funnel_stage.value_counts().to_dict())
p("orphan accounts:", int(mkt.account_id.str.match(r'ACCT-1(0[1-9]|1[0-5])').sum()))
p("total campaign spend:", round(mkt.campaign_spend.sum(), 2))
p("total revenue attributed:", round(mkt.revenue_attributed.sum(), 2))
p("ROI by channel:", ((mkt.groupby('campaign_channel').revenue_attributed.sum() - mkt.groupby('campaign_channel').campaign_spend.sum()) / mkt.groupby('campaign_channel').campaign_spend.sum() * 100).round(1).to_dict())
p("spend/rev/roi by campaign:")
g = mkt.groupby('campaign_name').agg(spend=('campaign_spend','sum'), rev=('revenue_attributed','sum'), leads=('lead_id','count'), resp=('campaign_response','mean'))
g['roi_pct'] = ((g.rev - g.spend)/g.spend*100).round(1)
g['resp_pct'] = (g.resp*100).round(1)
p(g[['spend','rev','leads','resp_pct','roi_pct']].round(2).to_string())
p("response rate by channel:", (mkt.groupby('campaign_channel').campaign_response.mean()*100).round(1).to_dict())
p("leads by channel:", mkt.campaign_channel.value_counts().to_dict())
p("leads by segment:", mkt.customer_segment.value_counts().to_dict())
p("closed won leads:", int((mkt.funnel_stage=='Closed Won').sum()))

# SUP facts
p("\n-- SUP --")
p("unique accounts:", sup.account_id.nunique(), "tickets:", sup.ticket_id.nunique())
p("created range:", sup.ticket_created_date.min(), sup.ticket_created_date.max())
p("priority counts:", sup.priority.value_counts().to_dict())
p("unresolved (null resolved):", int(sup.ticket_resolved_date.isna().sum()))
p("orphan rows:", int(sup.account_id.str.match(r'ACCT-1(0[1-9]|11[0-5])').sum()))
p("avg resolution days:", round((pd.to_datetime(sup.ticket_resolved_date) - pd.to_datetime(sup.ticket_created_date)).dt.total_seconds().div(86400).mean(), 2))
sup['res_days'] = (pd.to_datetime(sup.ticket_resolved_date) - pd.to_datetime(sup.ticket_created_date)).dt.total_seconds()/86400
p("avg resolution days by priority:", sup.groupby('priority').res_days.mean().round(2).to_dict())
p("product area counts:", sup.product_area.value_counts().to_dict())
p("avg resolution by product area:", sup.groupby('product_area').res_days.mean().round(2).to_dict())
p("sentiment:", sup.customer_sentiment.value_counts().to_dict())
p("region counts:", sup.region.value_counts().to_dict())
p("customer_tier counts:", sup.customer_tier.value_counts().to_dict())
p("total downtime:", int(sup.downtime_minutes.sum()))
p("security incidents:", int(sup.security_incident.sum()), "data loss:", int(sup.data_loss.sum()), "payment impact:", int(sup.payment_impact.sum()))
top_accts = sup.account_id.value_counts().head(10)
p("top 10 accounts by tickets:", top_accts.to_dict())

# cross-domain
crm_accts = set(crm.account_id)
sup['days_open'] = sup.ticket_created_date
recent = sup[pd.to_datetime(sup.ticket_created_date) >= '2025-01-01']
p("\n-- CROSS --")
p("crm accts:", len(crm_accts), "mkt accts in crm:", len(set(mkt.account_id) & crm_accts), "sup accts in crm:", len(set(sup.account_id) & crm_accts))
acct_val = crm[crm.deal_stage=='Won'].groupby('account_id').deal_value.sum()
acct_tix = sup.account_id.value_counts()
both = pd.DataFrame({'value': acct_val, 'tickets': acct_tix}).dropna()
p("top accounts won-value x tickets:", both.sort_values('value', ascending=False).head(8).round(0).to_string())
neg = sup[sup.customer_sentiment=='negative'].account_id.value_counts()
risk = pd.DataFrame({'value': acct_val, 'tickets': acct_tix, 'neg': neg}).dropna(subset=['neg'])
p("risk candidates (high value + neg tickets):", risk.sort_values('value', ascending=False).head(8).round(0).to_string())
p("avg won deal value for accts with >3 tickets_last_30:", round(crm[(crm.deal_stage=='Won') & crm.account_id.isin(sup[sup.tickets_last_30_days>3].account_id)].deal_value.mean(), 2))
pr_accts = set(mkt[mkt.campaign_channel=='Partner Referral'].account_id)
sub = crm[crm.account_id.isin(pr_accts)]
p("win rate for Partner Referral sourced accounts:", round((sub.deal_stage=='Won').mean()*100, 2), "%", "deals:", len(sub))

# join fan-out estimate: crm LEFT JOIN mkt on account_id, LEFT JOIN sup on account_id
fan = crm.merge(mkt.groupby('account_id').size().rename('m'), left_on='account_id', right_index=True, how='left')
fan['m'] = fan.m.fillna(1)
fan = fan.merge(sup.groupby('account_id').size().rename('s'), left_on='account_id', right_index=True, how='left')
fan['s'] = fan.s.fillna(1)
p("est. 2-way join fanout rows (deals x mkt):", int((crm.merge(mkt, on='account_id', how='left').shape[0])))
p("est unified full join rows:", int((fan.m*fan.s).sum()))

Path("/home/wazaglo/udacity/work").mkdir(exist_ok=True)
Path("/home/wazaglo/udacity/work/ground_truth.txt").write_text("\n".join(out))
