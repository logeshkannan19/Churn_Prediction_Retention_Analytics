"""
POWER BI DASHBOARD SPECIFICATION
================================
Comprehensive dashboard design for Customer Churn Analysis
Suitable for executive and operational teams.

Dashboard Name: Telecom Customer Churn Command Center
"""

DASHBOARD_SPECIFICATION = """

================================================================================
POWER BI DASHBOARD SPECIFICATION
================================================================================

DASHBOARD NAME: Customer Churn Command Center
PURPOSE: Real-time monitoring of customer churn metrics and retention performance
TARGET AUDIENCE: Executive leadership, Marketing, Customer Success teams
REFRESH FREQUENCY: Daily

================================================================================
PAGE 1: EXECUTIVE DASHBOARD (Home)
================================================================================

LAYOUT: Full-width header with navigation tabs below

HEADER SECTION:
┌─────────────────────────────────────────────────────────────────────────────┐
│  📊 CUSTOMER CHURN COMMAND CENTER                    [Date] [Refresh] [Filter]│
│      Last Updated: March 2025 | Data Source: Customer Database              │
└─────────────────────────────────────────────────────────────────────────────┘

KPI CARDS ROW (Top - 10 KPIs):
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ TOTAL         │ │ CHURN RATE   │ │ RETENTION    │ │ AT-RISK      │
│ CUSTOMERS     │ │              │ │ RATE         │ │ CUSTOMERS    │
│ 7,500         │ │ 26.5%        │ │ 73.5%        │ │ 1,988        │
│ ▲ 2.3% MoM   │ │ ▼ 1.2% MoM   │ │ ▲ 1.2% MoM  │ │ ▲ 5.1% MoM  │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ MONTHLY       │ │ ANNUAL REV   │ │ AVG CUSTOMER │ │ AVG CSAT     │
│ REVENUE       │ │ AT RISK      │ │ LIFETIME     │ │ SCORE        │
│ $450,234      │ │ $142,925     │ │ 28.4 months  │ │ 7.2/10       │
│ ▲ 3.1% MoM   │ │ ▼ 2.1% MoM  │ │ ▲ 1.5 MoM   │ │ ▲ 0.3 pts   │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

┌──────────────┐ ┌──────────────┐
│ HIGH-RISK     │ │ CRITICAL     │
│ SEGMENTS      │ │ ACTIONS      │
│ 3             │ │ 147          │
│ Due Today     │ │ Pending      │
└──────────────┘ └──────────────┘

VISUALIZATIONS (2x2 Grid):

┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│ CHURN TREND LINE CHART          │ │ CHURN BY CONTRACT TYPE          │
│                                 │ │                                 │
│ Shows monthly churn rate        │ │ Pie or donut chart:             │
│ over past 12 months             │ │ - Month-to-Month: 42%           │
│ Goal line at 25%                │ │ - One Year: 28%                 │
│                                 │ │ - Two Year: 15%                 │
│ [Line chart with area fill]     │ │                                 │
└─────────────────────────────────┘ └─────────────────────────────────┘

┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│ CUSTOMER SEGMENT DISTRIBUTION   │ │ CHURN RISK DISTRIBUTION         │
│                                 │ │                                 │
│ Stacked bar by segment:         │ │ Gauge chart showing:            │
│ - New: 18% (HIGH RISK)          │ │ Current: 26.5%                   │
│ - Developing: 25%               │ │ Target: <25%                     │
│ - Established: 32%              │ │ Best: 20%                        │
│ - Loyal: 25%                    │ │                                 │
└─────────────────────────────────┘ └─────────────────────────────────┘

BOTTOM SECTION - ALERTS & ACTIONS:
┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚠️ HIGH PRIORITY ALERTS                                    [View All Actions]│
│ ───────────────────────────────────────────────────────────────────────────│
│ • 147 customers flagged as "Critical" risk tier                   [Action]│
│ • Month-to-month segment exceeded 40% churn threshold             [Review] │
│ • Electronic check users showing 35% churn trend                 [Review] │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
PAGE 2: SEGMENT ANALYSIS
================================================================================

LAYOUT: Left sidebar filters + Main content area

LEFT SIDEBAR FILTERS:
┌─────────────────────┐
│ 📊 FILTERS          │
├─────────────────────┤
│ Customer Segment    │
│ ☑ All              │
│ ☐ New              │
│ ☐ Developing       │
│ ☐ Established      │
│ ☐ Loyal            │
├─────────────────────┤
│ Contract Type      │
│ ☐ Month-to-Month   │
│ ☐ One Year         │
│ ☐ Two Year         │
├─────────────────────┤
│ Risk Tier          │
│ ☐ Critical         │
│ ☐ High             │
│ ☐ Medium           │
│ ☐ Low              │
└─────────────────────┘

MAIN VISUALIZATIONS:

┌─────────────────────────────────────────────────────────────────────────────┐
│ SEGMENT PERFORMANCE MATRIX                                                   │
│                                                                              │
│              │ Retained │ Churned │ Churn Rate │ Revenue │ Revenue at Risk │
│ ────────────┼──────────┼─────────┼────────────┼─────────┼─────────────────│
│ New         │ 1,162    │ 422     │ 26.7%       │ $89,234 │ $28,456         │
│ Developing  │ 1,512    │ 312     │ 17.1%       │ $112,890│ $19,234         │
│ Established │ 1,891    │ 198     │ 9.5%        │ $134,567│ $12,890         │
│ Loyal       │ 1,688    │ 115     │ 6.4%        │ $113,543│ $7,234          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│ CHURN RATE BY SEGMENT           │ │ REVENUE IMPACT BY SEGMENT        │
│ (Horizontal bar chart)          │ │ (Stacked bar - retained/lost)    │
│                                 │ │                                 │
│ New:        ██████████████ 26.7%│ │ [$][$][$][$][$][$][X][X] New    │
│ Developing: ████████ 17.1%       │ │ [$][$][$][$][X] Develop  │
│ Establish:  ████ 9.5%           │ │ [$][$][$][X] Established │
│ Loyal:      ███ 6.4%            │ │ [$][$][$][$][$][$][$][X] Loyal   │
└─────────────────────────────────┘ └─────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ SEGMENT DETAIL CARDS (4 columns)                                            │
│                                                                              │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│ │ NEW (0-12m) │ │ DEVELOPING   │ │ ESTABLISHED │ │ LOYAL       │          │
│ │             │ │ (13-36m)     │ │ (37-60m)    │ │ (60m+)      │          │
│ │ Count: 1,584│ │ Count: 1,824 │ │ Count: 2,089│ │ Count: 1,803│          │
│ │ Churn: 26.7%│ │ Churn: 17.1% │ │ Churn: 9.5% │ │ Churn: 6.4% │          │
│ │ Avg Rev: $56│ │ Avg Rev: $62 │ │ Avg Rev: $64│ │ Avg Rev: $63│          │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
PAGE 3: TENURE DISTRIBUTION
================================================================================

LAYOUT: Funnel visualization + Distribution charts

┌─────────────────────────────────────────────────────────────────────────────┐
│ TENURE CHURN FUNNEL                                                           │
│                                                                              │
│ Total Customers ──────────── 7,500                                          │
│            │                                                                  │
│            ▼                                                                  │
│ Tenure 0-6 months ───────── 1,500 ── Churned: 475 ── Rate: 31.7%          │
│            │                                                                  │
│            ▼                                                                  │
│ Tenure 7-12 months ──────── 1,125 ── Churned: 312 ── Rate: 27.7%          │
│            │                                                                  │
│            ▼                                                                  │
│ Tenure 13-24 months ──────── 1,500 ── Churned: 345 ── Rate: 23.0%          │
│            │                                                                  │
│            ▼                                                                  │
│ Tenure 25-48 months ──────── 2,250 ── Churned: 338 ── Rate: 15.0%          │
│            │                                                                  │
│            ▼                                                                  │
│ Tenure 49-72 months ──────── 1,125 ── Churned: 90 ──── Rate: 8.0%          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│ TENURE HISTOGRAM                 │ │ CHURN RATE BY TENURE            │
│ (Histogram with churn overlay)   │ │ (Line chart showing decay)     │
│                                 │ │                                 │
│ █                               │ │ 35%│╲                           │
│ █ █                             │ │ 30%│  ╲                         │
│ █ █ █                           │ │ 25%│    ╲                       │
│ █ █ █ █                         │ │ 20%│      ╲____                 │
│ █ █ █ █ █                       │ │ 15%│            ╲___           │
│ █ █ █ █ █ █ █                   │ │ 10%│                  ╲___       │
│ █ █ █ █ █ █ █ █ █               │ │  5%│                       ╲____│
│ ───────────────────────────     │ │  0%───────────────────────────│
│ 0  12  24  36  48  60  72      │ │     0   12   24   36   48      │
└─────────────────────────────────┘ └─────────────────────────────────┘

================================================================================
PAGE 4: SERVICE ANALYSIS
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│ SERVICE ADOPTION & IMPACT                                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐ ┌─────────────────────────────────────────┐
│ SERVICE ADOPTION RATES          │ │ CHURN RATE BY SERVICE COUNT             │
│ (Donut charts in row)           │ │ (Horizontal bar)                        │
│                                 │ │                                         │
│ Online Security: 35%            │ │ 0 services: █████████████████████ 38%  │
│ Online Backup: 40%              │ │ 1 service:  ████████████████     28%  │
│ Device Protection: 42%          │ │ 2 services: ██████████           21%  │
│ Tech Support: 38%              │ │ 3 services: ██████               15%  │
│ Streaming TV: 55%               │ │ 4 services: ███                 10%  │
│ Streaming Movies: 55%           │ │ 5+ services: █                 5%   │
└─────────────────────────────────┘ └─────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ SERVICE COMBINATION MATRIX                                                    │
│                                                                              │
│                  │ Has Security │ No Security │ Churn Diff                  │
│ ────────────────┼──────────────┼──────────────┼─────────                    │
│ Has Support     │ 12.5%        │ 22.3%        │ -9.8%                       │
│ No Support      │ 28.4%        │ 35.2%        │ -6.8%                       │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
PAGE 5: FINANCIAL IMPACT
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│ REVENUE DASHBOARD                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

TOP KPI ROW:
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ TOTAL MRR    │ │ CHURNED MRR  │ │ RETAINED MRR │ │ ANNUAL IMPACT│
│ $450,234     │ │ $119,312     │ │ $330,922     │ │ $1,431,744   │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

VISUALIZATIONS:
┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│ MONTHLY REVENUE WATERFALL       │ │ REVENUE BY SEGMENT              │
│                                 │ │ (Treemap)                       │
│ Start: $450,234                 │ │                                 │
│ Less: Churn ($119,312)          │ │ [New $89K] [Dev $113K]         │
│ End: $330,922                   │ │ [Est $135K] [Loyal $114K]      │
│                                 │ │                                 │
│ [Waterfall chart]               │ │ [Treemap with $ values]        │
└─────────────────────────────────┘ └─────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ CUSTOMER LIFETIME VALUE ANALYSIS                                              │
│                                                                              │
│ Segment    │ Avg CLV  │ Current │ Potential │ Gap                          │
│ ──────────┼─────────┼─────────┼───────────┼─────────                     │
│ New       │ $1,584   │ $1,200  │ $2,500    │ $1,300                       │
│ Developing│ $2,232   │ $1,890  │ $3,000    │ $1,110                       │
│ Established│ $4,096  │ $3,500  │ $4,500    │ $1,000                       │
│ Loyal     │ $4,608   │ $4,200  │ $5,000    │ $800                         │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
PAGE 6: RISK PREDICTION & ALERTS
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│ ML-POWERED RISK PREDICTIONS                                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐ ┌─────────────────────────────────────────┐
│ RISK TIER DISTRIBUTION          │ │ CHURN PROBABILITY HISTOGRAM             │
│ (Donut chart)                   │ │                                         │
│                                 │ │    █                                   │
│ Critical: 8% (600 customers)    │ │   █ █                                  │
│ High: 18% (1,350 customers)    │ │  █ █ █                                 │
│ Medium: 32% (2,400 customers)  │ │ █ █ █ █    █                           │
│ Low: 42% (3,150 customers)     │ │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓            │
│                                 │ │ 0%   25%   50%   75%  100%             │
│ [Donut chart with drill-down]   │ │     Churn Probability Score            │
└─────────────────────────────────┘ └─────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ HIGH-RISK CUSTOMER LIST (Top 50)                                              │
│ Sortable, Filterable Table with Actions                                      │
│                                                                              │
│ Customer ID │ Tenure │ Contract │ Monthly Chg │ Churn Prob │ Risk │ Action   │
│ ─────────── ┼────────┼─────────┼────────────┼────────────┼──────┼───────── │
│ CUS0001234  │ 8 mo   │ M-t-M   │ $94.50     │ 87.3%      │ High │ [Offer]  │
│ CUS0005678  │ 11 mo  │ M-t-M   │ $89.00     │ 85.1%      │ High │ [Offer]  │
│ CUS0009012  │ 6 mo   │ M-t-M   │ $102.00    │ 83.4%      │ High │ [Offer]  │
│ ...         │ ...    │ ...     │ ...        │ ...        │ ...  │ ...      │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
PAGE 7: RETENTION TRACKER
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│ RETENTION PROGRAM PERFORMANCE                                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐ ┌─────────────────────────────────────────┐
│ CAMPAIGN EFFECTIVENESS          │ │ CAMPAIGN ROI TRACKER                    │
│ (Grouped bar chart)             │ │                                         │
│                                 │ │                                         │
│ Offer 1 (Contract): 34% conv   │ │ $150K invested → $450K saved            │
│ Offer 2 (Auto-pay): 28% conv   │ │ ROI: 200%                               │
│ Offer 3 (Bundle): 22% conv     │ │                                         │
│ Offer 4 (Price): 19% conv      │ │ [Gauge showing ROI vs target]           │
└─────────────────────────────────┘ └─────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ RETENTION OFFER PERFORMANCE TABLE                                             │
│                                                                              │
│ Offer Name        │ Sent │ Converted │ Savings │ Cost  │ ROI    │ Status     │
│ ─────────────────┼──────┼──────────┼─────────┼───────┼────────┼────────────│
│ Contract Upgrade │ 500  │ 170      │ $25,500 │ $8,500│ 200%   │ Active     │
│ Auto-Pay Enroll  │ 800  │ 224      │ $13,440 │ $4,000│ 236%   │ Active     │
│ Service Bundle   │ 600  │ 132      │ $7,920  │ $3,000│ 164%   │ Testing    │
│ Price Protection │ 400  │ 76       │ $9,120  │ $4,000│ 128%   │ Paused     │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
DESIGN GUIDELINES
================================================================================

COLOR PALETTE:
- Primary: #1E88E5 (Blue)
- Secondary: #43A047 (Green - for positive metrics)
- Accent: #E53935 (Red - for churn/alerts)
- Warning: #FB8C00 (Orange)
- Neutral: #78909C (Gray)
- Background: #FFFFFF (White) / #F5F5F5 (Light Gray)

TYPOGRAPHY:
- Headers: Segoe UI Semibold, 24px
- Subheaders: Segoe UI Semibold, 18px
- Body: Segoe UI, 12-14px
- KPI Values: Segoe UI Light, 28-32px

VISUALIZATION BEST PRACTICES:
- Use consistent color coding (Green=good, Red=churn)
- Include data labels on all charts
- Add trend indicators (▲▼) where applicable
- Include comparison periods (MoM, YoY)
- Use tooltips for detailed information

INTERACTIVITY:
- All charts should be clickable for drill-down
- Filters should be persistent across pages
- Export functionality for all tables
- Bookmarking for favorite views

================================================================================
IMPLEMENTATION NOTES
================================================================================

DATA SOURCES:
1. customer_data.csv - Main customer dataset
2. engineered_features.csv - ML-ready features
3. model_predictions.csv - Churn probability scores

CONNECTIONS:
- DirectQuery for real-time updates
- Scheduled refresh: Daily at 6 AM

SECURITY:
- Row-level security by customer segment
- Executive view shows aggregated data only
- Operational view allows customer-level drill-down

DEPLOYMENT:
- Publish to Power BI Workspace
- Create App for distribution
- Set up dashboard subscriptions for executives
- Configure mobile layout for iOS/Android

================================================================================
"""

def save_dashboard_spec():
    """Save Power BI dashboard specification."""
    with open('dashboard/powerbi_dashboard_spec.md', 'w') as f:
        f.write(DASHBOARD_SPECIFICATION)
    print("Power BI dashboard specification saved to dashboard/powerbi_dashboard_spec.md")


if __name__ == "__main__":
    save_dashboard_spec()
    print(DASHBOARD_SPECIFICATION)
