WITH Season_Data
AS (
    SELECT DISTINCT pl.[Season] AS [Season Code]
        ,LEFT(pl.[Season], 2) AS [Season]
        ,TRY_CONVERT(INTEGER, RIGHT([Season], 2)) AS [Year]
        ,CASE 
            WHEN LEFT(pl.[Season], 2) = 'SP'
                THEN 1
            WHEN LEFT(pl.[Season], 2) = 'SU'
                THEN 2
            WHEN LEFT(pl.[Season], 2) = 'SS'
                THEN 3
            WHEN LEFT(pl.[Season], 2) = 'FA'
                THEN 4
            WHEN LEFT(pl.[Season], 2) = 'HO'
                THEN 5
            ELSE 10
            END AS [Order]
    FROM [dPreorder Lines] AS pl
    LEFT JOIN [dBrand] AS br
        ON pl.[Brand Code] = br.[Brand Code]
    WHERE br.[Brand Name] = '{brand}'
        AND pl.[Item No] IN (
            SELECT [Item No]
            FROM [dItem]
            )
    )
SELECT [Season Code]
FROM Season_Data
ORDER BY TRY_CONVERT(INTEGER, RIGHT([Season], 2)) ASC
    ,CASE 
        WHEN LEFT([Season Code], 2) = 'SP'
            THEN 1
        WHEN LEFT([Season Code], 2) = 'SU'
            THEN 2
        WHEN LEFT([Season Code], 2) = 'FA'
            THEN 3
        WHEN LEFT([Season Code], 2) = 'HO'
            THEN 4
        ELSE 10
        END ASC;