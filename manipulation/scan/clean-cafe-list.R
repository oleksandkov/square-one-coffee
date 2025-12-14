# Clean Cafe List Generator
# Takes comprehensive cafe data and creates a clean summary table
# with cafe names and location counts

library(dplyr)
library(tidyr)
library(stringr)
library(readr)

# Read the comprehensive cafe data
cafes_raw <- read_csv(
  "data-private/derived/cafes/edmonton_cafes_comprehensive.csv",
  show_col_types = FALSE
)

# Function to determine if a place is truly a cafe/coffee shop
is_true_cafe <- function(name, types) {
  name_lower <- tolower(name)
  types_lower <- tolower(types)
  
  # Strong cafe indicators
  cafe_keywords <- c(
    "cafe", "coffee", "espresso", "latte", "cappuccino", 
    "starbucks", "tim hortons", "second cup", "good earth",
    "blenz", "beans", "brew", "roast", "roasters",
    "boba", "bubble tea", "tea house", "tea spot"
  )
  
  # Exclude these (not primarily cafes)
  exclude_keywords <- c(
    "gas station", "convenience", "petro", "shell", "esso",
    "7-eleven", "circle k", "a&w", "mcdonald", "dairy queen",
    "grocery", "supermarket", "sobeys", "safeway", "save-on",
    "hotel", "motel", "gym", "fitness", "movati",
    "restaurant", "pub", "bar", "grill", "steakhouse",
    "pizza", "donair", "pho", "sushi", "burger",
    "denny's", "ihop", "cora", "opa", "edo japan",
    "liquor", "market master", "freson"
  )
  
  # Check if it has cafe type
  has_cafe_type <- str_detect(types_lower, "cafe|coffee_shop")
  
  # Check name for cafe keywords
  has_cafe_name <- any(str_detect(name_lower, cafe_keywords))
  
  # Check for exclusions
  is_excluded <- any(str_detect(name_lower, exclude_keywords))
  
  # Return TRUE if it's a cafe and not excluded
  return((has_cafe_type || has_cafe_name) && !is_excluded)
}

# Filter to only true cafes
cafes_filtered <- cafes_raw %>%
  rowwise() %>%
  filter(is_true_cafe(name, types)) %>%
  ungroup()

cat("Filtered to", nrow(cafes_filtered), "true cafes/coffee shops from", nrow(cafes_raw), "total places\n")

# Clean and standardize names for grouping
clean_name <- function(name) {
  name %>%
    # Remove location-specific suffixes
    str_remove_all(" - [A-Z][a-z]+$") %>%  # Remove " - Location"
    str_remove_all(" \\([^)]+\\)$") %>%     # Remove "(Location)"
    str_remove_all(" #\\d+$") %>%            # Remove " #123"
    str_remove_all(" Unit \\d+.*$") %>%      # Remove " Unit 123"
    str_remove_all(", .*$") %>%              # Remove everything after comma
    # Standardize common chains
    str_replace("^Starbucks.*", "Starbucks") %>%
    str_replace("^Tim Hortons.*", "Tim Hortons") %>%
    str_replace("^Second Cup.*", "Second Cup") %>%
    str_replace("^McDonald's.*", "McDonald's") %>%
    str_replace("^Good Earth.*", "Good Earth Coffeehouse") %>%
    str_replace("^Blenz.*", "Blenz Coffee") %>%
    str_replace("^CoCo Fresh.*", "CoCo Fresh Tea & Juice") %>%
    str_replace("^Presse Cafe.*", "Presse Cafe") %>%
    str_replace("^Square One Coffee.*", "Square One Coffee") %>%
    str_replace("^Transcend.*", "Transcend Coffee") %>%
    str_replace("^The Colombian.*", "The Colombian Coffee House") %>%
    str_replace("^Iconoclast.*", "Iconoclast Koffiebar") %>%
    str_replace("^Caffé Rosso.*", "Caffé Rosso") %>%
    str_replace("^Little Brick.*", "Little Brick") %>%
    str_replace("^Block 1912.*", "Block 1912") %>%
    str_replace("^Remedy.*", "Remedy Cafe") %>%
    str_replace("^District Cafe.*", "District Cafe") %>%
    str_replace("^D Spot.*", "D Spot Dessert Cafe") %>%
    str_replace("^Marble Slab.*", "Marble Slab Creamery") %>%
    # Trim whitespace
    str_trim()
}

