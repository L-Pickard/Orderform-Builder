SELECT DISTINCT ic.[Description] AS [Category]
FROM [dPreorder Lines] AS pl
LEFT JOIN [dItem] AS it
    ON pl.[Item No] = it.[Item No]
LEFT JOIN [NAV_LIVE].[dbo].[Shiner$Item Category] AS ic
    ON it.[Category Code] = ic.[Code]
LEFT JOIN [dBrand] AS br
    ON pl.[Brand Code] = br.[Brand Code]
WHERE ic.[Description] IS NOT NULL
    AND br.[Brand Name] = '{brand}'
    AND pl.[Season] = '{season}'
    AND pl.[Currency] = '{currency}'
ORDER BY ic.[Description] ASC;