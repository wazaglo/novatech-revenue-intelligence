# Dashboard Executive Summary

I kept the raw Amazon Q output below because the rubric asks for it. Don't quote
the Customer Health counts from it though - Q read them off the joined 63,420-row
model, so tickets and sentiment are inflated. I left my note at the bottom with
the real numbers.

Source: Amazon Q "My Assistant" summary of the published dashboard
**WA - NovaTech Revenue Intelligence Dashboard** (us-west-2, UdacityQuicksightLab),
captured 2026-09-05 21:55 GMT. See `screenshots/490_chat_summary.png`.

> Raw Q output - kept verbatim for audit:
>
> Here's a comprehensive summary of the key findings from the NovaTech Revenue Intelligence Dashboard, drawn from the Sales Pipeline, Marketing Funnel, and Customer Health sheets.
>
> ## Sales Pipeline
> - Total Deal Value: $707,201 across all deals.
> - Win Rate: Out of 499 total opportunities, 315 were Won and 184 were Lost - a win rate of approximately 63%.
> - Regional Performance: Central $274,285 (38.8%), West $248,243 (35.1%), East $184,673 (26.1%). The Central region leads in deal value, followed closely by the West; the East trails by a notable margin.
>
> ## Marketing Funnel
> - Total Campaign Responses: 609 across 6 campaigns.
> - Top-Performing Campaigns by Response: Digital Retarget (146), NovaPulse Launch (144), Q3 Growth Sprint (135).
> - Underperforming Campaigns: NovaEdge Awareness generated only 17 responses; Year-End Accelerator had 59.
> - Channel Insights: Partner Referral is the highest-spend channel across all campaigns but delivers mixed efficiency. Organic Search and Paid Social tend to deliver stronger response rates relative to spend for campaigns like Digital Retarget and Q3 Growth Sprint.
>
> ## Customer Health
> - Ticket Volume: The dashboard tracks support tickets across 85+ companies, with significant variation in ticket activity over the last 30 days.
> - Highest ticket volume: YieldMax Software (18,825 tickets) and LionGate Holdings (15,432 tickets) on the joined activity view.
> - Customer Sentiment Distribution: Neutral 42,249 (66.6%), Negative 13,939 (22.0%), Positive 6,110 (9.6%), Unknown 1,122 (1.8%). The majority of customer interactions are neutral, but negative sentiment (22%) significantly outweighs positive sentiment (9.6%) - a potential area of concern.

My read: Sales and Marketing above check out against pandas and the dashboard
KPI ($707,201, 315/499, 609 responses). The Customer Health part doesn't - real
source counts are YieldMax 334 tickets (not 18,825) and sentiment neutral 1,953 /
negative 684 / positive 304 / 59 nulls (see `ground_truth/ground_truth.txt`).
Same fan-out issue as Q log #2. If a number goes in a deck, I take it off the
dashboard sheet, not off this Q summary.
