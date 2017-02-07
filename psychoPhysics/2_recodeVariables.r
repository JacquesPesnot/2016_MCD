
mainDirectory = 'E:/Stage CEA/analysis/'
#mainDirectory = '/neurospin/meg/meg_tmp/MCD_Jacques_2016/analysis/'

dataFolder = paste(mainDirectory, 'data/behavioral/', sep='')

# Import data set
nameFile = paste(dataFolder, 'raw_behavioral_data.txt', sep='')
data = read.csv(nameFile)

# Eliminate no response trials
data = data[!is.na(data$response),]

# Recde block names to have every block between 1 and 3
data$blockNumber = data$blockNumber %/% 3 + 1
data$blockNumber = factor(data$blockNumber, levels=c('1', '2', '3'))

# Exchange DC and AV ; very important step. 
levels(data$stimulus) = c(levels(data$stimulus), 'TEMP')
data[data$stimulus == 'AV',]$stimulus = 'TEMP' # Temporary name
data[data$stimulus == 'DC',]$stimulus = 'AV'
data[data$stimulus == 'TEMP',]$stimulus = 'DC'

# Filter pre-tests and bad subjects
data = data[data$subjectNumber %in% c(3:99),]

# Save data set
nameOutFile = paste(dataFolder, "full_behavioral_data.txt", sep="/")
write.table(data, file=nameOutFile, sep=",")
