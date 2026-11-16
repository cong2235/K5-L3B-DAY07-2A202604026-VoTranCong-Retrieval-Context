# Review sheet dev / kaggle-qwen2.5-7b-awq-k5

Grade each: grounded answer 0-2, each citation supports (T/F), abstention correct (T/F), context 0-2.

## D01 (answerable) - answered
**Q:** What is MCAR missing data?

**Expected:** Data that is missing completely at random: it is not related to any other variables and has no underlying cause for its absence.

**Answer:** MCAR (missing completely at random) data is missing data not related to any other variables, with no underlying cause for its absence. [B:openstax-pds:p87:1]

**Queries:** ['MCAR missing data definition']
**Citations:** ['B:openstax-pds:p87:1']

## D02 (answerable) - answered
**Q:** Why did the 1936 Literary Digest poll predict the wrong presidential winner?

**Expected:** Its mailing list of telephone and automobile owners was biased toward affluent individuals, who favored the Republican candidate.

**Answer:** The 1936 Literary Digest poll predicted a victory for Republican nominee Alf Landon, but the actual outcome was a landslide win for Franklin D. Roosevelt. This discrepancy was due to the biased sampling method, which favored affluent individuals and therefore Republican voters [B:openstax-pds:p72:1]. The poll used primarily closed-ended questions, which may not have accurately captured the opinions of all voters [B:openstax-pds:p72:2].

**Queries:** ['1936 Literary Digest poll error']
**Citations:** ['B:openstax-pds:p72:1', 'B:openstax-pds:p72:2']

## D03 (answerable) - answered
**Q:** How does stratified sampling work?

**Expected:** The population is split into subgroups (strata) and a random sample is taken from each stratum in proportion to its size.

**Answer:** Stratified sampling involves dividing the population into subgroups or strata based on certain characteristics and then randomly selecting participants from each subgroup. This ensures that each subgroup is represented in the sample, providing a more accurate representation of the entire population. [B:openstax-pds:p76:2]

**Queries:** ['stratified sampling']
**Citations:** ['B:openstax-pds:p76:2']

## D04 (answerable) - answered
**Q:** How is a cluster sample selected?

**Expected:** The population is divided into natural groups (clusters); a random sample of clusters is picked and all members of the chosen clusters are included.

**Answer:** A cluster sample is selected by first dividing the population into natural groups or clusters, such as schools, communities, or cities. Then, a random sample of these clusters is chosen, and all members within the selected clusters are included in the sample. This method allows the researcher to obtain a representative sample of the entire population while saving time and resources compared to visiting each individual unit in the population. [B:openstax-pds:p73:2] [B:openstax-pds:p73:1]

**Queries:** ['cluster sample selection']
**Citations:** ['B:openstax-pds:p73:2', 'B:openstax-pds:p73:1']

## D05 (answerable) - answered
**Q:** Under what condition is a log transformation of the data appropriate?

**Expected:** When the data is highly skewed, with most data points toward one end of the distribution.

**Answer:** A log transformation of the data is appropriate when the data is highly skewed, meaning most of the data points fall toward one end of the distribution [B:openstax-pds:p92:3]. This can cause problems in data analysis as the data may not follow a normal distribution. By taking the logarithm of the values, the distribution can be shifted toward a more symmetrical shape, making it easier to analyze.

**Queries:** ['log transformation condition']
**Citations:** ['B:openstax-pds:p92:3']

## D06 (answerable) - answered
**Q:** Which pandas function reads HTML tables from a web page?

**Expected:** read_html(), which converts HTML tables into a list of DataFrame objects.

**Answer:** The pandas function that reads HTML tables from a web page is `pd.read_html()` [B:openstax-pds:p78:2, B:openstax-pds:p79:1].

**Queries:** ['pandas read html table']
**Citations:** ['B:openstax-pds:p78:2', 'B:openstax-pds:p79:1']

## D07 (answerable) - answered
**Q:** If some of a large dataset becomes corrupted, how does splitting it into blocks help?

**Expected:** Only the affected chunk has to be retrieved rather than the entire dataset (fault tolerance).

**Answer:** Splitting a large dataset into blocks (chunks) helps in handling data corruption by allowing the retrieval and correction of only the affected chunk rather than the entire dataset. This increases fault tolerance and reduces the impact of corruption on the overall dataset [B:openstax-pds:p100:3].

