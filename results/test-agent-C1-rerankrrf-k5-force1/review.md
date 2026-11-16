# Review sheet test / C1-rerankrrf-k5-force1

Grade each: grounded answer 0-2, each citation supports (T/F), abstention correct (T/F), context 0-2.

## H01 (answerable) - answered
**Q:** What kind of data can the mode be applied to that the mean and the median cannot?

**Expected:** Non-numeric (qualitative) data; the mean and median apply only to numeric (quantitative) data.

**Answer:** The mode can be applied to non-numeric (qualitative) data, whereas the mean and the median can only be applied to numeric (quantitative) data. [B:openstax-pds:p119:0]

**Queries:** ['mode mean median data']
**Citations:** ['B:openstax-pds:p119:0']

## H02 (answerable) - answered
**Q:** How is the median found when a dataset has an odd number of values?

**Expected:** It is the single middle value of the ordered data.

**Answer:** When a dataset has an odd number of values, the median is the middle value in the ordered dataset. To find the position of the median, calculate \(\frac{n+1}{2}\), where \(n\) is the number of data values. This indicates the exact position of the median in the ordered list. [B:openstax-pds:p118:0]

**Queries:** ['median odd number of values']
**Citations:** ['B:openstax-pds:p118:0']

## H03 (answerable) - answered
**Q:** What does a smaller standard deviation imply about a dataset?

**Expected:** Less variability (values are concentrated close to the mean); a larger one implies more variability.

**Answer:** A smaller standard deviation implies less variability in a dataset [B:openstax-pds:p123:0].

**Queries:** ['standard deviation smaller implies']
**Citations:** ['B:openstax-pds:p123:0']

## H04 (answerable) - answered
**Q:** What is Bayes' Theorem used for?

**Expected:** A statistical technique that allows revising probabilities based on new information.

**Answer:** Bayes' Theorem is used to help assess probabilities associated with medical diagnoses, such as the probability a patient will develop cancer based on test screening results [B:openstax-pds:p136:1]. It also allows for the calculation of conditional probabilities and the revision of probability estimates based on new information [B:openstax-pds:p132:1].

**Queries:** ["Bayes' Theorem used for"]
**Citations:** ['B:openstax-pds:p136:1', 'B:openstax-pds:p132:1']

## H05 (answerable) - answered
**Q:** What is the Poisson distribution used to find the probability of?

**Expected:** The probability of a certain number of occurrences of a random variable in a specific interval, such as an interval of time.

**Answer:** The Poisson distribution is used to find the probability of a specific number of occurrences in a given interval, such as time or area. This includes scenarios like the number of customers arriving at a checkout lane per minute or the number of accidents at a busy intersection per month. [B:openstax-pds:p142:1]

**Queries:** ['Poisson distribution used to find the probability of']
**Citations:** ['B:openstax-pds:p142:1']

## H06 (answerable) - answered
**Q:** What does the data cleaning process include?

**Expected:** Identifying and correcting errors, inconsistencies and missing values so data is accurate, reliable and usable.

**Answer:** The data cleaning process includes removing duplicate or irrelevant data, handling missing data, and correcting formatting misconceptions [B:openstax-pds:p86:2]. Additionally, it encompasses data integration, where data from multiple sources is merged into a single dataset, and data transformation, which prepares the data for further analysis by converting data types, scaling numerical data, or encoding categorical variables [B:openstax-pds:p86:2].

**Queries:** ['data cleaning process']
**Citations:** ['B:openstax-pds:p86:2']

## H07 (answerable) - answered
**Q:** Why might text data be normalized when analyzing customer reviews?

**Expected:** So variations of the same word (e.g. colour and color) are treated as the same, giving a more accurate understanding of sentiment.

**Answer:** Text data is normalized when analyzing customer reviews to ensure that variations of the same word are treated uniformly, which provides a more accurate understanding of sentiment toward a product or service [B:openstax-pds:p98:0]. This normalization helps in making the data more easily interpretable for machine learning algorithms [B:openstax-pds:p98:0].

**Queries:** ['text data normalization customer reviews']
**Citations:** ['B:openstax-pds:p98:0']

## H08 (answerable) - answered
**Q:** What does the spell-checking and correction preprocessing technique do?

**Expected:** Corrects spelling errors to improve accuracy.

**Answer:** Spell-checking and correction is a preprocessing technique that corrects spelling errors to improve the accuracy and readability of the text. For example, it can transform "The writting was very inpprecise and had many trgical mistakes." into "The writing was very imprecise and had many tragic mistakes." [B:openstax-pds:p97:0]

