
mainDirectory = 'E:/Stage CEA/analysis/'
#mainDirectory = '/neurospin/meg/meg_tmp/MCD_Jacques_2016/analysis/'

dataFolder = paste(mainDirectory, 'data/behavioral/', sep='')
sourceFolder = paste(mainDirectory, 'psychoPhysics/', sep='')
source(paste(sourceFolder, 'functions.r', sep=''))

#### Import data set ####
nameFile = paste(dataFolder, 'full_behavioral_data.txt', sep='')
data = read.csv(nameFile)



#### Causality judgment ####
d = data[data$blocType == 'SEQUENCE_CJ',]
d$resp = 0                                                                    # 0 (notcommon)
d[d$response == 'common',]$resp = 1                                           # 1 (common)

# Check for DDD/DD/DC/CC/CCC stimuli if psychometric curves looks good
d1 = d[d$stimulus %in% c('DD', 'DC', 'CC'),]
d1$stimulus = factor(d1$stimulus, levels=c('DD', 'DC', 'CC'))   # Order stimuli
t1 = summarySE(d1, measurevar = "resp", groupvars = c('subjectName', 'stimulus'))
t1block = summarySE(d1, measurevar = "resp", groupvars = c('subjectName', 'blockNumber', 'stimulus'))
t1block = summarySE(t1block, measurevar = "resp", groupvars = c('blockNumber', 'stimulus'))

# Plot
p1 = plotPsychometricBySubject(t1, "Causality judgment \n", "% of 'same cause' judgment \n", col='#0000FF')
b1 = plotPsychometricByBlock(t1block, "1. Causality judgment \n (stimuli made for causality jugdment)", "% of 'same cause' judgment")


# Check if there is no major bias in the other stimuli
d2 = d[d$stimulus %in% c('AA', 'AV', 'VV'),]
d2$stimulus = factor(d2$stimulus, levels=c('AA', 'AV', 'VV'))   # Order stimuli
t2 = summarySE(d2, measurevar = "resp", groupvars = c('subjectName', 'stimulus'))
t2block = summarySE(d2, measurevar = "resp", groupvars = c('subjectName', 'blockNumber', 'stimulus'))
t2block = summarySE(t2block, measurevar = "resp", groupvars = c('blockNumber', 'stimulus'))

# Plot
p2 = plotPsychometricBySubject(t2, "Causality judgment \n", "% of 'same cause' judgment \n", col='#FF0000')
b2 = plotPsychometricByBlock(t2block, "2. Temporal order judgment \n (stimuli made for causality jugdment)", "% of 'light first' judgment")


# Rapid statistics
m1 = glmer(resp ~ as.numeric(stimulus) + (1|subjectName), family='binomial', data=d1)
summary(m1) # Should be significant

m2 = glmer(resp ~ as.numeric(stimulus) + (1|subjectName), family='binomial', data=d2)
summary(m2) # Should't be (control)




#### Order judgment ####
d = data[data$blocType == 'SEQUENCE_TOJ',]
d$resp = 0                                                                    # 0 (visualfirst)
d[d$response == 'visualfirst',]$resp = 1                                       # 1 (audiofirst)

# Check for AAA/AA/AV/VV/VVV stimuli if psychometric curves looks good
d3 = d[d$stimulus %in% c('AA', 'AV', 'VV'),]
d3$stimulus = factor(d3$stimulus, levels=c('AA', 'AV', 'VV'))   # Order stimuli
t3 = summarySE(d3, measurevar = "resp", groupvars = c('subjectName', 'stimulus'))
t3block = summarySE(d3, measurevar = "resp", groupvars = c('subjectName', 'blockNumber', 'stimulus'))
t3block = summarySE(t3block, measurevar = "resp", groupvars = c('blockNumber', 'stimulus'))

p3 = plotPsychometricBySubject(t3, "Temporal order judgment \n", "% of 'light first' judgment \n", col='#FF0000')
b3 = plotPsychometricByBlock(t3block, "2. Temporal order judgment \n (stimuli made for causality jugdment)", "% of 'light first' judgment")

# Check if there is no major bias in the other stimuli
d4 = d[d$stimulus %in% c('DD', 'DC', 'CC'),]
d4$stimulus = factor(d4$stimulus, levels=c('DD', 'DC', 'CC'))   # Order stimuli
t4 = summarySE(d4, measurevar = "resp", groupvars = c('subjectName', 'stimulus'))
t4block = summarySE(d4, measurevar = "resp", groupvars = c('subjectName', 'blockNumber', 'stimulus'))
t4block = summarySE(t4block, measurevar = "resp", groupvars = c('blockNumber', 'stimulus'))

# Plot
p4 = plotPsychometricBySubject(t4, "Temporal order judgment \n", "% of 'light first' judgment \n", col='#0000FF')
b4 = plotPsychometricByBlock(t4block, "2. Temporal order judgment \n (stimuli made for causality jugdment)", "% of 'light first' judgment")


# Rapid statistics
m3 = glmer(resp ~ as.numeric(stimulus) + (1|subjectName), family='binomial', data=d3)
summary(m3) # Should be significant

m4 = glmer(resp ~ as.numeric(stimulus) + (1|subjectName), family='binomial', data=d4)
summary(m4) # Should't be (control)




# Full plots
plotName = paste(sourceFolder, "3_PsychometricCurves_Subjects.bmp", sep="")
bmp(plotName, width=700, height=700)
multiplot(p1, p4, p3, p2)
dev.off()

plotName = paste(sourceFolder, "3_PsychometricCurves_Blocks.bmp", sep="")
bmp(plotName, width=700, height=700)
multiplot(b1, b4, b3, b2)
dev.off()