**Queries:** ['corrupted dataset blocks help']
**Citations:** ['B:openstax-pds:p100:3']

## D08 (answerable) - answered
**Q:** What problem does the trimmed mean address?

**Expected:** It mitigates the effect of outliers, which are values significantly different from most others.

**Answer:** The trimmed mean addresses the issue where the mean can be skewed by the presence of outliers, or data values that are significantly different from the rest of the dataset [B:openstax-pds:p114:6]. By removing a certain percentage of the smallest and largest values, the trimmed mean provides a more representative measure of the center of the dataset [B:openstax-pds:p116:1].

**Queries:** ['trimmed mean problem']
**Citations:** ['B:openstax-pds:p114:6', 'B:openstax-pds:p116:1']

## D09 (answerable) - answered
**Q:** Why is the range considered a weak measure of spread?

**Expected:** It uses only the minimum and maximum values and is influenced by outliers.

**Answer:** The range is considered a weak measure of spread because it only uses the minimum and maximum values of the dataset, ignoring all other data points. Additionally, it can be significantly affected by outliers, which can skew the results. [B:openstax-pds:p121:2]

**Queries:** ['range weak measure of spread']
**Citations:** ['B:openstax-pds:p121:2']

## D10 (answerable) - answered
**Q:** What does the variance measure?

**Expected:** The spread of data values, using the squared deviations from the mean.

**Answer:** Variance measures the average of the squared differences from the Mean. [B:openstax-pds:p95:1]

**Queries:** []
**Citations:** ['B:openstax-pds:p95:1']

## D11 (answerable) - abstain
**Q:** Which percentile does the first quartile correspond to?

**Expected:** The 25th percentile.

**Answer:** INSUFFICIENT_EVIDENCE: The passages do not provide information on the exact percentile corresponding to the first quartile.

**Queries:** []
**Citations:** []

## D12 (answerable) - answered
**Q:** How can quartiles be used to flag possible outliers?

**Expected:** Use the quartiles and the IQR to compute a lower and an upper bound; values outside the bounds are flagged.

**Answer:** Quartiles can be used to flag possible outliers by defining a range around the interquartile range (IQR). Specifically, any data point that falls below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR is considered a potential outlier. This method leverages the IQR to identify values that lie far from the bulk of the data. [B:openstax-pds:p90:1]

**Queries:** []
**Citations:** ['B:openstax-pds:p90:1']

## D13 (answerable) - answered
**Q:** Which techniques can identify missing data points or apparent outliers?

**Expected:** Visualization (scatterplots, box plots, IQR, histograms) or statistical methods such as mean, median and standard deviation.

**Answer:** Techniques for identifying missing data points or apparent outliers include visualization methods such as scatterplots, box plots, IQR, and histograms [B:openstax-pds:p87:0], as well as statistical methods like calculating the mean, median, and standard deviation [B:openstax-pds:p87:0].

**Queries:** ['techniques for identifying missing data points or apparent outliers']
**Citations:** ['B:openstax-pds:p87:0']

## D14 (answerable) - answered
**Q:** What does the IQR indicate about a dataset?

**Expected:** The spread of the middle half (middle 50%) of the data.

**Answer:** The interquartile range (IQR) indicates the spread of the middle half, or the middle 50%, of the data [B:openstax-pds:p127:0]. It is the difference between the third quartile (\(Q_3\)) and the first quartile (\(Q_1\)) [B:openstax-pds:p127:0]. Additionally, the IQR can be used to flag possible outliers in a dataset [B:openstax-pds:p127:1].

**Queries:** ['IQR indicates about a dataset']
**Citations:** ['B:openstax-pds:p127:0', 'B:openstax-pds:p127:1']

## D15 (answerable) - answered
**Q:** Why do data scientists usually compute binomial probabilities with software?

**Expected:** The computations are complicated and time-consuming, so they use Python, R, Excel or similar.

**Answer:** Data scientists usually compute binomial probabilities with software because these computations can be complicated and time-consuming [B:openstax-pds:p141:1]. [B:openstax-pds:p147:0] provides an example using Python's `binom.pmf()` function to calculate binomial probabilities.

