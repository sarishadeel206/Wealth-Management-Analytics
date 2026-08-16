const express = require("express");

const app = express();

const clientPortfolio = require("./clientPortfolio");
const schemePerformance = require("./schemePerformance");
const advisorPerformance = require("./advisorPerformance");
const sipAnalytics = require("./sipAnalytics");
const revenueMart = require("./revenue");
const redemptionAnalytics = require("./redemptionAnalytics");
const amc = require("./amc");
const executiveDashboard = require("./executiveDashboard");

app.use("/client-portfolio", clientPortfolio);
app.use("/scheme-performance", schemePerformance);
app.use("/advisor-performance", advisorPerformance);
app.use("/sip-analytics", sipAnalytics);
app.use("/revenue-mart", revenueMart);
app.use("/redemption-analytics", redemptionAnalytics);
app.use("/amc", amc);
app.use("/executive-dashboard", executiveDashboard);

const PORT = 3000;

app.listen(PORT, () => {
    console.log(`Server Running On Port ${PORT}`);
});