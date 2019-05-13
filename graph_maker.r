# By: Clara Duffy
# Date: 5/13/19
# Ling106 Independant Project

# set working directory
PATH <- "~/Desktop/college/ling106/ling-rest-reviews"
library("tidyverse")
library(glue)

revs <- read_csv(file.path(PATH, "trip_file.csv"))

# dataframe from the generated csv with rows for each different word at each price and rating
revs_pct <- revs %>%
  mutate(
    first_pct = as.double(substring(first, regexpr(" ", first) + 1, regexpr(")", first)-1))/num_words *100,
    second_pct = as.double(substring(second, regexpr(" ", second) + 1, regexpr(")", second)-1))/num_words*100,
    third_pct = as.double(substring(third, regexpr(" ", third) + 1, regexpr(")", third)-1))/num_words *100,
    fourth_pct = as.double(substring(fourth, regexpr(" ", fourth) + 1, regexpr(")", fourth)-1))/num_words *100,
    first = substring(first, 4, regexpr("',", first)-1),
    second = substring(second, 4, regexpr("',", second)-1),
    third = substring(third, 4, regexpr("',", third)-1),
    fourth = substring(fourth, 4, regexpr("',", fourth)-1)
    ) %>%
  gather(key="which", value="word", c(first, second, third, fourth)) %>%
  transmute( # this is very hack-y
    dollars = dollars,
    stars = stars, 
    word = word,
    pct = if_else((row_number()<= 10),first_pct, 
                  if_else((row_number()<=20), second_pct, 
                          if_else((row_number() <= 30), third_pct, fourth_pct)))
  )

#sorting it so it turns out better in the graph
revs_pct$stars <- factor(revs_pct$stars, levels = c('5', '4', '3'))

#plotting a large graph that is faceted in two variable spaces
gr <- ggplot(revs_pct, aes(x=(reorder(word, -pct)), y = pct, fill = word))

gr + facet_grid(rows=vars(stars), cols=vars(dollars), scales = "free_x", labeller = label_both) +
  geom_bar(stat = "identity") +
  labs(x="Word", y = "Percent of Total Words Used") +
  scale_fill_manual(values = c("a"="#33658A", "and"="#1C77C3", "the"="#39A9DB", "was"="#1B3B6F", "to"="#55DDE0")) +
  coord_cartesian(ylim = c(0, 7.5)) +
  ggtitle("Top 4 words in Each Type of Review", subtitle ="Based on percent of total words used.")


#line graph of word frequency against pricey-ness of restaurant, faceted by star rating
ggplot((revs_pct %>% filter(word == "a" | word == "and" | word == "the")), aes(x=dollars, y=pct, col=word)) + 
  facet_wrap(~stars, labeller = label_both) + 
  coord_cartesian(ylim = c(0, 7.5)) +
  geom_line(stat = "identity") +
  labs(x= "Pricey-ness of Restaurant", y = "Percent of Total Words Used") +
  ggtitle("Correlation of Simple Words and Pricey-ness of Restaurants", subtitle = "Sorted by different star ratings")

#reading another csv, that this time has the floating point numbers of the ratings rather than rounded numbers
#this data set has slightly more specific data due to no rounding and therefore despecification
revs_floats <- read_csv(file.path(PATH, "trip_file_floats.csv")) %>%
  mutate(
    first_pct = as.double(substring(first, regexpr(" ", first) + 1, regexpr(")", first)-1))/num_words *100,
    second_pct = as.double(substring(second, regexpr(" ", second) + 1, regexpr(")", second)-1))/num_words*100,
    third_pct = as.double(substring(third, regexpr(" ", third) + 1, regexpr(")", third)-1))/num_words *100,
    fourth_pct = as.double(substring(fourth, regexpr(" ", fourth) + 1, regexpr(")", fourth)-1))/num_words *100,
    first = substring(first, 4, regexpr("',", first)-1),
    second = substring(second, 4, regexpr("',", second)-1),
    third = substring(third, 4, regexpr("',", third)-1),
    fourth = substring(fourth, 4, regexpr("',", fourth)-1)
  ) %>%
  gather(key="which", value="word", c(first, second, third, fourth)) %>%
  transmute(
    dollars = dollars,
    stars = stars, 
    word = word,
    pct = if_else((row_number()<= 16),first_pct, 
                  if_else((row_number()<=32), second_pct, 
                          if_else((row_number() <= 48), third_pct, fourth_pct)))
  ) #pretty much the same operations as before, but the total number of bins in the percent changes, so the 
    #hack-y way of doing things had to be hard-coded slightly differently.

# line graph of word frequency based on star rating, faceted by dollar rating of restaurant
ggplot((revs_floats %>% filter(word == "a" | word == "and" | word == "the")), aes(x=stars, y=pct, col=word)) + 
  facet_grid(~dollars, labeller = label_both) + 
  coord_cartesian(ylim = c(0, 7.5)) +
  geom_line(stat = "identity") +
  labs(x= "Star Rating of Restaurant", y = "Percent of Total Words Used") +
  ggtitle("Correlation of Simple Words and Pricey-ness of Restaurants", subtitle = "Sorted by different pricey-ness (measured in \"dollars\")")