**Queries:** ['why data scientists compute binomial probabilities with software']
**Citations:** ['B:openstax-pds:p141:1', 'B:openstax-pds:p147:0']

## T01 (answerable) - answered
**Q:** What are APIs used for in web data collection?

**Expected:** They let developers access and retrieve data directly without web scraping, which is often more efficient and reliable.

**Answer:** APIs are used for accessing and retrieving data instantly without the need for web scraping, making them a more efficient and reliable method for data collection [B:openstax-pds:p77:1]. Specifically, APIs provided by social media platforms allow data scientists to collect structured data on user interactions and content [B:openstax-pds:p77:2].

**Queries:** ['APIs used for web data collection']
**Citations:** ['B:openstax-pds:p77:1', 'B:openstax-pds:p77:2']

## T02 (answerable) - answered
**Q:** How does a seven-day average help with noisy daily stock index values?

**Expected:** It smooths out day-to-day fluctuations so the overall trend over the month is visible (data smoothing).

**Answer:** A seven-day average helps with noisy daily stock index values by smoothing out the fluctuations that occur on a day-to-day basis. This makes it easier to identify the overall trend of the index over the course of a month [B:openstax-pds:p93:1].

**Queries:** ['seven-day average stock index noise']
**Citations:** ['B:openstax-pds:p93:1']

## T03 (answerable) - answered
**Q:** What is sample data?

**Expected:** Outcomes or measurements collected from a subset, or part, of the population of interest.

**Answer:** Sample data represents outcomes or measurements collected from a subset, or part, of the population of interest. This is necessary when it is impractical or impossible to collect data from an entire population [B:openstax-pds:p115:1].

**Queries:** ['sample data definition']
**Citations:** ['B:openstax-pds:p115:1']

## T04 (answerable) - abstain
**Q:** Which probability values are impossible?

**Expected:** A probability greater than 1 or a negative probability is not possible; probabilities lie between 0 and 1 inclusive.

**Answer:** INSUFFICIENT_EVIDENCE: The passages do not provide specific probability values or explain which values are impossible.

**Queries:** []
**Citations:** []

## T05 (answerable) - answered
**Q:** How do continuous random variables differ from discrete ones?

**Expected:** A continuous random variable can take any value within an interval (usually a measurement), whereas discrete variables take distinct countable values.

**Answer:** Continuous random variables can take on any value within a given range or interval, whereas discrete random variables take on a finite or countably infinite number of distinct values. For example, the number of text messages sent by a student during a day is a discrete random variable because it can only take on specific values like 26, 10, 17, etc. In contrast, the number of inches of rain in a month can be any value within a range, making it a continuous random variable. [B:openstax-pds:p138:1] [B:openstax-pds:p139:1]

**Queries:** ['continuous random variables vs discrete']
**Citations:** ['B:openstax-pds:p138:1', 'B:openstax-pds:p139:1']

## S01 (answerable) - answered
**Q:** In which situations is snowball sampling typically used?

**Expected:** When it is difficult to access a particular population; it relies on referrals between people with similar characteristics.

**Answer:** Snowball sampling is typically used in situations where it is difficult to access a particular population. It relies on the assumption that people with similar characteristics or experiences tend to associate with each other and can provide valuable referrals. This type of sampling can be useful in studying hard-to-reach or sensitive populations, but it may also be biased and limit the generalizability of findings. [B:openstax-pds:p74:2]

**Queries:** ['snowball sampling situations']
**Citations:** ['B:openstax-pds:p74:2']

## S02 (answerable) - abstain
**Q:** What must researchers be transparent about when they use purposive sampling?

**Expected:** Their sampling strategy and the potential biases from purposely selecting certain individuals.

**Answer:** INSUFFICIENT_EVIDENCE: The passages do not provide specific information about what researchers must be transparent about when using purposive sampling.

**Queries:** []
**Citations:** []

## S03 (answerable) - abstain
**Q:** Which external Python library is mainly used to scrape and parse HTML and XML?

**Expected:** Beautiful Soup.

**Answer:** INSUFFICIENT_EVIDENCE: The passages do not provide information about external Python libraries used for scraping and parsing HTML and XML.

**Queries:** []
**Citations:** []

## S04 (answerable) - abstain
**Q:** Should outliers be handled before or after validating the data?

**Expected:** Before: outliers should be identified and removed before validating the data.

