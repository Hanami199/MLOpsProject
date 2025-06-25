# 2. Software Development Method and Process Model

## 2.1 Software Development Method

For the development of the Film Recommendation WebApp, the team adopted an **Agile development methodology**, particularly inspired by **Scrum principles**. This was chosen due to the need for adaptability and iterative feedback loops across different team roles: Machine Learning Engineer (MLE), Data Engineer (DE), Software Developer (SD), and Software Engineer (SE).

### Key Agile Practices:
- **Iterative Development**: Weekly sprints were held, each followed by a recap meeting.
- **Task Division by Role**: Each role had clearly assigned responsibilities (e.g., MLE focused on models, DE on preprocessing).
- **Version Control & Branching**: All development was coordinated via **GitHub**, with individual branches per team member, and merging handled by the SE.
- **Continuous Integration**: The shared GitHub repository allowed everyone to test their component within the full system, as it evolved.

## 2.2 Software Process Model

We followed a **modified V-Model** process:

- **Requirements definition** → led by SE, derived from user needs and feasibility.
- **System design** → layout of components like model interface, search bar, and UI.
- **Implementation** → individual coding of ML models, pipelines, and frontend/backend.
- **Validation & Testing** → regular integration checks, prediction tests, and UI validation.
- **System delivery & feedback** → final app tested in end-to-end workflow.

---

# 3. Identification of Key Aspects

## 3.a Software Requirements

As detailed in the SRS:

- **Functional Requirements**:
  - Select 5–10 movies from a searchable list
  - Return k recommendations (typically 5)
  - Display metadata: genre, rating, title, image (optional)
  - Refresh and reselect capability

- **Non-Functional Requirements**:
  - <3s latency
  - Accessible from browser, mobile-friendly
  - Stateless, no login required
  - At least 5 concurrent users

## 3.b Software Development Methods

- **Versioning**: Git (GitHub repository)
- **Branching Model**: Feature branches per role (e.g., `ml/model.py`), merged via Pull Requests
- **Code Review**: All merge requests approved by the SE
- **Environments**: Requirements pinned in `requirements.txt` for reproducibility

## 3.c Software Testing Strategy

### Testing Plan:
- **Unit Tests**:
  - For each model method (e.g., `predict()`)
  - For preprocessing functions
- **Integration Tests**:
  - Model + Frontend integration (e.g., test full user interaction)
- **User Testing**:
  - Informal, from multiple devices
  - Tested for input errors, mobile responsiveness, missing data
- **Performance Testing**:
  - Time taken by `predict()` function benchmarked

### Bug Tracking:
- Issues tracked using GitHub Issues and Project board

---

# 4. Dataset Information

### Source:
- Netflix Shows Dataset from Kaggle: https://www.kaggle.com/datasets/shivamb/netflix-shows/data

### Variables:
- **Used**:
  - `type`, `title`, `director`, `cast`, `country`, `release_year`, `rating`, `duration`, `listed_in`, `description`
- **Dropped**:
  - `show_id` (ID field)
  - `date_added` (not informative for similarity)

### Cleaning & Preprocessing:
- Removed missing values
- Parsed duration into minutes or seasons (depending on type)
- One-hot encoding for categorical vars (e.g., genre, rating)
- Sentence embeddings for `description`, `title`, `cast`

### Data Exploration:

Key KPIs:
- ~6,000 entries
- Most entries are movies (~75%)
- Top genres: Dramas, Comedies, Documentaries
- Ratings: Mainly `TV-MA`, `PG`, `R`

**Clustering Insights**:
- `listed_in` values showed genre proximity (e.g., Comedy close to Stand-Up Comedy)
- `duration` highly skewed → normalized

---

# 5. Proposed ML Pipeline

## Overview
The ML pipeline aims to compute similarity between user-selected movies and return k most similar items in the dataset.

Input: `n` selected movie titles  
Output: `k` recommended movie titles with metadata

### Steps:
1. **Preprocessing**: One-hot encoding, sentence embeddings
2. **Embedding Generation**: For text fields (`description`, `listed_in`, `cast`)
3. **Similarity Computation**: Using vector distance metrics
4. **Recommendation**: Select closest neighbors based on aggregate similarity


## Model Variants and Evaluation

### ✅ KNN on One-Hot Encoded Dataset
- Variables used: genre, rating, duration, country
- Distance metric: cosine
- Fast and interpretable
- Result: Consistent recommendations
- ✅ **Final default model** due to speed and explainability

### 🧪 KNN on Embedding-Based Features
- Used: Sentence-BERT or similar on `description`, `title`, `cast`
- High semantic richness
- Slower inference (but acceptable)
- Result: More nuanced recommendations (e.g., matching by theme, not just genre)
- Status: Available, but not default

### ⚠️ VAE (Variational Autoencoder)
- Used to reduce dimensionality of embedding features
- Trained on latent space, then searched neighbors
- Poor results: low recommendation quality and interpretability
- Status: **Discarded**

### 📌 t-SNE and UMAP for Exploration
- Used to visualize proximity of movie points
- Good genre-grouping validation (e.g., horror distant from comedies)
- Not used in final pipeline, but helpful during EDA

## Model Interface

```python
# models.py
model.predict(user_movie_indices: np.array) -> List[int]
```

- Returns indices of most similar movies
- Abstraction ensures SD can swap models without logic changes

## Performance

| Model                     | Time (avg) | Quality        | Interpretability | Usage       |
|--------------------------|------------|----------------|------------------|-------------|
| KNN (One-Hot)            | <1 sec     | Good           | High             | ✅ Default   |
| KNN (Embeddings)         | ~1–2 sec   | Very Good      | Medium           | Available   |
| VAE                      | ~3 sec     | Poor           | Low              | Discarded   |


## Final Pipeline Justification
- **Simplicity**: KNN avoids training time and allows easy feature tweaking
- **Speed**: Minimal delay in prediction (<1 sec)
- **Interpretability**: Features are understandable (e.g., genre proximity)
- **Reusability**: Predict interface is modular and can host future models

## Diagram: ML Pipeline Overview

```mermaid
flowchart TD
    A[User Selects Movies] --> B[Convert to Indices]
    B --> C[Fetch Encoded Features]
    C --> D[Compute Distance (KNN)]
    D --> E[Return Top-K Nearest Movies]
    E --> F[Display Metadata in UI]
```