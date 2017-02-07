setwd("/home/JP250916/Desktop/Lien vers MCD_Jacques_2016/analysis/data/behavioral/")

#### Import files ####
listDir = 
temp = list.files(pattern="*.txt")

data = data.frame()
for (i in 1:length(temp)) {
  temp2 = read.csv(temp[i], header = TRUE, na.strings = c('None'))
  data <- rbind(data,temp2)
}

# Recode variables in a good format
data = data[!is.na(data$response),]
summary(data)



#### Causality judgment ####
d = data[data$blocType == 'SEQUENCE_CJ',]
d$resp = 0                                                                    # 0 (decorrelated)
d[d$response == 'common',]$resp = 1                                       # 1 (correlated)

# Check for DDD/DD/DC/CC/CCC stimuli if psychometric curves looks good
d1 = d[d$stimulus %in% c('DDD', 'DD', 'DC', 'CC', 'CCC'),]
d1$stimulus = factor(d1$stimulus, levels=c('DDD', 'DD', 'DC', 'CC', 'CCC'))   # Order stimuli
tab1 = aggregate(resp ~ stimulus, mean, data=d1)                              # Compute mean response by stimuli
plot(tab1$stimulus, tab1$resp)                                                # Plot the psychometric curve

# Check if there is no major bias in the other stimuli
d2 = d[d$stimulus %in% c('AAA', 'AA', 'AV', 'VV', 'VVV'),]
d2$stimulus = factor(d2$stimulus, levels=c('AAA', 'AA', 'AV', 'VV', 'VVV'))
tab2 = aggregate(resp ~ stimulus, mean, data=d2)
plot(tab2$stimulus, tab2$resp)

# Full plot
tab = rbind(tab1, tab2)
plot(tab$stimulus, tab$resp, ylim=c(0, 1))





#### Order judgment ####
d = data[data$blocType == 'SEQUENCE_TOJ',]
d$resp = 0                                                                    # 0 (audiofirst)
d[d$response == 'visualfirst',]$resp = 1                                      # 1 (visualfirst)

# Check for AAA/AA/AV/VV/VVV stimuli if psychometric curves looks good
d1 = d[d$stimulus %in% c('AAA', 'AA', 'AV', 'VV', 'VVV'),]
d1$stimulus = factor(d1$stimulus, levels=c('AAA', 'AA', 'AV', 'VV', 'VVV'))   # Order stimuli
tab1 = aggregate(resp ~ stimulus, mean, data=d1)                              # Compute mean response by stimuli
plot(tab1$stimulus, tab1$resp)                                                # Plot the psychometric curve

# Check if there is no major bias in the other stimuli
d2 = d[d$stimulus %in% c('DDD', 'DD', 'DC', 'CC', 'CCC'),]
d2$stimulus = factor(d2$stimulus, levels=c('DDD', 'DD', 'DC', 'CC', 'CCC'))
tab2 = aggregate(resp ~ stimulus, mean, data=d2)
plot(tab2$stimulus, tab2$resp)

# Full plot
tab = rbind(tab1, tab2)
plot(tab$stimulus, tab$resp, ylim=c(0, 1))







#### Unique judgment ####
d = data[data$blocType == 'UNIQUE',]
d$resp = 0                                                                    # 0 (audiofirst)
d[d$response == 'visualfirst',]$resp = 1                                      # 1 (visualfirst)

# Check for A2V/A1V/A0V/V1A/V2A stimuli if psychometric curves looks good
d = d[d$stimulus %in% c('A2V', 'A1V', 'A0V', 'V1A', 'V2A'),]
d$stimulus = factor(d$stimulus, levels=c('A2V', 'A1V', 'A0V', 'V1A', 'V2A'))  # Order stimuli
tab = aggregate(resp ~ stimulus, mean, data=d)                                # Compute mean response by stimuli
plot(tab$stimulus, tab$resp)                                                  # Plot the psychometric curve