# Create summary table with location counts
cafe_summary <- cafes_filtered %>%
  mutate(
    clean_name = clean_name(name),
    is_operational = business_status == "OPERATIONAL"
  ) %>%
  group_by(clean_name) %>%
  summarise(
    total_locations = n(),
    operational_locations = sum(is_operational, na.rm = TRUE),
    closed_locations = total_locations - operational_locations,
    avg_rating = round(mean(rating, na.rm = TRUE), 2),
    total_reviews = sum(user_ratings_total, na.rm = TRUE),
    has_multiple_locations = total_locations > 1,
    .groups = "drop"
  ) %>%
  arrange(desc(total_locations), desc(total_reviews), clean_name)

# Separate into chains vs. independents
chains <- cafe_summary %>%
  filter(has_multiple_locations) %>%
  select(
    name = clean_name,
    locations = total_locations,
    operational = operational_locations,
    closed = closed_locations,
    avg_rating,
    total_reviews
  )

independents <- cafe_summary %>%
  filter(!has_multiple_locations) %>%
  select(
    name = clean_name,
    operational = operational_locations,
    avg_rating,
    total_reviews
  )

# Print summaries
cat("\n=======================================================================\n")
cat("EDMONTON CAFE SUMMARY\n")
cat("=======================================================================\n\n")

cat("CHAINS (Multiple Locations):\n")
cat("-----------------------------\n")
print(chains, n = Inf)

cat("\n\nINDEPENDENT CAFES:\n")
cat("-----------------------------\n")
cat("Total independent cafes:", nrow(independents), "\n")
cat("\nTop 20 by reviews:\n")
print(head(independents %>% arrange(desc(total_reviews)), 20), n = 20)

cat("\n\nTop 20 by rating (min 20 reviews):\n")
print(
  head(
    independents %>% 
      filter(total_reviews >= 20) %>% 
      arrange(desc(avg_rating), desc(total_reviews)), 
    20
  ), 
  n = 20
)

# Save cleaned tables
write_csv(
  chains,
  "data-private/derived/cafes/edmonton_cafe_chains.csv"
)

write_csv(
  independents,
  "data-private/derived/cafes/edmonton_cafe_independents.csv"
)

# Create combined clean table
cafe_clean <- bind_rows(
  chains %>% mutate(type = "chain"),
  independents %>% 
    mutate(
      locations = 1,
      closed = 0,
      type = "independent"
    ) %>%
    select(name, locations, operational, closed, avg_rating, total_reviews, type)
) %>%
  arrange(desc(locations), desc(total_reviews), name)

write_csv(
  cafe_clean,
  "data-private/derived/cafes/edmonton_cafes_clean.csv"
)

cat("\n=======================================================================\n")
cat("FILES SAVED:\n")
cat("- data-private/derived/cafes/edmonton_cafe_chains.csv\n")
cat("- data-private/derived/cafes/edmonton_cafe_independents.csv\n")
cat("- data-private/derived/cafes/edmonton_cafes_clean.csv\n")
cat("=======================================================================\n")

# Print overall statistics
cat("\n=======================================================================\n")
cat("OVERALL STATISTICS:\n")
cat("=======================================================================\n")
cat("Total cafe businesses:", nrow(cafe_clean), "\n")
cat("  - Chains:", nrow(chains), "\n")
cat("  - Independents:", nrow(independents), "\n")
cat("Total locations:", sum(cafe_clean$locations), "\n")
cat("  - Operational:", sum(cafe_clean$operational), "\n")
cat("  - Closed:", sum(cafe_clean$closed), "\n")
cat("Average rating:", round(mean(cafe_clean$avg_rating, na.rm = TRUE), 2), "\n")
cat("Total reviews:", format(sum(cafe_clean$total_reviews, na.rm = TRUE), big.mark = ","), "\n")
cat("=======================================================================\n")
