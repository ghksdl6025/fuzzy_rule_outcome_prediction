# Fuzzy association rule based outcome prediction
  
suhwan Lee

## Fuzzy membership function in uniform interval
![uniform](./img/membership_function.png)

## Update

20.09.25

- Apriori algorithm with fuzzified itemset mining is done. Each label dataframe has unique rule only assigned for the label.
- Now, the next step is to construct classifier and plot network. Then compare the network and prediction performance to normal ARM method.

20.09.15

- Still writing code for generating association rules from fuzzified item set dataframe

20.09.14

- Update quantitative2fuzzy.py file generating **fuzzified event log**.
- Columns of fuzzied event log are caseid, label, and membership label while converting quantitative value to assigned memebership names
- That is, number of columns are not prefix length * possible memebership labels.
- Column explanation:  
  Quantitative atts_event order_membership label  
  ex) Duration_1_SS  
  Quantitatie atts = Duration  
  event order = 1
  membership label = SS  