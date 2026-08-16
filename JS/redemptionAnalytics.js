const express = require("express");
const { DBSQLClient } = require("@databricks/sql");

const router = express.Router();

console.log("REDEMPTION ANALYTICS FILE LOADED");

router.get("/", async (req, res) => {

    console.log("REDEMPTION ANALYTICS API HIT");

    const client = new DBSQLClient();

    try {

        await client.connect({
             host: "dbc-50098adb-0fbe.cloud.databricks.com",
             path: "/sql/1.0/warehouses/6a045ed63528215e",
             token: "ENTER YOUR TOKEN PATH"
        });

        console.log("DATABRICKS CONNECTED");

        const session = await client.openSession();

        const operation = await session.executeStatement(`
            SELECT *
            FROM wealth_catalog.mart.redemption_analytics_mart
            LIMIT 10
        `);

        const result = await operation.fetchAll();

        await operation.close();
        await session.close();

        res.json(result);

    } catch (err) {

        console.log(err);

        res.status(500).json({
            success: false,
            error: err.message
        });

    }

});

module.exports = router;