const axios = require("axios");
const OpenAI = require("openai");
const fs = require("fs");
const { calculatePortfolioAnalytics } = require("./portfolioCalculations");

const client = new OpenAI({
    baseURL: "https://openrouter.ai/api/v1",
    apiKey: "ENTER YOUR API PATH"
});

// ==============================
// Prepare Clean Data For AI
// ==============================

function preparePortfolioData(data) {

    return {

        portfolio: data.portfolio.map(p => ({

            client_id: p.client_id,
            client_name: p.client_name,
            advisor_name: p.advisor_name,
            total_investment: p.total_investment,
            current_value: p.current_value,
            gain_loss: p.gain_loss,
            gain_percent: p.gain_percent,
            active_scheme_count: p.active_scheme_count,
            total_units: p.total_units,
            last_updated_date: p.last_updated_date

        })),

        schemePerformance: data.schemePerformance.map(s => ({

            scheme_name: s.scheme_name,
            amc_name: s.amc_name,
            category_name: s.category_name,
            investor_count: s.investor_count,
            total_aum: s.total_aum,
            average_return: s.average_return,
            units_held: s.units_held,
            latest_nav: s.latest_nav

        })),

        advisorPerformance: data.advisorPerformance.map(a => ({

            advisor_name: a.advisor_name,
            total_clients: a.total_clients,
            total_aum: a.total_aum,
            average_client_aum: a.average_client_aum

        })),

        sipAnalytics: data.sipAnalytics,

        revenue: data.revenue,

        redemptionAnalytics: data.redemptionAnalytics,

        amcBusiness: data.amcBusiness,

        executiveDashboard: data.executiveDashboard

    };

}

// ==============================
// Generate Report
// ==============================