**Answer:** INSUFFICIENT_EVIDENCE: The passages do not provide information on the order of handling outliers relative to data validation.

**Queries:** []
**Citations:** []

## S05 (answerable) - abstain
**Q:** What kind of database is designed for unstructured data such as sensor readings or social media posts?

**Expected:** NoSQL databases, which use non-relational data models.

**Answer:** INSUFFICIENT_EVIDENCE: The passages do not provide information on specific databases designed for unstructured data like sensor readings or social media posts.

**Queries:** []
**Citations:** []

## S06 (answerable) - answered
**Q:** How can the variability of datasets with different units or means be compared?

**Expected:** With the coefficient of variation: the standard deviation expressed as a percentage of the mean.

**Answer:** The variability of datasets with different units or means can be compared using the coefficient of variation (CV), which measures the variation of a dataset by calculating the standard deviation as a percentage of the mean [B:openstax-pds:p124:1]. This allows for a standardized way to compare the relative variability between datasets regardless of their units or means.

**Queries:** ['compare variability datasets different units means']
**Citations:** ['B:openstax-pds:p124:1']

## S07 (answerable) - abstain
**Q:** What is a conditional probability?

**Expected:** The probability of an event given that another event has already occurred.

**Answer:** INSUFFICIENT_EVIDENCE: The passages do not provide a definition or explanation of conditional probability.

**Queries:** []
**Citations:** []

## S08 (answerable) - answered
**Q:** How is the probability of getting at least one four in three rolls of a die calculated?

**Expected:** Find the probability of no four on any roll and subtract it from 1 (complement rule).

**Answer:** The probability of getting at least one four in three rolls of a die can be calculated by first finding the probability of not observing a four on any of the rolls and then subtracting this probability from 1. The probability of not observing a four on a single roll is \( \frac{5}{6} \). Therefore, the probability of not observing a four in three rolls is \( \left(\frac{5}{6}\right)^3 \). The probability of getting at least one four in three rolls is then \( 1 - \left(\frac{5}{6}\right)^3 \).

[ B:openstax-pds:p135:1 ]

**Queries:** ['probability at least one four three rolls die']
**Citations:** ['B:openstax-pds:p135:1']

## S09 (answerable) - answered
**Q:** What are the two parameters of the normal distribution?

**Expected:** The mean (center) and the standard deviation (spread).

**Answer:** The two parameters of the normal distribution are the mean, \(\mu\), and the standard deviation, \(\sigma\) [B:openstax-pds:p144:1].

**Queries:** ['parameters of normal distribution']
**Citations:** ['B:openstax-pds:p144:1']

## S10 (answerable) - abstain
**Q:** How can an outlier in monthly employment data be replaced if it does not reflect real numbers?

**Expected:** Replace it with a value computed from the points before and after the outlier (the book calls it the median, computed as their mean).

**Answer:** INSUFFICIENT_EVIDENCE: The passages do not provide specific methods for replacing outliers in monthly employment data that do not reflect real numbers.

**Queries:** []
**Citations:** []

## X-D01 (ABSENT) - abstain
**Q:** What is the formula for the Pearson correlation coefficient?

**Answer:** INSUFFICIENT_EVIDENCE: The passages do not contain the formula for the Pearson correlation coefficient.

**Queries:** ['Pearson correlation coefficient formula']
**Citations:** []

## X-D02 (ABSENT) - answered
**Q:** How does the central limit theorem relate sample means to the normal distribution?

**Answer:** The central limit theorem states that the sampling distribution of the sample mean approaches a normal distribution as the sample size increases, regardless of the shape of the population distribution. This means that if you take multiple samples from a population and calculate their means, the distribution of these sample means will approximate a normal distribution, with the mean of the sample means being close to the population mean and the standard deviation of the sample means decreasing as the sample size increases [B:openstax-pds:p144:1].

**Queries:** ['central limit theorem sample means normal distribution']
**Citations:** ['B:openstax-pds:p144:1']

## X-D03 (ABSENT) - abstain
**Q:** How is the Shapiro-Wilk test used to check whether data is normally distributed?

**Answer:** INSUFFICIENT_EVIDENCE: The passages do not provide information on how the Shapiro-Wilk test is used to check for normal distribution.

**Queries:** []
**Citations:** []
