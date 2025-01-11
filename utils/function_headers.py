descriptive_statistics = [
    "Which land type (LC0_Desc) has the highest 'pH_H2O'.", 
    "Plot the average ‘OC’ for each land type (LC0_Desc). save it as a png.", 
    "Calculate the average pH for south EU.", 
    "Calculate the average pH for Austria, from the mentioned csv.", 
    "Calculate the max value of 'N' for Slovenia, from the mentioned csv.", 
    "Calculate the summary statistics for all numerical columns in the dataset.",
    "Generate a correlation matrix of these columns: EC, pH_CaCl2, pH_H2O, OC, CaCO3, P, N, K and visualize it using a heatmap.",
    "Plot the distribution of 'K' with a KDE overlay. save it as a png.",
    "Calculate the average 'K' for rows where 'EC' is greater than 10.",
    "Find the sum of 'K' for each unique value in the 'LC0_Desc' column. print the result."
] 

inferential_statistics  = [
    "Is there a significant relationship between land type (LC0_Desc) and pH_H2O? Use chi square from scipy.",
    "Is there a significant difference between 'N' in Austria and France? Use ANOVA from scipy.",
    "Which parameter has the strongest correlation with EC among {pH_CaCl2, pH_H2O, OC, CaCO3, P, N, K}?",
    "Perform a t-test to compare 'K' between Grassland and Cropland.",
    "Plot a linear regression analysis to see the relationship between 'pH_H2O' and 'K'.",
    "Construct a 95% confidence interval for the mean 'OC' content in the dataset.",
    "Using the Central Limit Theorem, simulate the sampling distribution of the mean 'pH_H2O' for sample sizes of 30. Plot the distribution and compare it to the normal distribution.",
    "Calculate the z-scores for 'EC' and identify any outliers (z-score > 3 or < -3).",
    "Perform a hypothesis test to determine if the mean 'K' content in the entire dataset is significantly different from 2%. Use a t-test for the hypothesis test.",
    "Calculate the p-value for the correlation between 'P' and 'K'. Determine if the correlation is statistically significant."
]

geo_information = [
    "Plot all the points that have pH_CaCl2 > 6. use geopandas. save the image as a png.",
    "Plot all the points with LC0_Desc=Woodland in Europe. Save the result as a png. Use geopandas.",
    "Plot all the points with LC0_Desc=Woodland & pH<6 in Europe. Save the result as a png. Use geopandas.",
    "Perform KMeans clustering on the TH_LAT and TH_LONG data to identify 3 clusters and plot them on a map. save it as a png.",
    "Create a map with markers for all locations where 'K' is above its median value, in Europe. use geopandas. save the result as a png.",
    "Generate a heatmap where each point is weighted by 'pH_CaCl2', in Europe. Don't merge these shapefiles just plot them. use geopandas. save the result as a png.",
    "Create a map with markers for points where 'K' is in the top 10 percentile, in Europe. Don't merge these shapefiles just plot them. use geopandas. save the result as a png.",
    "Plot clusters of points with 'pH_H2O'>5 and 'pH_H2O'<5 in Europe.",
    "Create a map displaying the distribution of soil types ('LC0_Desc') across Europe. Each soil type should be represented by a different color. Use geopandas and save the map as a png.",
    "Plot all the LC0_Desc='Grassland' and LC0_Desc='Woodland' points where 'OC'>20. Use geopandas and save the map as a png."
] 