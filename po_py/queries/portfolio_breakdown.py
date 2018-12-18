def china_mainland_shares_type_breakdown(indices, start_date, end_date=None):
    """Get index breakdown between China A- and B-shares.

    Positional arguments:
    :start_date str
    :end_date str
    :indices list

    Returns:
    :china_mainland_shares_type_breakdown str
    """
    if not end_date:
        end_date = start_date

    query = r"""IF OBJECT_ID('tempdb..#dataset') IS NOT NULL
    DROP TABLE  #dataset
    WITH cte AS(
        SELECT    a.weighting_date as date
                , a.entity_code, a.sedol
                , b.fs_perm_sec_id
                , b.proper_name, a.wgt
                , RIGHT(c.ticker_exchange, LEN(c.ticker_exchange)
                        -CHARINDEX('-', c.ticker_exchange)) AS exc_code
        FROM FundamentalsDB.dbo.tbl_weightings_history AS a
        LEFT JOIN FactSetDB.ids_v1.h_security_sedol AS b
        ON a.sedol=b.sedol
        LEFT JOIN FactSetDB.ids_v1.h_security_ticker_exchange AS c
        ON b.fs_perm_sec_id=c.fs_perm_sec_id
        WHERE a.entity_code IN ('""" + "','".join(indices) + """')
        AND a.weighting_date BETWEEN '""" +
    start_date + """' AND '""" + end_date +
    """)
    SELECT    a.*
            , b.fref_exchange_desc
            , b.fref_exchange_location_code
            , CASE WHEN RIGHT(proper_name, 7) = 'Class A'
              AND b.fref_exchange_location_code = 'CN' THEN 'A-Share'
              WHEN RIGHT(proper_name, 7) = 'Class B'
              AND b.fref_exchange_location_code = 'CN'THEN 'B-Share'
              WHEN b.fref_exchange_location_code IS NULL THEN
                                            'Missing Exchange'
              ELSE 'Missing Class' END AS share_type
    INTO  #dataset
    FROM cte AS a
    LEFT JOIN FactSetDB.ref_v2.fref_sec_exchange_map AS b
    ON a.exc_code = b.fref_exchange_code
    WHERE   b.fref_exchange_location_code = 'CN'
            OR b.fref_exchange_location_code IS NULL
    ORDER BY entity_code, b.fref_exchange_location_code, exc_code, wgt
    SELECT	  date
            , entity_code
            , SUM([A-Share]) AS[A-Shares]
            , SUM([B-Share]) AS[B-Shares]
            , SUM([Missing Exchange]) AS[Missing Exchange]
            , SUM([Missing Class]) AS[Missing Class]
    FROM
    (
        SELECT * FROM  # dataset
    ) AS a
    PIVOT
    (
        SUM(wgt)
        FOR share_type IN([A-Share], [B-Share]
                        , [Missing Exchange], [Missing Class])
    ) AS pvt
    GROUP BY entity_code, date"""

    return query
