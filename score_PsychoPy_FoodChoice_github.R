# Update 2022-Oct-14
 # 1. Variables renamed and reordered to approx match standard output for FCT
 # 2. Output file saved with Date stamp => No need to type in a file name, just highlight entire file and run

# Delete the default workspace
rm(list=ls())                     

# ## add library ##
library(plyr) # ** in this order **
library(dplyr)

### PATH TO FOLDER HERE IS SET HERE ###############

# set my_folder to the location of your study data
my_folder <-  setwd("")



#### THIS WILL NOT WORK IF SOME OF THE FILES ARE MISSING - CRASHES IF HEALTH, TASTE, OR CHOICE IS MISSING ###

# Import individual data files

## import Health

# NB: add or remove info from the wildcard that calls folder name to restrict file to import
files <- list.files()
fname <- Sys.glob(sprintf('%s/*/*behav.csv',my_folder))  

Lapply <- lapply(fname, read.table, header=TRUE, sep=",")

temp <-do.call('rbind.fill', Lapply)

output <- temp %>% dplyr::select(c('SubID','food_item', 'health_rating','h_rt', 'taste_rating','t_rt','choice_rating','c_rt','condition','rating_reversed', 'fat', 'ref_food'))

refs <- temp %>% dplyr::select(c('SubID','ref_food','date')) 
refs <- refs[1,]

ref_ratings_sub<-output$SubID[1]
ref_ratings_h<- output$health_rating[output$food==output$ref_food][1]
ref_ratings_t<- output$taste_rating[output$food==output$ref_food][1]
ref_info <- data.frame(SubID = ref_ratings_sub, ref_h = ref_ratings_h, ref_t = ref_ratings_t)

######## PROCESS for SUMMARY #############
# recode some things; rename ratings and reverse scoring if needed

output$fat.e <- ifelse(output$fat==1,1,-1)

output$order_h <- ifelse(output$rating_reversed == 0,1,2)
output$order_t <- ifelse(output$rating_reversed == 0,1,2)

output$choice <- ifelse(output$choice_rating>3,1,ifelse(output$choice_rating<3,0,NA))
output$choice_wneut <- ifelse(output$choice_rating>3,1,0)
output$neut_choice <- ifelse(output$choice_rating==3,1,0)

# code whether a SC trial at all
output$sc_bin[(output$taste_rating >3 & output$health_rating < 3) | (output$taste_rating <3 & output$health_rating > 3) 
               & output$taste_rating > 0 & output$health_rating > 0] <- 1
output$sc_bin[(output$taste_rating >3 & output$health_rating > 3) | (output$taste_rating <3 & output$health_rating < 3)
               & output$taste_rating > 0 & output$health_rating > 0] <- 0

# use of self-control (1 vs 0) - NOT expanded bins
output$sc[(output$taste_rating >3 & output$health_rating < 3 & output$choice_rating <3)  | (output$taste_rating <3 & output$health_rating > 3 & output$choice_rating >3) 
           & output$taste_rating > 0 & output$health_rating > 0 & output$choice_rating > 0] <- 1
output$sc[(output$taste_rating >3 & output$health_rating < 3 & output$choice_rating >3)  | (output$taste_rating <3 & output$health_rating > 3 & output$choice_rating <3)
           & output$taste_rating > 0 & output$health_rating > 0 & output$choice_rating > 0] <- 0
output$sc[output$choice_rating == 3] <- NA
output$sc[output$sc_bin == 0] <- NA


#########################################################################
############## Summarize data for a standard exel data file #############
#########################################################################

output_summary <- output %>%
  group_by(SubID) %>%
  summarise_at(c("order_h", "order_t", "health_rating",  "taste_rating", "choice_rating", "h_rt", "t_rt","c_rt", "choice", "choice_wneut", "neut_choice", "sc_bin", "sc"), mean, na.rm = TRUE)

# add count for sc_bin
output_summary_scbin_n <- output %>%
  group_by(SubID) %>%
  summarise_at(c("sc_bin"), sum, na.rm = TRUE)
output_summary_scbin_n <- output_summary_scbin_n %>%
  dplyr::rename(sc_bin_n = sc_bin)

output_summary_fat <- output %>%
  group_by(SubID,fat) %>%
  summarise_at(c("health_rating",  "taste_rating",  "choice_rating","h_rt","t_rt", "c_rt", "choice", "choice_wneut", "neut_choice"), mean, na.rm = TRUE)

# create one complete summary file
library(data.table)
output_summary_fat_trnsp<-dcast(setDT(output_summary_fat), SubID~fat, value.var=c("health_rating",  "taste_rating", "choice_rating","h_rt","t_rt",  "c_rt", "choice", "choice_wneut", "neut_choice"))

output_summary <- merge(output_summary,output_summary_scbin_n,by=c("SubID"))
output_summary <- merge(output_summary,output_summary_fat_trnsp,by=c("SubID"))
output_summary <- merge(output_summary,refs,by=c("SubID"))
output_summary <- merge(output_summary,ref_info,by=c("SubID"))

# *** CHANGE variable names to standard output ***
colnames(output_summary)[colnames(output_summary)      # Rename variables (changed ref_food name to match variable)
                   %in% c("SubID", "order_h", "order_t", "health_rating", "taste_rating", "choice_rating", "h_rt", "t_rt", "c_rt", "choice", 
                          "choice_wneut", "neut_choice", "sc_bin", "sc", "sc_bin_n", "health_rating_0", "health_rating_1", "taste_rating_0", "taste_rating_1", "choice_rating_0", 
                          "choice_rating_1", "h_rt_0", "h_rt_1", "t_rt_0", "t_rt_1", "c_rt_0", "c_rt_1", "choice_0", "choice_1", "choice_wneut_0", 
                          "choice_wneut_1", "neut_choice_0", "neut_choice_1", "ref_food", "date", "ref_h", "ref_t")] <- c("SubId", "re_ord_h", "re_ord_t", "h_mean", 
                          "t_mean", "c_mean", "h_RT", "t_RT", "c_RT", "choice", "choice_wneut", "neut_choice", "self_ctrl_bin", "self_ctrl", "self_ctrl_bin_count", "h_lo", 
                          "h_hi", "t_lo", "t_hi", "c_lo", "c_hi", "h_lo_RT", "h_hi_RT", "t_lo_RT", "t_hi_RT", "ch_lo_RT", "c_hi_RT", "cho_noneut_lo", "cho_noneut_hi", "cprop_lo", 
                          "cprop_hi", "cneu_lo", "cneu_hi", "ref", "date", "ref_h", "ref_t")


# *** REORDER COLUMNS to standard output (drop some columns) ***
output_summary <- output_summary[, c("SubId", "date", "ref",  "ref_h", "ref_t", "re_ord_h", "re_ord_t", 
                                              "h_lo", "h_hi", "t_lo", "t_hi", "c_lo", "c_hi", 
                                              "cneu_lo", "cneu_hi", "cho_noneut_lo", "cho_noneut_hi", 
                                              "self_ctrl_bin", "self_ctrl", "self_ctrl_bin_count",
                                              "h_lo_RT", "h_hi_RT", "t_lo_RT", "t_hi_RT", "ch_lo_RT", "c_hi_RT")]

# save a completed file - *** now automatically saves with today's date ***
write.csv(output_summary, file= sprintf('FoodChoice_PsychoPy_SUMMARY_%s.csv',Sys.Date()))

# save the trial-wise data
write.csv(output, file= sprintf('FoodChoice_PsychoPy_TRIALBYTRIAL_%s.csv',Sys.Date()))