**Queries:** ['spell-checking and correction preprocessing technique']
**Citations:** ['B:openstax-pds:p97:0']

## H09 (answerable) - answered
**Q:** In the home price example, what is the upper bound for outliers and is a price of $5,500,000 an outlier?

**Expected:** The upper bound is 1,159,375; 5,500,000 is above it, so it is a potential outlier.

**Answer:** The upper bound for outliers in the home price example is 1,159,375. A price of $5,500,000 is greater than this upper bound, so it is considered a potential outlier [B:openstax-pds:p128:0].

**Queries:** ['home price example upper bound outliers']
**Citations:** ['B:openstax-pds:p128:0']

## H10 (answerable) - answered
**Q:** A home sold for $270,000 where the mean is $350,000 and the standard deviation is $40,000. What does its z-score show?

**Expected:** The z-score is -2: the price is 2 standard deviations below the mean, significantly below it.

**Answer:** The z-score for the home sold at $270,000 can be calculated using the formula:

\[ z = \frac{x - \mu}{\sigma} \]

where \( x \) is the home price ($270,000), \( \mu \) is the mean ($350,000), and \( \sigma \) is the standard deviation ($40,000).

Plugging in the values:

\[ z = \frac{270,000 - 350,000}{40,000} = \frac{-80,000}{40,000} = -2 \]

So, the z-score shows that the home's selling price is 2 standard deviations below the mean. [B:openstax-pds:p129:0]

**Queries:** ['z-score home sale mean standard deviation']
**Citations:** ['B:openstax-pds:p129:0']

## H11 (answerable) - answered
**Q:** About what percentage of values lie within three standard deviations of the mean in a normal distribution?

**Expected:** About 99.7%.

**Answer:** About 99.7% of the values lie within three standard deviations of the mean in a normal distribution [B:openstax-pds:p146:0].

**Queries:** ['percentage of values within three standard deviations of the mean normal distribution']
**Citations:** ['B:openstax-pds:p146:0']

## H12 (answerable) - answered
**Q:** What should a sampling frame ideally include?

**Expected:** All members of the target population, with a clear and accessible way to identify and select units for the sample.

**Answer:** The sampling frame should ideally encompass all members of the target population and provide a clear and accessible way to identify and select individuals or units for inclusion in the sample. [B:openstax-pds:p75:0]

**Queries:** ['sampling frame ideally include']
**Citations:** ['B:openstax-pds:p75:0']

## H13 (answerable) - answered
**Q:** How is the probability that an employee earns more than $68,000 found with a normal curve?

**Expected:** Calculate the area under the normal curve to the right of $68,000.

**Answer:** To find the probability that an employee earns more than $68,000 using a normal curve, the area under the normal curve to the right of $68,000 is calculated [B:openstax-pds:p145:0]. This can be done using Python commands such as `norm.cdf()` to find the area to the left of $68,000, and then subtracting this from 1 to get the area to the right [B:openstax-pds:p148:1].

**Queries:** ['normal curve probability employee salary']
**Citations:** ['B:openstax-pds:p145:0', 'B:openstax-pds:p148:1']

## X-T01 (ABSENT) - abstain
**Q:** How do you run a chi-square test of independence on two categorical variables?

**Answer:** INSUFFICIENT_EVIDENCE: The passages do not provide instructions on how to run a chi-square test of independence on two categorical variables.

**Queries:** ['chi-square test of independence']
**Citations:** []

## X-T02 (ABSENT) - answered
**Q:** How can Selenium be used to scrape web pages that load content with JavaScript?

**Answer:** Selenium can be used to scrape web pages that load content with JavaScript by automating the interaction with the web page as a real user would. This allows Selenium to wait for the JavaScript to execute and then extract the data. However, the provided passages do not explicitly mention how Selenium is used for this purpose. Therefore, the answer based on the given passages is:

INSUFFICIENT_EVIDENCE: The passages do not provide specific details on how Selenium is used to scrape web pages that load content with JavaScript.

**Queries:** ['Selenium JavaScript web pages scraping']
**Citations:** []

## X-T03 (ABSENT) - abstain
**Q:** What is the formula for the mean of a geometric distribution?

**Answer:** INSUFFICIENT_EVIDENCE: The passages do not contain the formula for the mean of a geometric distribution.

**Queries:** ['formula for the mean of a geometric distribution']
**Citations:** []
