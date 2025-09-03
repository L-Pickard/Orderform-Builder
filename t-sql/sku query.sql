DECLARE @Brand NVARCHAR(30)
	,@Season NVARCHAR(10)
	,@Currency NVARCHAR(5)

SET @Brand = '{brand}'
SET @Season = '{season}'
SET @Currency = '{currency}';

WITH [Size Cat]
AS (
	SELECT DISTINCT it.[Common Item No]
		,sc.[Size Cat]
	FROM [dPreorder Lines] AS pl
	LEFT JOIN [dBrand] AS br
		ON pl.[Brand Code] = br.[Brand Code]
	LEFT JOIN [dItem] AS it
		ON pl.[Item No] = it.[Item No]
	LEFT JOIN (
		SELECT im.[Item No]
			,CASE 
				WHEN TRIM(im.[Size 1]) IN ('O/S', 'OS', 'OSFA', '4-7', '8-11', ''
						)
					THEN 'Accessory'
				WHEN TRIM(im.[Size 1]) IN (
						'25/28', '25/30', '26/30', '26/32', '27/30', '27/32', '28/30', 
						'28/32', '29/30', '29/32', '30/32', '31/32', '32/32', '33/32', 
						'34/32', '34/34', '36/32', '36/34'
						)
					THEN 'Pants'
				WHEN TRIM(im.[Size 1]) IN ('4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26'
						)
					AND im.[Category Code] = 'APWM'
					THEN 'Women'
				WHEN TRIM(im.[Size 1]) IN ('XXXS', 'XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXXL'
						)
					THEN 'Adult'
				WHEN TRIM(im.[Size 1]) IN ('4-6', '6-8', '8-10', '10-12', '12-14', '14-16'
						)
					AND im.[Size 1 Unit] = 'YOUTH'
					THEN 'Youth'
				WHEN TRIM(im.[Size 1]) IN ('26', '28', '30', '32', '34', '36', '38', '40'
						)
					AND im.[Category Code] IN ('APRL', 'APYT', 'APRL'
						)
					THEN 'Waist'
				WHEN TRIM(im.[Size 1]) IN ('XXS/XS', 'XS/S', 'S/M', 'M/L', 'L/XL', 'XL/XXL', 'XXL/XXXL'
						)
					THEN 'Adult /'
				WHEN im.[Size 1 Unit] IN ('CHILD', 'YOUTH')
					AND im.[Group Code] = 'FOOT'
					THEN 'Yth Footwear'
				WHEN im.[Size 1 Unit] NOT IN ('CHILD', 'YOUTH'
						)
					AND im.[Group Code] = 'FOOT'
					THEN 'Footwear'
				WHEN im.[Size 1 Unit] IN ('CHILD', 'YOUTH')
					AND im.[Group Code] IN (
						'G1WH', 'B1WH', 'B2WH', 'H2WH', 'HASH', 'G2WH', 'B1W', 'B2W', 
						'G1W', 'G2W', 'H1WH'
						)
					AND im.[Brand Code] = 'HLY'
					THEN 'Yth Heelys'
				WHEN im.[Size 1 Unit] NOT IN ('CHILD', 'YOUTH'
						)
					AND im.[Group Code] IN (
						'G1WH', 'B1WH', 'B2WH', 'H2WH', 'HASH', 'G2WH', 'B1W', 'B2W', 
						'G1W', 'G2W', 'H1WH'
						)
					AND im.[Brand Code] = 'HLY'
					THEN 'Heelys'
				WHEN im.[Size 1 Unit] IN ('CHILD', 'YOUTH')
					AND im.[Category Code] = 'QUHG'
					AND im.[Group Code] = 'SKATES'
					THEN 'Yth Rollerskates'
				WHEN im.[Size 1 Unit] NOT IN ('CHILD', 'YOUTH'
						)
					AND im.[Category Code] = 'QUHG'
					AND im.[Group Code] = 'SKATES'
					THEN 'Rollerskates'
				WHEN im.[Size 1 Unit] IN ('CHILD', 'YOUTH')
					AND im.[Group Code] IN ('B2W', 'B2WH', 'B1W', 'G2W', 'G1W', 'G2WH'
						)
					AND im.[Brand Code] = 'SWS'
					THEN 'Yth SWS'
				WHEN im.[Size 1 Unit] NOT IN ('CHILD', 'YOUTH'
						)
					AND im.[Group Code] IN ('B2W', 'B2WH', 'B1W', 'G2W', 'G1W', 'G2WH'
						)
					AND im.[Brand Code] = 'SWS'
					THEN 'SWS'
				WHEN im.[Size 1 Unit] IN ('CHILD', 'YOUTH')
					AND im.[Group Code] = 'POP'
					THEN 'Yth POP'
				WHEN im.[Size 1 Unit] NOT IN ('CHILD', 'YOUTH'
						)
					AND im.[Group Code] = 'POP'
					THEN 'POP'
				WHEN im.[Size 1 Unit] = ''
					THEN 'Misc'
				WHEN im.[Size 1 Unit] = 'ADULT'
					THEN 'Adult Misc'
				WHEN im.[Size 1 Unit] = 'YOUTH'
					THEN 'Youth Misc'
				WHEN im.[Size 1 Unit] = 'WOMEN'
					THEN 'Women Misc'
				ELSE im.[Size 1 Unit]
				END AS [Size Cat]
		FROM [dItem] AS im
		LEFT JOIN [dBrand] AS br
			ON im.[Brand Code] = br.[Brand Code]
		WHERE br.[Brand Name] = @Brand
			AND im.[Category] IN ({category})
		) AS sc
		ON it.[Common Item No] = sc.[Item No]
	WHERE br.[Brand Name] = @Brand
		AND pl.[Season] = @Season
		AND it.[Category] IN ({category})
		AND pl.[Currency] = @Currency
	)
SELECT pl.[Preorder Code]
	,it.[Common Item No] AS [Style No]
	,(
		SELECT TOP 1 [Size Cat]
		FROM [Size Cat]
		WHERE [Common Item No] = it.[Common Item No]
		) AS [Size Cat]
	,it.[Description]
	,it.[Description 2]
	,it.[Colours]
	,CASE 
		WHEN TRIM(it.[Size 1]) = ''
			THEN 'O/S'
		ELSE TRIM(it.[Size 1])
		END AS [Size 1]
	,CASE 
		WHEN TRIM(it.[EU Size]) <> ''
			THEN TRIM(it.[EU Size])
		ELSE (
				CASE 
					WHEN TRIM(it.[Size 1]) = ''
						THEN 'O/S'
					ELSE TRIM(it.[Size 1])
					END
				)
		END AS [EU Size]
	,CASE 
		WHEN TRIM(it.[US Size]) <> ''
			THEN TRIM(it.[US Size])
		ELSE (
				CASE 
					WHEN TRIM(it.[Size 1]) = ''
						THEN 'O/S'
					ELSE TRIM(it.[Size 1])
					END
				)
		END AS [US Size]
	,pl.[WHS]
	,pl.[SRP]
	,pl.[Item No]
FROM [dPreorder Lines] AS pl
LEFT JOIN [dBrand] AS br
	ON pl.[Brand Code] = br.[Brand Code]
LEFT JOIN [dItem] AS it
	ON pl.[Item No] = it.[Item No]
WHERE br.[Brand Name] = @Brand
	AND pl.[Season] = @Season
	AND it.[Category] IN ({category})
	AND pl.[Currency] = @Currency
OPTION (RECOMPILE);
