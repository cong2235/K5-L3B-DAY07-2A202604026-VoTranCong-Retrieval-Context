# Bảng chấm tay - test held-out (cấu hình chọn C1 và baseline)

Cách dùng: đọc từng mục, đối chiếu với SÁCH GỐC (không chỉ với đoạn trích dưới đây), rồi điền nhãn vào cột trống.

- **Grounded answer** (câu có đáp án): 0 = sai/thiếu evidence; 1 = đúng một phần; 2 = đúng và đủ. Từ chối câu có đáp án = 0.

- **Citation support**: với mỗi citation, đoạn được trích có hỗ trợ câu trả lời không (đúng/sai).

- **Context 0/1/2** (cần ít nhất 5 câu test cho cả baseline và C1): 0 = không có evidence; 1 = có nhưng thiếu điều kiện/nguồn; 2 = đủ evidence và nguồn.

- **Abstention** (câu thiếu bằng chứng): từ chối thật sự và không thêm khẳng định vô căn cứ = đúng. Từ chối mà không tìm kiếm không phải bằng chứng.

- "Nháp của trợ lý" chỉ là gợi ý để bạn kiểm tra, KHÔNG phải nhãn.


## H01 (có đáp án) - C1: answered | baseline: answered
**Câu hỏi:** What kind of data can the mode be applied to that the mean and the median cannot?

**Đáp án chuẩn:** Non-numeric (qualitative) data; the mean and median apply only to numeric (quantitative) data.  
**Evidence gold (trang 119):** "The mode can also be applied to non-numeric (qualitative) data, whereas the mean and the median can only
be applied for numeric (quantitative) data."

**C1 trả lời:** The mode can be applied to non-numeric (qualitative) data, whereas the mean and the median can only be applied to numeric (quantitative) data. [B:openstax-pds:p119:0]

**C1 tìm với:** ['mode mean median data'] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p119:0` (trong context: True), nội dung chunk: "The mode can also be applied to non-numeric (qualitative) data, whereas the mean and the median can only be applied for numeric (quantitative) data. For example, a restaurant manager might want to determine the mode for responses to customer surveys on the quality of the service of a restaurant, as shown in Table 3.1. Customer Service Rating Number of Respondents Excellent 267 Very Good 410 Good 392 Fair 107 Poor 18 " -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (answered, số lần tìm 1):** The mode can be applied to categorical data where the mean and median are not applicable. Specifically, the mode identifies the most frequently occurring value in a dataset, which can be useful for non-numeric data [B:openstax-pds:p118:2]. | context có evidence (máy kiểm): False

**Nhãn của bạn (C1):** grounded 0/1/2 = 2 ; context 0/1/2 = 2 ; abstention đúng ☐ ; lý do: Agent trả lời đúng thông tin, ngữ cảnh và đưa ra đúng evidence  |  **Baseline:** context 0/1/2 = 0 ; grounded = Tuy vẫn đưa ra evidence đúng nhưng 


## H02 (có đáp án) - C1: answered | baseline: abstain
**Câu hỏi:** How is the median found when a dataset has an odd number of values?

**Đáp án chuẩn:** It is the single middle value of the ordered data.  
**Evidence gold (trang 118):** "If there is an odd number of data values in the dataset, then there will be one data value that represents the
middle value, and this is the median."

**C1 trả lời:** When a dataset has an odd number of values, the median is the middle value in the ordered dataset. To find the position of the median, calculate \(\frac{n+1}{2}\), where \(n\) is the number of data values. This indicates the exact position of the median in the ordered list. [B:openstax-pds:p118:0]

**C1 tìm với:** ['median odd number of values'] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p118:0` (trong context: True), nội dung chunk: "To determine the median of a dataset, first order the data from smallest to largest, and then find the middle value in the ordered dataset. For example, to find the median value of 50 exam scores, find the score that splits the data into two equal parts. The exam scores for 25 students will be below the median, and 25 students will have exam scores above the median. If there is an odd number of data values in the dat" -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (abstain, số lần tìm 1):** INSUFFICIENT_EVIDENCE: The passages do not provide information on how to find the median when the dataset has an odd number of values. They only discuss the case where the number of data values is even. [B:openstax-pds:p118:1] [B:openstax-pds:p118:0] [B:openstax-pds:p118:2] | context có evidence (máy kiểm): False

