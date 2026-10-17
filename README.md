# CCADMACL_COM221_FINAL

## About
This project tests whether the colours of a TV-show poster relate to the show's IMDb rating. Each poster becomes colour features: RGBW means plus the year (MY), or plus the year and genres (MYG). The features go through scaling and PCA, then clustering (K-means, GMM, hierarchical, DBSCAN, BIRCH), and the clusters are compared with the IMDb ratings.

## Notebooks
1. `imdb.ipynb`: scrapes IMDb (top TV shows, episodes) into `CSV/` and downloads posters.
2. `imdb_individual_getter.ipynb`: scrapes one title by its IMDb ID.
3. `missing_posters_retriever.ipynb`: downloads posters listed in `CSV/missing_posters.csv`.
4. `duplicate_checker.ipynb`: finds duplicate and missing posters and cleans `CSV/imdb_episodes.csv`.
5. `episode_poster_modifier.ipynb`: renames the CSV columns to snake_case and removes duplicates.
6. `finalRGBW_MY.ipynb`: RGBW + year features, clustering.
7. `finalRGBW_MYG.ipynb`: RGBW + year + genre features, clustering.
8. `finalRGBW_MYGRevised.ipynb`: **final notebook**. It is the last version (2025-02-21) and saves `PKL/*.pkl`, the models that the UI ships.
9. `finalAnalysis.ipynb`: an earlier, separate analysis pass on the same data.

`UI/` is a Tkinter app (`UI/Main.py`) meant to predict a rating from a selected poster.

## Data not in the repo
- `imdb_episode_images/`: the episode posters (gitignored). Needed by notebooks 4, 8 and 9.
- `IMDB_TSV/`: the IMDb TSV dumps (gitignored, over GitHub's 100 MB limit). Needed by notebook 1.
- `tv_show_posters/` and `tv_shows_data.csv` at the repo root: needed by notebooks 6 and 7. They come from the CCADMACL_COM221_Exercises repo (`CSV/tv_shows_data.csv` here is the same CSV).

## Environment
Conda env `ml` (Python 3.10). `finalRGBW_MYGRevised.ipynb` also needs `playsound` (it plays `sounds/alarm*.mp3` when a run ends).

## Review notes (2026-10-18)
1. The UI crashes on start, also with `--version`. `UI/CustomComponents/__init__.py`, `UI/Services/__init__.py` and `UI/Views/__init__.py` import `Controllers.<module>` instead of their own package.
2. The "Select Image" button calls `selectImage` and `showImage` on `ServiceController`, which has neither method (`UI/Main.py:237`). In a 100-click simulation, every click raised `AttributeError`.
3. `EventHandlerController.selectImage` does not return the selected path, so the preview cannot show the image even after fix 2.
4. No UI code loads `UI/assets/pkl/*.pkl` or predicts a rating. `PosterRatePredictor` and `MainView` are stubs, so the app's purpose is not implemented.
5. In the colour feature extractor of notebooks 6–9, `w = (r + g + b) / 3` adds 8-bit (uint8) arrays. The sum wraps at 256 before the divide, so `w_mean` is wrong for every poster. It feeds the scaler, PCA, clusters and saved models. Casting to float first fixes it.
6. `finalAnalysis.ipynb` `get_imdb_data` reads columns `Slug`, `Title`, `Genres`, but `CSV/imdb_episodes.csv` has `imdb_id`, `title`, `genres`. The `except` hides the `KeyError`, so every row would drop silently.
7. The same function runs `eval()` on the CSV genre text. This can execute code from the data. Plain genre strings such as `Documentary` raise an error and the row drops.
8. In `imdb.ipynb`, the episode CSV header has 7 columns, but each row writes 6 (no `Rating Count`). The fields after the rating shift left, and `Poster` stays empty.
9. `random.sample` is unseeded in the analysis notebooks (the models use `random_state=42`). Results change from run to run (see note 12).
10. `tk==0.1.0` in `UI/requirements.txt` is an unrelated PyPI package. `tkinter` ships with Python.
11. `PKL/*.pkl` and `UI/assets/pkl/*.pkl` are byte-identical copies.
12. Run check (copy of the repo, CPU, env `ml`):
    - `finalRGBW_MY`: runs top to bottom (117 s). Best is K-means k=2, silhouette 0.264 (saved: 0.281).
    - `finalRGBW_MYG`: runs top to bottom (200 s). Best is GMM k=2, silhouette 0.281 (saved: 0.178). Best Davies-Bouldin is at k=4 (saved: k=6). The difference comes from the unseeded sample.
    - `finalAnalysis`: fails at cell 16 (no `imdb_episode_images/`).
    - `finalRGBW_MYGRevised`: fails at cell 1 (no `playsound`).
    - `episode_poster_modifier`, `duplicate_checker`: fail at cell 4 (`KeyError 'Slug'`). They are one-off tools whose changes the CSV already contains.
    - The 3 scraping notebooks were not run (live IMDb).
