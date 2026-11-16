| split | name | method | top_k | budget | filter | Hit@1 | Hit@3 | Hit@k | Context | ctx chars | median ms | p90 ms | miss Hit@3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dev | tfidf-k3-b800 | tfidf | 3 | 800 | False | 11/15 | 13/15 | 13/15 | 9/15 | 609 | 1.0 | 1.3 | D07, D08 |
| dev | dense-k3-b800 | dense | 3 | 800 | False | 10/15 | 13/15 | 13/15 | 9/15 | 603 | 33.0 | 42.7 | D08, D15 |
| dev | hybrid-k3-b800 | hybrid | 3 | 800 | False | 11/15 | 13/15 | 13/15 | 9/15 | 609 | 41.1 | 48.5 | D07, D08 |
| dev | tfidf-k3-b2400t | tfidf | 3 | 9600 | False | 11/15 | 13/15 | 13/15 | 13/15 | 2042 | 1.2 | 1.5 | D07, D08 |
| dev | tfidf-k5-b2400t | tfidf | 5 | 9600 | False | 11/15 | 13/15 | 14/15 | 14/15 | 3341 | 1.0 | 1.3 | D07, D08 |
| dev | dense-k3-b2400t | dense | 3 | 9600 | False | 10/15 | 13/15 | 13/15 | 13/15 | 1975 | 32.5 | 36.9 | D08, D15 |
| dev | dense-k5-b2400t | dense | 5 | 9600 | False | 10/15 | 13/15 | 15/15 | 15/15 | 3288 | 35.6 | 38.7 | D08, D15 |
| dev | hybrid-k3-b2400t | hybrid | 3 | 9600 | False | 11/15 | 13/15 | 13/15 | 13/15 | 1959 | 36.2 | 39.0 | D07, D08 |
| dev | hybrid-k5-b2400t | hybrid | 5 | 9600 | False | 11/15 | 13/15 | 14/15 | 14/15 | 3348 | 50.5 | 55.8 | D07, D08 |
| dev | dense-k8-b3600t | dense | 8 | 14400 | False | 10/15 | 13/15 | 15/15 | 15/15 | 5350 | 33.2 | 38.8 | D08, D15 |
| dev | hybrid-k8-b3600t | hybrid | 8 | 14400 | False | 11/15 | 13/15 | 15/15 | 15/15 | 5334 | 34.1 | 38.3 | D07, D08 |
| dev | hybrid-k3-b2400t-w2 | hybrid | 3 | 9600 | False | 11/15 | 13/15 | 13/15 | 13/15 | 1958 | 37.7 | 44.2 | D07, D08 |
| dev | hybrid-k5-b2400t-w2 | hybrid | 5 | 9600 | False | 11/15 | 13/15 | 14/15 | 14/15 | 3357 | 39.9 | 44.3 | D07, D08 |