async function getReport() {

    try {

        console.log("======================================");
        console.log("Fetching Portfolio Data...");
        console.log("======================================");

        const portfolioRes = await axios.get(
            "http://localhost:3000/client-portfolio"
        );

        const schemeRes = await axios.get(
            "http://localhost:3000/scheme-performance"
        );

        const advisorRes = await axios.get(
            "http://localhost:3000/advisor-performance"
        );

        const sipRes = await axios.get(
            "http://localhost:3000/sip-analytics"
        );

        const revenueRes = await axios.get(
            "http://localhost:3000/revenue-mart"
        );

        const redemptionRes = await axios.get(
            "http://localhost:3000/redemption-analytics"
        );

        const amcRes = await axios.get(
            "http://localhost:3000/amc"
        );

        const executiveRes = await axios.get(
            "http://localhost:3000/executive-dashboard"
        );

       const reportData = {

        portfolio: portfolioRes.data,

        schemePerformance: schemeRes.data,

        advisorPerformance: advisorRes.data,

        sipAnalytics: sipRes.data,

        revenue: revenueRes.data,

        redemptionAnalytics: redemptionRes.data,

        amcBusiness: amcRes.data,

        executiveDashboard: executiveRes.data};
        const analytics = calculatePortfolioAnalytics(reportData);

        console.log("Portfolio Data Loaded Successfully.");

        const cleanedData = preparePortfolioData(reportData);

        const finalData = { ...cleanedData,analytics};

        const response = await client.chat.completions.create({
                        model: "openai/gpt-4.1-mini",

            max_tokens: 7000,

            temperature: 0.2,

            messages: [

                {

                    role: "system",

                    content: `

You are a Senior Wealth Manager, Mutual Fund Analyst and Financial Planning Consultant working at Anytime Invest.

Your responsibility is to generate a premium client-ready Mutual Fund Portfolio Analysis Report.

The report must look like it has been prepared by a real financial advisor.

Never produce generic AI content.

Never assume values that are not present.

Never hallucinate.

If any value is unavailable write:

"Not Available in Portfolio Data"

====================================================

OUTPUT RULES

====================================================

Return ONLY valid HTML5.

Start directly with

<!DOCTYPE html>

End with

</html>

No markdown.

No explanation.

No JSON.

Everything must be inside one HTML file.

Embed CSS inside one <style> tag.

Do not use Bootstrap.

Do not use Tailwind.

No JavaScript.

====================================================

DESIGN

====================================================

Professional

Corporate

Minimal

Compact

PDF Friendly

A4 Print Friendly

White Background

Dark Blue Header

Professional Tables

Soft Gray Borders

Rounded Cards

Small Fonts

Use:

Body : 13px

Heading : 20px

Sub Heading : 16px

Table : 12px

Avoid huge spacing.

Avoid oversized cards.

Avoid unnecessary icons.

====================================================

MANDATORY REPORT STRUCTURE

====================================================

1.

Cover Page

Company Name

Report Title

Client Name

Advisor Name

Report Date

Report ID

Prepared By Anytime Invest

----------------------------------------------------

2.

Executive Dashboard

Portfolio Value

Investment

Gain Loss

Portfolio Health Score

Risk Level

Diversification Score

----------------------------------------------------

3.

Executive Summary

Minimum 180 words.

Professional language.

----------------------------------------------------

4.

Portfolio Snapshot

Professional table.

----------------------------------------------------

5.

Portfolio Performance Analysis

Minimum 200 words.

----------------------------------------------------

6.

Scheme Performance Analysis

Identify top performing schemes.

Identify weak schemes.

Explain observations.

----------------------------------------------------

7.

Advisor Performance Analysis

Explain advisor contribution.

----------------------------------------------------

8.

Portfolio Diversification

Minimum 180 words.

----------------------------------------------------

9.

Risk Assessment

Market Risk

Liquidity Risk

Concentration Risk

Overall Risk

Professional explanation.

----------------------------------------------------

10.

Portfolio Strengths

Minimum six points.

----------------------------------------------------

11.

Areas of Improvement

Minimum six points.

----------------------------------------------------

12.

Strategic Recommendations

Minimum eight recommendations.

Every recommendation must directly relate to the supplied data.

----------------------------------------------------

13.

Action Plan

Professional table.

Immediate

30 Days

90 Days

Annual Review

----------------------------------------------------

14.

Final Advisor Remarks

----------------------------------------------------

15.

Disclaimer

----------------------------------------------------

16.

Footer

Generated by Anytime Invest AI Advisory Platform

====================================================

VERY IMPORTANT

====================================================

CALCULATED ANALYTICS

====================================================

The dataset also contains a calculated analytics object.

Use it exactly as provided.

Do NOT recalculate any values.

Do NOT estimate any values.

The analytics object is already correct.

Never overwrite those values.

Never ignore the analytics object.

Use these fields exactly:

portfolioHealthScore
diversificationScore
riskScore
riskLevel
topScheme
worstScheme

Display portfolioHealthScore as Portfolio Health Score.

Display diversificationScore as Diversification Score.

Display riskScore and riskLevel in the Risk Assessment section.

Use topScheme as the Top Performing Scheme.

Use worstScheme as the Weakest Performing Scheme.

Never replace these values with "Not Available in Portfolio Data".

====================================================

Return ONLY one complete HTML5 document.

Start with <!DOCTYPE html>

End with </html>

Return only valid HTML.

Do not return markdown.

Do not wrap HTML inside triple backticks.

The HTML must be directly renderable in a browser.

The report must be suitable for direct PDF export using Chrome Print or Puppeteer.

Every section must be fully completed.

Never leave placeholders.

Never omit sections.
====================================================
`

                },

                {

                    role: "user",

                    content: `

Generate a complete professional wealth management report using the following cleaned portfolio dataset.

${JSON.stringify(finalData, null, 2)}

`

                }

            ]

        });
                const html = response.choices[0].message.content;

        if (!html) {

            throw new Error("OpenRouter returned an empty response.");

        }

        console.log("======================================");
        console.log("AI Report Generated Successfully");
        console.log("======================================");

        fs.writeFileSync(

            "report.html",

            html,

            "utf8"

        );

        console.log("======================================");
        console.log("REPORT SAVED SUCCESSFULLY");
        console.log("File : report.html");
        console.log("======================================");

    } catch (err) {

        console.log("======================================");
        console.log("REPORT GENERATION FAILED");
        console.log("======================================");

        if (err.response) {

            console.log("Status :", err.response.status);
            console.log(err.response.data);

        } else {

            console.log(err.message);

        }

    }

}

getReport();