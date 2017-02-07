
# This script concatenate all .txt files in the individual subjects folders.
mainFolder = 'E:/Stage CEA/analysis/data/behavioral'
#mainFolder = '/neurospin/meg/meg_tmp/MCD_Jacques_2016/analysis/data/behavioral'
setwd(mainFolder)

# Get all subfolders
listDir = list.dirs(mainFolder)
listDir = listDir[2:length(listDir)]

# Cycle across subfolders to get all file names
listFiles = c()
for (i in listDir){
  for (j in list.files(path=i, pattern="*.txt$")){
    nameFile = paste(i, j, sep="/")
    listFiles = c(listFiles, nameFile)
  }
}

# Concatenate all files into a big data set
data = data.frame()
for (i in 1:length(listFiles)) {
  temp = read.csv(listFiles[i], header = TRUE, na.strings = c('None'))
  data <- rbind(data,temp)
}

# Browse data frame
summary(data)

# Save data frame
nameOutFile = paste(mainFolder, "raw_behavioral_data.txt", sep="/")
write.table(data, file=nameOutFile, sep=",")
