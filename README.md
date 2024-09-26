# LyricEraClassifier

This project is a text-analysis engine designed to classify songs by the era they were released based on their lyrics. I was inspired by an article discussing the simplification of lyrics over time, so I built models for three distinct periods in U.S. music history:

- **Golden and Post Golden Age (1940-1969)**
- **Pre-Contemporary (1970-1999)**
- **Contemporary (2000-2020)**

The models were trained using Billboard's top songs from every even year in each era. Song lyrics were analyzed based on features like word length, frequency, profanity, and first-person pronoun usage.

### Key Features
- **Era classification**: Predicts the era of a song based on lyrical patterns.
- **Text features**: Evaluates lyrics by complexity (word length), repetition (word frequency), and profanity.
- **Sample tests**: Accurately classified "Ivy" by Frank Ocean (2016) as Contemporary and "Vienna" by Paul Anka (1977) as Pre-Contemporary.

### Limitations
- Only trained on mainstream music (top Billboard songs), so results may not generalize to alternative or obscure music.
- Tested on two samples; broader testing could reveal more inaccuracies.

