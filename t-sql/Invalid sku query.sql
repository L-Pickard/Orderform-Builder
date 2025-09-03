SELECT pl.[Preorder Code]
    ,pl.[Region]
    ,pl.[Brand Code]
    ,br.[Brand Name]
    ,pl.[Type]
    ,pl.[Season]
    ,pl.[Item No]
    ,CASE 
        WHEN pl.[Item No] IS NULL
            THEN 'Missing SKU Code'
        ELSE 'Invalid SKU Code'
        END AS [SKU Error]
    ,pl.[Item Description]
    ,pl.[Currency]
    ,pl.[WHS]
    ,pl.[SRP]
FROM [dPreorder Lines] AS pl
LEFT JOIN [dBrand] AS br
    ON pl.[Brand Code] = br.[Brand Code]
WHERE br.[Brand Name] = '{brand}'
    AND pl.[Season] = '{season}'
    AND pl.[Currency] = '{currency}'
    AND (
        pl.[Item No] IS NULL
        OR pl.[Item No] NOT IN (
            SELECT [Item No]
            FROM [dItem]
            )
        );