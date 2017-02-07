

mainDirectory = 'E:/Stage CEA/analysis/'
#mainDirectory = '/neurospin/meg/meg_tmp/MCD_Jacques_2016/analysis/'

dataFolder = paste(mainDirectory, 'data/behavioral/', sep='')
sourceFolder = paste(mainDirectory, 'psychoPhysics/', sep='')
source(paste(sourceFolder, 'functions.r', sep=''))

#### Import data set ####
nameFile = paste(dataFolder, 'full_behavioral_data.txt', sep='')
dat = read.csv(nameFile)



#### Causality judgment ####
d = data[data$blocType == 'SEQUENCE_CJ',]

# Check for DDD/DD/DC/CC/CCC stimuli if psychometric curves looks good
d1 = d[d$stimulus %in% c('DD', 'DC', 'CC'),]
d1$stimulus = factor(d1$stimulus, levels=c('DD', 'DC', 'CC'))   # Order stimuli
t1 = summarySE(d1, measurevar = "rt", groupvars = c('subjectName', 'stimulus'))
t1block = summarySE(d1, measurevar = "rt", groupvars = c('subjectName', 'blockNumber', 'stimulus'))
t1block = summarySE(t1block, measurevar = "rt", groupvars = c('blockNumber', 'stimulus'))

# Plot
p1 = plotRTBySubject(t1, "1. Causality judgment \n (stimuli made for causality jugdment)")
b1 = plotRTByBlock(t1block, "1. Causality judgment \n (stimuli made for causality jugdment)")


# Check if there is no major bias in the other stimuli
d2 = d[d$stimulus %in% c('AA', 'AV', 'VV'),]
d2$stimulus = factor(d2$stimulus, levels=c('AA', 'AV', 'VV'))   # Order stimuli
t2 = summarySE(d2, measurevar = "rt", groupvars = c('subjectName', 'stimulus'))
t2block = summarySE(d2, measurevar = "rt", groupvars = c('subjectName', 'blockNumber', 'stimulus'))
t2block = summarySE(t2block, measurevar = "rt", groupvars = c('blockNumber', 'stimulus'))

# Plot
p2 = plotRTBySubject(t2, "4. Causality judgment \n (stimuli made for temporal order jugdment)")
b2 = plotRTByBlock(t2block, "2. Temporal order judgment \n (stimuli made for causality jugdment)")





#### Order judgment ####
d = data[data$blocType == 'SEQUENCE_TOJ',]

# Check for AAA/AA/AV/VV/VVV stimuli if psychometric curves looks good
d3 = d[d$stimulus %in% c('AA', 'AV', 'VV'),]
d3$stimulus = factor(d3$stimulus, levels=c('AA', 'AV', 'VV'))   # Order stimuli
t3 = summarySE(d3, measurevar = "rt", groupvars = c('subjectName', 'stimulus'))
t3block = summarySE(d3, measurevar = "rt", groupvars = c('subjectName', 'blockNumber', 'stimulus'))
t3block = summarySE(t3block, measurevar = "rt", groupvars = c('blockNumber', 'stimulus'))

p3 = plotRTBySubject(t3, "3. Temporal order judgment \n (stimuli made for temporal order jugdment)")
b3 = plotRTByBlock(t3block, "2. Temporal order judgment \n (stimuli made for causality jugdment)")

# Check if there is no major bias in the other stimuli
d4 = d[d$stimulus %in% c('DD', 'DC', 'CC'),]
d4$stimulus = factor(d4$stimulus, levels=c('DD', 'DC', 'CC'))   # Order stimuli
t4 = summarySE(d4, measurevar = "rt", groupvars = c('subjectName', 'stimulus'))
t4block = summarySE(d4, measurevar = "rt", groupvars = c('subjectName', 'blockNumber', 'stimulus'))
t4block = summarySE(t4block, measurevar = "rt", groupvars = c('blockNumber', 'stimulus'))

# Plot
p4 = plotRTBySubject(t4, "2. Temporal order judgment \n (stimuli made for causality jugdment)")
b4 = plotRTByBlock(t4block, "2. Temporal order judgment \n (stimuli made for causality jugdment)")



# Full plots
plotName = paste(sourceFolder, "4_RT_Subjects.bmp", sep="")
bmp(plotName, width=700, height=700)
multiplot(p1, p4, p3, p2)
dev.off()

plotName = paste(sourceFolder, "4_RT_Blocks.bmp", sep="")
bmp(plotName, width=700, height=700)
multiplot(b1, b4, b3, b2)
dev.off()
