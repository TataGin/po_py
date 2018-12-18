"""Queries for fundamentala data."""


def constituents_fundamentals(indices, start_date, end_date=None):
    """Get stocks fundamentals, sector and country.

    Positional arguments:
    :start_date str
    :end_date str
    :indices list

    Returns:
    :constituents_fundamentals str
    """
    if not end_date:
        end_date = start_date

    query = r"""SELECT a.weighting_date
, a.entity_code
, a.sedol
, a.wgt
, b.gics_code
, LEFT(b.gics_code, 2) AS sector_code
, f.GicsName
, e.country_desc
, c.country_code
, d.[ReportFreq]
, d.[PricingCurrency]
, d.[Fx_price]
, d.[EstimateCurrency]
, d.[Fx_estimate]
, d.[ReportCurrency]
, d.[Fx_report]
, d.[PriceLast]
, d.[MarketCap]
, d.[ShareMarketCapUSD]
, d.[VolumeLast]
, d.[SharesOut]
, d.[DivYld]
, d.[EstDivYld]
, d.[EarnYld]
, d.[GaapEarnYld]
, d.[EstEarnYld]
, d.[OperEarnYld]
, d.[EbitBefUnusYld]
, d.[EbitOperYld]
, d.[EstLongTermGrowth]
, d.[EstLongTermGrowthAnalysts]
, d.[SalesYld]
, d.[FreeCashFlowYld]
, d.[OperCashFlowYld]
, d.[BookValueYld]
, d.[TangBookValueYld]
, d.[Sales_ttm]
, d.[OperIncome_ttm]
, d.[EbitBefUnus_ttm]
, d.[EbitOper_ttm]
, d.[GaapNetIncome_ttm]
, d.[NetIncBefXord_ttm]
, d.[NetIncome_ttm]
, d.[Assets_avg_ttm]
, d.[Assets_last]
, d.[CommonEquity_avg_ttm]
, d.[CommonEquity_last]
, d.[ShareholderEquity_avg_ttm]
, d.[ShareholderEquity_last]
, d.[BookPerShr_avg_ttm]
, d.[BookPerShr_last]
, d.[TangBookPerShr_avg_ttm]
, d.[TangBookPerShr_last]
, d.[Dividends_ttm]
, d.[StockPurchase_ttm]
, d.[StockSale_ttm]
, d.[NetBuyBackYld]
, d.[GrossBuyBackYld]
, d.[Cash_last]
, d.[CashEquiv_last]
, d.[InterestExpGross_ttm]
, d.[InterestExpNet_ttm]
, d.[DebtLT_avg_ttm]
, d.[DebtLT_last]
, d.[DebtST_avg_ttm]
, d.[DebtST_last]
, d.[Ebitda_ttm]
, d.[CostGoodsSold_ttm]
, d.[EnterpriseValue_last]
FROM FundamentalsDB.dbo.tbl_weightings_history AS a
LEFT JOIN FundamentalsDB.dbo.map_master_gics AS b
ON a.sedol = b.sedol
LEFT JOIN FundamentalsDB.dbo.ConstituentCountry AS c
ON a.sedol = c.sedol
LEFT JOIN FundamentalsDB.dbo.ConstituentFundamentals_archive AS d
ON a.sedol = d.sedol AND a.weighting_date = d.rundate
LEFT JOIN FactSetDB.ref_v2.country_map AS e
ON c.country_code = e.iso_country
LEFT JOIN FundamentalsDB.dbo.map_gics_code AS f
ON LEFT(b.gics_code, 2) = f.GicsNum
WHERE c.iteration = 1
AND d.iteration = 1
AND a.entity_code IN ('""" + "','".join(indices) + """')
AND a.weighting_date BETWEEN '""" + start_date + "' AND '" + end_date + "'"

    return query