_Nháp của trợ lý:_ Đúng ý chính; thêm công thức (n+1)/2: kiểm tra có trong p118 không.

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## H03 (có đáp án) - C1: answered | baseline: answered
**Câu hỏi:** What does a smaller standard deviation imply about a dataset?

**Đáp án chuẩn:** Less variability (values are concentrated close to the mean); a larger one implies more variability.  
**Evidence gold (trang 123):** "A smaller standard deviation implies less variability in a dataset, and a larger
standard deviation implies more variability in a dataset."

**C1 trả lời:** A smaller standard deviation implies less variability in a dataset [B:openstax-pds:p123:0].

**C1 tìm với:** ['standard deviation smaller implies'] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p123:0` (trong context: True), nội dung chunk: "far from the mean, relative to the typical distance from the mean. The standard deviation is always positive or zero. It is small when the data values are all concentrated close to the mean, exhibiting little variation, or spread. It is larger when the data values are spread out more from the mean, exhibiting more variation. A smaller standard deviation implies less variability in a dataset, and a larger standard dev" -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (answered, số lần tìm 0):** A smaller standard deviation implies that the data points tend to be closer to the mean of the dataset [B:openstax-pds:p95:1]. | context có evidence (máy kiểm): False

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## H04 (có đáp án) - C1: answered | baseline: answered
**Câu hỏi:** What is Bayes' Theorem used for?

**Đáp án chuẩn:** A statistical technique that allows revising probabilities based on new information.  
**Evidence gold (trang 136):** "Bayes’ Theorem is a statistical technique that allows for the revision of probability estimates based on new
information or evidence that allows for more accurate and efficient decision-making in uncertain situations."

**C1 trả lời:** Bayes' Theorem is used to help assess probabilities associated with medical diagnoses, such as the probability a patient will develop cancer based on test screening results [B:openstax-pds:p136:1]. It also allows for the calculation of conditional probabilities and the revision of probability estimates based on new information [B:openstax-pds:p132:1].

**C1 tìm với:** ["Bayes' Theorem used for"] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p136:1` (trong context: True), nội dung chunk: "Bayes’ Theorem is often used to help assess probabilities associated with medical diagnoses such as the probability a patient will develop cancer based on test screening results. This can be important in medical analysis to help assess the impact of a false positive, which is the scenario where the patient does not have the ailment but the screening test gives a false indication that the patient does have the ailment" -> hỗ trợ? ☐ đúng ☐ sai

- citation `B:openstax-pds:p132:1` (trong context: True), nội dung chunk: "Conditional Probability and Bayes’ Theorem Data scientists are often interested in determining conditional probabilities, or the occurrence of one event that is conditional or dependent on another event. For example, a medical researcher might be interested to know if an asthma diagnosis for a patient is dependent on the patient’s exposure to air pollutants. In addition, when calculating conditional probabilities, we" -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (answered, số lần tìm 1):** Bayes' Theorem is often used to help assess probabilities associated with medical diagnoses, such as the probability a patient will develop cancer based on test screening results. It allows the calculation of the conditional probability [B:openstax-pds:p136:1]. | context có evidence (máy kiểm): False

_Nháp của trợ lý:_ Kiểm tra p132:1 có hỗ trợ câu "conditional probabilities" không.

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## H05 (có đáp án) - C1: answered | baseline: answered
**Câu hỏi:** What is the Poisson distribution used to find the probability of?

**Đáp án chuẩn:** The probability of a certain number of occurrences of a random variable in a specific interval, such as an interval of time.  
**Evidence gold (trang 142):** "However, there are certain scenarios where a data scientist might be interested to know the
probability of a certain number of occurrences for a random variable in a specific interval, such as an interval
of time."

**C1 trả lời:** The Poisson distribution is used to find the probability of a specific number of occurrences in a given interval, such as time or area. This includes scenarios like the number of customers arriving at a checkout lane per minute or the number of accidents at a busy intersection per month. [B:openstax-pds:p142:1]

