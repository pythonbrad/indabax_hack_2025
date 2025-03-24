# Data Cleaning Assumption

## 1. Geographic Data Normalization

### District/Arrondissement Processing
- **Matching Algorithm**: Python `difflib` (SequenceMatcher)
  - Ratio threshold: 0.5 for automatic matching
  - Selection criteria: Best match (eg. Yaoundé 1 -> Yaounde 1er)
- **Reference Data**: OpenStreetMap district polygons via OpenGeoData

## 2. Date Standardization
- **Target Format**: `YYYY-MM-DD`
- **Handled Input Formats**:
  - `YYYY-MM-DD`
  - `DD-MM-YYYY`
  - `MM/DD/YYYY`
  - `YYYY/MM/DD`

## 3. Sentiment Analysis Implementation

### Health Condition: "Autre à préciser"
- **Classification Rules**:
  - **Positive**: Explicit positive terms ("rien", "aucun", "normal")
  - **Neutral**: Factual descriptions ("neutre")
  - **Negative**: Default classification for all other cases

## 4. Quality Control Matrix

| Data Type | Issue | Solution | Validation |
|-----------|-------|----------|------------|
| Districts | Spelling variants | `difflib` matching | Manual sampling |
| Date fields | Multiple formats | Forced `YYYY-MM-DD` | Regex + date parser |
| Vague responses | "rien", "aucun", "non spécifié", "pas spécifié" | Normalized to "N/A" | Replacement dictionary |

## Implementation Notes
1. **District Matching**:
   - Pre-processed all names to lowercase
   - Removed diacritics and precision before matching

2. **Date Handling**:
   - Invalid dates converted to `NA`

3. **Health Condition: "Autre à preciser"**:
   - Only explicitly positive/neutral terms get special classification
   - All ambiguous cases treated as negative
