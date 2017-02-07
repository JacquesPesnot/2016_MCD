
# Import packages

library (ggplot2)
library(lmerTest)
library(MASS)

# Create functions

summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE,
                      conf.interval=.95, .drop=TRUE) {
  library(plyr)
  
  # New version of length which can handle NA's: if na.rm==T, don't count them
  length2 <- function (x, na.rm=FALSE) {
    if (na.rm) sum(!is.na(x))
    else       length(x)
  }
  
  # This does the summary. For each group's data frame, return a vector with
  # N, mean, and sd
  datac <- ddply(data, groupvars, .drop=.drop,
                 .fun = function(xx, col) {
                   c(N    = length2(xx[[col]], na.rm=na.rm),
                     mean = mean   (xx[[col]], na.rm=T),
                     sd   = sd     (xx[[col]], na.rm=T)
                   )
                 },
                 measurevar
  )
  
  # Rename the "mean" column    
  datac <- rename(datac, c("mean" = measurevar))
  
  datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean
  
  # Confidence interval multiplier for standard error
  # Calculate t-statistic for confidence interval: 
  # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
  ciMult <- qt(conf.interval/2 + .5, datac$N-1)
  datac$ci <- datac$se * ciMult
  
  return(datac)
}


plotPsychometricBySubject <- function(tab, title, ylab, col="#000000"){
  meanSubj = summarySE(tab, measurevar = "resp", groupvars = c('stimulus'))
  p = (ggplot(tab, aes(x=stimulus, y=resp, color=subjectName))
       + geom_point(size=3, alpha=.4, color="#000000") # Individual data points
       + geom_line(aes(group=subjectName), size=1, alpha=.4, color="#000000") # Individual data points
       + geom_point(data=meanSubj, aes(x=stimulus, y=resp), size=8, color=col, shape=18) # Group mean
       + geom_line(data=meanSubj, aes(x=stimulus, y=resp, group=N), color=col, size=1.5) # Group mean
       + geom_errorbar(data=meanSubj, aes(ymin=resp-se, ymax=resp+se), size=1, width=.1, color=col)
       + guides(color=FALSE)
       + ggtitle(title)
       + theme_bw()
       + theme(plot.title = element_text(face="bold", size=20))
       + theme(axis.title.x = element_text(size=18))
       + theme(axis.title.y = element_text(size=18))
       + xlab("")
       + ylab(ylab)
       + coord_cartesian(ylim=c(0,1)))
  p
  return(p)
}


plotPsychometricByBlock <- function(tab, title, ylab){
  p = (ggplot(tab, aes(x=stimulus, y=resp, color=blockNumber))
       + geom_point(size=4) # Individual data points
       + geom_line(aes(group=blockNumber), size=1.2) # Individual data points
       + geom_errorbar(data=tab, aes(ymin=resp-se, ymax=resp+se, color=blockNumber), size=1, width=.1)
       + scale_colour_discrete(h = c(250, 253), l=c(80, 60, 40))
       + ggtitle(title)
       + theme_bw()
       + theme(plot.title = element_text(face="bold"))
       + xlab("")
       + ylab(ylab)
       + coord_cartesian(ylim=c(0,1)))
  p
  return(p)
}


plotRTBySubject <- function(tab, title){
  meanSubj = summarySE(tab, measurevar = "rt", groupvars = c('stimulus'))
  p = (ggplot(tab, aes(x=stimulus, y=rt, color=subjectName))
       + geom_point(size=3, alpha=.5) # Individual data points
       + geom_line(aes(group=subjectName), size=1, alpha=.5) # Individual data points
       + geom_point(data=meanSubj, aes(x=stimulus, y=rt), size=6, color="#000000", shape=18) # Group mean
       + geom_line(data=meanSubj, aes(x=stimulus, y=rt, group=N), color="#000000", size=1.2) # Group mean
       + geom_errorbar(data=meanSubj, aes(ymin=rt-se, ymax=rt+se), size=1, width=.1, color="#000000")
       + guides(color=FALSE)
       + ggtitle(title)
       + theme_bw()
       + theme(plot.title = element_text(face="bold"))
       + xlab("")
       + ylab("RT (s)")
       + coord_cartesian(ylim=c(0,1.2)))
  p
  return(p)
}

plotRTByBlock <- function(tab, title){
  p = (ggplot(tab, aes(x=stimulus, y=rt, color=blockNumber))
       + geom_point(size=4) # Individual data points
       + geom_line(aes(group=blockNumber), size=1.2) # Individual data points
       + geom_errorbar(data=tab, aes(ymin=rt-se, ymax=rt+se, color=blockNumber), size=1, width=.1)
       + scale_colour_discrete(h = c(250, 253), l=c(80, 60, 40))
       + ggtitle(title)
       + theme_bw()
       + theme(plot.title = element_text(face="bold"))
       + xlab("")
       + ylab("RT (s)")
       + coord_cartesian(ylim=c(0,1.2)))
  p
  return(p)
}




as.numeric.factor <- function(x){as.numeric(levels(x))[x]}

multiplot <- function(..., plotlist=NULL, file, cols=2, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}