SELECT DISTINCT br.[Brand Name]
FROM [dPreorder Lines] AS pl
LEFT JOIN dBrand AS br
    ON pl.[Brand Code] = br.[Brand Code]
WHERE pl.[Item No] IN (
        SELECT [Item No]
        FROM [dItem]
        )
ORDER BY br.[Brand Name] ASC;