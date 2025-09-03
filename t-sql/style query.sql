DECLARE @Brand NVARCHAR(30)
    ,@Season NVARCHAR(10)
    ,@Currency NVARCHAR(5)

SET @Brand = '{brand}'
SET @Season = '{season}'
SET @Currency = '{currency}';

WITH [Styles]
AS (
    SELECT it.[Common Item No] AS [Style No]
        ,pl.[Item No]
        ,pl.[Row No]
        ,pl.[Season]
        ,pl.[WHS]
        ,pl.[SRP]
        ,pl.[Preorder Code]
    FROM [dPreorder Lines] AS pl
    LEFT JOIN [dBrand] AS br
        ON pl.[Brand Code] = br.[Brand Code]
    LEFT JOIN [dItem] AS it
        ON pl.[Item No] = it.[Item No]
    WHERE br.[Brand Name] = @Brand
        AND pl.[Season] = @Season
        AND it.[Category] IN ({category})
        AND pl.[Currency] = @Currency
    )
SELECT DISTINCT st.[Style No]
    ,CASE 
        WHEN LEFT(st.[Item No], 3) IN ('SCA', 'INA', 'ABA')
            AND it.[Season] = st.[Season]
            AND (
                SELECT COUNT(*)
                FROM [dItem]
                WHERE [Vendor Reference] = it.[Vendor Reference]
                    AND [Colours] <> it.[Colours]
                    AND [Season] <> it.[Season]
                ) = 0
            THEN 'New'
        WHEN LEFT(st.[Item No], 3) IN ('SCA', 'INA', 'ABA')
            AND it.[Season] = st.[Season]
            AND (
                SELECT COUNT(*)
                FROM [dItem]
                WHERE [Vendor Reference] = it.[Vendor Reference]
                    AND [Colours] <> it.[Colours]
                    AND [Season] <> it.[Season]
                ) > 0
            THEN 'C/O NC'
        WHEN LEFT(st.[Item No], 3) NOT IN ('SCA', 'INA', 'ABA')
            AND it.[Season] = st.[Season]
            THEN 'New'
        ELSE 'C/O'
        END AS 'New'
    ,CASE 
        WHEN PATINDEX('%-D[0-9]%', st.[Preorder Code]) > 0
            THEN UPPER(RIGHT(st.[Preorder Code], CHARINDEX('-', REVERSE(st.[Preorder Code])) - 1))
        ELSE 'D1'
        END AS [Drop]
    ,CASE 
        WHEN TRIM(it.[Size 1]) IN ('O/S', 'OS', 'OSFA', '4-7', '8-11', '')
            THEN 'Accessory'
        WHEN TRIM(it.[Size 1]) IN (
                '25/28', '25/30', '26/30', '26/32', '27/30', '27/32', '28/30', '28/32', '29/30', '29/32'
                , '30/32', '31/32', '32/32', '33/32', '34/32', '34/34', '36/32', '36/34'
                )
            THEN 'Pants'
        WHEN TRIM(it.[Size 1]) IN ('4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26'
                )
            AND it.[Category Code] = 'APWM'
            THEN 'Women'
        WHEN TRIM(it.[Size 1]) IN ('XXXS', 'XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXXL'
                )
            THEN 'Adult'
        WHEN TRIM(it.[Size 1]) IN ('4-6', '6-8', '8-10', '10-12', '12-14', '14-16')
            AND it.[Size 1 Unit] = 'YOUTH'
            THEN 'Youth'
        WHEN TRIM(it.[Size 1]) IN ('26', '28', '30', '32', '34', '36', '38', '40')
            AND it.[Category Code] IN ('APRL', 'APYT', 'APRL')
            THEN 'Waist'
        WHEN TRIM(it.[Size 1]) IN ('XXS/XS', 'XS/S', 'S/M', 'M/L', 'L/XL', 'XL/XXL', 'XXL/XXXL'
                )
            THEN 'Adult /'
        WHEN it.[Size 1 Unit] IN ('CHILD', 'YOUTH')
            AND it.[Group Code] = 'FOOT'
            THEN 'Yth Footwear'
        WHEN it.[Size 1 Unit] NOT IN ('CHILD', 'YOUTH')
            AND it.[Group Code] = 'FOOT'
            THEN 'Footwear'
        WHEN it.[Size 1 Unit] IN ('CHILD', 'YOUTH')
            AND it.[Group Code] IN ('G1WH', 'B1WH', 'B2WH', 'H2WH', 'HASH', 'G2WH', 'B1W', 'B2W', 'G1W', 'G2W', 'H1WH')
            AND it.[Brand Code] = 'HLY'
            THEN 'Yth Heelys'
        WHEN it.[Size 1 Unit] NOT IN ('CHILD', 'YOUTH')
            AND it.[Group Code] IN ('G1WH', 'B1WH', 'B2WH', 'H2WH', 'HASH', 'G2WH', 'B1W', 'B2W', 'G1W', 'G2W', 'H1WH')
            AND it.[Brand Code] = 'HLY'
            THEN 'Heelys'
        WHEN it.[Size 1 Unit] IN ('CHILD', 'YOUTH')
            AND it.[Category Code] = 'QUHG'
            AND it.[Group Code] = 'SKATES'
            THEN 'Yth Rollerskates'
        WHEN it.[Size 1 Unit] NOT IN ('CHILD', 'YOUTH')
            AND it.[Category Code] = 'QUHG'
            AND it.[Group Code] = 'SKATES'
            THEN 'Rollerskates'
        WHEN it.[Size 1 Unit] IN ('CHILD', 'YOUTH')
            AND it.[Group Code] IN ('B2W', 'B2WH', 'B1W', 'G2W', 'G1W', 'G2WH')
            AND it.[Brand Code] = 'SWS'
            THEN 'Yth SWS'
        WHEN it.[Size 1 Unit] NOT IN ('CHILD', 'YOUTH')
            AND it.[Group Code] IN ('B2W', 'B2WH', 'B1W', 'G2W', 'G1W', 'G2WH')
            AND it.[Brand Code] = 'SWS'
            THEN 'SWS'
        WHEN it.[Size 1 Unit] IN ('CHILD', 'YOUTH')
            AND it.[Group Code] = 'POP'
            THEN 'Yth POP'
        WHEN it.[Size 1 Unit] NOT IN ('CHILD', 'YOUTH')
            AND it.[Group Code] = 'POP'
            THEN 'POP'
        WHEN it.[Size 1 Unit] = ''
            THEN 'Misc'
        WHEN it.[Size 1 Unit] = 'ADULT'
            THEN 'Adult Misc'
        WHEN it.[Size 1 Unit] = 'YOUTH'
            THEN 'Youth Misc'
        WHEN it.[Size 1 Unit] = 'WOMEN'
            THEN 'Women Misc'
        ELSE it.[Size 1 Unit]
        END AS [Size Cat]
    ,it.[Description]
    ,it.[Description 2]
    ,it.[Colours]
    ,(
        SELECT TOP 1 [WHS]
        FROM [Styles]
        WHERE [Style No] = st.[Style No]
        ) AS [WHS]
    ,(
        SELECT TOP 1 [SRP]
        FROM [Styles]
        WHERE [Style No] = st.[Style No]
        ) AS [SRP]
    ,(
        SELECT TOP 1 [Row No]
        FROM [Styles]
        WHERE [Style No] = st.[Style No]
        ) AS [Row No]
FROM [Styles] AS st
LEFT JOIN [dItem] AS it
    ON st.[Style No] = it.[Item No]
ORDER BY [Row No];