**C1 tìm với:** ['Poisson distribution used to find the probability of'] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p142:1` (trong context: True), nội dung chunk: "The Poisson distribution is applied when counting the number of occurrences in a certain interval. The random variable then counts the number of occurrences in the interval. A common application for the Poisson distribution is to model arrivals of customers for a queue, such as when there might be 6 customers per minute arriving at a checkout lane in the grocery store and the store manager wants to ensure that custom" -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (answered, số lần tìm 0):** [INSUFFICIENT_EVIDENCE: The passages do not provide specific information on what the Poisson distribution is used to find the probability of.] | context có evidence (máy kiểm): False

_Nháp của trợ lý:_ Kiểm tra ví dụ "checkout lane / accidents at intersection" có trong p142:1 không (có thể không có trong sách).

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## H06 (có đáp án) - C1: answered | baseline: answered
**Câu hỏi:** What does the data cleaning process include?

**Đáp án chuẩn:** Identifying and correcting errors, inconsistencies and missing values so data is accurate, reliable and usable.  
**Evidence gold (trang 84):** "cleaning process includes identifying and correcting any errors, inconsistencies, and missing values in a
dataset and is essential for ensuring that the data is accurate, reliable, and usable for analysis or other
purposes."

**C1 trả lời:** The data cleaning process includes removing duplicate or irrelevant data, handling missing data, and correcting formatting misconceptions [B:openstax-pds:p86:2]. Additionally, it encompasses data integration, where data from multiple sources is merged into a single dataset, and data transformation, which prepares the data for further analysis by converting data types, scaling numerical data, or encoding categorical variables [B:openstax-pds:p86:2].

**C1 tìm với:** ['data cleaning process'] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p86:2` (trong context: True), nội dung chunk: "1. Data integration. Data integration refers to merging data from multiple sources into a single dataset. 2. Data cleaning. In this step, data is assessed for any errors or inconsistencies, and appropriate actions are taken to correct them. This may include removing duplicate values, handling missing data, and correcting formatting misconceptions. 3. Data transformation. This step prepares the data for the next step " -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (answered, số lần tìm 1):** The data cleaning process includes extracting irrelevant or duplicate data, handling missing values, and correcting errors or inconsistencies. [B:openstax-pds:p86:1] | context có evidence (máy kiểm): False

_Nháp của trợ lý:_ Cite p86:2, không phải đoạn gold (p84): kiểm tra p86:2 có nói "removing duplicate...", và đáp án có thiếu "errors/inconsistencies" không.

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## H07 (có đáp án) - C1: answered | baseline: answered
**Câu hỏi:** Why might text data be normalized when analyzing customer reviews?

**Đáp án chuẩn:** So variations of the same word (e.g. colour and color) are treated as the same, giving a more accurate understanding of sentiment.  
**Evidence gold (trang 98):** "For example, when analyzing customer reviews, it may be beneficial to normalize text data so that variations of
the same word (e.g., “colour” and “color”) are treated as the same, providing a more accurate understanding of
sentiment toward a product or service."

**C1 trả lời:** Text data is normalized when analyzing customer reviews to ensure that variations of the same word are treated uniformly, which provides a more accurate understanding of sentiment toward a product or service [B:openstax-pds:p98:0]. This normalization helps in making the data more easily interpretable for machine learning algorithms [B:openstax-pds:p98:0].

