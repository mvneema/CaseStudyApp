import streamlit as st
import time

# Page config
st.set_page_config(
    page_title="Case Study Solver",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'practicing' not in st.session_state:
    st.session_state.practicing = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'show_solution' not in st.session_state:
    st.session_state.show_solution = False
if 'selected_case' not in st.session_state:
    st.session_state.selected_case = 'loyalty_program'

# Case data (we'll expand this)
CASES = {
    "loyalty_program": {
        "title": "Customer Loyalty Program Analysis",
        "difficulty": "Intermediate",
        "time": "15-20 min",
        "type": "Customer Retention",
        "skills": ["Metrics Definition", "Business Strategy", "Data Infrastructure"],
        "scenario": """You're a data analyst at a growing coffee shop chain (think Starbucks-style). The company has a mobile app with a loyalty program where customers can earn points, get promotional offers, and order ahead.

The Head of Marketing wants to better understand customer loyalty and optimize the program. She's come to you with several questions about customer behavior and program effectiveness.""",
        "questions": [
            "What metrics would you use to measure customer loyalty?",
            "Some customers only purchase coffee when they have promotional discount codes. Is this okay? How would you think about these customers?",
            "Not all customers use the app to make purchases - some pay with credit cards at the register without scanning their loyalty card. How would you track these purchases and connect them to customer profiles?",
            "You notice that certain customers consistently buy only coffee, while others buy coffee + bagel combos. The company wants to increase food attachment. What would you do?"
        ],
        "frameworks": ["RFM Analysis", "Customer Lifetime Value", "Market Basket Analysis", "Root Cause Analysis"],
        "solutions": {
            0: {
                "framework": "Think in categories - Behavioral, Engagement, and Economic metrics",
                "answer": """**Behavioral Metrics:**
- **Purchase frequency** - How often customers buy (daily/weekly/monthly)
- **Recency** - Days since last purchase (key part of RFM analysis)
- **Retention rate** - % of customers who return month-over-month
- **Churn rate** - % of customers who stop purchasing
- **Customer tenure** - How long they've been a customer

**Engagement Metrics:**
- **Repeat purchase rate** - % of customers who buy more than once
- **Product diversity** - Number of different items purchased
- **App engagement** - App logins, feature usage, time spent
- **Loyalty program participation** - Points earned/redeemed

**Economic Metrics:**
- **Customer Lifetime Value (CLV)** - Total revenue over customer relationship
- **Average order value (AOV)**
- **Margin per customer** - Revenue minus discounts/costs
- **Share of wallet** - What % of their coffee spend goes to us vs. competitors

**Key insight:** Prioritize RFM (Recency, Frequency, Monetary) as the core loyalty score, then supplement with CLV for long-term value.""",
                "good_points": [
                    "Mentioning CLV shows you understand long-term value",
                    "Including retention/churn shows you think about sustainability",
                    "Frequency and recency are core behavioral signals"
                ],
                "missing_points": [
                    "Segmenting metrics into categories (behavioral/engagement/economic)",
                    "Explicitly mentioning RFM framework",
                    "Considering margin, not just revenue",
                    "App engagement metrics for digital products"
                ]
            },
            1: {
                "framework": "Business tradeoffs analysis - think pros AND cons",
                "answer": """**It depends on the business goal and customer economics.**

**Arguments FOR keeping promo-only customers:**
- They still generate revenue and contribute to fixed costs
- Even discounted purchases likely have positive contribution margin
- They increase foot traffic and brand visibility
- Some may convert to full-price customers over time
- They might refer others or provide social proof

**Arguments AGAINST:**
- Low/negative customer profitability if discounts are too steep
- May never convert to full-price buyers (creates dependency)
- Taking promotional capacity from high-value customers
- Could devalue the brand perception

**Recommended approach:**
1. **Segment these customers** - Track their CLV, margin, conversion rate
2. **Calculate unit economics** - Are they profitable on contribution margin?
3. **Test conversion strategies** - Gradually reduce promo frequency
4. **Set thresholds** - Define acceptable promo-dependency levels

**Key question:** What's their lifetime value trajectory? New customers converting is different than long-term promo-dependent users.""",
                "good_points": [
                    "Acknowledging there are tradeoffs (not a simple yes/no)",
                    "Mentioning profitability/unit economics",
                    "Suggesting to segment and analyze, not just decide"
                ],
                "missing_points": [
                    "Specific mention of contribution margin",
                    "Testing/experimentation approach",
                    "Conversion rate tracking from promo → full price"
                ]
            },
            2: {
                "framework": "Data infrastructure & customer identity resolution",
                "answer": """**This is a customer identity resolution challenge. Here are the data sources and approaches:**

**Data Sources Available:**
1. **Credit/debit card transactions** - Partner with payment processors to get merchant-level data
2. **Loyalty card swipes** - Physical card scans at POS even without app
3. **Email receipts** - Collect email at checkout for digital receipts
4. **Phone number lookup** - Quick phone number entry at POS linked to account
5. **WiFi tracking** - Device IDs when customers connect to store WiFi (privacy considerations apply)

**Implementation Strategy:**

**Approach 1: Card-Linking Programs**
- Let customers register their credit/debit cards in the app (similar to Starbucks)
- When that card is used at ANY location, it auto-attributes to their profile
- This captures both app and non-app purchases

**Approach 2: Email/Phone Matching**
- Fuzzy matching between POS data (emails/phone numbers collected at register) and customer database
- Incentivize customers to provide contact info with points/discounts

**Approach 3: POS System Integration**
- Upgrade POS systems to prompt cashiers: "Do you have a loyalty account?"
- Quick phone number or email lookup at checkout
- Automatically links transaction to profile

**Approach 4: Merchant Category Tracking**
- Partner with credit card networks for merchant-level purchase data
- Track when registered cards are used at our locations

**The Goal:** Create a **unified customer view** across all channels (app, in-store, online). This is critical for:
- Accurate loyalty measurement
- Personalized recommendations
- Understanding true customer behavior

**Key Metrics to Track:**
- % of transactions we CAN attribute to known customers
- Gap between total transactions and attributed transactions
- Set goal to reduce unattributed purchases over time

**Privacy Note:** Be transparent about data collection and give customers control over what's tracked.""",
                "good_points": [
                    "Identifying card-linking as a solution shows knowledge of common loyalty program practices",
                    "Mentioning multiple data sources shows comprehensive thinking",
                    "Recognizing this as an identity resolution problem",
                    "Thinking about incentivizing customers to identify themselves"
                ],
                "missing_points": [
                    "Specific mention of 'unified customer view' as the goal",
                    "Privacy considerations and transparency",
                    "Tracking the % of unattributed transactions as a metric",
                    "POS system integration requirements"
                ]
            },
            3: {
                "framework": "Diagnose → Hypothesize → Test → Optimize",
                "answer": """**Step 1: Diagnose WHY customers aren't buying food**

First, run analysis to understand the root cause:

**Customer Segmentation:**
- **Timing analysis** - When do coffee-only purchases happen? (Afternoon vs. morning might explain it)
- **Price sensitivity** - Is food relatively more expensive than perceived value?
- **Demographic patterns** - Age, location, income level differences?
- **Purchase history** - Are these new customers or long-time coffee-only buyers?

**Data to Analyze:**
- **Market basket analysis** - What DO coffee buyers purchase together when they buy food?
- **Customer surveys** - Direct question: "Why don't you typically add food to your coffee order?"
- **Competitive analysis** - Do competitors have better food options or pricing?
- **Quality signals** - Check reviews, complaints, food ratings

**Step 2: Form Hypotheses Based on Diagnosis**

**Hypothesis 1: Awareness Issue**
- Customers don't know about food options
- Menu placement is poor
- Limited visibility of food items

**Hypothesis 2: Pricing/Value**
- Food is too expensive relative to value
- No attractive bundle pricing
- Competition offers better value

**Hypothesis 3: Quality/Variety**
- Food options aren't appealing
- Limited variety for different dayparts
- Quality concerns

**Hypothesis 4: Preference/Timing**
- Customers genuinely just want coffee
- Buying food elsewhere
- Coming at times when they don't want food

**Step 3: Test Interventions Based on Root Cause**

**If Awareness is the Issue:**
- ✅ In-app personalized recommendations: "Coffee lovers also enjoy..."
- ✅ POS prompts: Train baristas to suggest pairings
- ✅ Menu redesign: Better placement, add photos of combos
- ✅ Push notifications: "Try our new morning combo"

**If Pricing is the Issue:**
- ✅ Bundle discounts: "Add a bagel for $2 with any coffee"
- ✅ Time-based promotions: "$6 coffee + bagel special until 10am"
- ✅ Loyalty program: "Buy 10 coffees, get a free bagel"

**If Quality/Variety is the Issue:**
- ✅ Improve food offerings: Add variety, better quality
- ✅ Seasonal items: Rotate menu to keep it fresh
- ✅ Sample programs: Free bagel with 10th coffee purchase
- ✅ Customer co-creation: Survey what food they'd want

**If Preference is the Issue:**
- ✅ Accept some customers just want coffee
- ✅ Focus on upselling premium coffee instead (lattes, specialty drinks)
- ✅ Sell coffee-related merchandise (beans, mugs, subscriptions)

**Step 4: Measure & Optimize**

**Key Metrics to Track:**
- **Food attachment rate** - % of coffee transactions that include food
- **Incremental revenue per customer** - Did total basket size increase?
- **Margin impact** - Are we cannibalizing higher-margin items?
- **Customer satisfaction** - Did promotions affect experience negatively?
- **A/B test results** - Which intervention works best?

**Example A/B Test:**
- Control group: Standard menu
- Variant A: "Add a bagel for $2" prompt at checkout
- Variant B: Bundle pricing on menu
- Variant C: Barista verbal suggestion
- Measure which drives highest attachment rate

**Alternative Strategy to Consider:**

Maybe increasing food attachment ISN'T the best goal. Consider:
- **Premium coffee upsell** - If customers love coffee, sell them lattes, cold brew, specialty drinks
- **Coffee subscriptions** - Unlimited coffee for monthly fee
- **Retail products** - Coffee beans, brewing equipment, branded merchandise
- **Higher frequency** - If they come for coffee, make them come MORE often

**Key Insight:** The strategy depends on the business goal:
- Maximize revenue per customer?
- Increase overall margin?
- Build visit frequency?
- Improve customer satisfaction?

Always align the approach with what leadership cares about most.""",
                "good_points": [
                    "Using market basket analysis shows understanding of analytical techniques",
                    "Mentioning A/B testing for interventions",
                    "Thinking about different root causes (awareness, price, quality, preference)",
                    "Connecting to business goals rather than just suggesting tactics",
                    "Considering alternative strategies beyond just food attachment"
                ],
                "missing_points": [
                    "Explicit diagnose → hypothesize → test framework",
                    "Customer surveys as a direct feedback mechanism",
                    "Timing/daypart analysis",
                    "Measuring margin impact, not just revenue",
                    "Acknowledging some customers might just prefer coffee only"
                ]
            }
        },
        "common_mistakes": [
            "Jumping to solutions without clarifying business goals",
            "Only giving one-sided answers without showing tradeoffs",
            "Being too vague - use specific metrics and actions",
            "Ignoring data feasibility - acknowledge infrastructure needs",
            "Not connecting back to business impact"
        ],
        "key_takeaways": [
            "Structure your metrics into categories (behavioral/engagement/economic)",
            "Always think in tradeoffs for business questions",
            "Ask clarifying questions about business goals",
            "Connect analysis to actionable recommendations",
            "Use established frameworks (RFM, CLV) when applicable"
        ]
    },
    
    "reddit_comments": {
        "title": "Reddit Comments Drop - Root Cause Analysis",
        "difficulty": "Beginner",
        "time": "10-15 min",
        "type": "Root Cause Analysis",
        "skills": ["Problem Diagnosis", "MECE Framework", "Data Investigation"],
        "scenario": """You're a data analyst at Reddit. During your weekly metrics review, you notice that the total number of comments across the platform has decreased by 5% compared to last week.

Your manager asks you to investigate and identify the root cause of this decline. This is a critical engagement metric that the executive team monitors closely.""",
        "questions": [
            "Walk me through how you would diagnose why comments are down 5%. What's your approach?",
            "What specific data would you look at first to narrow down the cause?",
            "If you discover it's segment-specific (only affecting mobile users), how would you proceed?",
            "How would you validate your hypothesis and what would you recommend?"
        ],
        "frameworks": ["MECE Framework", "Root Cause Analysis", "Funnel Analysis", "Cohort Analysis"],
        "solutions": {
            0: {
                "framework": "Use MECE (Mutually Exclusive, Collectively Exhaustive) framework to systematically investigate: Internal, External, User Behavior, and Data/Measurement factors",
                "answer": """**Step 1: Clarify the Problem (Ask Questions First)**

Before jumping into analysis, I'd ask:
- **When exactly did this start?** - Sudden drop or gradual decline?
- **Where is it happening?** - All regions? Specific platforms (mobile/desktop)?
- **What type of comments?** - All comments or specific subreddits/types?
- **Any recent changes?** - New features, updates, policy changes?

**Step 2: Present My Framework (MECE)**

I'll investigate systematically across 4 categories:

**1. DATA/MEASUREMENT** - Is this a tracking issue?
**2. INTERNAL FACTORS** - Did we change anything?
**3. EXTERNAL FACTORS** - Market/competitor/seasonal effects?
**4. USER BEHAVIOR** - Have usage patterns shifted?

**Step 3: Systematically Investigate**

### **Category 1: DATA/MEASUREMENT** ⚠️ (Check FIRST)

**Why first?** Fastest to verify and eliminates false alarms.

**Questions to investigate:**
- Has our comment tracking changed?
- Was there a code deployment affecting logging?
- Did we change how we calculate "comments"? (e.g., now excluding deleted/spam?)
- Are we seeing this across all dashboards/reports?

**What to check:**
- Event logging errors
- Data pipeline issues
- Metric definition changes
- Attribution changes (comment counts on deleted posts?)

**If YES → Problem solved (data quality issue, not real decline)**
**If NO → Move to Internal Factors**

---

### **Category 2: INTERNAL FACTORS** 🔧

**Product changes, technical issues, process modifications**

**What to investigate:**

**A) Product/UX Changes:**
- Did we redesign the comment box?
- New authentication requirements (login wall)?
- UI changes making commenting harder? (extra clicks, smaller button)
- A/B tests running on commenting features?

**B) Technical Issues:**
- Server errors affecting comment submission?
- Mobile app bugs?
- API issues for third-party apps?
- Database performance problems?

**C) Policy/Moderation Changes:**
- Stricter spam filters removing more comments?
- New community guidelines?
- Auto-moderation rules tightened?
- Shadowban policy changes?

**Example hypothesis:**
"If we made commenting require an extra authentication step, that could reduce casual commenting by 5%."

**How to verify:**
- Check deployment logs for releases around the drop date
- Review feature flags/A/B tests
- Examine error logs and submission failure rates
- Compare comment submission funnel before/after

---

### **Category 3: EXTERNAL FACTORS** 🌍

**Market, competitors, seasonality, world events**

**What to investigate:**

**A) Seasonality/Calendar:**
- Is February historically lower engagement?
- Holiday effects (Presidents' Day weekend)?
- Back-to-school/work season patterns?

**B) Competition:**
- Did TikTok/Twitter/Discord launch viral features?
- Competitor pulling users away?
- New social platform trending?

**C) Major Events:**
- Breaking news event shifting attention?
- Sports events (Super Bowl week)?
- Natural disasters or crises?

**D) Economic/Industry:**
- Platform controversies affecting engagement?
- Regulatory changes?
- Internet outages in major regions?

**Example:**
"During Super Bowl week, users might browse Reddit but comment less because they're watching the game."

**How to verify:**
- Historical seasonality analysis (same week last year)
- Competitor feature launch tracking
- News cycle analysis
- Cross-platform engagement comparisons

---

### **Category 4: USER BEHAVIOR** 👥

**Changes in how users engage**

**What to investigate:**

**A) Segment Analysis:**
- New users vs. power users - who's commenting less?
- Desktop vs. mobile vs. app - platform breakdown?
- Geographic - specific countries/regions?
- Subreddit categories - which topics declining?

**B) Cohort Analysis:**
- Are specific user cohorts churning?
- New signups commenting less (onboarding issue)?
- Long-time users disengaging?

**C) Content Quality:**
- Are posts themselves less engaging?
- Fewer high-quality posts to comment on?
- Content moderation affecting discussion quality?

**D) User Journey:**
- Friction points in commenting flow?
- Login/authentication barriers?
- Notification changes affecting return visits?

**Example hypothesis:**
"If mobile app users stopped commenting but desktop is fine, likely a mobile-specific bug or UX issue."

**How to verify:**
- Segment the 5% drop by platform, region, user type
- Funnel analysis: view post → click comment → submit comment
- Cohort retention analysis
- Content engagement metrics (upvotes, views, etc.)

---

**Step 4: Form Primary Hypothesis**

Based on systematic elimination:

"My primary hypothesis is **[most likely cause based on evidence]**, because:
- Timeline matches (started on X date)
- Segment analysis shows pattern
- Other factors ruled out

For example:
'I believe the drop is due to a recent mobile app update that introduced a bug in the comment submission flow, because:
- The drop is entirely from mobile users (desktop stable)
- Started exactly when we released app version 2.5
- No external or measurement factors detected
- User error logs show increased failed submissions'"

---

**Step 5: Validation Plan**

"To validate this hypothesis, I would:

**Data Analysis:**
1. Compare mobile comment rates before/after app update
2. Check app error logs for comment submission failures
3. Segment by app version (users on old vs. new version)
4. Review user support tickets about commenting

**Testing:**
1. Attempt to reproduce the bug on mobile
2. A/B test: rollback 10% of users to old app version
3. Monitor if their commenting recovers

**Expected outcome:**
If hypothesis correct, rolled-back users should return to normal commenting rates."

---

**Common Patterns to Look For:**

✓ **Sudden drop** → Likely internal change or technical issue
✓ **Gradual decline** → Likely external factor or user behavior shift  
✓ **Platform-specific** → Technical issue on that platform
✓ **Segment-specific** → UX change affecting that segment
✓ **Timing patterns** → Seasonal or event-driven

**My Recommendation:**

Start with **DATA** → **INTERNAL** → **EXTERNAL** → **USER BEHAVIOR**

This prioritizes:
1. Fastest to verify (data issues)
2. Most controllable (internal changes)
3. Observable patterns (external/behavior)""",
                "good_points": [
                    "Starting with clarifying questions before diving in",
                    "Using MECE framework to ensure comprehensive coverage",
                    "Checking data quality issues FIRST (common oversight)",
                    "Systematic elimination rather than jumping to conclusions",
                    "Providing specific examples for each category",
                    "Forming testable hypotheses"
                ],
                "missing_points": [
                    "Explicitly stating the MECE framework upfront",
                    "Prioritization logic (why check data first, then internal, etc.)",
                    "Specific data sources or tools you'd use",
                    "Timeline for investigation (how quickly can you diagnose?)"
                ]
            },
            1: {
                "framework": "Prioritize data sources by verification speed and impact magnitude",
                "answer": """**Priority Order for Data Investigation:**

### **TIER 1: Immediate Checks (Within 1 hour)**

**1. Data Quality/Tracking Issues** ⚡
*Why first: Fastest to verify, eliminates false alarms*

**Specific checks:**
- **Dashboard comparison** - Is the drop showing in ALL dashboards? (If only one, likely that dashboard's issue)
- **Raw logs vs. aggregated metrics** - Pull raw comment event logs, count manually
- **Metric definition changes** - Check if we changed how we define "valid comments"
  - Example: Now excluding bot comments, spam, or deleted comments?
- **Data pipeline health** - Any ETL job failures? Missing data partitions?

**Data sources:**
- Event logging system (e.g., Kafka, Kinesis)
- Data pipeline monitoring (Airflow, dbt logs)
- Metric definition documentation
- Version control for analytics code

**What to look for:**
```sql
-- Compare raw event counts vs. dashboard
SELECT 
    date,
    COUNT(*) as raw_comment_count
FROM comment_events_raw
WHERE date >= '2025-02-01'
GROUP BY date;

-- Check for logging gaps
SELECT 
    date_hour,
    COUNT(*) as comments_per_hour
FROM comments
WHERE date >= '2025-02-01'
GROUP BY date_hour
ORDER BY date_hour;
-- Look for sudden drops to zero or unusual patterns
```

---

**2. Recent Deployments/Changes** 🔧
*Why second: Internal changes are most likely culprit*

**Specific checks:**
- **Code deployments** - What shipped in the last 7 days?
  - Check deployment logs, release notes
  - Correlate drop timing with deployment timestamp
- **Feature flags** - Any A/B tests or gradual rollouts affecting commenting?
- **Database changes** - Schema migrations, index changes affecting performance?

**Data sources:**
- Deployment logs (GitHub, GitLab, Jenkins)
- Feature flag system (LaunchDarkly, Optimizely)
- Change management tickets (Jira)
- Production incident logs

**What to look for:**
```
Recent deployments timeline:
- Feb 3, 10am: Mobile app v2.5 released
- Feb 3, 2pm: Backend API update
- Feb 4: Comments started declining

→ Strong correlation suggests app/API change
```

---

**3. Error Logs & System Health** 🚨
*Why third: Technical issues show up here*

**Specific checks:**
- **Application error rates** - Spike in comment submission errors?
- **API response times** - Commenting endpoint slower/timing out?
- **Database performance** - Query latency increased?
- **Mobile app crash reports** - Any crashes related to commenting?

**Data sources:**
- Application logs (Splunk, Datadog, New Relic)
- APM tools (performance monitoring)
- Crash reporting (Crashlytics, Sentry)
- Database query logs

**What to look for:**
```
Error rate analysis:
- Comment submission endpoint: 2% error rate → 15% error rate
- Error type: "Authentication timeout"
- Timing: Started Feb 3 after deployment

→ Indicates technical issue blocking submissions
```

---

### **TIER 2: Deep Dive Analysis (Within 4 hours)**

**4. Segmentation Analysis** 📊
*Identify which users/platforms/regions affected*

**Dimensions to segment:**

**Platform breakdown:**
```sql
SELECT 
    platform, -- mobile_app, mobile_web, desktop
    DATE(created_at) as date,
    COUNT(*) as comments,
    COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY DATE(created_at)) as pct
FROM comments
WHERE created_at >= '2025-01-27'  -- Week before drop
GROUP BY platform, date
ORDER BY date, platform;
```

**User segment breakdown:**
```sql
-- New vs. returning users
SELECT 
    user_type,  -- new, returning, power_user
    date,
    COUNT(*) as comments
FROM comments c
JOIN user_segments us ON c.user_id = us.user_id
WHERE date >= '2025-01-27'
GROUP BY user_type, date;
```

**Geographic breakdown:**
```sql
SELECT 
    country,
    date,
    COUNT(*) as comments
FROM comments
WHERE date >= '2025-01-27'
GROUP BY country, date
ORDER BY country, date;
```

**Subreddit category:**
```sql
SELECT 
    s.category,  -- news, gaming, sports, etc.
    date,
    COUNT(*) as comments
FROM comments c
JOIN subreddits s ON c.subreddit_id = s.id
WHERE date >= '2025-01-27'
GROUP BY s.category, date;
```

**What insights to extract:**
- "Drop is 100% from mobile app users, desktop unchanged" → Mobile bug
- "Only affecting US users, international stable" → Regional issue
- "New users down 50%, power users unchanged" → Onboarding problem
- "Gaming subreddits stable, news subreddits down" → Content-specific issue

---

**5. Funnel Analysis** 🔀
*Where are users dropping off in the comment flow?*

**Comment funnel stages:**
```
Stage 1: View post with comments section
Stage 2: Click "Add Comment" button
Stage 3: Type in comment box
Stage 4: Click "Submit"
Stage 5: Comment successfully posted
```

**Funnel metrics:**
```sql
WITH funnel AS (
  SELECT 
    date,
    COUNT(DISTINCT CASE WHEN event = 'view_post' THEN user_id END) as views,
    COUNT(DISTINCT CASE WHEN event = 'click_comment_button' THEN user_id END) as clicked,
    COUNT(DISTINCT CASE WHEN event = 'typed_comment' THEN user_id END) as typed,
    COUNT(DISTINCT CASE WHEN event = 'clicked_submit' THEN user_id END) as submitted,
    COUNT(DISTINCT CASE WHEN event = 'comment_posted' THEN user_id END) as posted
  FROM user_events
  WHERE date >= '2025-01-27'
  GROUP BY date
)
SELECT 
  date,
  clicked / views as view_to_click_rate,
  typed / clicked as click_to_type_rate,
  submitted / typed as type_to_submit_rate,
  posted / submitted as submit_to_post_rate
FROM funnel
ORDER BY date;
```

**What to look for:**
- Sudden drop in ANY stage indicates where the problem is
- Example: "Submit to post rate dropped from 95% → 80%" = submission failures

---

**6. Cohort & Retention Analysis** 👥
*Are specific user cohorts affected?*

**Cohort retention:**
```sql
-- Weekly cohort commenting behavior
SELECT 
    DATE_TRUNC('week', u.signup_date) as cohort_week,
    DATE_TRUNC('week', c.created_at) as activity_week,
    COUNT(DISTINCT c.user_id) as active_commenters
FROM users u
LEFT JOIN comments c ON u.user_id = c.user_id
WHERE u.signup_date >= '2025-01-01'
GROUP BY cohort_week, activity_week
ORDER BY cohort_week, activity_week;
```

**What insights:**
- "Jan 2025 cohort stopped commenting" → Onboarding change affected them
- "All cohorts down equally" → Platform-wide issue, not cohort-specific

---

### **TIER 3: External & Contextual (Within 24 hours)**

**7. Competitive & Market Analysis** 🌍

**Data sources:**
- SimilarWeb, App Annie (competitor traffic data)
- Google Trends (search interest)
- Social listening tools (Brandwatch, Mention)
- News aggregators

**What to check:**
- Did a competitor launch a viral feature?
- Major news event shifting attention?
- Industry-wide trend (all social platforms seeing decline)?

---

**8. Historical Patterns & Seasonality** 📅

**Year-over-year comparison:**
```sql
SELECT 
    DATE_PART('week', created_at) as week_of_year,
    DATE_PART('year', created_at) as year,
    COUNT(*) as comments
FROM comments
WHERE created_at >= '2024-01-01'
GROUP BY week_of_year, year
ORDER BY year, week_of_year;
```

**What to look for:**
- Same week last year: Was it also 5% lower than previous week?
- Seasonal pattern: February historically slower?

---

### **Summary: Investigation Priority**

**Hour 1:**
✅ Data quality check  
✅ Recent deployments  
✅ Error logs  

**Hours 2-4:**
✅ Segmentation analysis  
✅ Funnel analysis  
✅ Cohort analysis  

**Hours 5-24:**
✅ External factors  
✅ Historical patterns  

**Expected Outcome:**

By end of Hour 1: Know if it's data/technical issue (70% of cases)  
By end of Hour 4: Identified specific segment/cause (90% of cases)  
By end of Day 1: Complete root cause analysis with recommendations

**Key Principle:**

**Start with highest-probability, fastest-to-verify causes first.**
Don't spend hours on external analysis if you haven't checked if there's a bug!""",
                "good_points": [
                    "Prioritizing by verification speed and likelihood",
                    "Specific SQL queries showing exactly what to check",
                    "Clear timeline expectations for investigation",
                    "Segmentation across multiple dimensions (platform, user type, geography)",
                    "Funnel analysis to pinpoint where drop-off occurs"
                ],
                "missing_points": [
                    "Tools/systems to use for each check",
                    "Who to involve (engineers, product, support)",
                    "Communication plan while investigating",
                    "Fallback if primary hypothesis is wrong"
                ]
            },
            2: {
                "framework": "Deep-dive segmentation + mobile-specific technical investigation",
                "answer": """**If the drop is mobile-specific, this significantly narrows the investigation:**

### **Step 1: Confirm Mobile Specificity** 📱

**Verify the segment:**
```sql
SELECT 
    platform_type,
    DATE(created_at) as date,
    COUNT(*) as comment_count,
    COUNT(*) - LAG(COUNT(*)) OVER (PARTITION BY platform_type ORDER BY date) as daily_change
FROM comments
WHERE created_at >= '2025-01-27'
GROUP BY platform_type, date
ORDER BY date, platform_type;

Expected result:
Date       | Platform      | Comments | Change
2025-02-02 | Desktop       | 500K     | +2K
2025-02-02 | Mobile Web    | 300K     | +1K
2025-02-02 | Mobile App    | 200K     | -25K  ← The problem!
```

**Sub-segment mobile further:**
- iOS vs. Android
- App version
- Device type
- OS version

```sql
SELECT 
    mobile_os,  -- iOS, Android
    app_version,
    DATE(created_at) as date,
    COUNT(*) as comments
FROM comments
WHERE platform_type = 'mobile_app'
  AND created_at >= '2025-01-27'
GROUP BY mobile_os, app_version, date
ORDER BY date, mobile_os, app_version;
```

---

### **Step 2: Mobile App Technical Investigation** 🔧

Since it's mobile-specific, focus on mobile app factors:

**A) Recent Mobile App Changes**

**Check deployment history:**
```
Mobile releases timeline:
- iOS v2.5.1 - Released Feb 3, 10am EST
- Android v2.5.0 - Released Feb 2, 3pm EST
- Comments started dropping: Feb 3, 2pm EST

→ Correlates with iOS release!
```

**Review release notes:**
- What changed in commenting functionality?
- Any UI/UX updates to comment flow?
- Authentication changes?
- API endpoint updates?

---

**B) Mobile App Error Analysis**

**Crash reports:**
```
Crashlytics/Sentry analysis:
- Search for crashes related to "comment", "submit", "post"
- Filter by date range: Feb 3 onwards
- Group by error message and stack trace

Example findings:
Crash: "CommentViewController.submitComment()"
Frequency: 15,000 crashes
Affected versions: iOS 2.5.1
Error: "nil unwrapping error in authToken"

→ Authentication bug in new version!
```

**API error logging:**
```sql
-- Mobile API errors
SELECT 
    endpoint,
    error_code,
    error_message,
    COUNT(*) as error_count,
    DATE(timestamp) as date
FROM api_error_logs
WHERE endpoint LIKE '%comment%'
  AND platform = 'mobile_app'
  AND timestamp >= '2025-02-01'
GROUP BY endpoint, error_code, error_message, date
ORDER BY date, error_count DESC;
```

**Common mobile-specific errors:**
- 401 Unauthorized (auth token issues)
- 408 Request Timeout (slow mobile networks)
- 500 Internal Server Error (backend issue)
- Network connectivity errors
- Client-side validation failures

---

**C) Mobile App Performance Analysis**

**API response time:**
```sql
SELECT 
    platform,
    endpoint,
    DATE(timestamp) as date,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY response_time_ms) as p50_latency,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time_ms) as p95_latency
FROM api_requests
WHERE endpoint = '/api/v1/comments/create'
  AND timestamp >= '2025-01-27'
GROUP BY platform, endpoint, date
ORDER BY date, platform;
```

**What to look for:**
```
Desktop: p95 latency = 200ms (stable)
Mobile:  p95 latency = 200ms → 5000ms (degraded Feb 3)

→ Mobile users experiencing 5-second delays!
```

---

**D) Mobile UX/UI Investigation**

**User flow analysis:**

**Old mobile flow:**
```
1. Tap comment icon
2. Comment box appears
3. Type comment
4. Tap "Post"
5. Comment posted ✓
```

**New mobile flow (if UI changed):**
```
1. Tap comment icon
2. Login prompt appears (NEW!)
3. Authenticate
4. Comment box appears
5. Type comment
6. Tap "Post"
7. Comment posted

→ Added friction: extra authentication step
→ Users abandoning before commenting
```

**Mobile funnel metrics:**
```sql
SELECT 
    platform,
    app_version,
    COUNT(CASE WHEN event = 'click_comment' THEN 1 END) as clicked_comment,
    COUNT(CASE WHEN event = 'comment_posted' THEN 1 END) as posted_comment,
    COUNT(CASE WHEN event = 'comment_posted' THEN 1 END)::FLOAT / 
    COUNT(CASE WHEN event = 'click_comment' THEN 1 END) as conversion_rate
FROM mobile_events
WHERE date >= '2025-01-27'
  AND platform = 'mobile_app'
GROUP BY platform, app_version
ORDER BY app_version;
```

**Expected finding:**
```
Version 2.4: Conversion rate = 75%
Version 2.5: Conversion rate = 40%  ← Drop!

→ New version has UX issue preventing commenting
```

---

### **Step 3: User Feedback & Support Tickets** 💬

**Check mobile app reviews:**
```
App Store / Google Play reviews (Feb 3 onwards):
- Filter for 1-2 star reviews
- Search keywords: "comment", "broken", "can't comment", "error"

Example reviews:
"Can't post comments anymore, keeps saying error"
"Commenting is broken after latest update"
"App crashes when I try to comment"

→ Confirms user-facing issue with commenting
```

**Customer support tickets:**
```sql
SELECT 
    DATE(created_at) as date,
    issue_category,
    platform,
    COUNT(*) as ticket_count
FROM support_tickets
WHERE issue_category LIKE '%comment%'
  AND created_at >= '2025-01-27'
GROUP BY date, issue_category, platform
ORDER BY date, ticket_count DESC;
```

**Expected pattern:**
```
Feb 1-2: ~50 tickets/day about comments
Feb 3+:  ~500 tickets/day about comments (10x increase!)

→ Spike in support tickets confirms user-facing problem
```

---

### **Step 4: Form Specific Hypothesis** 🎯

Based on mobile-specific investigation:

**Primary Hypothesis:**

"The iOS app version 2.5.1 released on Feb 3 introduced a **critical bug** in the comment submission flow that causes the app to crash when users tap 'Post Comment'.

**Evidence:**
1. ✅ 100% of drop is from iOS mobile app users
2. ✅ Drop started 2 hours after iOS v2.5.1 release
3. ✅ Crashlytics shows 15K crashes in CommentViewController
4. ✅ Error logs show nil unwrapping error in auth token handling
5. ✅ User reviews confirm 'app crashes when commenting'
6. ✅ Support tickets spiked 10x for comment issues

**Root Cause:**
Code change in v2.5.1 assumed authToken is always present, but for users with expired sessions, authToken is nil → crash."

---

### **Step 5: Immediate Action Plan** 🚨

**Immediate (Next 2 hours):**

1. **Hotfix deployment**
   ```
   - Rollback iOS app to v2.4.0 (stable version)
   - OR push emergency hotfix v2.5.2 with nil-check
   - Priority: P0 - Production incident
   ```

2. **Communication**
   ```
   - Notify users: "We're aware of a commenting issue and working on a fix"
   - Support team: Provide script for responding to tickets
   - Executive team: Brief on situation and ETA for fix
   ```

3. **Temporary workaround**
   ```
   - Advise users to use mobile web (which is working)
   - Force logout/login to refresh auth tokens
   ```

---

**Short-term (Next 24 hours):**

1. **Root cause analysis**
   ```
   - Review code change that introduced bug
   - Identify why QA didn't catch this
   - Document timeline and impact
   ```

2. **Monitoring**
   ```
   - Track comment recovery rate after hotfix
   - Monitor crash reports to ensure fix works
   - Verify desktop/Android unaffected
   ```

3. **Post-mortem preparation**
   ```
   - Document incident timeline
   - Calculate impact (lost comments, user frustration)
   - Identify prevention measures
   ```

---

**Long-term (Next 1-2 weeks):**

1. **Process improvements**
   ```
   - Add automated tests for comment submission flow
   - Implement gradual rollout (5% → 25% → 100%)
   - Enhanced monitoring for comment metrics
   - Better crash detection pre-release
   ```

2. **Technical debt**
   ```
   - Refactor authentication handling to be more robust
   - Add nil-safety checks across codebase
   - Improve error messaging to users
   ```

3. **Communication**
   ```
   - Publish post-mortem (internal)
   - Learnings documentation
   - Update on-call playbooks
   ```

---

### **Step 6: Validation Metrics** 📊

**Track these metrics hourly after fix:**

```sql
-- Comment recovery tracking
SELECT 
    DATE_TRUNC('hour', created_at) as hour,
    COUNT(*) as comments,
    COUNT(*) / LAG(COUNT(*)) OVER (ORDER BY DATE_TRUNC('hour', created_at)) as growth_rate
FROM comments
WHERE platform = 'ios_mobile_app'
  AND created_at >= NOW() - INTERVAL '24 hours'
GROUP BY hour
ORDER BY hour;

Expected: Comments should return to ~200K/day within 12 hours of fix
```

**Success criteria:**
- ✅ iOS crash rate returns to <0.1%
- ✅ Comment count recovers to baseline (±2%)
- ✅ Support tickets drop to normal levels
- ✅ App Store rating stabilizes

---

### **Key Takeaways for Mobile-Specific Issues:**

1. **Version tracking is critical** - Always segment by app version
2. **Crash logs are goldmines** - Check them early
3. **User reviews signal issues** - Monitor app store feedback
4. **Gradual rollouts prevent this** - 100% rollout = 100% risk
5. **Mobile has unique constraints** - Network, auth, crashes not seen on web

**When it's mobile-specific:**
→ It's almost always a technical issue (bug, performance, crash)  
→ NOT a user behavior or external factor  
→ Requires immediate engineering response""",
                "good_points": [
                    "Immediately sub-segmenting mobile (iOS vs. Android, versions)",
                    "Checking crash logs and error reports systematically",
                    "Reviewing app store reviews for user-reported issues",
                    "Connecting timeline of app release to metric drop",
                    "Clear immediate vs. short-term vs. long-term action plan",
                    "Specific validation metrics to track recovery"
                ],
                "missing_points": [
                    "Escalation path (who to notify, when)",
                    "Risk assessment (how much revenue/engagement lost)",
                    "Rollback vs. hotfix decision criteria",
                    "Communication templates for users/stakeholders"
                ]
            },
            3: {
                "framework": "Hypothesis validation through A/B testing, data analysis, and iteration",
                "answer": """**Comprehensive Validation & Recommendation Framework:**

### **Step 1: Validate Your Hypothesis** 🔬

Based on your diagnosis, you have a hypothesis (e.g., "iOS app v2.5.1 has a commenting bug"). Now validate it rigorously.

---

**Validation Method 1: Data Analysis** 📊

**Compare before/after the suspected cause:**

```sql
-- If hypothesis is "iOS v2.5.1 caused the drop"
SELECT 
    app_version,
    DATE(created_at) as date,
    COUNT(*) as comments,
    AVG(COUNT(*)) OVER (
        PARTITION BY app_version 
        ORDER BY DATE(created_at) 
        ROWS BETWEEN 7 PRECEDING AND CURRENT ROW
    ) as seven_day_avg
FROM comments
WHERE platform = 'ios_mobile_app'
  AND created_at >= '2025-01-15'
GROUP BY app_version, date
ORDER BY date, app_version;

Expected result:
v2.4.0: Stable ~50K comments/day
v2.5.1: Dropped to ~25K comments/day (50% drop)

→ Strong evidence supporting hypothesis
```

**Statistical significance test:**
```python
from scipy import stats

# Comments before change (baseline)
before = [48000, 49000, 50000, 49500, 50500, 49000, 50000]  # 7 days

# Comments after change
after = [25000, 24000, 26000, 25500, 24500, 25000, 26000]   # 7 days

# T-test
t_stat, p_value = stats.ttest_ind(before, after)

print(f"P-value: {p_value}")  # If p < 0.05, statistically significant drop

→ Confirms this isn't random variation
```

---

**Validation Method 2: Reproduce the Issue** 🐛

**Manual testing:**
```
Test Plan:
1. Get device with iOS v2.5.1
2. Attempt to post a comment
3. Document exact steps and error
4. Compare with v2.4.0 behavior

Expected outcome: Can reliably reproduce crash/error
```

**QA testing:**
- Automated test suite (if available)
- Manual regression testing
- Different device types, OS versions
- Edge cases (no network, slow network, logged out, etc.)

---

**Validation Method 3: A/B Test (Controlled Rollback)** 🧪

If you need more certainty before a full fix:

**Experiment design:**
```
Hypothesis: v2.5.1 causes commenting issues

Test: Rollback 20% of iOS users to v2.4.0

Control group (80%): Stays on v2.5.1
Treatment group (20%): Rolled back to v2.4.0

Metric: Comments per user per day
Duration: 24-48 hours
```

**Analysis:**
```sql
WITH user_groups AS (
  SELECT 
    user_id,
    CASE WHEN user_id % 5 = 0 THEN 'rollback_v2.4' 
         ELSE 'current_v2.5' 
    END as test_group
  FROM users
  WHERE platform = 'ios_mobile_app'
)
SELECT 
    ug.test_group,
    COUNT(DISTINCT c.user_id) as active_commenters,
    COUNT(*) as total_comments,
    COUNT(*)::FLOAT / COUNT(DISTINCT c.user_id) as comments_per_user
FROM user_groups ug
LEFT JOIN comments c ON ug.user_id = c.user_id
WHERE c.created_at >= NOW() - INTERVAL '24 hours'
GROUP BY ug.test_group;

Expected result:
rollback_v2.4:  3.5 comments/user  (healthy)
current_v2.5:   1.8 comments/user  (broken)

→ Proves v2.5.1 is the cause
```

---

**Validation Method 4: External Evidence** 📱

**User reports:**
- App store reviews mentioning the issue
- Support tickets with error screenshots
- Social media complaints (Twitter, Reddit)

**Engineering confirmation:**
- Code review of changes in v2.5.1
- Crash logs showing stack traces
- Error logs showing failure patterns

**Triangulation:**
When data + reproduction + user reports + engineering analysis ALL point to same cause → High confidence

---

### **Step 2: Quantify the Impact** 💰

Before making recommendations, quantify business impact:

**User impact:**
```sql
-- Users affected
SELECT 
    COUNT(DISTINCT user_id) as affected_users,
    COUNT(DISTINCT user_id) * 100.0 / 
        (SELECT COUNT(*) FROM users WHERE platform = 'ios_mobile_app') 
    as pct_affected
FROM users
WHERE platform = 'ios_mobile_app'
  AND app_version = '2.5.1';

Example: 2M affected users (40% of iOS base)
```

**Engagement impact:**
```sql
-- Lost comments
SELECT 
    SUM(baseline_comments - actual_comments) as comments_lost
FROM (
    SELECT 
        date,
        50000 as baseline_comments,  -- Historical average
        COUNT(*) as actual_comments
    FROM comments
    WHERE platform = 'ios_mobile_app'
      AND date >= '2025-02-03'
    GROUP BY date
) t;

Example: 175,000 comments lost over 7 days
```

**Revenue impact (if applicable):**
```
Assumptions:
- 1% of comments lead to Reddit Premium signup
- Avg premium value = $6/month

Lost revenue = 175,000 * 0.01 * $6 = $10,500/week

Or: Lost ad impressions from reduced engagement
```

**Brand impact:**
- App store rating: 4.5 stars → 3.8 stars
- Support ticket volume: +1000%
- User frustration / churn risk

---

### **Step 3: Make Data-Driven Recommendations** 📋

**Recommendation Framework: Immediate → Short-term → Long-term**

---

### **IMMEDIATE ACTIONS** (Next 2-4 hours)

**Recommendation 1: Emergency Hotfix**

**What:**
```
Deploy v2.5.2 with critical bug fix:
- Add nil-check for authToken before comment submission
- Add error handling with user-friendly message
- Add logging for debugging
```

**Why:**
- Stops the bleeding (prevents further comment loss)
- Quickest path to recovery
- Minimal risk (targeted fix)

**How:**
```
1. Engineering: Write & test hotfix (1 hour)
2. QA: Smoke test on staging (30 min)
3. Deployment: Gradual rollout (2 hours)
   - 5% of users first
   - Monitor for 30 min
   - If stable, expand to 100%
```

**Success metrics:**
- Crash rate <0.1%
- Comment count returns to baseline within 12 hours
- No new regressions

**Alternative (if hotfix risky):**
```
Rollback ALL iOS users to v2.4.0 (stable version)
- Lose new features in v2.5.1, but commenting works
- Buys time for proper fix
```

---

**Recommendation 2: Incident Communication**

**Internal:**
```
To: Engineering, Product, Support, Exec teams
Subject: P0 Incident - iOS Commenting Failure

Summary: iOS v2.5.1 introduced critical bug affecting 40% of iOS users
Impact: 50% drop in iOS comments, 175K comments lost
Status: Hotfix deploying now, ETA 2 hours to resolution
Next steps: Post-mortem Feb 10, 2pm
```

**External (if needed):**
```
To: Affected users
Via: In-app notification, email

"We're aware some iOS users are experiencing issues posting 
comments. We've identified the problem and are rolling out a 
fix now. Thank you for your patience."
```

**Support team:**
```
Ticket response template:
"Thank you for reporting this. We've identified a bug in the 
latest iOS app affecting commenting. Please update to version 
2.5.2 (available now) which resolves this issue."
```

---

### **SHORT-TERM ACTIONS** (Next 24-72 hours)

**Recommendation 3: Comprehensive Testing**

**What:**
```
- Regression test all commenting flows
- Test on all iOS versions (14, 15, 16, 17)
- Test on different device types (iPhone 12, 13, 14, 15)
- Test edge cases (offline, slow network, logged out)
```

**Why:**
- Ensure hotfix doesn't introduce new bugs
- Validate fix works across all scenarios
- Rebuild confidence in commenting functionality

---

**Recommendation 4: Enhanced Monitoring**

**Set up real-time alerts:**
```python
# Alert if comments drop >5% in any 1-hour period
if (current_hour_comments / baseline_comments) < 0.95:
    send_alert_to_oncall(
        severity='P1',
        message='Comments down >5% in last hour',
        platform=platform,
        affected_users=affected_count
    )
```

**Dashboard updates:**
```
Add to executive dashboard:
- Comments by platform (real-time)
- Comment submission error rate
- App crash rate by version
- Comment funnel conversion rate

→ Never miss another drop
```

---

**Recommendation 5: Post-Mortem**

**Conduct within 48 hours:**

**Agenda:**
1. Timeline of events
2. Root cause analysis
3. Why didn't we catch this?
4. Action items to prevent recurrence

**Key questions:**
- Why didn't QA catch this bug?
- Why did we deploy to 100% immediately?
- What monitoring should we have had?

**Deliverable:**
- Written post-mortem document
- Action items with owners and due dates
- Process improvements

---

### **LONG-TERM ACTIONS** (Next 2-4 weeks)

**Recommendation 6: Process Improvements**

**1. Automated Testing**
```
Add to CI/CD pipeline:
- Unit tests for comment submission
- Integration tests for full comment flow
- Regression tests run before every deployment
- Automated crash detection

Goal: Catch bugs before production
```

**2. Gradual Rollouts**
```
New policy: All mobile releases follow gradual rollout:
- Day 1: 5% of users
- Day 2: 25% of users (if no issues)
- Day 3: 50% of users
- Day 4: 100% of users

With automated monitoring at each stage

→ Limits blast radius if bugs slip through
```

**3. Enhanced QA Process**
```
Checklist for commenting features:
☐ Test on iOS 14, 15, 16, 17
☐ Test with/without auth
☐ Test on slow network
☐ Test error scenarios
☐ Load test (1000 concurrent comments)

+ Mandatory QA sign-off before production
```

---

**Recommendation 7: Technical Debt**

**Code improvements:**
```
1. Refactor authentication handling
   - Make nil-safe throughout codebase
   - Better error handling and user messaging
   
2. Improve error logging
   - Add structured logging for debugging
   - Track user journey context
   
3. Circuit breakers
   - Auto-disable broken features
   - Graceful degradation
```

---

**Recommendation 8: Incident Response Playbook**

**Create runbook for future metric drops:**
```markdown
# Commenting Drop Playbook

## Detection
- Alert triggers when comments <95% baseline

## Investigation Checklist
☐ Check data pipeline health
☐ Review recent deployments
☐ Segment by platform/region/user
☐ Check error logs and crashes
☐ Review user reports

## Response
- P0: >20% drop → Immediate rollback
- P1: 10-20% drop → Hotfix within 4 hours
- P2: 5-10% drop → Investigate and fix within 24 hours

## Communication
- Template for user notification
- Template for exec brief
- Escalation path
```

---

### **Step 4: Present Recommendations** 🎤

**To stakeholders, structure as:**

**Executive Summary:**
```
Problem: iOS app v2.5.1 bug causing 50% drop in comments
Impact: 175K lost comments, $10K/week revenue at risk, brand damage
Solution: Deployed hotfix v2.5.2, comments recovering
Prevention: Gradual rollouts + enhanced monitoring going forward
```

**Detailed Recommendations:**
1. ✅ **Immediate: Hotfix deployed** (DONE)
2. 🔄 **Short-term: Enhanced monitoring** (In Progress)
3. 📅 **Long-term: Process improvements** (Planned)

**Ask:**
"Does leadership support the gradual rollout policy for all mobile releases?"

---

### **Key Principles for Strong Recommendations:**

✅ **Data-driven** - Back with numbers, not opinions  
✅ **Action-oriented** - Clear what to do, who does it, when  
✅ **Risk-assessed** - Acknowledge tradeoffs and downsides  
✅ **Preventative** - Not just fix current issue, prevent future ones  
✅ **Stakeholder-aware** - Address exec concerns (revenue, brand, etc.)  

---

**Final Answer Structure for Interview:**

```
"To validate my hypothesis that iOS v2.5.1 caused the issue:

1. DATA: I'd compare comment rates before/after v2.5.1 deployment
2. TESTING: Reproduce the bug manually and in QA
3. A/B TEST: Roll back 20% of users to v2.4, measure recovery
4. USER REPORTS: Verify crash logs and support tickets align

If validated, my recommendations are:

IMMEDIATE:
- Deploy hotfix v2.5.2 with bug fix (2-hour ETA)
- Communicate to users and support team

SHORT-TERM:
- Comprehensive testing across all iOS versions
- Enhanced real-time monitoring and alerts
- Post-mortem within 48 hours

LONG-TERM:
- Mandatory gradual rollouts for all mobile releases
- Automated testing in CI/CD pipeline
- Incident response playbooks

This prevents both immediate damage and future occurrences."
```

This shows:
- ✅ Systematic validation
- ✅ Quantified impact
- ✅ Tiered recommendations (urgent → strategic)
- ✅ Prevention mindset
- ✅ Clear communication

**This is what top candidates do!**""",
                "good_points": [
                    "Multiple validation methods (data, testing, A/B test)",
                    "Quantifying business impact with numbers",
                    "Tiered recommendations (immediate/short/long-term)",
                    "Including prevention measures, not just fixes",
                    "Clear communication templates for stakeholders",
                    "Post-mortem and learning focus"
                ],
                "missing_points": [
                    "Decision criteria for rollback vs. hotfix",
                    "Resource requirements (engineering hours, budget)",
                    "Timeline dependencies and critical path",
                    "Stakeholder sign-off requirements"
                ]
            }
        },
        "common_mistakes": [
            "Jumping straight to solutions without systematic diagnosis",
            "Not checking data quality issues first (false alarms)",
            "Asking too many clarifying questions upfront (analysis paralysis)",
            "Not using a framework (random guessing vs. structured approach)",
            "Having only one hypothesis instead of backup theories",
            "Ignoring business context (revenue, user impact, urgency)",
            "Not prioritizing investigation steps (checking slow things first)"
        ],
        "key_takeaways": [
            "Always use MECE framework: Internal, External, User, Data factors",
            "Check data/measurement issues FIRST - fastest to verify",
            "Form testable hypotheses, don't just guess",
            "Segment the problem (platform, region, user type) to narrow scope",
            "Prioritize by likelihood AND speed of verification",
            "Think in tiers: Immediate fix, Short-term actions, Long-term prevention",
            "Validate rigorously before making recommendations"
        ]
    },
    
    "instagram_stories": {
        "title": "Instagram Stories Launch - Metric Design",
        "difficulty": "Intermediate",
        "time": "15-20 min",
        "type": "Metric Design & Product Analytics",
        "skills": ["Metric Selection", "Product Thinking", "Tradeoff Analysis", "Success Criteria"],
        "scenario": """You're a data analyst at Instagram (Meta). The product team is preparing to launch a new feature called "Stories" - ephemeral photo/video posts that disappear after 24 hours.

The Head of Product asks you: "We're launching Stories next month. How should we measure if this launch is successful? What metrics should we track, and how will we know if we should invest more in this feature or pivot?"

This is a critical feature that could significantly impact user engagement and retention.""",
        "questions": [
            "How would you define success for the Instagram Stories feature? What does 'success' mean in this context?",
            "What specific metrics would you track to measure the performance of Stories? Organize them by priority.",
            "How would you determine if Stories is cannibalizing regular Instagram posts vs. creating incremental engagement?",
            "After 3 months, what data would you analyze to decide whether to invest more, maintain, or pivot on Stories?"
        ],
        "frameworks": ["North Star Metric", "AARRR Framework", "Input vs Output Metrics", "Counter Metrics"],
        "solutions": {
            0: {
                "framework": "Define success through the lens of Business Goals, User Value, and Guardrail Metrics",
                "answer": """**Step 1: Clarify the Business Context**

Before jumping to metrics, I'd ask:
- **What's the business goal?** (Engagement? Growth? Retention? Revenue?)
- **Who is the target user?** (All users? Power users? Casual users?)
- **What problem does Stories solve?** (More authentic sharing? FOMO? Competition with Snapchat?)
- **What's the success timeline?** (30 days? 90 days? 1 year?)

**Step 2: Define Success at Three Levels**

### **Level 1: Business Success** 💼
*"Does this help Instagram's business?"*

**Primary goal options:**
- **Increase engagement** - Users spend more time on Instagram
- **Improve retention** - Users come back more frequently
- **Drive growth** - Attract new users or re-engage dormant ones
- **Monetization** - Eventually enable ads in Stories

**My assumption:** Primary goal is **increasing engagement and retention** (based on Snapchat competition)

**Success definition:**
"Stories is successful if it increases overall user engagement without cannibalizing core feed interactions, leading to higher retention rates."

---

### **Level 2: Feature Success** 🎯
*"Are users actually using Stories?"*

**Adoption metrics:**
- **X% of monthly active users** create at least one Story (adoption rate)
- **Y% of daily active users** view Stories daily (consumption rate)
- **Z Stories created per day** (absolute volume)

**Engagement metrics:**
- Users create Stories **at least 2x per week** (frequency)
- Stories viewers watch **>50% of Stories** they start (completion rate)
- **Avg time spent** on Stories per session

**Example success criteria:**
- "Within 3 months: 30% of DAU create Stories weekly, 60% of DAU view Stories daily"

---

### **Level 3: User Value** ❤️
*"Do users actually like this?"*

**Qualitative signals:**
- User surveys: "Stories makes Instagram better" (NPS score)
- Feature ratings: 4+ stars
- User feedback sentiment (positive mentions in reviews/support)

**Behavioral signals:**
- **Retention lift** - Users who create Stories have higher 7-day retention
- **Session frequency** - Stories users open app more often
- **Network effects** - Stories creators attract more engagement from friends

**Success definition:**
"Users who engage with Stories (create or view) show 10%+ higher retention than non-Stories users"

---

**Step 3: Define What Success is NOT (Guardrails)** ⚠️

It's critical to define what we DON'T want:

**Anti-patterns to avoid:**
- ❌ Stories cannibalizes feed posts (total posts decrease)
- ❌ Stories engagement is low-quality (users skip most Stories)
- ❌ Only existing power users adopt (no new behavior created)
- ❌ Privacy concerns increase (negative PR)
- ❌ Ad revenue decreases (if feed engagement drops)

**Guardrail metrics:**
- Feed posts per user should NOT decrease >5%
- Feed engagement (likes, comments) should remain stable
- User complaints about privacy should not spike
- Overall time in app should increase or stay flat (not just shift to Stories)

---

**Step 4: Comprehensive Success Statement**

"Instagram Stories is successful if:

**Primary Success:**
1. 30%+ of DAU create Stories within 90 days
2. 60%+ of DAU view Stories daily within 90 days
3. Stories users show 10%+ higher retention vs. non-users

**Secondary Success:**
4. Overall engagement (time in app) increases by 5%+
5. Session frequency increases by 10%+

**Guardrails (Must Not Fail):**
6. Feed posts per user decrease by <5%
7. Feed engagement remains within 95% of baseline
8. No significant increase in privacy complaints
9. User satisfaction (NPS) remains stable or improves

If these criteria are met, Stories is creating incremental value without harming the core product."

---

**Framework Used:**

I used a **multi-layered success definition**:
- **Business layer** - Strategic goals (engagement, retention)
- **Product layer** - Feature adoption and usage
- **User layer** - Actual user value and satisfaction
- **Guardrail layer** - What must NOT go wrong

This ensures we're not just measuring activity, but measuring whether Stories creates real value for business AND users.

---

**Key Principles:**

✅ **Start with "why"** - What business problem are we solving?
✅ **Balance leading and lagging indicators** - Adoption (leading) + Retention (lagging)
✅ **Define anti-goals** - Be explicit about what could go wrong
✅ **Segment users** - Success might vary by user type
✅ **Time-bound** - Success criteria should have deadlines

**Common Mistakes to Avoid:**

❌ Only tracking vanity metrics ("1M Stories created!")
❌ Not considering cannibalization of existing features
❌ Forgetting to measure user value (just measuring activity)
❌ No guardrail metrics (could optimize wrong thing)
❌ Not aligning metrics to business goals""",
                "good_points": [
                    "Starting with clarifying questions about business goals",
                    "Defining success at multiple levels (business, product, user)",
                    "Including guardrail/counter-metrics (what could go wrong)",
                    "Thinking about both adoption AND value created",
                    "Considering cannibalization risks",
                    "Time-bounding success criteria"
                ],
                "missing_points": [
                    "Specific numeric targets (30% adoption, 60% DAU)",
                    "Distinguishing between leading indicators (early signals) and lagging indicators (long-term impact)",
                    "Segmentation strategy (power users vs. casual users)",
                    "Network effects consideration (Stories creators drive viewership)"
                ]
            },
            1: {
                "framework": "North Star Metric + AARRR Framework + Input/Output Metrics",
                "answer": """**Framework: Organize metrics into tiers based on importance and actionability**

---

## **Tier 1: North Star Metric** 🌟

**The ONE metric that best captures product success:**

**My recommendation: Weekly Active Stories Users (WASU)**

**Definition:** Number of users who create OR view at least one Story in a week

**Why this metric:**
- ✅ Captures both creation and consumption
- ✅ Balances supply (creators) and demand (viewers)
- ✅ Weekly cadence matches Stories behavior (ephemeral, frequent)
- ✅ Directly ties to engagement and retention
- ✅ Easy to understand and communicate to leadership

**Success target:** 
- Month 1: 20% of WAU
- Month 3: 40% of WAU  
- Month 6: 60% of WAU

---

## **Tier 2: Primary Metrics** 📊
*Track weekly, report to leadership*

### **A) Adoption Metrics** (Are people trying it?)

**1. Stories Creator Rate**
```
Definition: % of DAU who post at least 1 Story in a day
Calculation: (Users who posted Story) / DAU
Target: 15% of DAU within 3 months
Why: Measures supply-side adoption
```

**2. Stories Viewer Rate**
```
Definition: % of DAU who view at least 1 Story in a day
Calculation: (Users who viewed Stories) / DAU
Target: 50% of DAU within 3 months
Why: Measures demand-side adoption
```

**3. Stories Share of Feed**
```
Definition: % of users who see Stories in their feed
Calculation: (Users shown Stories module) / DAU
Target: 80% of DAU
Why: Measures distribution/discoverability
```

---

### **B) Engagement Metrics** (Are people using it well?)

**4. Stories Posted per Creator**
```
Definition: Average Stories posted per creator per day
Calculation: Total Stories / Unique creators
Target: 2-3 Stories per creator per day
Why: Measures depth of engagement (not just breadth)
```

**5. Stories Viewed per Viewer**
```
Definition: Average Stories viewed per viewer per day
Calculation: Total Story views / Unique viewers
Target: 10+ Stories per viewer per day
Why: Measures consumption depth
```

**6. Story Completion Rate**
```
Definition: % of Stories watched to completion
Calculation: (Stories watched 100%) / Total Stories started
Target: >60% completion rate
Why: Measures content quality and user interest
```

**7. Average Time Spent on Stories**
```
Definition: Avg seconds spent viewing Stories per session
Calculation: Total time on Stories / Sessions with Stories
Target: 5+ minutes per session
Why: Measures sustained engagement
```

---

### **C) Retention Metrics** (Does it make users stick around?)

**8. Stories User Retention**
```
Definition: Day 7 and Day 30 retention for Stories users
Cohort: Users who created/viewed Stories in Week 1
Measurement: % who return in Week 2, Week 4
Target: 10%+ higher than non-Stories users
Why: Proves Stories drives retention
```

**9. Stories Frequency**
```
Definition: How often Stories users return
Calculation: Avg days active per week (for Stories users)
Target: 5+ days/week for Stories users
Why: Measures habit formation
```

---

## **Tier 3: Secondary Metrics** 📈
*Track daily, review weekly*

### **D) Content Quality Metrics**

**10. Reply Rate**
```
Stories with at least 1 reply / Total Stories
Target: 30%+ have replies
Why: Measures social interaction quality
```

**11. Share/Forward Rate**
```
Stories shared to others / Total Stories viewed
Target: 10%+ share rate
Why: Measures viral/network effects
```

**12. Camera Usage**
```
% Stories using Instagram camera vs. uploads
Target: 70%+ using Instagram camera
Why: Measures native behavior (better for engagement)
```

---

### **E) Growth Metrics**

**13. New User Stories Adoption**
```
% of new signups who post Story within 7 days
Target: 25%+ of new users
Why: Measures onboarding effectiveness
```

**14. Re-engagement of Dormant Users**
```
% of dormant users (inactive >30 days) who return via Stories
Target: 5% reactivation rate
Why: Stories might bring back lapsed users
```

---

## **Tier 4: Guardrail/Counter Metrics** ⚠️
*Critical to prevent negative outcomes*

**15. Feed Post Cannibalization**
```
Definition: Change in feed posts per user (before vs. after Stories)
Calculation: (Post-launch posts/user) - (Pre-launch posts/user)
Acceptable: -5% or less
Why: Ensure Stories is additive, not substitutive
```

**16. Feed Engagement Stability**
```
Metrics: Likes, comments, saves per feed post
Acceptable: Within 95% of baseline
Why: Ensure feed health maintained
```

**17. Total Time in App**
```
Definition: Overall minutes per user per day
Target: +5% or more (not flat or declining)
Why: Ensure Stories adds engagement, doesn't just shift it
```

**18. Creator Burnout Rate**
```
Definition: % of Stories creators who drop off after 1 week
Acceptable: <30% churn
Why: Ensure feature is sustainable
```

**19. Privacy Concerns**
```
Support tickets about Stories privacy / Total support tickets
Acceptable: <2% of tickets
Why: Monitor reputation/trust impact
```

---

## **Tier 5: Input Metrics** 🎯
*Leading indicators we can directly influence*

**20. Stories Discoverability**
```
% of users who see "Create Story" button daily
Target: 90%+ of DAU see the entry point
Why: Can't use if you can't find it
```

**21. Stories Creation Friction**
```
% of users who start but don't finish creating Story
Target: <20% abandonment
Why: Identifies UX issues
```

**22. Stories Notification Opt-in**
```
% of users who enable Stories notifications
Target: 40%+ opt-in rate
Why: Drives re-engagement
```

---

## **How to Prioritize These Metrics:**

### **Daily Dashboard:**
- North Star Metric (WASU)
- Creator Rate
- Viewer Rate
- Completion Rate
- Guardrail metrics (cannibalization)

### **Weekly Review:**
- All Primary Metrics (Tier 2)
- Retention cohorts
- Guardrail metrics

### **Monthly Deep Dive:**
- Full metric suite
- Segmentation analysis (by user type, geography)
- Cohort retention curves
- A/B test results

---

## **Metric Organization Framework Used:**

**1. AARRR (Pirate Metrics)**
- **Acquisition:** New user adoption (#13, #14)
- **Activation:** First Story creation (#20, #21)
- **Retention:** Stories user retention (#8, #9)
- **Referral:** Share rate (#11)
- **Revenue:** (Future: ads in Stories)

**2. Input vs. Output Metrics**
- **Input** (controllable): Discoverability (#20), Notifications (#22)
- **Output** (results): Retention (#8), Engagement (#7)

**3. Leading vs. Lagging Indicators**
- **Leading** (early signals): Creator rate (#1), Completion rate (#6)
- **Lagging** (long-term): Retention (#8), Time in app (#17)

---

## **Key Principles:**

✅ **One North Star** - Align team on single success metric
✅ **Layered metrics** - From high-level to granular
✅ **Guardrails matter** - Prevent optimizing wrong thing
✅ **Actionable metrics** - Each metric should inform decisions
✅ **Balance breadth & depth** - Adoption + Engagement

**Avoid:**
❌ Tracking 50+ metrics (analysis paralysis)
❌ Vanity metrics with no action (total Stories created)
❌ Only lagging indicators (can't course-correct)
❌ No guardrails (risk unintended consequences)""",
                "good_points": [
                    "Defining a clear North Star Metric (WASU)",
                    "Organizing metrics into tiers by importance",
                    "Including both adoption AND engagement metrics",
                    "Thinking about leading vs. lagging indicators",
                    "Including guardrail/counter-metrics",
                    "Making metrics actionable with specific targets"
                ],
                "missing_points": [
                    "Explaining the AARRR framework explicitly",
                    "Segmentation strategy (how metrics differ by user cohort)",
                    "Data instrumentation requirements (what events to track)",
                    "Reporting cadence and ownership (who monitors what)"
                ]
            },
            2: {
                "framework": "Incrementality Analysis + Cohort Comparison + Holdout Testing",
                "answer": """**The Cannibalization Question: Are we just shifting engagement or creating new value?**

This is critical - if Stories just steals from Feed, we haven't created value, we've just reshuffled deck chairs.

---

## **Framework: Multi-Method Incrementality Analysis**

Use **3 complementary approaches** to determine cannibalization:

---

### **Method 1: Before/After Comparison** 📊

**Simple but informative: Compare user behavior before and after Stories launch**

**Metrics to compare:**

**A) Feed Post Volume**
```sql
-- User-level feed posting behavior
WITH pre_stories AS (
  SELECT 
    user_id,
    COUNT(*) as feed_posts_per_week
  FROM posts
  WHERE post_type = 'feed'
    AND created_at BETWEEN '2016-06-01' AND '2016-07-31'  -- Before Stories
  GROUP BY user_id
),
post_stories AS (
  SELECT 
    user_id,
    COUNT(*) as feed_posts_per_week
  FROM posts
  WHERE post_type = 'feed'
    AND created_at BETWEEN '2016-09-01' AND '2016-10-31'  -- After Stories (60 days later)
  GROUP BY user_id
)
SELECT 
    AVG(pre.feed_posts_per_week) as avg_posts_before,
    AVG(post.feed_posts_per_week) as avg_posts_after,
    (AVG(post.feed_posts_per_week) - AVG(pre.feed_posts_per_week)) / 
        AVG(pre.feed_posts_per_week) as pct_change
FROM pre_stories pre
JOIN post_stories post ON pre.user_id = post.user_id;
```

**What to look for:**
- ✅ **No cannibalization:** Feed posts stay flat or increase
- ⚠️ **Mild cannibalization:** Feed posts decrease 5-10%
- ❌ **Significant cannibalization:** Feed posts decrease >15%

---

**B) Total Content Creation**
```
Metric: (Feed Posts + Stories) per user per week

Before Stories: 3.5 feed posts/week
After Stories:  2.8 feed posts + 4.2 Stories = 7.0 total posts/week

Result: Total content INCREASED by 100% → Incremental ✅
```

**Interpretation:**
- If total content increases significantly → Stories is additive
- If total content stays flat → Stories is substitutive (cannibalization)

---

**C) Engagement Time Allocation**
```sql
-- Time spent in Feed vs. Stories
SELECT 
    DATE_TRUNC('week', session_date) as week,
    SUM(CASE WHEN surface = 'feed' THEN time_seconds ELSE 0 END) as feed_time,
    SUM(CASE WHEN surface = 'stories' THEN time_seconds ELSE 0 END) as stories_time,
    SUM(time_seconds) as total_time
FROM user_sessions
WHERE session_date >= '2016-08-01'
GROUP BY week
ORDER BY week;
```

**What to look for:**
- ✅ **Incremental:** Total time increases (e.g., 20 min/day → 25 min/day)
- ⚠️ **Partial cannibalization:** Total time flat but Feed drops, Stories rises
- ❌ **Full cannibalization:** Total time same, just reallocated

**Example outcome:**
```
Week        | Feed Time | Stories Time | Total Time
------------|-----------|--------------|------------
Pre-launch  | 20 min    | 0 min        | 20 min
4 weeks in  | 18 min    | 8 min        | 26 min  ← +30% total ✅
12 weeks in | 17 min    | 12 min       | 29 min  ← +45% total ✅
```

**Conclusion:** Mild feed cannibalization (-15%) but massive total time gain (+45%) → Net positive

---

### **Method 2: User Cohort Comparison** 👥

**Compare Stories users vs. non-Stories users (controlling for selection bias)**

**The challenge:** Stories users might already be more engaged. Need to control for this.

**Approach: Matched Cohort Analysis**

```sql
-- Match Stories users with similar non-Stories users
WITH stories_users AS (
  -- Users who created at least 1 Story
  SELECT DISTINCT user_id
  FROM stories
  WHERE created_at BETWEEN '2016-08-01' AND '2016-08-31'
),
matched_non_stories AS (
  -- Match on: signup date, pre-Stories engagement level, follower count
  SELECT 
    nu.user_id,
    nu.signup_date,
    nu.pre_stories_sessions_per_week,
    nu.follower_count
  FROM non_stories_users nu
  INNER JOIN stories_users su
    ON nu.signup_cohort = su.signup_cohort  -- Same signup month
    AND ABS(nu.pre_stories_sessions - su.pre_stories_sessions) < 2  -- Similar engagement
    AND nu.follower_count BETWEEN su.follower_count * 0.8 AND su.follower_count * 1.2
  LIMIT 1  -- 1:1 matching
)
-- Now compare feed engagement between matched groups
SELECT 
    'Stories Users' as cohort,
    AVG(feed_posts_per_week) as avg_feed_posts,
    AVG(feed_time_per_week) as avg_feed_time,
    AVG(sessions_per_week) as avg_sessions
FROM user_engagement
WHERE user_id IN (SELECT user_id FROM stories_users)

UNION ALL

SELECT 
    'Non-Stories Users (Matched)' as cohort,
    AVG(feed_posts_per_week),
    AVG(feed_time_per_week),
    AVG(sessions_per_week)
FROM user_engagement
WHERE user_id IN (SELECT user_id FROM matched_non_stories);
```

**Interpretation:**

**Scenario A: Incremental (Good)**
```
Cohort                    | Feed Posts | Feed Time | Sessions
--------------------------|------------|-----------|----------
Stories Users             | 2.5/week   | 15 min    | 12/week
Non-Stories Users         | 2.8/week   | 16 min    | 8/week
Difference                | -11%       | -6%       | +50%
```
→ Stories users post slightly less to Feed BUT visit way more often
→ Net positive: Higher session frequency = better retention

**Scenario B: Cannibalization (Bad)**
```
Stories Users             | 1.5/week   | 10 min    | 8/week
Non-Stories Users         | 2.8/week   | 16 min    | 8/week
Difference                | -46%       | -38%      | 0%
```
→ Stories users post much less to Feed, no session increase
→ Red flag: Just shifting behavior, not adding value

---

### **Method 3: Holdout Experiment** 🧪

**Gold standard: Run a controlled experiment**

**Design:**
```
Randomly assign 10% of users to "No Stories" group
- They don't see Stories feature at all
- Compare their behavior to the 90% with Stories

Duration: 4-8 weeks
```

**Analysis:**
```sql
-- Incrementality calculation
WITH control_group AS (
  SELECT 
    AVG(total_posts) as avg_posts,
    AVG(time_in_app) as avg_time,
    AVG(sessions) as avg_sessions
  FROM users
  WHERE experiment_group = 'no_stories'
    AND cohort_week = '2016-08-01'
),
treatment_group AS (
  SELECT 
    AVG(total_posts) as avg_posts,
    AVG(time_in_app) as avg_time,
    AVG(sessions) as avg_sessions
  FROM users
  WHERE experiment_group = 'with_stories'
    AND cohort_week = '2016-08-01'
)
SELECT 
    (t.avg_time - c.avg_time) / c.avg_time as pct_time_lift,
    (t.avg_sessions - c.avg_sessions) / c.avg_sessions as pct_session_lift,
    (t.avg_posts - c.avg_posts) / c.avg_posts as pct_post_lift
FROM treatment_group t, control_group c;
```

**Example results:**
```
Metric              | Control (No Stories) | Treatment (Stories) | Lift
--------------------|----------------------|---------------------|-------
Time in app         | 22 min/day           | 28 min/day          | +27%
Sessions/week       | 14                   | 18                  | +29%
Total posts/week    | 3.0                  | 6.5                 | +117%
Feed posts/week     | 3.0                  | 2.5                 | -17%
```

**Interpretation:**
- ✅ Overall engagement WAY up (+27% time, +29% sessions)
- ✅ Total content creation doubles
- ⚠️ Feed posts decline 17%
- ✅ **Conclusion:** Mild cannibalization, but massive net gain

---

## **Synthesis: How to Determine Cannibalization**

**Use this decision framework:**

### **Green Light (Incremental) ✅**
```
✓ Total time in app increases >10%
✓ Total content (Feed + Stories) increases significantly
✓ Feed posts decrease <10%
✓ Session frequency increases
✓ Retention improves

→ Stories is creating NEW engagement
```

### **Yellow Light (Partial Cannibalization) ⚠️**
```
~ Total time increases 0-10%
~ Feed posts decrease 10-20%
~ Total content increases moderately
~ Session frequency stable

→ Stories is somewhat substitutive, but acceptable tradeoff
→ Monitor closely, might need to adjust
```

### **Red Light (Significant Cannibalization) ❌**
```
✗ Total time in app flat or declining
✗ Feed posts decrease >20%
✗ Total content flat
✗ Session frequency declining
✗ Retention worsening

→ Stories is just shifting behavior, not adding value
→ Need to pivot or improve feed to retain balance
```

---

## **Practical Recommendation:**

**Week 1-4:** Use Method 1 (Before/After) - fastest signal

**Week 4-8:** Add Method 2 (Cohort Comparison) - control for selection bias

**Week 8+:** Run Method 3 (Holdout Test) - definitive answer

**Dashboard to monitor:**
```
Stories Incrementality Dashboard

📊 Total Engagement:
- Time in app: +23% ✅
- Sessions/week: +18% ✅

📉 Feed Health:
- Feed posts: -12% ⚠️
- Feed time: -8% ⚠️

✅ Net Assessment: INCREMENTAL
Stories creating +15% net engagement despite mild feed cannibalization
```

---

## **Key Takeaway:**

**Some cannibalization is OKAY if:**
1. Total engagement increases significantly
2. Retention improves
3. User satisfaction is high
4. The decline is small (<15%)

**Stories should be judged on NET impact, not just whether Feed stays unchanged.**

The goal isn't to preserve Feed at all costs - it's to maximize overall Instagram value.""",
                "good_points": [
                    "Using multiple methods to triangulate the answer",
                    "Showing actual SQL queries for analysis",
                    "Understanding that some cannibalization might be acceptable",
                    "Proposing a holdout experiment for definitive answer",
                    "Providing a clear decision framework (green/yellow/red)",
                    "Thinking about net impact, not just individual metrics"
                ],
                "missing_points": [
                    "Statistical significance testing for the differences observed",
                    "Segmentation analysis (maybe cannibalization varies by user type)",
                    "Time-series analysis (is cannibalization temporary or permanent?)",
                    "Consideration of network effects (if creators decrease, viewers might too)"
                ]
            },
            3: {
                "framework": "Data-Driven Decision Matrix: Success Criteria → Investment Decision",
                "answer": """**The Investment Decision: After 3 months, should we double down, maintain, or pivot?**

This requires looking at the full picture across multiple dimensions, not just one metric.

---

## **Framework: Multi-Dimensional Decision Matrix**

Evaluate Stories across 5 key dimensions, then make investment recommendation.

---

### **Dimension 1: Adoption & Usage** 📈

**Questions to answer:**
- Did users adopt the feature?
- Are they using it regularly?
- Is usage growing or plateauing?

**Data to analyze:**

**A) Adoption Curve**
```sql
-- Weekly adoption trajectory
SELECT 
    DATE_TRUNC('week', first_story_date) as cohort_week,
    COUNT(DISTINCT user_id) as new_stories_users,
    SUM(COUNT(DISTINCT user_id)) OVER (ORDER BY DATE_TRUNC('week', first_story_date)) as cumulative_users
FROM (
    SELECT user_id, MIN(created_at) as first_story_date
    FROM stories
    GROUP BY user_id
) first_stories
GROUP BY cohort_week
ORDER BY cohort_week;
```

**Success indicators:**
✅ Adoption accelerating (J-curve growth)
✅ 30%+ of MAU have tried Stories
✅ Week-over-week growth rate >10%

**Warning signs:**
❌ Adoption plateauing after initial spike
❌ <15% of MAU engaged
❌ Growth rate declining

---

**B) Power User Analysis**
```sql
-- Distribution of Stories usage
SELECT 
    stories_created_per_user,
    COUNT(*) as num_users,
    SUM(COUNT(*)) OVER (ORDER BY stories_created_per_user) as cumulative_users
FROM (
    SELECT 
        user_id,
        CASE 
            WHEN COUNT(*) = 0 THEN 'None'
            WHEN COUNT(*) BETWEEN 1 AND 5 THEN '1-5'
            WHEN COUNT(*) BETWEEN 6 AND 20 THEN '6-20'
            WHEN COUNT(*) > 20 THEN '20+'
        END as stories_created_per_user
    FROM stories
    WHERE created_at >= CURRENT_DATE - 90
    GROUP BY user_id
) user_segments
GROUP BY stories_created_per_user;
```

**What to look for:**
- ✅ Healthy distribution (not just power users)
- ✅ Growing "casual creators" segment (6-20 Stories)
- ❌ Only power users engaged (top 5% create 90% of Stories)

---

### **Dimension 2: Engagement Quality** ⭐

**Questions:**
- Are users genuinely engaged or just trying it once?
- Is content quality high?
- Are network effects forming?

**Data to analyze:**

**A) Retention Cohorts**
```sql
-- Day 7, Day 30 retention for Stories users
WITH first_story AS (
    SELECT user_id, MIN(DATE(created_at)) as first_date
    FROM stories
    GROUP BY user_id
)
SELECT 
    first_date as cohort,
    COUNT(DISTINCT fs.user_id) as cohort_size,
    COUNT(DISTINCT CASE 
        WHEN s2.created_at BETWEEN fs.first_date + 7 AND fs.first_date + 13 
        THEN fs.user_id END) * 100.0 / COUNT(DISTINCT fs.user_id) as day7_retention,
    COUNT(DISTINCT CASE 
        WHEN s2.created_at BETWEEN fs.first_date + 30 AND fs.first_date + 36 
        THEN fs.user_id END) * 100.0 / COUNT(DISTINCT fs.user_id) as day30_retention
FROM first_story fs
LEFT JOIN stories s2 ON fs.user_id = s2.user_id
GROUP BY first_date
ORDER BY first_date;
```

**Success criteria:**
✅ Day 7 retention >40%
✅ Day 30 retention >25%
✅ Retention improving over time (later cohorts better than early)

---

**B) Engagement Depth**
```
Metrics:
- Completion rate: >60% of Stories watched to end
- Reply rate: >20% of Stories get a reply
- Time per session: >5 minutes on Stories
- Stories per creator: 2-3/day average

Success: All metrics above thresholds and stable/improving
```

---

### **Dimension 3: Business Impact** 💰

**Questions:**
- Does Stories improve our core business metrics?
- What's the incrementality?
- Any negative impacts?

**Data to analyze:**

**A) Overall Platform Health**
```sql
-- Compare key metrics before vs. after Stories
WITH baseline AS (
    SELECT 
        AVG(daily_time_spent) as avg_time,
        AVG(sessions_per_week) as avg_sessions,
        AVG(retention_day30) as avg_retention
    FROM user_metrics
    WHERE metric_date BETWEEN '2016-06-01' AND '2016-07-31'  -- Pre-Stories
),
post_stories AS (
    SELECT 
        AVG(daily_time_spent) as avg_time,
        AVG(sessions_per_week) as avg_sessions,
        AVG(retention_day30) as avg_retention
    FROM user_metrics
    WHERE metric_date BETWEEN '2016-09-01' AND '2016-10-31'  -- Post-Stories (60 days)
)
SELECT 
    (p.avg_time - b.avg_time) / b.avg_time as time_lift,
    (p.avg_sessions - b.avg_sessions) / b.avg_sessions as session_lift,
    (p.avg_retention - b.avg_retention) / b.avg_retention as retention_lift
FROM baseline b, post_stories p;
```

**Success indicators:**
✅ Time in app: +10% or more
✅ Sessions: +15% or more
✅ Retention: +5% or more
✅ MAU growth accelerating

---

**B) Revenue Impact** (if applicable)
```
Questions:
- If we run ads in Stories, what's potential revenue?
- Is there ANY negative revenue impact? (e.g., Feed ads performing worse)
- User LTV increasing?

Success: Revenue neutral or positive, clear path to monetization
```

---

### **Dimension 4: User Sentiment** ❤️

**Questions:**
- Do users actually like Stories?
- Any backlash or complaints?
- Would users miss it if we removed it?

**Data to analyze:**

**A) Survey Data**
```
Questions to ask users:
1. "How would you feel if Stories was removed?" 
   - Very disappointed / Somewhat disappointed / Not disappointed

2. "How has Stories changed your Instagram experience?"
   - Much better / Better / Same / Worse / Much worse

Success: >40% "Very disappointed" on Q1, >60% "Better/Much better" on Q2
```

**B) App Store Reviews & NPS**
```sql
-- Sentiment analysis of reviews mentioning "Stories"
SELECT 
    DATE_TRUNC('month', review_date) as month,
    AVG(CASE WHEN review_text ILIKE '%stories%' THEN star_rating ELSE NULL END) as stories_avg_rating,
    AVG(star_rating) as overall_avg_rating
FROM app_reviews
WHERE review_date >= '2016-08-01'
GROUP BY month;
```

**Success:**
✅ Stories mentions have 4+ star average
✅ Overall app rating stable or improved
✅ Positive sentiment in review text

---

**C) Support Tickets & Complaints**
```
Metrics:
- % of support tickets about Stories: <5%
- Privacy complaints: Not increasing
- Bug reports trending down (early bugs fixed)

Success: Low complaint rate, no major controversies
```

---

### **Dimension 5: Competitive Position** 🎯

**Questions:**
- Are we closing the gap with Snapchat?
- Are we winning back users?
- What's our differentiation?

**Data to analyze:**

**A) User Migration**
```sql
-- Are we re-engaging Snapchat users?
SELECT 
    COUNT(DISTINCT CASE 
        WHEN last_session BETWEEN CURRENT_DATE - 60 AND CURRENT_DATE - 30 
        THEN user_id END) as dormant_users,
    COUNT(DISTINCT CASE 
        WHEN last_session BETWEEN CURRENT_DATE - 60 AND CURRENT_DATE - 30
        AND user_id IN (SELECT user_id FROM stories WHERE created_at >= CURRENT_DATE - 30)
        THEN user_id END) as reactivated_via_stories,
    (reactivated_via_stories * 100.0 / dormant_users) as reactivation_rate
FROM user_activity;
```

**Success:**
✅ Dormant user reactivation >5%
✅ Stories driving new user growth
✅ Competitive feature parity achieved

---

**B) Market Benchmarks**
```
Questions to research:
- Snapchat Stories DAU: X million
- Instagram Stories DAU: Y million (are we catching up?)
- Time spent: Are we competitive?

Success: Closing gap with Snapchat, or pulling ahead
```

---

## **Decision Matrix: Invest More, Maintain, or Pivot?**

Based on the 5 dimensions, use this rubric:

---

### **SCENARIO A: INVEST MORE** 💰💰💰

**When all/most of these are true:**

✅ **Adoption:** 30%+ MAU engaged, growth accelerating
✅ **Engagement:** Retention >40% D7, completion rate >60%
✅ **Business:** +15% time in app, +10% retention, MAU accelerating
✅ **Sentiment:** Users love it (>40% "very disappointed" if removed)
✅ **Competition:** Closing gap with Snapchat or pulling ahead

**Investment recommendations:**
1. **Double engineering headcount** on Stories
2. **Add features:** AR filters, music, links, shopping
3. **Expand placement:** Make Stories more prominent in feed
4. **Monetization:** Start testing Stories ads
5. **Marketing:** Promote Stories heavily to non-users
6. **Global expansion:** Localize for key markets

**Why double down:**
"Stories is a major success. Users love it, engagement is through the roof, and we're gaining on Snapchat. This is a generational product opportunity - we should go all-in."

---

### **SCENARIO B: MAINTAIN** 🔄

**When results are mixed:**

~ **Adoption:** 15-25% MAU, moderate growth
~ **Engagement:** Retention 25-35% D7, engagement okay but not great
~ **Business:** +5-10% key metrics, no harm but not transformational
~ **Sentiment:** Users neutral to positive, no strong love/hate
~ **Competition:** Not losing ground but not winning either

**Investment recommendations:**
1. **Keep current team size** (don't scale up yet)
2. **Iterate on product:** Fix friction points, improve quality
3. **Run experiments:** Test different UX, features, placements
4. **Monitor metrics:** Wait for clearer signal before big investment
5. **Targeted features:** Add selective improvements based on user feedback

**Why maintain:**
"Stories shows promise but hasn't proven transformational yet. Let's continue investing at current levels, iterate on the product, and reassess in another quarter. We're not killing it, but we're also not scaling investment until we see stronger product-market fit."

---

### **SCENARIO C: PIVOT** 🔀

**When most of these are true:**

❌ **Adoption:** <15% MAU, plateauing or declining
❌ **Engagement:** Retention <20% D7, low completion rates
❌ **Business:** No improvement in key metrics, or negative trends
❌ **Sentiment:** Users indifferent or negative
❌ **Competition:** Not competitive, not moving needle

**Pivot recommendations:**

**Option 1: Repositioning**
- Change who Stories is for (e.g., only close friends, not public)
- Change what Stories is for (e.g., focus on messaging, not broadcasting)
- Change placement (less prominent, don't force)

**Option 2: Feature Pruning**
- Scale back investment (reduce to 1-2 engineers)
- Keep as niche feature for power users
- Focus on other growth initiatives

**Option 3: Sunset**
- If truly failing and no path forward
- Remove feature gracefully
- Learn lessons for future launches

**Why pivot:**
"Stories hasn't achieved product-market fit despite 3 months of effort. Users aren't adopting it at scale, engagement is weak, and it's not moving our core metrics. We should either significantly change the approach or reallocate resources to higher-impact initiatives."

---

## **The Decision Framework in Practice:**

**Score each dimension 1-5:**

| Dimension       | Score | Weight | Weighted Score |
|-----------------|-------|--------|----------------|
| Adoption        | 4     | 25%    | 1.0            |
| Engagement      | 5     | 30%    | 1.5            |
| Business Impact | 4     | 25%    | 1.0            |
| User Sentiment  | 4     | 15%    | 0.6            |
| Competition     | 3     | 5%     | 0.15           |
| **TOTAL**       |       |        | **4.25/5**     |

**Decision rubric:**
- **4.0-5.0:** INVEST MORE
- **3.0-3.9:** MAINTAIN
- **<3.0:** PIVOT

**Example:** Score of 4.25 → **Invest More** ✅

---

## **What to Present to Leadership:**

**Executive Summary:**
```
Stories 90-Day Review: INVEST MORE

✅ Adoption: 35% of MAU creating/viewing Stories
✅ Engagement: 45% D7 retention, 65% completion rate
✅ Business Impact: +18% time in app, +12% retention
✅ User Love: 48% would be "very disappointed" if removed
~ Competitive: Catching up to Snapchat but not ahead yet

RECOMMENDATION: Double investment in Stories
- Add 10 more engineers
- Launch Stories ads by Q4
- Add AR filters and music
- Aggressive marketing campaign

Projected Impact: +25% DAU growth, $500M annual revenue (ads)
```

---

## **Key Principles:**

✅ **Multi-dimensional** - One metric isn't enough
✅ **Quantitative + Qualitative** - Data AND user sentiment
✅ **Forward-looking** - What's the growth trajectory?
✅ **Risk-adjusted** - What could go wrong?
✅ **Actionable** - Clear investment recommendation

**This is how senior analysts think about product decisions.** 🎯""",
                "good_points": [
                    "Multi-dimensional evaluation framework (not just one metric)",
                    "Clear decision criteria for invest/maintain/pivot",
                    "Combining quantitative data with qualitative signals",
                    "Showing actual SQL queries for the analysis",
                    "Thinking about competitive positioning",
                    "Providing specific, actionable recommendations",
                    "Executive summary format for presenting to leadership"
                ],
                "missing_points": [
                    "Risk assessment (what are the risks of each decision?)",
                    "Resource requirements (cost of each investment level)",
                    "Alternative opportunities (what else could we invest in?)",
                    "Phased approach (can we test before full commitment?)"
                ]
            }
        },
        "common_mistakes": [
            "Choosing vanity metrics that don't tie to business goals",
            "Not defining what success looks like upfront",
            "Forgetting guardrail/counter-metrics (what could go wrong)",
            "Not considering cannibalization of existing features",
            "Picking too many metrics without prioritization",
            "Only looking at aggregate data, not segmenting by user type",
            "Not thinking about leading vs. lagging indicators",
            "Confusing correlation with causation (need incrementality analysis)"
        ],
        "key_takeaways": [
            "Always start by defining business goals and what 'success' means",
            "Choose ONE North Star Metric that best captures success",
            "Organize metrics into tiers: Primary, Secondary, Guardrails",
            "Include counter-metrics to catch unintended consequences",
            "Analyze incrementality, not just absolute metrics (Stories vs. control)",
            "Balance adoption (breadth) with engagement (depth)",
            "Use multiple methods to validate findings (before/after, cohorts, experiments)",
            "Make investment decisions based on multi-dimensional analysis"
        ]
    }
}

# CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .case-card {
        padding: 1.5rem;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        margin: 1rem 0;
        background: #f9f9f9;
    }
    .difficulty-intermediate {
        color: #f59e0b;
        font-weight: bold;
    }
    .difficulty-beginner {
        color: #10b981;
        font-weight: bold;
    }
    .difficulty-advanced {
        color: #ef4444;
        font-weight: bold;
    }
    .framework-tag {
        display: inline-block;
        background: #e0f2fe;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    .question-box {
        background: #fffbeb;
        padding: 1rem;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .solution-section {
        background: #f0fdf4;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .good-point {
        color: #16a34a;
    }
    .missing-point {
        color: #dc2626;
    }
</style>
""", unsafe_allow_html=True)

def home_page():
    st.markdown("""
    <div class="main-header">
        <h1>📚 Interactive Case Study Practice Tool</h1>
        <p>Master analytics case interviews with practice, frameworks, and detailed solutions</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📖 Browse Cases", use_container_width=True):
            st.session_state.current_page = 'library'
            st.rerun()
    
    with col2:
        if st.button("🎯 Practice Mode", use_container_width=True):
            st.session_state.current_page = 'practice_setup'
            st.rerun()
    
    with col3:
        if st.button("📝 Frameworks", use_container_width=True):
            st.session_state.current_page = 'frameworks'
            st.rerun()
    
    with col4:
        if st.button("💡 My Solutions", use_container_width=True, disabled=True):
            st.info("Coming soon!")
    
    st.markdown("---")
    st.subheader("📚 Featured Cases")
    
    # Display case cards
    for case_id, case_data in CASES.items():
        # Choose emoji based on difficulty
        if case_data['difficulty'] == 'Beginner':
            emoji = '🟢'
        elif case_data['difficulty'] == 'Intermediate':
            emoji = '🟡'
        else:
            emoji = '🔴'
        
        st.markdown(f"""
        <div class="case-card">
            <h3>{emoji} {case_data['title']}</h3>
            <p><span class="difficulty-{case_data['difficulty'].lower()}">{case_data['difficulty']}</span> | 
            {case_data['type']} | ⏱️ {case_data['time']}</p>
            <p>{case_data['scenario'][:150]}...</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("View Details", key=f"view_{case_id}"):
                st.session_state.selected_case = case_id
                st.session_state.current_page = 'case_detail'
                st.rerun()
        with col2:
            if st.button("Start Practice", key=f"practice_{case_id}"):
                st.session_state.selected_case = case_id
                st.session_state.current_page = 'practice_setup'
                st.rerun()

def case_library_page():
    st.title("📖 Case Library")
    
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        difficulty_filter = st.selectbox("Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])
    with col2:
        type_filter = st.selectbox("Case Type", ["All", "Customer Retention", "Root Cause Analysis", "Metrics Analysis"])
    with col3:
        search = st.text_input("🔍 Search cases")
    
    # Apply filters
    filtered_cases = {}
    for case_id, case_data in CASES.items():
        # Check difficulty filter
        if difficulty_filter != "All" and case_data['difficulty'] != difficulty_filter:
            continue
        
        # Check type filter
        if type_filter != "All" and case_data['type'] != type_filter:
            continue
        
        # Check search filter
        if search and search.lower() not in case_data['title'].lower() and search.lower() not in case_data['scenario'].lower():
            continue
        
        # If passes all filters, include it
        filtered_cases[case_id] = case_data
    
    # Display filtered cases
    if not filtered_cases:
        st.info("No cases match your filters. Try adjusting your selection.")
    else:
        for case_id, case_data in filtered_cases.items():
            # Choose emoji based on difficulty
            if case_data['difficulty'] == 'Beginner':
                emoji = '🟢'
            elif case_data['difficulty'] == 'Intermediate':
                emoji = '🟡'
            else:
                emoji = '🔴'
            
            st.markdown(f"""
            <div class="case-card">
                <h3>{emoji} {case_data['title']}</h3>
                <p><strong>Difficulty:</strong> {case_data['difficulty']} | 
                <strong>Type:</strong> {case_data['type']} | 
                <strong>Time:</strong> {case_data['time']}</p>
                <p><strong>Skills:</strong> {', '.join(case_data['skills'])}</p>
                <p>{case_data['scenario'][:200]}...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("View Full Case", key=f"full_{case_id}"):
                st.session_state.selected_case = case_id
                st.session_state.current_page = 'case_detail'
                st.rerun()

def case_detail_page():
    # Safety check - if no case selected, go back to library
    if 'selected_case' not in st.session_state:
        st.session_state.selected_case = 'loyalty_program'
    
    case_id = st.session_state.selected_case
    case = CASES[case_id]
    
    if st.button("← Back"):
        st.session_state.current_page = 'library'
        st.rerun()
    
    st.title(case['title'])
    st.markdown(f"**{case['difficulty']}** | {case['type']} | ⏱️ {case['time']}")
    
    st.markdown("---")
    
    # Scenario
    st.subheader("📋 Scenario")
    st.info(case['scenario'])
    
    # Questions
    st.subheader("❓ Questions You'll Answer")
    for i, q in enumerate(case['questions'], 1):
        st.markdown(f"""
        <div class="question-box">
            <strong>Question {i}:</strong> {q}
        </div>
        """, unsafe_allow_html=True)
    
    # Frameworks
    st.subheader("🎯 Key Frameworks")
    for framework in case['frameworks']:
        st.markdown(f'<span class="framework-tag">{framework}</span>', unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Start Practice Mode", use_container_width=True):
            st.session_state.current_page = 'practice_setup'
            st.rerun()
    with col2:
        if st.button("📖 View Full Solution", use_container_width=True):
            st.session_state.show_solution = True
            st.session_state.current_page = 'full_solution'
            st.rerun()

def practice_setup_page():
    # Safety check
    if 'selected_case' not in st.session_state:
        st.session_state.selected_case = 'loyalty_program'
    
    case_id = st.session_state.get('selected_case', 'loyalty_program')
    case = CASES[case_id]
    
    if st.button("← Back"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.title("🎯 Practice Mode Setup")
    st.subheader(case['title'])
    
    st.markdown("---")
    
    # Scenario
    st.subheader("📋 Scenario")
    st.info(case['scenario'])
    
    # Questions preview
    st.subheader("❓ Questions You'll Answer")
    for i, q in enumerate(case['questions'], 1):
        st.markdown(f"{i}. {q}")
    
    # Options
    st.markdown("---")
    st.subheader("⚙️ Practice Options")
    
    col1, col2 = st.columns(2)
    with col1:
        timer_option = st.radio(
            "⏱️ Time Limit:",
            ["No timer", "10 minutes", "15 minutes", "20 minutes"],
            index=3
        )
    
    with col2:
        hints = st.checkbox("💡 Enable hints during practice", value=True)
    
    st.markdown("---")
    
    if st.button("▶️ Start Practice", use_container_width=True, type="primary"):
        st.session_state.practicing = True
        st.session_state.current_question = 0
        st.session_state.user_answers = {}
        st.session_state.current_page = 'practice'
        st.rerun()

def practice_page():
    case_id = st.session_state.get('selected_case', 'loyalty_program')
    case = CASES[case_id]
    current_q = st.session_state.current_question
    
    # Progress bar
    progress = (current_q + 1) / len(case['questions'])
    st.progress(progress)
    st.markdown(f"**Question {current_q + 1} of {len(case['questions'])}**")
    
    st.markdown("---")
    
    # Current question
    st.markdown(f"""
    <div class="question-box">
        <h3>Question {current_q + 1}</h3>
        <p>{case['questions'][current_q]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer text area
    st.subheader("✍️ Your Answer")
    answer = st.text_area(
        "Type your answer here...",
        value=st.session_state.user_answers.get(current_q, ""),
        height=300,
        key=f"answer_{current_q}"
    )
    
    # Save answer
    st.session_state.user_answers[current_q] = answer
    
    st.markdown("---")
    
    # Warning dialog for empty answers
    if 'show_warning' not in st.session_state:
        st.session_state.show_warning = False
    
    if st.session_state.show_warning:
        st.warning("⚠️ You haven't entered any response. Are you sure you want to continue without answering?")
        col_warn1, col_warn2 = st.columns(2)
        with col_warn1:
            if st.button("Yes, continue anyway", type="secondary"):
                st.session_state.show_warning = False
                if st.session_state.pending_action == 'next':
                    st.session_state.current_question += 1
                elif st.session_state.pending_action == 'finish':
                    st.session_state.current_page = 'review'
                    st.session_state.current_question = 0
                st.rerun()
        with col_warn2:
            if st.button("No, let me answer"):
                st.session_state.show_warning = False
                st.rerun()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_q > 0:
            if st.button("← Previous Question"):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        if st.button("💡 Need a hint?"):
            if current_q in case['solutions']:
                st.info(f"**Framework:** {case['solutions'][current_q]['framework']}")
    
    with col3:
        if current_q < len(case['questions']) - 1:
            if st.button("Next Question →"):
                # Check if answer is empty
                if not answer or answer.strip() == "":
                    st.session_state.show_warning = True
                    st.session_state.pending_action = 'next'
                    st.rerun()
                else:
                    st.session_state.current_question += 1
                    st.rerun()
        else:
            if st.button("🏁 Finish & Review", type="primary"):
                # Check if answer is empty
                if not answer or answer.strip() == "":
                    st.session_state.show_warning = True
                    st.session_state.pending_action = 'finish'
                    st.rerun()
                else:
                    st.session_state.current_page = 'review'
                    st.session_state.current_question = 0
                    st.rerun()

def review_page():
    case_id = st.session_state.get('selected_case', 'loyalty_program')
    case = CASES[case_id]
    current_q = st.session_state.current_question
    
    st.title("✅ Solution Review")
    st.markdown(f"**Question {current_q + 1} of {len(case['questions'])}**")
    
    st.markdown("---")
    
    # Question
    st.markdown(f"""
    <div class="question-box">
        <strong>Question {current_q + 1}:</strong> {case['questions'][current_q]}
    </div>
    """, unsafe_allow_html=True)
    
    # Get user's answer
    user_answer = st.session_state.user_answers.get(current_q, "").strip()
    
    # Side by side comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Your Answer")
        if user_answer:
            st.markdown(f"```\n{user_answer}\n```")
        else:
            st.warning("⚠️ No answer provided")
    
    with col2:
        st.subheader("✅ Sample Solution")
        if current_q in case['solutions']:
            solution = case['solutions'][current_q]
            st.markdown(f"**Framework:** {solution['framework']}")
            st.markdown("---")
            with st.expander("View full solution", expanded=True):
                st.markdown(solution['answer'])
    
    # Intelligent feedback based on user's actual answer
    if current_q in case['solutions']:
        st.markdown("---")
        solution = case['solutions'][current_q]
        
        # Only show feedback if user actually answered
        if user_answer:
            st.markdown("### 📊 Answer Analysis")
            
            # Simple keyword-based analysis (you can make this smarter later with AI)
            user_answer_lower = user_answer.lower()
            
            # Check for key concepts in the user's answer
            strengths = []
            areas_to_improve = []
            
            # Question 1 - Metrics
            if current_q == 0:
                # Check for good points
                if any(word in user_answer_lower for word in ['clv', 'lifetime value', 'customer lifetime']):
                    strengths.append("Mentioned Customer Lifetime Value (CLV) - shows understanding of long-term value")
                if any(word in user_answer_lower for word in ['retention', 'churn']):
                    strengths.append("Included retention/churn metrics - shows you think about sustainability")
                if any(word in user_answer_lower for word in ['frequency', 'recency']):
                    strengths.append("Mentioned frequency/recency - core behavioral signals")
                if any(word in user_answer_lower for word in ['rfm', 'r-f-m']):
                    strengths.append("Referenced RFM framework - excellent structured approach")
                if any(word in user_answer_lower for word in ['margin', 'profitability', 'profit']):
                    strengths.append("Considered margin/profitability - not just revenue")
                if any(word in user_answer_lower for word in ['engagement', 'app usage', 'active']):
                    strengths.append("Included engagement metrics - important for digital products")
                
                # Check for missing concepts
                if not any(word in user_answer_lower for word in ['clv', 'lifetime value']):
                    areas_to_improve.append("Consider adding Customer Lifetime Value (CLV) as a key economic metric")
                if not any(word in user_answer_lower for word in ['rfm', 'recency', 'frequency', 'monetary']):
                    areas_to_improve.append("Try using the RFM (Recency, Frequency, Monetary) framework to structure your metrics")
                if not any(word in user_answer_lower for word in ['category', 'segment', 'behavioral', 'economic', 'engagement']):
                    areas_to_improve.append("Organize metrics into categories (behavioral, engagement, economic)")
                if not any(word in user_answer_lower for word in ['margin', 'profitability', 'contribution']):
                    areas_to_improve.append("Don't forget profitability metrics - revenue alone doesn't tell the full story")
            
            # Question 2 - Promo customers
            elif current_q == 1:
                # Check for good points
                if any(word in user_answer_lower for word in ['depends', 'tradeoff', 'pros and cons', 'both']):
                    strengths.append("Acknowledged tradeoffs - not giving a simple yes/no answer")
                if any(word in user_answer_lower for word in ['margin', 'profitability', 'unit economics', 'contribution']):
                    strengths.append("Considered profitability/unit economics")
                if any(word in user_answer_lower for word in ['segment', 'analyze', 'track']):
                    strengths.append("Suggested segmenting and analyzing rather than just deciding")
                if any(word in user_answer_lower for word in ['convert', 'conversion', 'eventually']):
                    strengths.append("Thought about conversion potential over time")
                if any(word in user_answer_lower for word in ['test', 'experiment', 'a/b']):
                    strengths.append("Mentioned testing/experimentation approach")
                
                # Check for missing concepts
                if not any(word in user_answer_lower for word in ['depends', 'tradeoff', 'both sides']):
                    areas_to_improve.append("Show you can see both sides - discuss pros AND cons")
                if not any(word in user_answer_lower for word in ['margin', 'profitability', 'economics']):
                    areas_to_improve.append("Mention contribution margin or unit economics")
                if not any(word in user_answer_lower for word in ['clv', 'lifetime value', 'long-term']):
                    areas_to_improve.append("Consider the customer's lifetime value trajectory, not just current behavior")
            
            # Question 3 - Tracking non-app purchases
            elif current_q == 2:
                # Check for good points
                if any(word in user_answer_lower for word in ['card', 'credit card', 'debit card', 'payment']):
                    strengths.append("Identified card-linking as a solution - common loyalty program practice")
                if any(word in user_answer_lower for word in ['email', 'phone', 'contact']):
                    strengths.append("Mentioned email/phone matching for customer identification")
                if any(word in user_answer_lower for word in ['pos', 'point of sale', 'register']):
                    strengths.append("Recognized POS system integration needs")
                if any(word in user_answer_lower for word in ['unified', 'single view', 'identity resolution', '360']):
                    strengths.append("Understood this as a unified customer view challenge")
                if any(word in user_answer_lower for word in ['incentive', 'points', 'reward', 'encourage']):
                    strengths.append("Thought about incentivizing customers to identify themselves")
                if any(word in user_answer_lower for word in ['privacy', 'transparent', 'consent']):
                    strengths.append("Considered privacy implications - important for customer trust")
                
                # Check for missing concepts
                if not any(word in user_answer_lower for word in ['card', 'credit', 'payment']):
                    areas_to_improve.append("Card-linking programs are the most common solution for this problem")
                if not any(word in user_answer_lower for word in ['unified', 'single view', 'complete view']):
                    areas_to_improve.append("Frame this as creating a 'unified customer view' across channels")
                if not any(word in user_answer_lower for word in ['multiple', 'several', 'data source']):
                    areas_to_improve.append("Consider multiple data sources (cards, email, phone, WiFi, etc.)")
                if not any(word in user_answer_lower for word in ['track', 'measure', 'metric', '%', 'percent']):
                    areas_to_improve.append("Suggest tracking % of unattributed transactions as a success metric")
            
            # Question 4 - Food attachment
            elif current_q == 3:
                # Check for good points
                if any(word in user_answer_lower for word in ['why', 'root cause', 'diagnose', 'understand', 'analyze']):
                    strengths.append("Started by diagnosing WHY - not jumping straight to solutions")
                if any(word in user_answer_lower for word in ['market basket', 'affinity', 'association']):
                    strengths.append("Used market basket analysis - appropriate analytical technique")
                if any(word in user_answer_lower for word in ['test', 'a/b', 'experiment', 'pilot']):
                    strengths.append("Suggested testing interventions rather than just implementing")
                if any(word in user_answer_lower for word in ['price', 'bundle', 'discount', 'promotion']):
                    strengths.append("Considered pricing strategies to drive attachment")
                if any(word in user_answer_lower for word in ['awareness', 'menu', 'visibility', 'recommend']):
                    strengths.append("Thought about awareness/discovery as a potential issue")
                if any(word in user_answer_lower for word in ['goal', 'objective', 'depends', 'business']):
                    strengths.append("Connected strategy to business goals - not just tactics")
                if any(word in user_answer_lower for word in ['survey', 'ask', 'feedback', 'customer input']):
                    strengths.append("Suggested getting direct customer feedback")
                
                # Check for missing concepts
                if not any(word in user_answer_lower for word in ['why', 'root cause', 'diagnose']):
                    areas_to_improve.append("Start with diagnosis - understand WHY before jumping to solutions")
                if not any(word in user_answer_lower for word in ['hypothesis', 'hypotheses', 'might be']):
                    areas_to_improve.append("Form hypotheses about root causes (awareness? price? quality? preference?)")
                if not any(word in user_answer_lower for word in ['test', 'experiment', 'a/b']):
                    areas_to_improve.append("Suggest A/B testing different interventions to see what works")
                if not any(word in user_answer_lower for word in ['metric', 'measure', 'track', 'kpi']):
                    areas_to_improve.append("Define how you'll measure success (food attachment rate, revenue, margin)")
                if not any(word in user_answer_lower for word in ['alternative', 'instead', 'different goal']):
                    areas_to_improve.append("Consider alternative strategies - maybe upselling premium coffee is better than forcing food")
            
            # Reddit Case - Root Cause Analysis
            # Question 1 - Diagnostic approach
            elif case_id == 'reddit_comments' and current_q == 0:
                # Check for good points
                if any(word in user_answer_lower for word in ['mece', 'framework', 'systematic', 'structured']):
                    strengths.append("Used a structured framework (MECE or similar) - shows organized thinking")
                if any(word in user_answer_lower for word in ['clarify', 'ask questions', 'understand', 'define']):
                    strengths.append("Started with clarifying questions - important before jumping to analysis")
                if any(word in user_answer_lower for word in ['data', 'measurement', 'tracking', 'logging']):
                    strengths.append("Checked data quality issues - critical first step many candidates miss")
                if any(word in user_answer_lower for word in ['internal', 'external', 'user', 'behavior']):
                    strengths.append("Covered multiple categories of potential causes")
                if any(word in user_answer_lower for word in ['segment', 'platform', 'region', 'breakdown']):
                    strengths.append("Thought about segmenting to narrow down the problem")
                if any(word in user_answer_lower for word in ['hypothesis', 'test', 'validate']):
                    strengths.append("Mentioned forming and testing hypotheses - data-driven approach")
                
                # Check for missing concepts
                if not any(word in user_answer_lower for word in ['mece', 'framework', 'systematic']):
                    areas_to_improve.append("Explicitly state your framework (MECE: Internal, External, User, Data)")
                if not any(word in user_answer_lower for word in ['data', 'measurement', 'tracking']):
                    areas_to_improve.append("Always check data quality FIRST - it's the fastest to verify and eliminates false alarms")
                if not any(word in user_answer_lower for word in ['prioritize', 'order', 'first', 'start with']):
                    areas_to_improve.append("Show prioritization logic - explain why you check certain things first")
                if not any(word in user_answer_lower for word in ['segment', 'breakdown', 'drill down']):
                    areas_to_improve.append("Mention segmentation (by platform, region, user type) to narrow the scope")
            
            # Question 2 - Data investigation priority
            elif case_id == 'reddit_comments' and current_q == 1:
                # Check for good points
                if any(word in user_answer_lower for word in ['data quality', 'tracking', 'measurement', 'logging']):
                    strengths.append("Prioritized data quality checks - fastest to verify")
                if any(word in user_answer_lower for word in ['deployment', 'release', 'code change', 'feature']):
                    strengths.append("Checked recent deployments - internal changes are common culprits")
                if any(word in user_answer_lower for word in ['segment', 'platform', 'breakdown', 'split']):
                    strengths.append("Mentioned segmentation analysis to identify affected groups")
                if any(word in user_answer_lower for word in ['sql', 'query', 'database', 'table']):
                    strengths.append("Showed technical depth with specific data queries")
                if any(word in user_answer_lower for word in ['funnel', 'conversion', 'drop-off', 'flow']):
                    strengths.append("Mentioned funnel analysis to find where users are dropping off")
                if any(word in user_answer_lower for word in ['error log', 'crash', 'bug', 'technical issue']):
                    strengths.append("Thought to check error logs and technical health")
                
                # Check for missing concepts
                if not any(word in user_answer_lower for word in ['priority', 'order', 'first', 'sequence']):
                    areas_to_improve.append("Explain your prioritization - why check X before Y?")
                if not any(word in user_answer_lower for word in ['data', 'tracking', 'measurement']):
                    areas_to_improve.append("Always start with data quality checks - eliminates false alarms quickly")
                if not any(word in user_answer_lower for word in ['segment', 'breakdown']):
                    areas_to_improve.append("Segment the data (platform, user type, region) to narrow the problem")
                if not any(word in user_answer_lower for word in ['timeline', 'how long', 'hours', 'days']):
                    areas_to_improve.append("Give time estimates - shows you understand urgency and resource tradeoffs")
            
            # Question 3 - Mobile-specific investigation
            elif case_id == 'reddit_comments' and current_q == 2:
                # Check for good points
                if any(word in user_answer_lower for word in ['ios', 'android', 'app version', 'mobile os']):
                    strengths.append("Sub-segmented mobile further (iOS vs Android, versions) - good deep-dive")
                if any(word in user_answer_lower for word in ['crash', 'error', 'bug', 'log']):
                    strengths.append("Checked crash logs and error reports - key for mobile issues")
                if any(word in user_answer_lower for word in ['app store', 'review', 'rating', 'user feedback']):
                    strengths.append("Looked at app store reviews for user-reported issues")
                if any(word in user_answer_lower for word in ['release', 'deployment', 'version', 'update']):
                    strengths.append("Connected timeline of app release to metric drop")
                if any(word in user_answer_lower for word in ['performance', 'latency', 'response time', 'slow']):
                    strengths.append("Considered performance issues, not just crashes")
                if any(word in user_answer_lower for word in ['ux', 'ui', 'flow', 'friction']):
                    strengths.append("Thought about UX changes that might add friction")
                
                # Check for missing concepts
                if not any(word in user_answer_lower for word in ['version', 'ios', 'android']):
                    areas_to_improve.append("Sub-segment mobile by OS and app version - mobile issues are often version-specific")
                if not any(word in user_answer_lower for word in ['crash', 'error log', 'crashlytics']):
                    areas_to_improve.append("Check crash logs and error tracking tools (Crashlytics, Sentry)")
                if not any(word in user_answer_lower for word in ['app store', 'review', 'rating']):
                    areas_to_improve.append("Monitor app store reviews - users often report issues there first")
                if not any(word in user_answer_lower for word in ['immediate', 'hotfix', 'rollback', 'action']):
                    areas_to_improve.append("For production bugs affecting users, outline immediate action plan")
            
            # Question 4 - Validation and recommendations
            elif case_id == 'reddit_comments' and current_q == 3:
                # Check for good points
                if any(word in user_answer_lower for word in ['a/b test', 'experiment', 'control group', 'test']):
                    strengths.append("Proposed A/B testing to validate hypothesis rigorously")
                if any(word in user_answer_lower for word in ['immediate', 'short-term', 'long-term', 'tier']):
                    strengths.append("Structured recommendations by time horizon - shows strategic thinking")
                if any(word in user_answer_lower for word in ['impact', 'revenue', 'users', 'cost', 'quantify']):
                    strengths.append("Quantified business impact - connects analysis to business outcomes")
                if any(word in user_answer_lower for word in ['prevent', 'future', 'process', 'monitoring']):
                    strengths.append("Included prevention measures, not just fixing current issue")
                if any(word in user_answer_lower for word in ['hotfix', 'rollback', 'deploy', 'fix']):
                    strengths.append("Clear immediate action (hotfix or rollback)")
                if any(word in user_answer_lower for word in ['post-mortem', 'learning', 'document', 'retrospective']):
                    strengths.append("Mentioned post-mortem/learning process")
                
                # Check for missing concepts
                if not any(word in user_answer_lower for word in ['validate', 'test', 'verify', 'confirm']):
                    areas_to_improve.append("Explain how you'd validate your hypothesis before implementing fixes")
                if not any(word in user_answer_lower for word in ['immediate', 'short', 'long']):
                    areas_to_improve.append("Structure recommendations by urgency: Immediate → Short-term → Long-term")
                if not any(word in user_answer_lower for word in ['prevent', 'future', 'monitoring', 'alert']):
                    areas_to_improve.append("Include prevention measures (monitoring, alerts, process improvements)")
                if not any(word in user_answer_lower for word in ['impact', 'cost', 'revenue', 'users affected']):
                    areas_to_improve.append("Quantify business impact to help prioritize the fix")
            
            # Instagram Stories Case - Metric Design
            # Question 1 - Defining success
            elif case_id == 'instagram_stories' and current_q == 0:
                # Check for good points
                if any(word in user_answer_lower for word in ['business goal', 'objective', 'why', 'purpose']):
                    strengths.append("Started by clarifying business goals - shows strategic thinking")
                if any(word in user_answer_lower for word in ['guardrail', 'counter', 'risk', 'downside', 'anti-goal']):
                    strengths.append("Included guardrail/counter-metrics - prevents unintended consequences")
                if any(word in user_answer_lower for word in ['retention', 'engagement', 'time', 'frequency']):
                    strengths.append("Focused on key outcome metrics (retention, engagement)")
                if any(word in user_answer_lower for word in ['cannibalize', 'cannibalization', 'shift', 'substitute']):
                    strengths.append("Thought about cannibalization of existing features")
                if any(word in user_answer_lower for word in ['adoption', 'usage', 'dau', 'mau', 'active']):
                    strengths.append("Considered both adoption and ongoing usage")
                if any(word in user_answer_lower for word in ['user value', 'satisfaction', 'nps', 'sentiment']):
                    strengths.append("Thought about user value, not just activity metrics")
                
                # Check for missing concepts
                if not any(word in user_answer_lower for word in ['business', 'goal', 'objective']):
                    areas_to_improve.append("Start by clarifying what business goal Stories is trying to achieve")
                if not any(word in user_answer_lower for word in ['guardrail', 'counter', 'risk', 'downside']):
                    areas_to_improve.append("Include guardrail metrics - what could go wrong? (e.g., feed cannibalization)")
                if not any(word in user_answer_lower for word in ['adoption', 'usage', 'both']):
                    areas_to_improve.append("Distinguish between adoption (trying it) and engagement (using it regularly)")
                if not any(word in user_answer_lower for word in ['target', 'threshold', '%', 'number']):
                    areas_to_improve.append("Provide specific numeric targets (e.g., '30% of DAU within 90 days')")
            
            # Question 2 - Specific metrics
            elif case_id == 'instagram_stories' and current_q == 1:
                # Check for good points
                if any(word in user_answer_lower for word in ['north star', 'primary', 'key', 'most important']):
                    strengths.append("Identified a primary/North Star metric - shows prioritization")
                if any(word in user_answer_lower for word in ['tier', 'priority', 'primary', 'secondary', 'organize']):
                    strengths.append("Organized metrics by priority - avoids tracking too many things")
                if any(word in user_answer_lower for word in ['leading', 'lagging', 'early', 'late', 'indicator']):
                    strengths.append("Distinguished between leading and lagging indicators")
                if any(word in user_answer_lower for word in ['input', 'output', 'controllable', 'result']):
                    strengths.append("Thought about input metrics (what we control) vs output metrics (results)")
                if any(word in user_answer_lower for word in ['adoption', 'engagement', 'retention']):
                    strengths.append("Covered the key metric categories (adoption, engagement, retention)")
                if any(word in user_answer_lower for word in ['aarrr', 'pirate', 'acquisition', 'activation']):
                    strengths.append("Referenced AARRR framework - shows structured thinking")
                
                # Check for missing concepts
                if not any(word in user_answer_lower for word in ['north star', 'primary', 'most important', 'key']):
                    areas_to_improve.append("Define ONE North Star Metric that best captures overall success")
                if not any(word in user_answer_lower for word in ['tier', 'priority', 'organize', 'level']):
                    areas_to_improve.append("Organize metrics into tiers (Primary, Secondary, Guardrails) to show prioritization")
                if not any(word in user_answer_lower for word in ['adoption', 'engagement', 'retention']):
                    areas_to_improve.append("Cover all three phases: Adoption (trying), Engagement (using), Retention (sticking)")
                if not any(word in user_answer_lower for word in ['target', 'threshold', 'goal', '%']):
                    areas_to_improve.append("Specify targets for each metric (e.g., '30% adoption within 90 days')")
            
            # Question 3 - Cannibalization analysis
            elif case_id == 'instagram_stories' and current_q == 2:
                # Check for good points
                if any(word in user_answer_lower for word in ['before', 'after', 'baseline', 'compare']):
                    strengths.append("Proposed before/after comparison - simple but effective analysis")
                if any(word in user_answer_lower for word in ['total', 'overall', 'aggregate', 'net']):
                    strengths.append("Thought about total/net engagement, not just individual metrics")
                if any(word in user_answer_lower for word in ['experiment', 'a/b', 'test', 'control', 'holdout']):
                    strengths.append("Proposed controlled experiment - gold standard for incrementality")
                if any(word in user_answer_lower for word in ['cohort', 'segment', 'matched', 'similar users']):
                    strengths.append("Mentioned cohort comparison to control for selection bias")
                if any(word in user_answer_lower for word in ['sql', 'query', 'data', 'analysis']):
                    strengths.append("Showed technical depth with specific data analysis approach")
                if any(word in user_answer_lower for word in ['acceptable', 'tradeoff', 'net positive', 'worth it']):
                    strengths.append("Understood that some cannibalization might be acceptable if net impact is positive")
                
                # Check for missing concepts
                if not any(word in user_answer_lower for word in ['before', 'after', 'compare', 'baseline']):
                    areas_to_improve.append("Compare user behavior before vs. after Stories launch")
                if not any(word in user_answer_lower for word in ['total', 'net', 'overall', 'aggregate']):
                    areas_to_improve.append("Look at total engagement, not just individual metrics (is the pie growing?)")
                if not any(word in user_answer_lower for word in ['experiment', 'test', 'control', 'holdout']):
                    areas_to_improve.append("Propose a holdout experiment for definitive incrementality measurement")
                if not any(word in user_answer_lower for word in ['acceptable', 'tradeoff', 'worth']):
                    areas_to_improve.append("Acknowledge some cannibalization is okay if net value is created")
            
            # Question 4 - Investment decision
            elif case_id == 'instagram_stories' and current_q == 3:
                # Check for good points
                if any(word in user_answer_lower for word in ['dimension', 'multiple', 'various', 'several factors']):
                    strengths.append("Evaluated multiple dimensions, not just one metric")
                if any(word in user_answer_lower for word in ['invest', 'maintain', 'pivot', 'decision', 'recommendation']):
                    strengths.append("Provided clear investment recommendation")
                if any(word in user_answer_lower for word in ['adoption', 'engagement', 'business', 'sentiment']):
                    strengths.append("Covered key evaluation dimensions (adoption, engagement, business impact, sentiment)")
                if any(word in user_answer_lower for word in ['criteria', 'threshold', 'rubric', 'framework']):
                    strengths.append("Defined decision criteria/thresholds - shows structured thinking")
                if any(word in user_answer_lower for word in ['retention', 'cohort', 'trajectory', 'trend']):
                    strengths.append("Looked at retention and growth trajectory, not just current state")
                if any(word in user_answer_lower for word in ['competitive', 'snapchat', 'market', 'competition']):
                    strengths.append("Considered competitive positioning")
                
                # Check for missing concepts
                if not any(word in user_answer_lower for word in ['dimension', 'multiple', 'various', 'several']):
                    areas_to_improve.append("Evaluate across multiple dimensions (adoption, engagement, business, sentiment, competition)")
                if not any(word in user_answer_lower for word in ['invest', 'maintain', 'pivot', 'recommendation']):
                    areas_to_improve.append("Provide a clear recommendation: Invest More, Maintain, or Pivot")
                if not any(word in user_answer_lower for word in ['criteria', 'threshold', 'if', 'then']):
                    areas_to_improve.append("Define decision criteria (e.g., 'If adoption >30%, invest more')")
                if not any(word in user_answer_lower for word in ['qualitative', 'sentiment', 'feedback', 'user']):
                    areas_to_improve.append("Include qualitative signals (user sentiment, feedback) not just quantitative")
            
            # Display analysis
            col1, col2 = st.columns(2)
            
            with col1:
                if strengths:
                    st.markdown("### ✅ What You Did Well")
                    for strength in strengths:
                        st.markdown(f"<p class='good-point'>✓ {strength}</p>", unsafe_allow_html=True)
                else:
                    st.markdown("### ✅ What You Did Well")
                    st.info("💡 Try incorporating some of the key concepts from the sample solution")
            
            with col2:
                if areas_to_improve:
                    st.markdown("### 💡 Areas to Strengthen")
                    for area in areas_to_improve:
                        st.markdown(f"<p class='missing-point'>• {area}</p>", unsafe_allow_html=True)
                else:
                    st.markdown("### 💡 Areas to Strengthen")
                    st.success("Great coverage of key concepts!")
        else:
            # No answer provided
            st.info("💡 **Tip:** Try answering the question first, then review the solution to see how your approach compares. This helps you learn the frameworks better!")
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_q > 0:
            if st.button("← Previous Question"):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        if st.button("View Full Solution"):
            st.session_state.current_page = 'full_solution'
            st.rerun()
    
    with col3:
        if current_q < len(case['questions']) - 1:
            if st.button("Next Question →"):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("🏠 Back to Home"):
                st.session_state.current_page = 'home'
                st.session_state.practicing = False
                st.session_state.current_question = 0
                st.session_state.user_answers = {}
                st.rerun()

def full_solution_page():
    # Safety check
    if 'selected_case' not in st.session_state:
        st.session_state.selected_case = 'loyalty_program'
    
    case_id = st.session_state.get('selected_case', 'loyalty_program')
    case = CASES[case_id]
    
    if st.button("← Back"):
        st.session_state.current_page = 'case_detail'
        st.rerun()
    
    st.title("📖 Complete Solution")
    st.subheader(case['title'])
    
    # Tabs for each question
    tabs = st.tabs([f"Q{i+1}" for i in range(len(case['questions']))] + ["Key Takeaways"])
    
    for i, tab in enumerate(tabs[:-1]):
        with tab:
            st.markdown(f"""
            <div class="question-box">
                <h4>Question {i+1}</h4>
                <p>{case['questions'][i]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if i in case['solutions']:
                solution = case['solutions'][i]
                
                st.markdown(f"""
                <div class="solution-section">
                    <h4>🎯 Framework</h4>
                    <p>{solution['framework']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### ✅ Sample Solution")
                st.markdown(solution['answer'])
    
    # Key takeaways tab
    with tabs[-1]:
        st.markdown("### 🚫 Common Mistakes")
        for mistake in case['common_mistakes']:
            st.markdown(f"❌ {mistake}")
        
        st.markdown("---")
        
        st.markdown("### 💡 Key Takeaways")
        for takeaway in case['key_takeaways']:
            st.markdown(f"✓ {takeaway}")
        
        st.markdown("---")
        
        st.markdown("### 📚 Related Frameworks")
        for framework in case['frameworks']:
            st.markdown(f'<span class="framework-tag">{framework}</span>', unsafe_allow_html=True)

def frameworks_page():
    st.title("📝 Framework Cheat Sheets")
    
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div class="case-card">
        <h3>📊 Metrics Frameworks</h3>
        <ul>
            <li><strong>RFM Analysis</strong> - Recency, Frequency, Monetary value</li>
            <li><strong>AARRR (Pirate Metrics)</strong> - Acquisition, Activation, Retention, Revenue, Referral</li>
            <li><strong>Cohort Analysis</strong> - Group users by time period to track behavior</li>
            <li><strong>Customer Lifetime Value (CLV)</strong> - Total value of customer over relationship</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="case-card">
        <h3>🎯 Problem-Solving Frameworks</h3>
        <ul>
            <li><strong>Root Cause Analysis</strong> - 5 Whys, Fishbone diagrams</li>
            <li><strong>Hypothesis-Driven Investigation</strong> - Form hypotheses, test with data</li>
            <li><strong>A/B Testing</strong> - Control vs. variant, statistical significance</li>
            <li><strong>Prioritization</strong> - RICE (Reach, Impact, Confidence, Effort)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="case-card">
        <h3>💼 Business Strategy Frameworks</h3>
        <ul>
            <li><strong>Profitability Analysis</strong> - Revenue, costs, contribution margin</li>
            <li><strong>Market Sizing</strong> - Top-down vs. bottom-up approaches</li>
            <li><strong>Pricing Strategy</strong> - Cost-plus, value-based, competitive</li>
            <li><strong>Market Basket Analysis</strong> - Product affinity, cross-selling</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main app routing
def main():
    page = st.session_state.current_page
    
    if page == 'home':
        home_page()
    elif page == 'library':
        case_library_page()
    elif page == 'case_detail':
        case_detail_page()
    elif page == 'practice_setup':
        practice_setup_page()
    elif page == 'practice':
        practice_page()
    elif page == 'review':
        review_page()
    elif page == 'full_solution':
        full_solution_page()
    elif page == 'frameworks':
        frameworks_page()

if __name__ == "__main__":
    main()
