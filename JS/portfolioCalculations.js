function calculatePortfolioAnalytics(data) {

    const portfolio = data.portfolio;
    const schemes = data.schemePerformance;

    const investment = portfolio[0].total_investment;
    const currentValue = portfolio[0].current_value;
    const gainPercent = portfolio[0].gain_percent * 100;
    const activeSchemes = portfolio[0].active_scheme_count;

    // ==========================
    // Portfolio Health Score
    // ==========================

    let health = 100;

    if (gainPercent < 0)
        health -= 30;
    else if (gainPercent < 2)
        health -= 15;

    if (activeSchemes < 5)
        health -= 15;

    health = Math.max(0, Math.min(100, Math.round(health)));

    // ==========================
    // Diversification Score
    // ==========================

    const categories = [...new Set(schemes.map(s => s.category_name))];
    const amcs = [...new Set(schemes.map(s => s.amc_name))];

    let diversification = 40;

    diversification += categories.length * 10;
    diversification += amcs.length * 5;

    diversification = Math.min(100, diversification);

    // ==========================
    // Risk Score
    // ==========================

    let risk = 20;

    if (gainPercent < 0)
        risk += 25;

    if (categories.length <= 2)
        risk += 20;

    if (activeSchemes <= 4)
        risk += 20;

    risk = Math.min(100, risk);

    let riskLevel = "Low";

    if (risk >= 70)
        riskLevel = "High";

    else if (risk >= 40)
        riskLevel = "Moderate";

    // ==========================
    // Top Scheme
    // ==========================

    const topScheme = [...schemes].sort(

        (a, b) => b.average_return - a.average_return

    )[0];

    // ==========================
    // Worst Scheme
    // ==========================

    const worstScheme = [...schemes].sort(

        (a, b) => a.average_return - b.average_return

    )[0];

    return {

        portfolioHealthScore: health,

        diversificationScore: diversification,

        riskScore: risk,

        riskLevel,

        totalInvestment: investment,

        currentValue,

        topScheme,

        worstScheme

    };

}

module.exports = {

    calculatePortfolioAnalytics

};