**C1 tìm với:** ['text data normalization customer reviews'] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p98:0` (trong context: True), nội dung chunk: "language processing tasks. It also makes the data more easily interpretable for machine learning algorithms. For example, when analyzing customer reviews, it may be beneficial to normalize text data so that variations of the same word (e.g., “colour” and “color”) are treated as the same, providing a more accurate understanding of sentiment toward a product or service." -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (answered, số lần tìm 1):** Text data is normalized when analyzing customer reviews to ensure consistent treatment of variations of the same word, such as "colour" and "color". This helps in accurately understanding sentiment towards a product or service [B:openst:openstax-pds:p98:0]. | context có evidence (máy kiểm): True

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## H08 (có đáp án) - C1: answered | baseline: abstain
**Câu hỏi:** What does the spell-checking and correction preprocessing technique do?

**Đáp án chuẩn:** Corrects spelling errors to improve accuracy.  
**Evidence gold (trang 97):** "Correcting
spelling errors
to improve
accuracy"

**C1 trả lời:** Spell-checking and correction is a preprocessing technique that corrects spelling errors to improve the accuracy and readability of the text. For example, it can transform "The writting was very inpprecise and had many trgical mistakes." into "The writing was very imprecise and had many tragic mistakes." [B:openstax-pds:p97:0]

**C1 tìm với:** ['spell-checking and correction preprocessing technique'] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p97:0` (trong context: True), nội dung chunk: "Preprocessing Technique Explanation Example Spell-checking and correction Correcting spelling errors to improve accuracy Suppose we have a text like: “The writting was very inpprecise and had many trgical mistakes.” With spellchecking and correction, this text can be processed and corrected to: “The writing was very imprecise and had many tragic mistakes.” This involves identifying and correcting misspelled words. In" -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (abstain, số lần tìm 0):** INSUFFICIENT_EVIDENCE: The passages do not provide information on what spell-checking and correction preprocessing technique does. | context có evidence (máy kiểm): False

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## H09 (có đáp án) - C1: answered | baseline: answered
**Câu hỏi:** In the home price example, what is the upper bound for outliers and is a price of $5,500,000 an outlier?

**Đáp án chuẩn:** The upper bound is 1,159,375; 5,500,000 is above it, so it is a potential outlier.  
**Evidence gold (trang 128):** "The upper bound for outliers is 1,159,375. The data value of 5,500,000 is greater than the upper bound of
1,159,375. Therefore, the home price of $5,500,000 is a potential outlier."

**C1 trả lời:** The upper bound for outliers in the home price example is 1,159,375. A price of $5,500,000 is greater than this upper bound, so it is considered a potential outlier [B:openstax-pds:p128:0].

**C1 tìm với:** ['home price example upper bound outliers'] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p128:0` (trong context: True), nội dung chunk: "Now, calculate the interquartile range (IQR): Calculate the value of 1.5 interquartile range (IQR): Calculate the lower and upper bound for outliers: The lower bound for outliers is −201,625. Of course, no home price is less than −201,625, so no outliers are present for the lower end of the dataset. The upper bound for outliers is 1,159,375. The data value of 5,500,000 is greater than the upper bound of 1,159,375. Th" -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (answered, số lần tìm 1):** The upper bound for outliers in the home price example is 1,159,375. A price of $5,500,000 is indeed an outlier since it exceeds this upper bound [B:openstax-pds:p128:0]. | context có evidence (máy kiểm): True

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## H10 (có đáp án) - C1: answered | baseline: abstain
**Câu hỏi:** A home sold for $270,000 where the mean is $350,000 and the standard deviation is $40,000. What does its z-score show?

**Đáp án chuẩn:** The z-score is -2: the price is 2 standard deviations below the mean, significantly below it.  
**Evidence gold (trang 129):** "-score of −2 indicates that the selling price for this home is 2 standard deviations below the mean,
which represents a data value that is significantly below the mean."

**C1 trả lời:** The z-score for the home sold at $270,000 can be calculated using the formula:

\[ z = \frac{x - \mu}{\sigma} \]

where \( x \) is the home price ($270,000), \( \mu \) is the mean ($350,000), and \( \sigma \) is the standard deviation ($40,000).

Plugging in the values:

\[ z = \frac{270,000 - 350,000}{40,000} = \frac{-80,000}{40,000} = -2 \]

So, the z-score shows that the home's selling price is 2 standard deviations below the mean. [B:openstax-pds:p129:0]

**C1 tìm với:** ['z-score home sale mean standard deviation'] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p129:0` (trong context: True), nội dung chunk: "EXAMPLE 3.13 Problem For the home example in Example 3.12, the value is the home price of $270,000, the mean is $350,000, and the standard deviation is $40,000. Calculate the -score. Solution The -score can be calculated as follows: This -score of −2 indicates that the selling price for this home is 2 standard deviations below the mean, which represents a data value that is significantly below the mean. Using Python " -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (abstain, số lần tìm 0):** INSUFFICIENT_Evidence: The passages do not provide information on how to calculate or interpret z-scores. | context có evidence (máy kiểm): False

_Nháp của trợ lý:_ Xem đáp án cuối có ra -2 và giải thích đúng không.

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## H11 (có đáp án) - C1: answered | baseline: abstain
**Câu hỏi:** About what percentage of values lie within three standard deviations of the mean in a normal distribution?

**Đáp án chuẩn:** About 99.7%.  
**Evidence gold (trang 146):** "About 99.7% of the -values lie between
and
units from the mean (within three standard
deviations of the mean)."

**C1 trả lời:** About 99.7% of the values lie within three standard deviations of the mean in a normal distribution [B:openstax-pds:p146:0].

**C1 tìm với:** ['percentage of values within three standard deviations of the mean normal distribution'] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p146:0` (trong context: True), nội dung chunk: "• About 95% of the -values lie between and units from the mean (within two standard deviations of the mean). • About 99.7% of the -values lie between and units from the mean (within three standard deviations of the mean). Notice that almost all the x-values lie within three standard deviations of the mean. • The -scores for and are and , respectively. • The -scores for and are and , respectively. • The -scores for an" -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (abstain, số lần tìm 0):** INSUFFICIENT_EVIDENCE: The specific percentage of values within three standard deviations of the mean in a normal distribution is not provided in the given passages. | context có evidence (máy kiểm): False

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## H12 (có đáp án) - C1: answered | baseline: answered
**Câu hỏi:** What should a sampling frame ideally include?

**Đáp án chuẩn:** All members of the target population, with a clear and accessible way to identify and select units for the sample.  
**Evidence gold (trang 75):** "careful consideration of the sampling frame should ideally encompass all members of
the target population and provide a clear and accessible way to identify and select individuals or units for
inclusion in the sample."

**C1 trả lời:** The sampling frame should ideally encompass all members of the target population and provide a clear and accessible way to identify and select individuals or units for inclusion in the sample. [B:openstax-pds:p75:0]

**C1 tìm với:** ['sampling frame ideally include'] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p75:0` (trong context: True), nội dung chunk: "the sample. Additionally, careful consideration of the sampling frame should ideally encompass all members of the target population and provide a clear and accessible way to identify and select individuals or units for inclusion in the sample. Sampling bias can occur at various stages of the sampling process, and it can greatly impact the accuracy and validity of research findings." -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (answered, số lần tìm 1):** The sampling frame should ideally encompass all members of the target population and provide a clear and accessible way to identify and select individuals or units for inclusion in the sample. [B:openstix-pds:p75:0] | context có evidence (máy kiểm): True

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## H13 (có đáp án) - C1: answered | baseline: abstain
**Câu hỏi:** How is the probability that an employee earns more than $68,000 found with a normal curve?

**Đáp án chuẩn:** Calculate the area under the normal curve to the right of $68,000.  
**Evidence gold (trang 145):** "Then, to find the probability that an employee
earns more than $68,000, calculate the area under the normal curve to the right of the data value $68,000."

**C1 trả lời:** To find the probability that an employee earns more than $68,000 using a normal curve, the area under the normal curve to the right of $68,000 is calculated [B:openstax-pds:p145:0]. This can be done using Python commands such as `norm.cdf()` to find the area to the left of $68,000, and then subtracting this from 1 to get the area to the right [B:openstax-pds:p148:1].

**C1 tìm với:** ['normal curve probability employee salary'] | context có evidence (máy kiểm): True

- citation `B:openstax-pds:p145:0` (trong context: True), nội dung chunk: "probability that a random employee earns more than $68,000. Solution A normal curve can be drawn to represent this scenario, in which the mean of $60,000 would be plotted on the horizontal axis, corresponding to the peak of the curve. Then, to find the probability that an employee earns more than $68,000, calculate the area under the normal curve to the right of the data value $68,000. Figure 3.8 illustrates the area" -> hỗ trợ? ☐ đúng ☐ sai

- citation `B:openstax-pds:p148:1` (trong context: True), nội dung chunk: "Suppose that at a software company, the mean employee salary is $60,000 with a standard deviation of $7,500. Use Python to calculate the probability that a random employee earns more than $68,000. In this example: is the measurement of interest mean is the mean of the normal distribution standard deviation is the standard deviation of the normal distribution The corresponding function in Python is written as: norm.cd" -> hỗ trợ? ☐ đúng ☐ sai

**Baseline trả lời (abstain, số lần tìm 0):** INSUFFICIENT_EVIDENCE: The passages do not provide information on how to find the probability that an employee earns more than $68,000 using a normal curve. | context có evidence (máy kiểm): False

_Nháp của trợ lý:_ Kiểm tra `norm.cdf()` và citation p148:1 có hỗ trợ không.

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## X-T01 (THIẾU BẰNG CHỨNG) - C1: abstain | baseline: abstain
**Câu hỏi:** How do you run a chi-square test of independence on two categorical variables?

**Lý do thiếu bằng chứng (cần bạn kiểm tra):** Chi-square tests and hypothesis-test procedures are not covered in the indexed chapters.

**C1 trả lời:** INSUFFICIENT_EVIDENCE: The passages do not provide instructions on how to run a chi-square test of independence on two categorical variables.

**C1 tìm với:** ['chi-square test of independence'] | context có evidence (máy kiểm): n/a

**Baseline trả lời (abstain, số lần tìm 1):** INSUFFICIENT_EVIDENCE: The passages do not contain information on how to run a chi-square test of independence on two categorical variables. | context có evidence (máy kiểm): n/a

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## X-T02 (THIẾU BẰNG CHỨNG) - C1: answered | baseline: abstain
**Câu hỏi:** How can Selenium be used to scrape web pages that load content with JavaScript?

**Lý do thiếu bằng chứng (cần bạn kiểm tra):** Web scraping is covered (pp. 76-85, e.g. Beautiful Soup) but Selenium/Scrapy and dynamic pages are not.

**C1 trả lời:** Selenium can be used to scrape web pages that load content with JavaScript by automating the interaction with the web page as a real user would. This allows Selenium to wait for the JavaScript to execute and then extract the data. However, the provided passages do not explicitly mention how Selenium is used for this purpose. Therefore, the answer based on the given passages is:

INSUFFICIENT_EVIDENCE: The passages do not provide specific details on how Selenium is used to scrape web pages that load content with JavaScript.

**C1 tìm với:** ['Selenium JavaScript web pages scraping'] | context có evidence (máy kiểm): n/a

**Baseline trả lời (abstain, số lần tìm 0):** INSUFFICIENT_EVIDENCE: The provided passages do not contain information on how Selenium can be used to scrape web pages that load content with JavaScript. | context có evidence (máy kiểm): n/a

_Nháp của trợ lý:_ Không từ chối, trả lời bằng kiến thức ngoài (không citation) rồi mới nói passages không nêu: có vẻ KHÔNG đạt.

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___


## X-T03 (THIẾU BẰNG CHỨNG) - C1: abstain | baseline: abstain
**Câu hỏi:** What is the formula for the mean of a geometric distribution?

**Lý do thiếu bằng chứng (cần bạn kiểm tra):** Binomial, Poisson, exponential and normal distributions are covered; the geometric (and uniform) distribution is not.

**C1 trả lời:** INSUFFICIENT_EVIDENCE: The passages do not contain the formula for the mean of a geometric distribution.

**C1 tìm với:** ['formula for the mean of a geometric distribution'] | context có evidence (máy kiểm): n/a

**Baseline trả lời (abstain, số lần tìm 1):** INSUFFICIENT_EVIDENCE: The passages do not contain the formula for the mean of a geometric distribution. | context có evidence (máy kiểm): n/a

**Nhãn của bạn (C1):** grounded 0/1/2 = ___ ; context 0/1/2 = ___ ; abstention đúng ☐ ; lý do: ______  |  **Baseline:** context 0/1/2 = ___ ; grounded = ___
